from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, OptionList
from textual.widgets.option_list import Option
from textual.containers import Container, Horizontal, Vertical
from textual import on, work

from clima.api import obtener_clima, buscar_ciudades
from clima.historial import guardar_consulta


def _weather_label(description: str) -> str:
    """Return an ASCII weather label based on the description text."""
    desc = (description or '').lower()
    if 'clear' in desc or 'despejado' in desc or 'cielo claro' in desc:
        return '[ SOL ]'
    if 'thunderstorm' in desc or 'tormenta' in desc:
        return '[ TORMENTA ]'
    if 'rain' in desc or 'lluvia' in desc:
        return '[ LLUVIA ]'
    if 'drizzle' in desc or 'llovizna' in desc:
        return '[ LLOVIZNA ]'
    if 'snow' in desc or 'nieve' in desc:
        return '[ NIEVE ]'
    if any(w in desc for w in ('mist', 'fog', 'niebla', 'bruma', 'haze')):
        return '[ NIEBLA ]'
    if 'cloud' in desc or 'nub' in desc:
        return '[ NUBLADO ]'
    return '[ CLIMA ]'


class ClimaView(Container):
    """Weather query view."""

    _suggestion_timer = None
    _current_suggestions: list = []

    def compose(self) -> ComposeResult:
        yield Static(
            '[bold]Consultar Clima Actual[/bold]',
            classes='section-title',
        )
        with Horizontal(classes='search-row'):
            yield Input(
                placeholder='Nombre de la ciudad...',
                id='city-input',
            )
            yield Button('Consultar', id='query-btn', variant='primary')
        yield OptionList(id='city-suggestions')
        yield Container(id='weather-result')

    def on_mount(self) -> None:
        self.query_one('#city-suggestions', OptionList).display = False

    # ── Autocomplete ─────────────────────────────────────────────
    @on(Input.Changed, '#city-input')
    def _on_city_changed(self, event: Input.Changed) -> None:
        query = event.value.strip()
        if self._suggestion_timer is not None:
            self._suggestion_timer.stop()
            self._suggestion_timer = None
        if len(query) < 2:
            self._hide_suggestions()
            return
        self._suggestion_timer = self.set_timer(0.35, lambda: self._kick_suggestions(query))

    def _kick_suggestions(self, query: str) -> None:
        self._fetch_suggestions(query)

    @work(thread=True)
    def _fetch_suggestions(self, query: str) -> None:
        results = buscar_ciudades(query)
        self.app.call_from_thread(self._show_suggestions, results)

    def _show_suggestions(self, results: list) -> None:
        self._current_suggestions = results
        ol = self.query_one('#city-suggestions', OptionList)
        ol.clear_options()
        if not results:
            ol.display = False
            return
        for i, r in enumerate(results):
            ol.add_option(Option(r['display'], id=str(i)))
        ol.display = True

    def _hide_suggestions(self) -> None:
        try:
            ol = self.query_one('#city-suggestions', OptionList)
            ol.display = False
        except Exception:
            pass

    @on(OptionList.OptionSelected, '#city-suggestions')
    def _on_suggestion_selected(self, event: OptionList.OptionSelected) -> None:
        try:
            city_name = self._current_suggestions[int(event.option.id)]['name']
        except (ValueError, IndexError, TypeError):
            city_name = ''
        if city_name:
            self.query_one('#city-input', Input).value = city_name
            self._hide_suggestions()
            self.fetch_weather(city_name)

    # ── Events ──────────────────────────────────────────────────
    @on(Button.Pressed, '#query-btn')
    def _on_query(self, event: Button.Pressed) -> None:
        self._hide_suggestions()
        self._start_query()

    @on(Input.Submitted, '#city-input')
    def _on_submit(self, event: Input.Submitted) -> None:
        self._hide_suggestions()
        self._start_query()

    def _start_query(self) -> None:
        city = self.query_one('#city-input', Input).value.strip()
        if not city:
            self.app.notify('Ingresa una ciudad.', severity='warning')
            return
        self.fetch_weather(city)

    # ── Worker ──────────────────────────────────────────────────
    @work(thread=True)
    def fetch_weather(self, city: str) -> None:
        result_container = self.query_one('#weather-result', Container)
        self.app.call_from_thread(setattr, result_container, 'loading', True)

        try:
            data = obtener_clima(city)
            username = self.app.current_user
            guardar_consulta(username, data)
            self.app.last_weather_data = data
            self.app.call_from_thread(self._render_weather, data)
        except Exception as exc:
            self.app.call_from_thread(self._render_error, str(exc))
        finally:
            self.app.call_from_thread(setattr, result_container, 'loading', False)

    def _render_weather(self, data: dict) -> None:
        container = self.query_one('#weather-result', Container)
        container.remove_children()

        label = _weather_label(data.get('descripcion', ''))
        ciudad = data.get('ciudad', '?')
        temp = data.get('temperatura', '?')
        sensacion = data.get('sensacion_termica', '?')
        descripcion = data.get('descripcion', '?')
        humedad = data.get('humedad', '?')
        viento = data.get('viento_kmh', '?')

        container.mount(
            Vertical(
                Static(f'[bold cyan]{label}[/bold cyan]', classes='weather-emoji'),
                Static(f'[bold]{ciudad}[/bold]', classes='weather-city'),
                Static(f'[bold cyan]{temp}°C[/bold cyan]', classes='weather-temp'),
                Static(
                    f'[dim]{descripcion.capitalize()}[/dim]',
                    classes='text-center mb-1',
                ),
                classes='weather-main-panel',
            ),
            Horizontal(
                Vertical(
                    Static('Sensacion termica', classes='detail-label'),
                    Static(f'[bold]{sensacion}°C[/bold]', classes='detail-value'),
                    classes='weather-detail-card',
                ),
                Vertical(
                    Static('Humedad', classes='detail-label'),
                    Static(f'[bold]{humedad}%[/bold]', classes='detail-value'),
                    classes='weather-detail-card',
                ),
                Vertical(
                    Static('Viento', classes='detail-label'),
                    Static(f'[bold]{viento} km/h[/bold]', classes='detail-value'),
                    classes='weather-detail-card',
                ),
                classes='weather-details-row',
            ),
        )

        self.app.notify(f'Clima de {ciudad} obtenido', severity='information')

    def _render_error(self, error: str) -> None:
        container = self.query_one('#weather-result', Container)
        container.remove_children()
        container.mount(Static(
            f'[bold red]Error:[/bold red] {error}',
            classes='text-center mt-1',
        ))

    def refresh_data(self) -> None:
        pass
