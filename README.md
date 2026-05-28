# GuardiánClima ITBA — Guía de Instalación y Configuración


## 1. Requisitos previos

Antes de comenzar, asegurate de tener instalado:

- **Python 3.10 o superior** → [descargar en python.org](https://www.python.org/downloads/)
- **pip** (viene incluido con Python)
- Acceso a internet (para las APIs de clima e IA)

---

## 2. Instalación de librerías

El proyecto usa cuatro librerías externas. Para instalarlas todas de una vez:

```
pip install -r requirements.txt
```

### ¿Qué instala ese comando?

| Librería | Versión mínima | Para qué sirve |
|----------|---------------|----------------|
| `textual` | 3.0.0 | Framework que genera la interfaz visual en la terminal (paneles, botones, tablas, colores) |
| `requests` | 2.31.0 | Realiza las llamadas HTTP a la API de OpenWeatherMap para traer datos del clima |
| `google-genai` | 1.0.0 | SDK oficial de Google para conectarse a Gemini (la IA que genera los consejos de ropa) |
| `python-dotenv` | 1.0.0 | Lee el archivo `.env` y carga las claves secretas sin que aparezcan en el código |

---

## 3. Obtención de las API keys

La aplicación necesita **dos claves de acceso** a servicios externos. A continuación se explica cómo obtener cada una.

### 3.1 OpenWeatherMap (datos del clima)

1. Entrá a [https://home.openweathermap.org/users/sign_up](https://home.openweathermap.org/users/sign_up)
2. Creá una cuenta gratuita (solo necesitás un email)
3. Una vez registrado, andá a **"My API keys"** en el menú de tu perfil
4. Copiá la clave que aparece por defecto (o generá una nueva con el botón "Generate")
5. **Importante:** las claves nuevas pueden tardar hasta **10 minutos** en activarse

La clave se ve así: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

### 3.2 Google Gemini (Inteligencia Artificial)

1. Entrá a [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Iniciá sesión con tu cuenta de Google
3. Hacé clic en **"Create API key"**
4. Seleccioná un proyecto de Google Cloud (podés crear uno nuevo gratuito)
5. Copiá la clave generada

La clave se ve así: `AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5`



## 4. Configuración segura de las API keys (archivo `.env`)

### ¿Por qué no poner las claves directamente en el código?

Si las claves se escriben directamente en el código fuente, corren el riesgo de:
- Quedar expuestas si subís el proyecto a GitHub u otra plataforma
- Ser usadas por terceros para consumir tu cuota de API

La solución es usar un archivo `.env` (con un punto adelante) que **nunca se sube al repositorio**.

### Paso a paso

**1.** En la carpeta raíz del proyecto, encontrás el archivo `.env.example`. Abrilo con cualquier editor de texto (Notepad, VS Code, etc.). Su contenido es:

```
OWM_API_KEY=tu_clave_aqui
GEMINI_API_KEY=tu_clave_aqui
```

**2.** Creá una copia de ese archivo en la misma carpeta y llamala exactamente `.env` (con punto adelante, sin extensión adicional).

**3.** Reemplazá `tu_clave_aqui` con tus claves reales:

```
OWM_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
GEMINI_API_KEY=AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5
```

**4.** Guardá el archivo. **No lo subas a ningún repositorio.** El archivo `.gitignore` ya está configurado para ignorarlo automáticamente.

### Estructura de nombres (importante)

| Nombre de la variable | Valor |
|-----------------------|-------|
| `OWM_API_KEY` | Tu clave de OpenWeatherMap |
| `GEMINI_API_KEY` | Tu clave de Google Gemini |

Los nombres deben escribirse exactamente así (respetando mayúsculas y el guion bajo), porque es como los busca el código en `config.py`.

---

## 5. Ejecución de la aplicación

Una vez instaladas las librerías y configurado el `.env`, ejecutá:

```
python main.py
```

La interfaz se abre directamente en la terminal.


## 6. Flujo de uso — menú a menú

### Pantalla inicial: Login / Registro

Al abrir la app aparece la pantalla de autenticación con dos pestañas:

- **Iniciar Sesión** → ingresá tu usuario y contraseña y presioná Enter o el botón
- **Registrarse** → elegí un nombre de usuario y una contraseña que cumpla las 5 reglas de seguridad que se muestran en pantalla en tiempo real:
  - Mínimo 8 caracteres
  - Al menos 1 mayúscula
  - Al menos 1 minúscula
  - Al menos 1 número
  - Al menos 1 símbolo especial (`!@#$%^&*`)


### Panel principal: 6 opciones en el menú lateral

Una vez logueado, aparece el panel con la barra de navegación a la izquierda. Podés hacer clic en los botones o presionar las teclas **1 a 6** para navegar.

---

#### Opción 1 — Consultar Clima

1. Escribí el nombre de una ciudad en el campo de búsqueda
2. Aparecerán sugerencias de autocompletado mientras escribís
3. Seleccioná la ciudad de la lista o presioná Enter para buscar directamente
4. Se muestra:
   - Temperatura actual y sensación térmica
   - Descripción del estado del cielo
   - Humedad y velocidad del viento
5. La consulta queda guardada automáticamente en tu historial

---

#### Opción 2 — Mi Historial

- Muestra una tabla con todas tus búsquedas anteriores (fecha, ciudad, temperatura, condición, humedad, viento)
- Podés escribir una ciudad en el filtro y presionar el botón de buscar para ver solo las consultas de esa ciudad
- Se actualiza automáticamente cada vez que entrás a esta sección

---

#### Opción 3 — Estadísticas

Muestra un análisis global de todas las consultas realizadas por todos los usuarios:

- Ciudad más consultada
- Total de consultas registradas
- Temperatura promedio global
- Gráfico de barras con consultas por ciudad
- Distribución de condiciones climáticas (soleado, nublado, lluvia, etc.)

---

#### Opción 4 — Consejo IA

Permite obtener un consejo de vestimenta generado por Google Gemini. Tiene **tres modos**:

- **Última consulta** → usa el último clima que buscaste en la Opción 1
- **Del historial** → elegís cualquier entrada anterior de tu historial usando un selector desplegable
- **Nueva búsqueda** → buscás una ciudad específica ahí mismo sin salir de la pestaña

En cualquiera de los tres casos, presioná el botón **"Pedir Consejo a la IA"** y Gemini responde con una recomendación práctica.

---

#### Opción 5 — Acerca De

Información sobre la aplicación, guía de uso interna y créditos del equipo de desarrollo.

---

#### Opción 6 — Cerrar Sesión

Cierra la sesión actual y vuelve a la pantalla de login. Los datos quedan guardados.

---

## 7. Datos almacenados

La aplicación guarda dos archivos CSV en la carpeta `data/`:

| Archivo | Contenido |
|---------|-----------|
| `usuarios_simulados.csv` | Usuarios registrados (nombre y contraseña) |
| `historial_global.csv` | Registro de todas las consultas de clima de todos los usuarios |

Estos archivos se crean automáticamente la primera vez que se registra un usuario o se realiza una consulta. No hace falta crearlos manualmente.

---

## 8. Solución de problemas comunes

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| `ModuleNotFoundError` al ejecutar | Librerías no instaladas | Correr `pip install -r requirements.txt` |
| "API Key inválida" al buscar clima | Clave de OWM incorrecta o no activada | Verificar el `.env` y esperar hasta 10 min si es nueva |
| "Error al consultar la IA" | Clave de Gemini incorrecta o sin cuota | Verificar el `.env` y revisar cuota en Google AI Studio |
| Ciudad no encontrada | Nombre de ciudad en idioma incorrecto | Probar en inglés o usar el autocompletado |
| Pantalla en blanco al iniciar | Terminal muy pequeña | Agrandar la ventana de la terminal |

---

*GuardiánClima ITBA — Challenge Tecnología 2026*
