# Módulo de gestión de usuarios - GuardiánClima ITBA
# Maneja registro, autenticación y verificación de usuarios

import csv
import os
import sys

# Agregar directorio raíz del proyecto al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, USERS_FILE


def _asegurar_archivo_usuarios():
    """
    Crea el directorio data/ y el archivo CSV de usuarios si no existen.
    El archivo se crea con la cabecera: username,password_simulada
    """
    try:
        # Crear directorio de datos si no existe
        os.makedirs(DATA_DIR, exist_ok=True)

        # Crear archivo CSV con cabeceras si no existe
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'w', encoding='utf-8', newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['username', 'password_simulada'])
    except Exception as e:
        print(f"Error al asegurar archivo de usuarios: {e}")


def usuario_existe(username: str) -> bool:
    """
    Verifica si un nombre de usuario ya existe en el CSV.

    Args:
        username: Nombre de usuario a verificar.

    Returns:
        True si el usuario existe, False en caso contrario.
    """
    # Asegurar que el archivo existe antes de leer
    _asegurar_archivo_usuarios()

    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Comparación sin distinción de mayúsculas/minúsculas
                if fila['username'].strip().lower() == username.strip().lower():
                    return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error al verificar usuario: {e}")
        return False

    return False


def autenticar(username: str, password: str) -> bool:
    """
    Verifica credenciales contra el archivo CSV.

    Args:
        username: Nombre de usuario.
        password: Contraseña en texto plano (simulación educativa).

    Returns:
        True si las credenciales coinciden, False en caso contrario.
    """
    # Asegurar que el archivo existe antes de leer
    _asegurar_archivo_usuarios()

    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Verificar que usuario y contraseña coincidan
                if (fila['username'].strip().lower() == username.strip().lower() and
                        fila['password_simulada'].strip() == password):
                    return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
        return False

    return False


def registrar_usuario(username: str, password: str) -> None:
    """
    Registra un nuevo usuario en el archivo CSV.
    Almacena la contraseña en texto plano (simulación educativa).

    Args:
        username: Nombre de usuario a registrar.
        password: Contraseña en texto plano.
    """
    # Asegurar que el archivo existe antes de escribir
    _asegurar_archivo_usuarios()

    try:
        # Agregar nueva fila con el usuario y contraseña
        with open(USERS_FILE, 'a', encoding='utf-8', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([username, password])
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
