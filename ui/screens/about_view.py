from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Container, VerticalScroll


class AboutView(Container):
    """About / help view with app info, usage guide, and team credits."""

    def compose(self) -> ComposeResult:
        with VerticalScroll(id='about-scroll'):
            # ── Header ──────────────────────────────────────────
            with Container(classes='about-section'):
                yield Static(
                    '  [bold cyan]GuardiánClima ITBA[/bold cyan]',
                    classes='about-header',
                )
                yield Static(
                    '[italic]Aplicación de consulta climática con interfaz premium '
                    'desarrollada para el challenge de Tecnología del ITBA.[/italic]\n\n'
                    'GuardiánClima te permite consultar el clima actual de cualquier ciudad, '
                    'mantener un historial de búsquedas, ver estadísticas globales de uso '
                    'y recibir consejos de vestimenta potenciados por Inteligencia Artificial.',
                    classes='about-body',
                )

            # ── Cómo usar ──────────────────────────────────────
            with Container(classes='about-section'):
                yield Static(
                    '>>  [bold yellow]Cómo usar cada opción[/bold yellow]',
                    classes='about-header',
                )
                yield Static(
                    '[bold cyan]1.   Consultar Clima[/bold cyan]\n'
                    '   Ingresá el nombre de una ciudad y obtené los datos '
                    'meteorológicos actuales: temperatura, sensación térmica, '
                    'humedad, viento y descripción del clima.\n\n'
                    '[bold cyan]2.   Mi Historial[/bold cyan]\n'
                    '   Consultá tus búsquedas anteriores filtrando por ciudad. '
                    'Los datos se muestran en una tabla con fecha, temperatura, '
                    'condición, humedad y viento.\n\n'
                    '[bold cyan]3.   Estadísticas[/bold cyan]\n'
                    '   Visualizá estadísticas globales: ciudad más consultada, '
                    'total de consultas, temperatura promedio, distribución por '
                    'ciudad y condiciones climáticas.\n\n'
                    '[bold cyan]4.   Consejo IA[/bold cyan]\n'
                    '   Basándose en tu última consulta climática, la IA te sugiere '
                    'cómo vestirte para el día. ¡Necesitás consultar el clima primero!\n\n'
                    '[bold cyan]5.  Acerca De[/bold cyan]\n'
                    '   Esta pantalla. Información sobre la app, su funcionamiento '
                    'interno y el equipo.\n\n'
                    '[bold cyan]6.   Cerrar Sesión[/bold cyan]\n'
                    '   Cerrá tu sesión y volvé a la pantalla de login.',
                    classes='about-body',
                )

            # ── Funcionamiento interno ──────────────────────────
            with Container(classes='about-section'):
                yield Static(
                    '>>  [bold green]Funcionamiento interno[/bold green]',
                    classes='about-header',
                )
                yield Static(
                    '[bold]Sistema de usuarios[/bold]\n'
                    '  • Registro y autenticación con archivo CSV simulado.\n'
                    '  • Validación de contraseñas con 5 criterios de seguridad '
                    '(longitud, mayúsculas, minúsculas, números, caracteres especiales).\n\n'
                    '[bold red][!]  Advertencia de seguridad:[/bold red]\n'
                    '  [italic]El almacenamiento actual de contraseñas en texto plano '
                    'es inseguro y se usa solo con fines educativos. En un entorno '
                    'de producción se utilizaría hashing seguro (bcrypt / Argon2) '
                    'con salt para proteger las credenciales.[/italic]\n\n'
                    '[bold]Consulta de clima[/bold]\n'
                    '  • API REST de OpenWeatherMap.\n'
                    '  • Se envía una petición HTTP y se parsea la respuesta JSON.\n\n'
                    '[bold]Historial[/bold]\n'
                    '  • Archivo CSV global compartido entre todos los usuarios.\n'
                    '  • Cada consulta queda registrada con fecha, ciudad y datos climáticos.\n\n'
                    '[bold]Estadísticas[/bold]\n'
                    '  • Cálculos realizados sobre el historial global.\n'
                    '  • Promedios, conteos y distribuciones en tiempo real.\n\n'
                    '[bold]Consejo IA[/bold]\n'
                    '  • Integración con Google Gemini API.\n'
                    '  • Prompt engineering para generar consejos de vestimenta '
                    'contextualizados al clima actual.',
                    classes='about-body',
                )

            # ── Equipo ──────────────────────────────────────────
            with Container(classes='about-section'):
                yield Static(
                    '>>  [bold yellow]Equipo de desarrollo[/bold yellow]',
                    classes='about-header',
                )
                yield Static(
                    '  [bold]•[/bold]  Coccé Maia\n'
                    '  [bold]•[/bold]  Góngora Rosi Iñaki\n'
                    '  [bold]•[/bold]  Maccari Agustina\n'
                    '  [bold]•[/bold]  Sánchez Clariá Facundo\n\n'
                    '  [bold cyan]Grupo:[/bold cyan]  BDefenders\n'
                    '  [bold cyan]Universidad:[/bold cyan]  ITBA – Instituto Tecnológico de Buenos Aires',
                    classes='about-body',
                )

    def refresh_data(self) -> None:
        """No dynamic data to refresh."""
        pass
