# GuardiánClima ITBA — Documentación del Proyecto

> Documentación pensada para personas **sin experiencia técnica** que quieran entender cómo está construida esta aplicación.

---

## ¿Qué es GuardiánClima?

**GuardiánClima** es una aplicación de clima que corre en la terminal (la pantalla negra donde se escriben comandos). Permite a los usuarios:

- Buscar el clima actual de cualquier ciudad del mundo
- Ver su historial de consultas anteriores
- Explorar estadísticas globales de todas las búsquedas
- Recibir consejos de vestimenta generados por Inteligencia Artificial
- Registrarse e iniciar sesión con usuario y contraseña

---

## Estructura del proyecto (los archivos y carpetas)

```
Guardian ITBA/
│
├── main.py                  ← El punto de arranque: ejecutar esto inicia la app
├── config.py                ← Configuración central (claves de APIs, rutas de archivos)
├── requirements.txt         ← Lista de librerías externas necesarias
├── .env                     ← Claves secretas (APIs) — no se sube a GitHub
├── .env.example             ← Plantilla de ejemplo para crear el .env
├── consigna.txt             ← Requisitos del proyecto (en español)
│
├── auth/                    ← Todo lo relacionado con usuarios y contraseñas
│   ├── manager.py           ← Registro, login y guardado de usuarios
│   └── validator.py         ← Reglas de seguridad para las contraseñas
│
├── clima/                   ← Todo lo relacionado con el clima
│   ├── api.py               ← Llama a la API de OpenWeatherMap para traer datos
│   └── historial.py         ← Guarda y recupera el historial de consultas
│
├── ia/                      ← Inteligencia Artificial
│   └── gemini.py            ← Llama a Google Gemini para generar consejos de ropa
│
├── estadisticas/            ← Análisis de datos
│   └── stats.py             ← Calcula estadísticas sobre todas las consultas
│
├── ui/                      ← Todo lo visual (la interfaz gráfica en la terminal)
│   ├── app.py               ← Controlador principal: maneja pantallas y sesión
│   ├── styles.tcss          ← Estilos visuales (colores, tamaños, bordes)
│   └── screens/             ← Cada "pantalla" de la aplicación
│       ├── login_screen.py      ← Pantalla de login y registro
│       ├── dashboard_screen.py  ← Menú principal con barra lateral
│       ├── clima_view.py        ← Vista de búsqueda del clima
│       ├── historial_view.py    ← Vista del historial personal
│       ├── stats_view.py        ← Vista de estadísticas globales
│       ├── consejo_view.py      ← Vista de consejos de la IA
│       └── about_view.py        ← Vista "Acerca de" con ayuda
│
└── data/                    ← Datos guardados por la app (se generan automáticamente)
    ├── usuarios_simulados.csv   ← Base de datos de usuarios
    └── historial_global.csv     ← Registro de todas las consultas de clima
```

---

## Cómo funciona el flujo completo

La aplicación sigue este camino cuando la usás:

```
1. Ejecutás main.py
       ↓
2. Se abre la pantalla de Login / Registro
       ↓
3. Ingresás con tu usuario y contraseña (o te registrás)
       ↓
4. Accedés al Panel Principal (Dashboard) con 6 opciones en el menú
       ↓
   ┌─── Opción 1: Consultar Clima
   │         Buscás una ciudad → la app llama a OpenWeatherMap → muestra temperatura, viento, humedad
   │         Cada búsqueda se guarda automáticamente en el historial
   │
   ├─── Opción 2: Mi Historial
   │         Ves todas tus búsquedas anteriores ordenadas por fecha
   │         Podés filtrar por ciudad
   │
   ├─── Opción 3: Estadísticas
   │         La app analiza todas las consultas de todos los usuarios
   │         Muestra: ciudad más consultada, temperatura promedio, gráficos de barras
   │
   ├─── Opción 4: Consejo IA
   │         Basado en el último clima que consultaste, Google Gemini te dice qué ropa ponerte
   │
   ├─── Opción 5: Acerca De
   │         Información sobre la app y guía de uso
   │
   └─── Opción 6: Cerrar Sesión
             Volvés a la pantalla de login
```

---

## Explicación de cada archivo

### `main.py` — El arranque

