import sys
import os

# Ensure project root is in path for backend imports
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from textual.app import App, ComposeResult
from textual.reactive import reactive

from ui.screens.login_screen import LoginScreen
from ui.screens.dashboard_screen import DashboardScreen


class GuardianClimaApp(App):
    """GuardiánClima ITBA – Tu clima, tu estilo."""

    TITLE = 'GuardiánClima ITBA'
    CSS_PATH = 'styles.tcss'

    current_user: reactive[str] = reactive('', init=False)
    last_weather_data: reactive[dict | None] = reactive(None, init=False)

    def on_mount(self) -> None:
        self.push_screen(LoginScreen())

    def do_login(self, username: str) -> None:
        """Set the current user and navigate to the dashboard."""
        self.current_user = username
        self.switch_screen(DashboardScreen())

    def do_logout(self) -> None:
        """Clear user state and return to the login screen."""
        self.current_user = ''
        self.last_weather_data = None
        self.switch_screen(LoginScreen())
