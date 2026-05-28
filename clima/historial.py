# Módulo de historial de consultas climáticas - GuardiánClima ITBA
# Gestiona el almacenamiento y recuperación del historial de consultas

import csv
import os
import sys
from datetime import datetime

# Agregar directorio raíz del proyecto al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, HISTORIAL_FILE

# Columnas del archivo CSV de historial
COLUMNAS_HISTORIAL = [
    'NombreDeUsuario',
    'Ciudad',
    'Fecha_Hora',
    'Temperatura_C',
    'Condicion_Clima',
    'Humedad_Porcentaje',
    'Viento_kmh'
]


def _asegurar_archivo_historial():
    """
    Crea el directorio data/ y el archivo CSV de historial con cabeceras
    si no existen. Esto garantiza que siempre haya un archivo válido.
    """
    try:
        # Crear directorio de datos si no existe
        os.makedirs(DATA_DIR, exist_ok=True)

        # Crear archivo CSV con cabeceras si no existe
        if not os.path.exists(HISTORIAL_FILE):
            with open(HISTORIAL_FILE, 'w', encoding='utf-8', newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(COLUMNAS_HISTORIAL)
    except Exception as e:
        print(f"Error al asegurar archivo de historial: {e}")


def guardar_consulta(username: str, datos_clima: dict) -> None:
    """
    Guarda una consulta climática en el historial global CSV.

    Args:
        username: Nombre del usuario que realizó la consulta.
        datos_clima: dict con claves: ciudad, temperatura, descripcion,
                     humedad, viento_kmh
    """
    # Asegurar que el archivo existe antes de escribir
    _asegurar_archivo_historial()

    try:
        # Generar marca de tiempo actual
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Escribir nueva fila en el archivo CSV
        with open(HISTORIAL_FILE, 'a', encoding='utf-8', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                username,
                datos_clima.get('ciudad', ''),
                fecha_hora,
                datos_clima.get('temperatura', ''),
                datos_clima.get('descripcion', ''),
                datos_clima.get('humedad', ''),
                datos_clima.get('viento_kmh', '')
            ])
    except Exception as e:
        print(f"Error al guardar consulta en el historial: {e}")


def obtener_historial_personal(username: str, ciudad: str) -> list:
    """
    Obtiene el historial de consultas de un usuario específico para una ciudad.

    Args:
        username: Nombre del usuario.
        ciudad: Nombre de la ciudad (comparación sin distinción de mayúsculas).

    Returns:
        Lista de dicts con los datos de cada consulta del usuario para esa ciudad.
    """
    # Asegurar que el archivo existe antes de leer
    _asegurar_archivo_historial()

    resultados = []

    try:
        with open(HISTORIAL_FILE, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Filtrar por usuario y ciudad (sin distinción de mayúsculas para ciudad)
                if (fila['NombreDeUsuario'].strip().lower() == username.strip().lower() and
                        fila['Ciudad'].strip().lower() == ciudad.strip().lower()):
                    resultados.append(dict(fila))
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al obtener historial personal: {e}")
        return []

    return resultados


def obtener_historial_usuario(username: str) -> list:
    """
    Obtiene todas las consultas del historial para un usuario específico,
    sin filtrar por ciudad.

    Args:
        username: Nombre del usuario.

    Returns:
        Lista de dicts con todos los registros del usuario, ordenados cronológicamente.
    """
    _asegurar_archivo_historial()

    resultados = []

    try:
        with open(HISTORIAL_FILE, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila['NombreDeUsuario'].strip().lower() == username.strip().lower():
                    resultados.append(dict(fila))
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al obtener historial de usuario: {e}")
        return []

    return resultados


def obtener_todo_historial() -> list:
    """
    Obtiene todas las filas del historial global.

    Returns:
        Lista de dicts con todos los registros del historial.
    """
    # Asegurar que el archivo existe antes de leer
    _asegurar_archivo_historial()

    resultados = []

    try:
        with open(HISTORIAL_FILE, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                resultados.append(dict(fila))
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al obtener todo el historial: {e}")
        return []

    return resultados