Es el archivo más corto del proyecto. Su único trabajo es importar la aplicación y ejecutarla. Es equivalente al botón de encendido.

---

### `config.py` — El tablero de configuración

Guarda las variables que toda la aplicación necesita saber:

- **OWM_API_KEY**: La clave secreta para usar la API de OpenWeatherMap (la que trae los datos del clima)
- **GEMINI_API_KEY**: La clave secreta para usar Google Gemini (la IA)
- **DATA_DIR**: La carpeta donde se guardan los archivos CSV con datos
- **USERS_FILE**: Ruta exacta al archivo de usuarios
- **HISTORIAL_FILE**: Ruta exacta al archivo de historial

Estas variables las lee desde el archivo `.env` para que las claves secretas nunca queden escritas directamente en el código.

---

### `.env` y `.env.example` — Las claves secretas

El archivo `.env` contiene las claves reales de las APIs. No se comparte públicamente (está en el `.gitignore`).
El `.env.example` es una plantilla que muestra qué claves hacen falta, sin revelar los valores reales:

```
OWM_API_KEY=tu_clave_aqui
GEMINI_API_KEY=tu_clave_aqui
```

---

### `requirements.txt` — Las librerías necesarias

Lista las dependencias externas del proyecto (herramientas que no vienen incluidas en Python):

| Librería | Para qué sirve |
|----------|----------------|
| `textual` | Crear la interfaz visual en la terminal |
| `requests` | Hacer llamadas HTTP a las APIs externas |
| `google-genai` | Conectarse a Google Gemini (IA) |
| `python-dotenv` | Leer las claves del archivo `.env` |

Se instalan todas con: `pip install -r requirements.txt`

---

## Módulo AUTH — Usuarios y contraseñas

### `auth/manager.py` — El guardián de cuentas

Maneja todo lo relacionado con las cuentas de usuario:

**Funciones principales:**

- `registrar_usuario(username, password)` → Crea una cuenta nueva y la guarda en el CSV
- `autenticar(username, password)` → Verifica si el usuario y contraseña son correctos
- `usuario_existe(username)` → Revisa si un nombre de usuario ya está en uso

Los datos se guardan en `data/usuarios_simulados.csv`:

```
username,password_simulada
martin,MiClave123!
ana,Segura!456
```

> ⚠️ **Aviso educativo**: En esta versión las contraseñas se guardan sin encriptar. En una aplicación real, siempre se guardarían encriptadas (con hashing).

---

### `auth/validator.py` — El inspector de contraseñas

Verifica que las contraseñas cumplan 5 reglas de seguridad antes de permitir el registro:

| Regla | Ejemplo válido |
|-------|---------------|
| Mínimo 8 caracteres | `Abc123!x` ✓ |
| Al menos 1 letra mayúscula | `A...` ✓ |
| Al menos 1 letra minúscula | `...a` ✓ |
| Al menos 1 número | `...1` ✓ |
| Al menos 1 símbolo especial | `...!` ✓ |

La pantalla de registro muestra en tiempo real qué reglas ya se cumplen (en verde) y cuáles faltan (en rojo), a medida que el usuario escribe.

---

## Módulo CLIMA — Datos meteorológicos

### `clima/api.py` — El mensajero del clima

Se conecta a la API de **OpenWeatherMap** (un servicio web que tiene datos del clima de todo el mundo) y trae la información actual de una ciudad.

**Datos que trae:**

```
Ciudad:             Buenos Aires
Temperatura:        18°C
Sensación térmica:  15°C
Humedad:            72%
Descripción:        Parcialmente nublado
Viento:             23 km/h
```

También tiene una función de **autocompletado**: mientras escribís el nombre de una ciudad, sugiere opciones (igual que Google cuando buscás algo).

Si algo falla (sin internet, ciudad inexistente, clave incorrecta), muestra un mensaje de error claro.

---

### `clima/historial.py` — El archivo de memoria

Cada vez que alguien consulta el clima, esta parte del código lo registra automáticamente en `data/historial_global.csv`.

**Funciones principales:**

- `guardar_consulta(username, datos)` → Anota la consulta con fecha y hora
- `obtener_historial_usuario(username)` → Devuelve todas las búsquedas de un usuario
- `obtener_historial_personal(username, ciudad)` → Filtra por ciudad
- `obtener_todo_historial()` → Trae el historial de todos los usuarios (para estadísticas)

