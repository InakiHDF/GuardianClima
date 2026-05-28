import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# API Keys - se cargan desde variables de entorno por seguridad
OWM_API_KEY = os.getenv("OWM_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorio de datos
DATA_DIR = os.path.join(BASE_DIR, "data")

# Archivos de datos
USERS_FILE = os.path.join(DATA_DIR, "usuarios_simulados.csv")
HISTORIAL_FILE = os.path.join(DATA_DIR, "historial_global.csv")
