# Módulo de validación de contraseñas - GuardiánClima ITBA
# Implementa validación con 5 criterios de seguridad

import re


def validar_contrasena(password: str) -> dict:
    """
    Valida una contraseña según criterios de seguridad.

    Args:
        password: La contraseña a validar.

    Returns:
        dict con claves:
        - 'es_valida': bool (True si TODOS los criterios se cumplen)
        - 'criterios': lista de dicts, cada uno con:
            - 'nombre': str (nombre de la regla)
            - 'cumple': bool (si la regla se cumple)
            - 'mensaje_error': str (mensaje de error si no se cumple)
            - 'sugerencia': str (sugerencia para corregir)
    """
    # Definir los 5 criterios de seguridad
    criterios = []

    # Criterio 1: Mínimo 8 caracteres
    cumple_longitud = len(password) >= 8
    criterios.append({
        'nombre': 'Longitud mínima',
        'cumple': cumple_longitud,
        'mensaje_error': 'La contraseña debe tener al menos 8 caracteres.' if not cumple_longitud else '',
        'sugerencia': 'Agregá más caracteres hasta llegar a 8 como mínimo.' if not cumple_longitud else ''
    })

    # Criterio 2: Al menos 1 letra mayúscula
    cumple_mayuscula = bool(re.search(r'[A-Z]', password))
    criterios.append({
        'nombre': 'Letra mayúscula',
        'cumple': cumple_mayuscula,
        'mensaje_error': 'La contraseña debe contener al menos una letra mayúscula.' if not cumple_mayuscula else '',
        'sugerencia': 'Incluí al menos una letra en mayúscula (A-Z).' if not cumple_mayuscula else ''
    })

    # Criterio 3: Al menos 1 letra minúscula
    cumple_minuscula = bool(re.search(r'[a-z]', password))
    criterios.append({
        'nombre': 'Letra minúscula',
        'cumple': cumple_minuscula,
        'mensaje_error': 'La contraseña debe contener al menos una letra minúscula.' if not cumple_minuscula else '',
        'sugerencia': 'Incluí al menos una letra en minúscula (a-z).' if not cumple_minuscula else ''
    })

    # Criterio 4: Al menos 1 dígito numérico
    cumple_digito = bool(re.search(r'[0-9]', password))
    criterios.append({
        'nombre': 'Dígito numérico',
        'cumple': cumple_digito,
        'mensaje_error': 'La contraseña debe contener al menos un número.' if not cumple_digito else '',
        'sugerencia': 'Incluí al menos un dígito (0-9).' if not cumple_digito else ''
    })

    # Criterio 5: Al menos 1 carácter especial
    caracteres_especiales = r'[!@#$%^&*()_+\-=]'
    cumple_especial = bool(re.search(caracteres_especiales, password))
    criterios.append({
        'nombre': 'Carácter especial',
        'cumple': cumple_especial,
        'mensaje_error': 'La contraseña debe contener al menos un carácter especial.' if not cumple_especial else '',
        'sugerencia': 'Incluí al menos uno de estos caracteres: !@#$%^&*()_+-=' if not cumple_especial else ''
    })

    # La contraseña es válida solo si todos los criterios se cumplen
    es_valida = all(criterio['cumple'] for criterio in criterios)

    return {
        'es_valida': es_valida,
        'criterios': criterios
    }


def obtener_mensaje_rechazo(resultado: dict) -> str:
    """
    Genera un mensaje completo de rechazo con sugerencias
    basado en el resultado de la validación.

    Args:
        resultado: dict devuelto por validar_contrasena()

    Returns:
        str con el mensaje de rechazo formateado
    """
    # Si la contraseña es válida, no hay mensaje de rechazo
    if resultado.get('es_valida', False):
        return "La contraseña cumple con todos los criterios de seguridad."

    # Construir mensaje con los criterios que no se cumplen
    lineas = ["❌ La contraseña no cumple con los siguientes criterios:\n"]

    for criterio in resultado.get('criterios', []):
        if not criterio['cumple']:
            lineas.append(f"  • {criterio['mensaje_error']}")
            lineas.append(f"    💡 Sugerencia: {criterio['sugerencia']}")

    lineas.append("\n🔐 Corregí los puntos anteriores e intentá nuevamente.")

    return '\n'.join(lineas)