El archivo CSV resultante tiene este formato:

```
NombreDeUsuario,Ciudad,Fecha_Hora,Temperatura_C,Condicion_Clima,Humedad_Porcentaje,Viento_kmh
martin,Buenos Aires,2026-05-25 14:30:00,18.5,Nublado,72,23.1
ana,Mendoza,2026-05-25 15:00:00,22.0,Soleado,40,10.5
```

---

## Módulo IA — Inteligencia Artificial

### `ia/gemini.py` — El asesor de moda inteligente

Se conecta a **Google Gemini** (la IA de Google) y le envía los datos del clima actual. La IA responde con un consejo práctico de qué ropa usar.

**Ejemplo de prompt que se le manda a la IA:**
> "Hoy en Buenos Aires hay 18°C, sensación térmica de 15°C, está parcialmente nublado, humedad del 72% y viento de 23 km/h. ¿Qué ropa recomendás? Respondé en 3-4 oraciones, de forma práctica y concisa."

**Ejemplo de respuesta de la IA:**
> "Para las condiciones de hoy en Buenos Aires, recomiendo llevar una campera liviana o buzo, ya que la sensación térmica es algo fresca. El pantalón largo es ideal dado el viento moderado. Si salís al mediodía podés prescindir de la campera, pero llevala por las dudas para la tarde."

El código también detecta automáticamente qué versión de Gemini está disponible y usa la mejor.

---

## Módulo ESTADÍSTICAS — Análisis de datos

### `estadisticas/stats.py` — El analista de datos

Lee todo el historial global y calcula estadísticas útiles:

**Lo que calcula:**

| Estadística | Descripción |
|-------------|-------------|
| Total de consultas | Cuántas búsquedas se hicieron en total |
| Ciudad más consultada | Qué ciudad se buscó más veces |
| Temperatura promedio | Promedio de todas las temperaturas registradas |
| Consultas por ciudad | Ranking de ciudades más buscadas |
| Condiciones del tiempo | Qué tipo de clima aparece más (nublado, soleado, etc.) |

Estos datos se muestran en la pantalla de Estadísticas con gráficos de barras hechos con caracteres ASCII (█████).

---

## Módulo UI — La interfaz visual

La interfaz está construida con **Textual**, una librería de Python que permite crear aplicaciones visualmente ricas dentro de la terminal, con paneles, botones, tablas y colores.

---

### `ui/app.py` — El director de orquesta

Es el cerebro central de la interfaz. Se encarga de:

- Iniciar la aplicación y mostrar la pantalla de login
- Recordar qué usuario está logueado (`current_user`)
- Guardar el último clima consultado (`last_weather_data`) para que la vista de IA pueda usarlo
- Cambiar entre la pantalla de login y el dashboard
- Manejar el cierre de sesión

---

### `ui/styles.tcss` — El diseñador gráfico

Archivo de estilos similar al CSS de las páginas web, pero para la terminal. Define:

