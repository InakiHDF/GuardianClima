# Módulo de consulta a la API de OpenWeatherMap - GuardiánClima ITBA
# Obtiene datos meteorológicos en tiempo real

import requests
import sys
import os

# Agregar directorio raíz del proyecto al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OWM_API_KEY

# URL base de la API de OpenWeatherMap
OWM_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def obtener_clima(ciudad: str) -> dict:
    """
    Consulta el clima actual de una ciudad via OpenWeatherMap API.

    Args:
        ciudad: Nombre de la ciudad a consultar.

    Returns:
        dict con claves:
        - 'ciudad': str (nombre de la ciudad desde la respuesta de la API)
        - 'temperatura': float (temperatura en Celsius)
        - 'sensacion_termica': float (sensación térmica en Celsius)
        - 'humedad': int (porcentaje de humedad)
        - 'descripcion': str (descripción del clima en español)
        - 'viento_kmh': float (velocidad del viento en km/h)
        - 'icono': str (código del ícono del clima)

    Raises:
        Exception: Con mensaje descriptivo en español ante cualquier error.
    """
    # Verificar que la API Key esté configurada
    if not OWM_API_KEY:
        raise Exception("No se configuró la API Key de OpenWeatherMap. Revisá el archivo .env")

    # Parámetros de la consulta a la API
    parametros = {
        'q': ciudad,
        'appid': OWM_API_KEY,
        'units': 'metric',  # Unidades métricas (Celsius)
        'lang': 'es'        # Respuestas en español
    }

    try:
        # Realizar la consulta con timeout de 10 segundos
        respuesta = requests.get(OWM_BASE_URL, params=parametros, timeout=10)

        # Manejar errores HTTP específicos
        if respuesta.status_code == 401:
            raise Exception("API Key de OpenWeatherMap inválida o aún no activada")
        elif respuesta.status_code == 404:
            raise Exception(f"Ciudad '{ciudad}' no encontrada")
        elif respuesta.status_code != 200:
            raise Exception(f"Error en la API de OpenWeatherMap (código {respuesta.status_code})")

        # Parsear la respuesta JSON
        datos = respuesta.json()

        # Extraer y estructurar los datos del clima
        descripcion_raw = datos['weather'][0]['description']
        # Corregir "nuboso" → "nublado" (OWM en español usa "nuboso" en lugar de "nublado")
        descripcion = descripcion_raw.replace('nuboso', 'nublado').replace('Nuboso', 'Nublado')
        # Capitalizar primera letra
        descripcion = descripcion.capitalize()

        clima = {
            'ciudad': datos.get('name', ciudad),
            'temperatura': datos['main']['temp'],
            'sensacion_termica': datos['main']['feels_like'],
            'humedad': datos['main']['humidity'],
            'descripcion': descripcion,
            'viento_kmh': round(datos['wind']['speed'] * 3.6, 2),  # Convertir m/s a km/h
            'icono': datos['weather'][0]['icon']
        }

        return clima

    except requests.exceptions.ConnectionError:
        # Error de conexión a internet
        raise Exception("Sin conexión a internet")
    except requests.exceptions.Timeout:
        # Timeout en la consulta
        raise Exception("La consulta a OpenWeatherMap tardó demasiado. Intentá de nuevo.")
    except requests.exceptions.RequestException as e:
        # Otros errores de requests
        raise Exception(f"Error de conexión con OpenWeatherMap: {str(e)}")
    except KeyError as e:
        # Error al parsear la respuesta (datos inesperados)
        raise Exception(f"Error al procesar la respuesta del clima: dato faltante {str(e)}")
    except Exception as e:
        # Re-lanzar excepciones ya manejadas
        if "Ciudad" in str(e) or "API Key" in str(e) or "Sin conexión" in str(e) or "tardó demasiado" in str(e) or "Error" in str(e):
            raise
        raise Exception(f"Error inesperado al obtener el clima: {str(e)}")


def buscar_ciudades(query: str) -> list:
    """
    Busca ciudades por nombre usando la API de geocodificación de OWM.

    Returns:
        Lista de dicts con claves 'display' (texto para mostrar) y 'name' (nombre para consultar clima).
    """
    if not OWM_API_KEY:
        return []

    try:
        respuesta = requests.get(
            "http://api.openweathermap.org/geo/1.0/direct",
            params={'q': query, 'limit': 5, 'appid': OWM_API_KEY},
            timeout=5,
        )
        if respuesta.status_code != 200:
            return []

        resultados = []
        for item in respuesta.json():
            name = item.get('name', '')
            country = item.get('country', '')
            state = item.get('state', '')
            if not name:
                continue
            display = f"{name}, {state}, {country}" if state else f"{name}, {country}"
            resultados.append({'display': display, 'name': name})
        return resultados

    except Exception:
        return []
