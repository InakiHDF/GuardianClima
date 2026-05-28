# Módulo de integración con Google Gemini - GuardiánClima ITBA
# Usa el nuevo SDK google-genai (google.generativeai está deprecado)

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GEMINI_API_KEY

# Modelos en orden de preferencia
_MODELOS_PREFERIDOS = [
    'gemini-2.5-flash',
    'gemini-2.5-pro',
    'gemini-2.0-flash', # Probablemente eliminar por obsoleto, pero lo dejo por las dudas
    'gemini-2.0-flash-lite',
    'gemini-flash-latest',
]

_modelo_cache: str = ''


def _detectar_modelo(client) -> str:
    """
    Detecta el primer modelo disponible para esta API key,
    según la lista de preferencia. Cachea el resultado.
    """
    global _modelo_cache
    if _modelo_cache:
        return _modelo_cache

    try:
        disponibles = {
            m.name.removeprefix('models/')
            for m in client.models.list()
            if hasattr(m, 'supported_generation_methods')
            and 'generateContent' in (m.supported_generation_methods or [])
        }
        for modelo in _MODELOS_PREFERIDOS:
            if modelo in disponibles:
                _modelo_cache = modelo
                return modelo
        if disponibles:
            _modelo_cache = next(iter(disponibles))
            return _modelo_cache
    except Exception:
        pass

    _modelo_cache = 'gemini-2.5-flash'
    return _modelo_cache


def obtener_consejo_vestimenta(temperatura: float, sensacion_termica: float,
                                condicion: str, humedad: int,
                                viento: float, ciudad: str) -> str:
    """
    Obtiene un consejo de vestimenta usando Google Gemini API (SDK google-genai).

    Args:
        temperatura: Temperatura actual en grados Celsius.
        sensacion_termica: Sensación térmica en grados Celsius.
        condicion: Descripción de la condición climática.
        humedad: Porcentaje de humedad.
        viento: Velocidad del viento en km/h.
        ciudad: Nombre de la ciudad consultada.

    Returns:
        str con el consejo generado por IA, o un mensaje de error.
    """
    if not GEMINI_API_KEY:
        return "Error: No se configuró la API Key de Gemini. Revisá el archivo .env"

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        modelo = _detectar_modelo(client)

        prompt = (
            f"Sos un asistente de moda y clima. Basándote en las siguientes "
            f"condiciones climáticas actuales en {ciudad}, dame un consejo breve "
            f"y práctico sobre cómo vestirme hoy.\n\n"
            f"Condiciones:\n"
            f"- Temperatura: {temperatura}°C\n"
            f"- Sensación térmica: {sensacion_termica}°C\n"
            f"- Condición: {condicion}\n"
            f"- Humedad: {humedad}%\n"
            f"- Viento: {viento} km/h\n\n"
            f"Dame un consejo conciso (máximo 3-4 oraciones) sobre qué ropa usar. "
            f"Sé específico y práctico."
        )

        respuesta = client.models.generate_content(model=modelo, contents=prompt)
        return respuesta.text

    except ImportError:
        return "Error: Instalá la librería con: pip install google-genai"
    except Exception as e:
        return f"Error al consultar Gemini: {str(e)}"
