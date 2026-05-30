from textual.app import ComposeResult
from textual.widgets import Static, Button, Input, Select, OptionList
from textual.widgets.option_list import Option
from textual.containers import Container, Horizontal
from textual import on, work
from textual.reactive import reactive

from ia.gemini import obtener_consejo_vestimenta
from clima.historial import obtener_historial_usuario
from clima.api import obtener_clima, buscar_ciudades


class ConsejoView(Container):
    """Vista de consejo IA — estructura plana, 3 modos."""

    MODO_ULTIMA    = "ultima"
    MODO_HISTORIAL = "historial"
    MODO_NUEVA     = "nueva"

    modo_actual: reactive[str] = reactive(MODO_ULTIMA)

    _suggestion_timer = None
    _current_suggestions: list = []

    def compose(self) -> ComposeResult:
        yield Static('[bold]Consejo IA: Como Me Visto Hoy?[/bold]', classes='section-title')

        # ── Selector de modo ────────────────────────────────────────
        with Horizontal(id='modo-selector'):
            yield Button('Ultima consulta', id='btn-modo-ultima',    classes='modo-btn modo-active')
            yield Button('Del historial',   id='btn-modo-historial', classes='modo-btn')
            yield Button('Nueva busqueda',  id='btn-modo-nueva',     classes='modo-btn')

        # ── Modo ULTIMA: contexto del último clima ───────────────────
        yield Static(
            '[dim]Primero consulta el clima en la opcion 1.[/dim]',
            id='weather-context',
            classes='consejo-panel',
        )

        # ── Modo HISTORIAL: selector de entradas ─────────────────────
        yield Static('Elegi una entrada de tu historial:', id='historial-label', classes='panel-label')
        yield Select([], id='historial-select', prompt='Selecciona una entrada...')

        # ── Modo NUEVA: input + autocomplete ─────────────────────────
        yield Static('Busca el clima de una ciudad para pedir consejo:', id='nueva-label', classes='panel-label')
        with Horizontal(id='nueva-search-row', classes='search-row'):
            yield Input(placeholder='Nombre de la ciudad...', id='consejo-city-input')
            yield Button('Buscar', id='consejo-search-btn', variant='default')
        yield OptionList(id='consejo-suggestions')
        yield Static('', id='consejo-search-result', classes='consejo-result-text')

        # ── Siempre visible ──────────────────────────────────────────
        yield Button('Pedir Consejo a la IA', id='ask-ai-btn', variant='primary')
        yield Static('', id='ai-response')

    def on_mount(self) -> None:
        self._apply_mode_visibility(self.MODO_ULTIMA)
        self.query_one('#consejo-suggestions', OptionList).display = False

    # ================================================================
    # Visibilidad por modo
    # ================================================================

    def _apply_mode_visibility(self, modo: str) -> None:
        is_ultima    = modo == self.MODO_ULTIMA
        is_historial = modo == self.MODO_HISTORIAL
        is_nueva     = modo == self.MODO_NUEVA

        self.query_one('#weather-context').display       = is_ultima
        self.query_one('#historial-label').display       = is_historial
        self.query_one('#historial-select').display      = is_historial
        self.query_one('#nueva-label').display           = is_nueva
        self.query_one('#nueva-search-row').display      = is_nueva
        self.query_one('#consejo-search-result').display = is_nueva

        self._hide_suggestions()

    # ================================================================
    # Helpers — siempre en hilo principal
    # ================================================================

    def _set_search_result(self, text: str) -> None:
        try:
            self.query_one('#consejo-search-result', Static).update(text)
        except Exception:
            pass

    def _set_ai_response(self, text: str) -> None:
        try:
            self.query_one('#ai-response', Static).update(text)
        except Exception:
            pass

    # ================================================================
    # Refresh
    # ================================================================

    def refresh_data(self) -> None:
        self._refresh_ultima_context()
        if self.modo_actual == self.MODO_HISTORIAL:
            self._load_historial_options()

    def _refresh_ultima_context(self) -> None:
        data = self.app.last_weather_data
        try:
            ctx = self.query_one('#weather-context', Static)
        except Exception:
            return
        if data is None:
            ctx.update('[dim]Primero consulta el clima en la opcion 1.[/dim]')
            return
        ciudad    = data.get('ciudad', '?')
        temp      = data.get('temperatura', '?')
        sensacion = data.get('sensacion_termica', '?')
        desc      = data.get('descripcion', '?')
        humedad   = data.get('humedad', '?')
        viento    = data.get('viento_kmh', '?')
        ctx.update(
            f'[bold cyan]{ciudad}[/bold cyan]  |  '
            f'{temp}C (ST {sensacion}C)  |  {desc}  |  '
            f'Hum {humedad}%  |  Viento {viento} km/h'
        )

    def _load_historial_options(self) -> None:
        username = self.app.current_user
        if not username:
            return
        try:
            entries = obtener_historial_usuario(username)
            self._historial_entries = []
            options = []
            for entry in reversed(entries):
                ciudad  = entry.get('Ciudad', '')
                temp    = entry.get('Temperatura_C', '')
                cond    = entry.get('Condicion_Clima', '')
                fecha   = entry.get('Fecha_Hora', '')[:16]
                hum_raw = entry.get('Humedad_Porcentaje', '0')
                vto_raw = entry.get('Viento_kmh', '0')
                label   = f"{fecha}  |  {ciudad}  |  {temp}C  |  {cond}"
                idx = len(self._historial_entries)
                self._historial_entries.append({
                    'ciudad':            ciudad,
                    'temperatura':       float(temp)    if temp    else 0.0,
                    'sensacion_termica': float(temp)    if temp    else 0.0,
                    'descripcion':       cond,
                    'humedad':           float(hum_raw) if hum_raw else 0.0,
                    'viento_kmh':        float(vto_raw) if vto_raw else 0.0,
                })
                options.append((label, idx))
            self.query_one('#historial-select', Select).set_options(options)
        except Exception:
            pass

    # ================================================================
    # Autocomplete
    # ================================================================

    @on(Input.Changed, '#consejo-city-input')
    def _on_city_changed(self, event: Input.Changed) -> None:
        query = event.value.strip()
        if self._suggestion_timer is not None:
            self._suggestion_timer.stop()
            self._suggestion_timer = None
        if len(query) < 2:
            self._hide_suggestions()
            return
        self._suggestion_timer = self.set_timer(0.35, lambda: self._fetch_suggestions(query))

    @work(thread=True)
    def _fetch_suggestions(self, query: str) -> None:
        results = buscar_ciudades(query)
        self.app.call_from_thread(self._show_suggestions, results)

    def _show_suggestions(self, results: list) -> None:
        self._current_suggestions = results
        try:
            ol = self.query_one('#consejo-suggestions', OptionList)
            ol.clear_options()
            if not results:
                ol.display = False
                return
            for i, r in enumerate(results):
                ol.add_option(Option(r['display'], id=str(i)))
            ol.display = True
        except Exception:
            pass

    def _hide_suggestions(self) -> None:
        try:
            self.query_one('#consejo-suggestions', OptionList).display = False
        except Exception:
            pass

    @on(OptionList.OptionSelected, '#consejo-suggestions')
    def _on_suggestion_selected(self, event: OptionList.OptionSelected) -> None:
        event.stop()
        try:
            city_name = self._current_suggestions[int(event.option.id)]['name']
        except (ValueError, IndexError, TypeError):
            city_name = ''
        if city_name:
            self.query_one('#consejo-city-input', Input).value = city_name
            self._hide_suggestions()
            self._fetch_nueva_ciudad(city_name)

    # ================================================================
    # Cambio de modo
    # ================================================================

    def _get_current_data(self) -> dict | None:
        if self.modo_actual == self.MODO_ULTIMA:
            return self.app.last_weather_data
        elif self.modo_actual == self.MODO_HISTORIAL:
            try:
                sel = self.query_one('#historial-select', Select)
                val = sel.value
                if val is not Select.BLANK and hasattr(self, '_historial_entries'):
                    return self._historial_entries[int(val)]
            except Exception:
                pass
            return None
        elif self.modo_actual == self.MODO_NUEVA:
            return getattr(self, '_nueva_busqueda_data', None)
        return None

    def _set_modo(self, modo: str) -> None:
        self.modo_actual = modo
        self._apply_mode_visibility(modo)

        self.query_one('#btn-modo-ultima').set_class(    modo == self.MODO_ULTIMA,    'modo-active')
        self.query_one('#btn-modo-historial').set_class( modo == self.MODO_HISTORIAL, 'modo-active')
        self.query_one('#btn-modo-nueva').set_class(     modo == self.MODO_NUEVA,     'modo-active')

        self._set_ai_response('')
        if modo != self.MODO_NUEVA:
            self._nueva_busqueda_data = None  # type: ignore[assignment]

        if modo == self.MODO_HISTORIAL:
            self._load_historial_options()

    @on(Button.Pressed, '#btn-modo-ultima')
    def _on_modo_ultima(self, event: Button.Pressed) -> None:
        event.stop()
        self._set_modo(self.MODO_ULTIMA)

    @on(Button.Pressed, '#btn-modo-historial')
    def _on_modo_historial(self, event: Button.Pressed) -> None:
        event.stop()
        self._set_modo(self.MODO_HISTORIAL)

    @on(Button.Pressed, '#btn-modo-nueva')
    def _on_modo_nueva(self, event: Button.Pressed) -> None:
        event.stop()
        self._set_modo(self.MODO_NUEVA)

    # ================================================================
    # Nueva búsqueda
    # ================================================================

    @on(Button.Pressed, '#consejo-search-btn')
    def _on_consejo_search(self, event: Button.Pressed) -> None:
        event.stop()
        self._hide_suggestions()
        city = self.query_one('#consejo-city-input', Input).value.strip()
        if city:
            self._fetch_nueva_ciudad(city)
        else:
            self._set_search_result('Escribi el nombre de una ciudad primero.')

    @on(Input.Submitted, '#consejo-city-input')
    def _on_consejo_input_submitted(self, event: Input.Submitted) -> None:
        event.stop()
        self._hide_suggestions()
        city = event.value.strip()
        if city:
            self._fetch_nueva_ciudad(city)
        else:
            self._set_search_result('Escribi el nombre de una ciudad primero.')

    @work(thread=True)
    def _fetch_nueva_ciudad(self, city: str) -> None:
        self.app.call_from_thread(self._set_search_result, 'Buscando...')
        try:
            data = obtener_clima(city)
            self._nueva_busqueda_data = data
            ciudad = data.get('ciudad', city)
            temp   = data.get('temperatura', '?')
            desc   = data.get('descripcion', '?')
            self.app.call_from_thread(
                self._set_search_result,
                f'Clima: {ciudad}  |  {temp}C  |  {desc}  —  Ya podes pedir el consejo.',
            )
        except Exception as e:
            self._nueva_busqueda_data = None  # type: ignore[assignment]
            self.app.call_from_thread(self._set_search_result, f'Error: {e}')

    # ================================================================
    # Pedir consejo a la IA
    # ================================================================

    @on(Button.Pressed, '#ask-ai-btn')
    def _on_ask(self, event: Button.Pressed) -> None:
        event.stop()
        data = self._get_current_data()
        if data is None:
            mensajes = {
                self.MODO_ULTIMA:    'Primero consulta el clima de una ciudad (opcion 1).',
                self.MODO_HISTORIAL: 'Selecciona una entrada de tu historial.',
                self.MODO_NUEVA:     'Primero busca una ciudad usando el campo de arriba.',
            }
            self.app.notify(mensajes.get(self.modo_actual, 'Sin datos de clima.'), severity='error')
            return
        self.ask_ai(data)

    @work(thread=True)
    def ask_ai(self, data: dict) -> None:
        self.app.call_from_thread(self._set_ai_response, 'Consultando a Gemini...')
        try:
            advice = obtener_consejo_vestimenta(
                temperatura=data.get('temperatura', 0),
                sensacion_termica=data.get('sensacion_termica', 0),
                condicion=data.get('descripcion', ''),
                humedad=data.get('humedad', 0),
                viento=data.get('viento_kmh', 0),
                ciudad=data.get('ciudad', ''),
            )
            self.app.call_from_thread(
                self._set_ai_response,
                f'Consejo de vestimenta:\n\n{advice}',
            )
        except Exception as e:
            self.app.call_from_thread(self._set_ai_response, f'Error al consultar la IA: {e}')