- **Colores**: Fondo oscuro (#0d0d0d), texto en gris claro, acentos en cyan
- **Tamaños**: Ancho de la barra lateral (34 caracteres), ancho del card de login (72)
- **Bordes**: Estilo de las cajas y paneles
- **Espaciado**: Márgenes y padding entre elementos

---

### `ui/screens/login_screen.py` — La puerta de entrada

Muestra dos pestañas: **Iniciar Sesión** y **Registrarse**.

**En el login:**
- Campo de usuario
- Campo de contraseña (los caracteres se ocultan)
- Botón "Ingresar" (o presionar Enter)
- Botón "Salir" para cerrar la app

**En el registro:**
- Campo de usuario
- Campo de contraseña con feedback en tiempo real de las 5 reglas de seguridad
- Botón "Crear cuenta"

Si el login es exitoso, automáticamente cambia al Dashboard.

---

### `ui/screens/dashboard_screen.py` — El panel de control

Es la pantalla principal después de loguearse. Tiene:

- **Barra lateral izquierda** con 6 botones de navegación
- **Área de contenido** a la derecha que cambia según lo seleccionado
- **Header** con el nombre de la app y un reloj en tiempo real

Los atajos de teclado del 1 al 6 permiten navegar rápidamente entre secciones sin usar el mouse.

---

### `ui/screens/clima_view.py` — La consulta del clima

Pantalla para buscar el clima de una ciudad:

1. El usuario escribe el nombre de la ciudad
2. Aparecen sugerencias de autocompletado (igual que Google)
3. Al confirmar, se llama a la API en segundo plano (sin congelar la pantalla)
4. Se muestra el resultado con temperatura, descripción, humedad y viento
5. La consulta se guarda automáticamente en el historial

Usa **hilos de ejecución en segundo plano** (workers) para que mientras carga los datos la interfaz siga respondiendo.

---

### `ui/screens/historial_view.py` — El historial personal

Muestra una tabla con todas las consultas del usuario actual:

| Fecha/Hora | Ciudad | Temp (°C) | Condición | Humedad (%) | Viento (km/h) |
|------------|--------|-----------|-----------|-------------|---------------|
| 2026-05-25 14:30 | Buenos Aires | 18.5 | Nublado | 72 | 23.1 |

Permite filtrar por nombre de ciudad. Se recarga automáticamente cada vez que entrás a esta sección.

---

### `ui/screens/stats_view.py` — Las estadísticas globales

Muestra un panel de análisis con:

- **Cards de resumen**: Ciudad top, total de consultas, temperatura promedio
- **Gráfico de barras** de consultas por ciudad (con barras █████ ASCII)
- **Distribución** de condiciones climáticas (soleado, nublado, lluvia, etc.)

Se recalcula automáticamente cada vez que entrás a la sección.

---

### `ui/screens/consejo_view.py` — El consejo de la IA

Muestra el contexto del último clima consultado y un botón para pedirle consejo a la IA.

- Si no consultaste ningún clima todavía, te avisa que primero vayas a "Consultar Clima"
- Al presionar el botón, llama a Gemini en segundo plano y muestra el consejo cuando llega

---

### `ui/screens/about_view.py` — Acerca de la app

Pantalla informativa con:

- Descripción general de la app
- Guía de uso de cada opción del menú
- Explicación técnica de cómo funciona cada componente
- Lista de conceptos académicos demostrados en el proyecto
- Nombres del equipo de desarrollo e institución

---

## Archivos de datos (generados automáticamente)

### `data/usuarios_simulados.csv`

Se crea automáticamente la primera vez que alguien se registra. Guarda usuarios y contraseñas en texto plano (solo para este proyecto educativo).

### `data/historial_global.csv`

Se crea automáticamente la primera vez que alguien consulta el clima. Acumula todas las consultas de todos los usuarios y es la fuente de datos para las estadísticas.

---

## Tecnologías utilizadas

| Tecnología | Tipo | Para qué se usa |
|-----------|------|-----------------|
| Python | Lenguaje de programación | Todo el backend y lógica de la app |
| Textual | Librería Python | Interfaz visual en la terminal |
| OpenWeatherMap API | Servicio web externo | Datos del clima en tiempo real |
| Google Gemini API | Servicio de IA externo | Consejos de vestimenta generados por IA |
| CSV | Formato de archivo | Almacenamiento de usuarios e historial |
| requests | Librería Python | Comunicación con las APIs |
| python-dotenv | Librería Python | Lectura segura de claves secretas |

---

## Conceptos académicos demostrados

| Área | Conceptos |
|------|-----------|
| **Programación** | Python modular, programación orientada a objetos, hilos (threads), manejo de errores |
| **Ciberseguridad** | Validación de contraseñas, protección de claves API, advertencias sobre seguridad en almacenamiento |
| **Análisis de datos** | Procesamiento de CSV, cálculo de estadísticas, visualización con gráficos ASCII |
| **Inteligencia Artificial** | Ingeniería de prompts, integración de APIs de IA generativa |
| **Cloud / Conectividad** | APIs REST, parseo de JSON, servicios web de terceros |

---

## Cómo ejecutar el proyecto

1. **Clonar el repositorio** y abrir la carpeta del proyecto
2. **Instalar dependencias**:
   ```
   pip install -r requirements.txt
   ```
3. **Configurar las claves API**: Copiar `.env.example` como `.env` y completar las claves de OpenWeatherMap y Google Gemini
4. **Ejecutar la aplicación**:
   ```
   python main.py
   ```

---

*Proyecto desarrollado para el Challenge Tecnología — ITBA*
