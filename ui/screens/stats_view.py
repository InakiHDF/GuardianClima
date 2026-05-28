from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Container, Horizontal, Vertical

from estadisticas.stats import calcular_estadisticas


class StatsView(Container):
    """Global usage statistics view."""

    def compose(self) -> ComposeResult:
        yield Static(
            '[bold]Estadísticas Globales de Uso[/bold]',
            classes='section-title',
        )

        # Top stat cards
        with Horizontal(classes='stats-cards-row'):
            with Vertical(classes='stat-card'):
                yield Static('Ciudad más consultada', classes='stat-card-title')
                yield Static('—', id='stat-top-city', classes='stat-card-value')
            with Vertical(classes='stat-card stat-card-warning'):
                yield Static('Total de consultas', classes='stat-card-title')
                yield Static('—', id='stat-total', classes='stat-card-value')
            with Vertical(classes='stat-card stat-card-accent'):
                yield Static('Temperatura promedio', classes='stat-card-title')
                yield Static('—', id='stat-avg-temp', classes='stat-card-value')

        # Bar chart section
        with Vertical(classes='stats-section'):
            yield Static('[bold]>> Consultas por ciudad[/bold]', classes='stats-section-title')
            yield Static('', id='stats-bar-chart')

        # Conditions section
        with Vertical(classes='stats-section'):
            yield Static('[bold]>> Distribución de condiciones climáticas[/bold]', classes='stats-section-title')
            yield Static('', id='stats-conditions')

        yield Static('', id='stats-empty')

    # ── Refresh ─────────────────────────────────────────────────
    def refresh_data(self) -> None:
        """Fetch stats and update the display."""
        try:
            data = calcular_estadisticas()
        except Exception:
            self.query_one('#stats-empty', Static).update(
                '[dim]Error al calcular estadísticas.[/dim]'
            )
            return

        total = data.get('total_consultas', 0)
        empty_widget = self.query_one('#stats-empty', Static)

        if total == 0:
            empty_widget.update('[dim]No hay datos aún. Consultá el clima primero.[/dim]')
            self.query_one('#stat-top-city', Static).update('—')
            self.query_one('#stat-total', Static).update('0')
            self.query_one('#stat-avg-temp', Static).update('—')
            self.query_one('#stats-bar-chart', Static).update('')
            self.query_one('#stats-conditions', Static).update('')
            return

        empty_widget.update('')

        # Top cards
        ciudad_max = data.get('ciudad_mas_consultada', '—')
        consultas_max = data.get('consultas_ciudad_max', 0)
        temp_prom = data.get('temperatura_promedio', 0)

        self.query_one('#stat-top-city', Static).update(
            f'[bold cyan]{ciudad_max}[/bold cyan]\n[dim]{consultas_max} consultas[/dim]'
        )
        self.query_one('#stat-total', Static).update(
            f'[bold yellow]{total}[/bold yellow]'
        )
        self.query_one('#stat-avg-temp', Static).update(
            f'[bold green]{temp_prom:.1f}°C[/bold green]'
        )

        # Bar chart
        consultas_por_ciudad: dict = data.get('consultas_por_ciudad', {})
        if consultas_por_ciudad:
            max_count = max(consultas_por_ciudad.values()) if consultas_por_ciudad else 1
            bar_width = 30
            lines: list[str] = []
            # Sort descending by count
            sorted_cities = sorted(
                consultas_por_ciudad.items(), key=lambda x: x[1], reverse=True
            )
            for city, count in sorted_cities:
                bar_len = max(1, int((count / max_count) * bar_width))
                bar = '█' * bar_len
                lines.append(
                    f'  [cyan]{city:<20}[/cyan] [bold green]{bar}[/bold green] {count}'
                )
            self.query_one('#stats-bar-chart', Static).update('\n'.join(lines))
        else:
            self.query_one('#stats-bar-chart', Static).update('[dim]Sin datos.[/dim]')

        # Conditions distribution
        condiciones: dict = data.get('condiciones', {})
        if condiciones:
            total_cond = sum(condiciones.values())
            lines = []
            sorted_conds = sorted(
                condiciones.items(), key=lambda x: x[1], reverse=True
            )
            for cond, count in sorted_conds:
                pct = (count / total_cond * 100) if total_cond else 0
                bar_len = max(1, int(pct / 100 * 25))
                bar = '▓' * bar_len
                lines.append(
                    f'  [yellow]{cond:<20}[/yellow] [bold]{bar}[/bold] {pct:.1f}%  ({count})'
                )
            self.query_one('#stats-conditions', Static).update('\n'.join(lines))
        else:
            self.query_one('#stats-conditions', Static).update('[dim]Sin datos.[/dim]')
