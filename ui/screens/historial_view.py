from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, DataTable
from textual.containers import Container, Horizontal
from textual import on, work

from clima.historial import obtener_historial_personal, obtener_historial_usuario


class HistorialView(Container):
    """Personal weather query history view."""

    def compose(self) -> ComposeResult:
        yield Static(
            '[bold]Mi Historial Personal de Consultas[/bold]',
            classes='section-title',
        )
        with Horizontal(classes='search-row'):
            yield Input(
                placeholder='Filtrar por ciudad... (vacío = todo)',
                id='historial-city-input',
            )
            yield Button('Buscar', id='search-historial-btn', variant='primary')
        yield DataTable(id='historial-table')
        yield Static('', id='historial-msg')

    def on_mount(self) -> None:
        table = self.query_one('#historial-table', DataTable)
        table.add_column('Fecha/Hora', key='fecha')
        table.add_column('Ciudad', key='ciudad')
        table.add_column('Temp (°C)', key='temp')
        table.add_column('Condición', key='condicion')
        table.add_column('Humedad (%)', key='humedad')
        table.add_column('Viento (km/h)', key='viento')

    # ── Events ──────────────────────────────────────────────────
    @on(Button.Pressed, '#search-historial-btn')
    def _on_search(self, event: Button.Pressed) -> None:
        self._start_search()

    @on(Input.Submitted, '#historial-city-input')
    def _on_submit(self, event: Input.Submitted) -> None:
        self._start_search()

    def _start_search(self) -> None:
        city = self.query_one('#historial-city-input', Input).value.strip()
        self.fetch_historial(city)

    # ── Worker ──────────────────────────────────────────────────
    @work(thread=True)
    def fetch_historial(self, city: str) -> None:
        table = self.query_one('#historial-table', DataTable)
        self.app.call_from_thread(setattr, table, 'loading', True)

        try:
            username = self.app.current_user
            if city:
                rows = obtener_historial_personal(username, city)
                label = f'ciudad "[bold]{city}[/bold]"'
            else:
                rows = obtener_historial_usuario(username)
                label = 'tu historial completo'
            self.app.call_from_thread(self._populate_table, rows, label)
        except Exception as exc:
            self.app.call_from_thread(
                self.query_one('#historial-msg', Static).update,
                f'[bold red] Error: {exc}[/bold red]',
            )
        finally:
            self.app.call_from_thread(setattr, table, 'loading', False)

    def _populate_table(self, rows: list, label: str) -> None:
        table = self.query_one('#historial-table', DataTable)
        msg = self.query_one('#historial-msg', Static)
        table.clear()

        if not rows:
            msg.update(f'[dim]No se encontraron registros para {label}.[/dim]')
            return

        msg.update(f'[green]Se encontraron {len(rows)} registro(s) para {label}.[/green]')

        for row in rows:
            table.add_row(
                str(row.get('Fecha_Hora', '')),
                str(row.get('Ciudad', '')),
                str(row.get('Temperatura_C', '')),
                str(row.get('Condicion_Clima', '')),
                str(row.get('Humedad_Porcentaje', '')),
                str(row.get('Viento_kmh', '')),
            )

    def refresh_data(self) -> None:
        """Al activar la vista, carga todo el historial del usuario automáticamente."""
        self.query_one('#historial-city-input', Input).value = ''
        self.fetch_historial('')
