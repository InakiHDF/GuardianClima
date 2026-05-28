from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Label, Static, Rule, ContentSwitcher
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual import on

from ui.screens.clima_view import ClimaView
from ui.screens.historial_view import HistorialView
from ui.screens.stats_view import StatsView
from ui.screens.consejo_view import ConsejoView
from ui.screens.about_view import AboutView


_NAV_ITEMS = [
    ('nav-clima',     'clima',     '[1] Consultar Clima'),
    ('nav-historial', 'historial', '[2] Mi Historial'),
    ('nav-stats',     'stats',     '[3] Estadísticas'),
    ('nav-consejo',   'consejo',   '[4] Consejo IA'),
    ('nav-about',     'about',     '[5] Acerca De'),
    ('nav-logout',    'logout',    '[6] Cerrar Sesión'),
]


class DashboardScreen(Screen):
    """Main dashboard with sidebar navigation and content switcher."""

    BINDINGS = [
        ('1', 'switch_1', 'Clima'),
        ('2', 'switch_2', 'Historial'),
        ('3', 'switch_3', 'Estadísticas'),
        ('4', 'switch_4', 'Consejo IA'),
        ('5', 'switch_5', 'Acerca De'),
        ('6', 'switch_6', 'Cerrar Sesión'),
    ]

    selected_nav: reactive[str] = reactive('clima')

    # ── Compose ─────────────────────────────────────────────────
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id='dashboard-wrapper'):
            with Vertical(id='sidebar'):
                yield Static(
                    '[bold]GuardiánClima[/bold]',
                    id='sidebar-logo',
                )
                yield Label('', id='welcome-label')
                yield Rule()
                for btn_id, _key, label in _NAV_ITEMS:
                    yield Button(label, id=btn_id, classes='nav-btn')

            with ContentSwitcher(id='content-switcher', initial='clima-view'):
                yield ClimaView(id='clima-view')
                yield HistorialView(id='historial-view')
                yield StatsView(id='stats-view')
                yield ConsejoView(id='consejo-view')
                yield AboutView(id='about-view')

        yield Footer()

    # ── Lifecycle ───────────────────────────────────────────────
    def on_mount(self) -> None:
        username = self.app.current_user or '...'
        self.query_one('#welcome-label', Label).update(
            f'> [bold]{username}[/bold]'
        )
        # Trigger initial highlight
        self.selected_nav = 'clima'

    # ── Watch selected_nav ──────────────────────────────────────
    def watch_selected_nav(self, value: str) -> None:
        # Update button highlights
        for btn_id, key, _label in _NAV_ITEMS:
            btn = self.query_one(f'#{btn_id}', Button)
            if key == value:
                btn.add_class('-active')
            else:
                btn.remove_class('-active')

        # Switch content
        view_id = f'{value}-view'
        switcher = self.query_one('#content-switcher', ContentSwitcher)
        try:
            switcher.current = view_id
        except Exception:
            pass

        # Refresh the active view's data
        try:
            active_view = self.query_one(f'#{view_id}')
            if hasattr(active_view, 'refresh_data'):
                active_view.refresh_data()
        except Exception:
            pass

    # ── Nav button handler ──────────────────────────────────────
    @on(Button.Pressed, '.nav-btn')
    def _on_nav_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id or ''
        # Remove focus immediately so the button never keeps the focus highlight
        self.screen.set_focus(None)
        for bid, key, _label in _NAV_ITEMS:
            if bid == btn_id:
                if key == 'logout':
                    self.app.do_logout()
                else:
                    self.selected_nav = key
                return

    # ── Keyboard shortcuts ──────────────────────────────────────
    def action_switch_1(self) -> None:
        self.selected_nav = 'clima'

    def action_switch_2(self) -> None:
        self.selected_nav = 'historial'

    def action_switch_3(self) -> None:
        self.selected_nav = 'stats'

    def action_switch_4(self) -> None:
        self.selected_nav = 'consejo'

    def action_switch_5(self) -> None:
        self.selected_nav = 'about'

    def action_switch_6(self) -> None:
        self.app.do_logout()
