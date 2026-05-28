from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.containers import Vertical, Container, Horizontal
from textual import on

from auth.manager import usuario_existe, autenticar, registrar_usuario
from auth.validator import validar_contrasena


class LoginScreen(Screen):
    """Pantalla de inicio de sesión y registro."""

    def compose(self) -> ComposeResult:
        with Container(id='login-wrapper'):
            with Vertical(id='login-card'):
                yield Static(
                    '[bold]GuardiánClima ITBA[/bold]',
                    id='login-banner',
                )
                yield Static(
                    'Tu clima, tu estilo',
                    id='login-subtitle',
                )

                # Manual tab bar (replaces TabbedContent)
                with Horizontal(id='tab-bar'):
                    yield Button(
                        'Iniciar Sesión',
                        id='tab-login-btn',
                        classes='tab-btn tab-active',
                    )
                    yield Button(
                        'Registrarse',
                        id='tab-reg-btn',
                        classes='tab-btn',
                    )

                # Login section (shown by default)
                with Container(id='section-login'):
                    yield Input(
                        placeholder='Nombre de usuario',
                        id='login-user',
                    )
                    yield Input(
                        placeholder='Contraseña',
                        password=True,
                        id='login-pass',
                    )
                    yield Button(
                        'Iniciar Sesión',
                        id='login-btn',
                        variant='primary',
                    )

                # Register section (hidden by default)
                with Container(id='section-register', classes='hidden'):
                    yield Input(
                        placeholder='Nuevo nombre de usuario',
                        id='reg-user',
                    )
                    yield Input(
                        placeholder='Contraseña',
                        password=True,
                        id='reg-pass',
                    )
                    yield Static('', id='password-feedback')
                    yield Button(
                        'Registrarse',
                        id='register-btn',
                        variant='success',
                    )

                # Shared message area (sits right below active section)
                yield Static('', id='form-msg')
                yield Button(
                    'Salir de la Aplicación',
                    id='exit-btn',
                    variant='error',
                )

    # ── Tab switching ────────────────────────────────────────────
    @on(Button.Pressed, '#tab-login-btn')
    def _switch_to_login(self, event: Button.Pressed) -> None:
        self._show_tab('login')

    @on(Button.Pressed, '#tab-reg-btn')
    def _switch_to_register(self, event: Button.Pressed) -> None:
        self._show_tab('register')

    def _show_tab(self, tab: str) -> None:
        tab_login = self.query_one('#tab-login-btn', Button)
        tab_reg = self.query_one('#tab-reg-btn', Button)
        section_login = self.query_one('#section-login', Container)
        section_reg = self.query_one('#section-register', Container)
        self.query_one('#form-msg', Static).update('')

        if tab == 'login':
            tab_login.add_class('tab-active')
            tab_reg.remove_class('tab-active')
            section_login.display = True
            section_reg.display = False
        else:
            tab_reg.add_class('tab-active')
            tab_login.remove_class('tab-active')
            section_login.display = False
            section_reg.display = True

        self.screen.set_focus(None)

    # ── Password validation feedback ─────────────────────────────
    @on(Input.Changed, '#reg-pass')
    def _on_reg_pass_changed(self, event: Input.Changed) -> None:
        feedback_widget = self.query_one('#password-feedback', Static)
        pwd = event.value
        if not pwd:
            feedback_widget.update('')
            return

        result = validar_contrasena(pwd)
        lines: list[str] = []
        for criterio in result.get('criterios', []):
            # No usar corchetes en el icono: Rich los interpreta como markup tags
            if criterio['cumple']:
                icon = '[bold green]OK[/bold green]'
            else:
                icon = '[bold red]NO[/bold red]'
            nombre = criterio.get('nombre', '')
            sugerencia = criterio.get('sugerencia', '') if not criterio['cumple'] else ''
            line = f'{icon}  {nombre}'
            if sugerencia:
                line += f'\n     [dim]{sugerencia}[/dim]'
            lines.append(line)

        feedback_widget.update('\n'.join(lines))

    # ── Login ────────────────────────────────────────────────────
    @on(Button.Pressed, '#login-btn')
    def _handle_login(self, event: Button.Pressed) -> None:
        self._do_login()

    def _do_login(self) -> None:
        msg = self.query_one('#form-msg', Static)
        username = self.query_one('#login-user', Input).value.strip()
        password = self.query_one('#login-pass', Input).value

        if not username or not password:
            msg.update('[bold red] Completá ambos campos.[/bold red]')
            return

        if autenticar(username, password):
            msg.update('')
            self.app.do_login(username)
        else:
            msg.update('[bold red] Usuario o contraseña incorrectos.[/bold red]')

    # ── Register ─────────────────────────────────────────────────
    @on(Button.Pressed, '#register-btn')
    def _handle_register(self, event: Button.Pressed) -> None:
        self._do_register()

    def _do_register(self) -> None:
        msg = self.query_one('#form-msg', Static)
        username = self.query_one('#reg-user', Input).value.strip()
        password = self.query_one('#reg-pass', Input).value

        if not username:
            msg.update('[bold red] Ingresá un nombre de usuario.[/bold red]')
            return

        if usuario_existe(username):
            msg.update('[bold red] Ese usuario ya existe.[/bold red]')
            return

        result = validar_contrasena(password)
        if not result.get('es_valida', False):
            msg.update('[bold red] La contraseña no cumple los criterios.[/bold red]')
            return

        registrar_usuario(username, password)
        msg.update('')
        self.app.do_login(username)

    # ── Salir ────────────────────────────────────────────────────
    @on(Button.Pressed, '#exit-btn')
    def _handle_exit(self, event: Button.Pressed) -> None:
        self.app.exit()

    # ── Enter key submission ─────────────────────────────────────
    @on(Input.Submitted, '#login-user')
    @on(Input.Submitted, '#login-pass')
    def _login_submit(self, event: Input.Submitted) -> None:
        self._do_login()

    @on(Input.Submitted, '#reg-user')
    @on(Input.Submitted, '#reg-pass')
    def _register_submit(self, event: Input.Submitted) -> None:
        self._do_register()
