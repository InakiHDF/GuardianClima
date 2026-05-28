# Módulo de estadísticas globales - GuardiánClima ITBA
# Calcula estadísticas a partir del historial de consultas climáticas

import sys
import os

# Agregar directorio raíz del proyecto al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clima.historial import obtener_todo_historial


def calcular_estadisticas() -> dict:
    """
    Calcula estadísticas globales del historial de consultas climáticas.

    Returns:
        dict con claves:
        - 'total_consultas': int (cantidad total de consultas)
        - 'ciudad_mas_consultada': str (ciudad con más consultas, o 'N/A')
        - 'consultas_ciudad_max': int (cantidad de consultas de la ciudad más consultada)
        - 'temperatura_promedio': float (promedio redondeado a 1 decimal, o 0.0)
        - 'consultas_por_ciudad': dict {nombre_ciudad: cantidad}
        - 'condiciones': dict {condición_clima: cantidad}
        - 'temperaturas_por_ciudad': dict {nombre_ciudad: [temp1, temp2, ...]}
    """
    try:
        # Obtener todos los registros del historial
        historial = obtener_todo_historial()

        # Cantidad total de consultas realizadas
        total_consultas = len(historial)

        # Si no hay datos, devolver valores por defecto
        if total_consultas == 0:
            return {
                'total_consultas': 0,
                'ciudad_mas_consultada': 'N/A',
                'consultas_ciudad_max': 0,
                'temperatura_promedio': 0.0,
                'consultas_por_ciudad': {},
                'condiciones': {},
                'temperaturas_por_ciudad': {}
            }

        # Diccionarios para acumular datos
        consultas_por_ciudad = {}  # Contador de consultas por ciudad
        condiciones = {}           # Contador de condiciones climáticas
        temperaturas_por_ciudad = {}  # Temperaturas registradas por ciudad
        todas_las_temperaturas = []   # Todas las temperaturas para el promedio global

        # Iterar sobre cada registro del historial
        for registro in historial:
            ciudad = registro.get('Ciudad', '').strip()
            condicion = registro.get('Condicion_Clima', '').strip()
            temp_str = registro.get('Temperatura_C', '').strip()

            # Contar consultas por ciudad
            if ciudad:
                consultas_por_ciudad[ciudad] = consultas_por_ciudad.get(ciudad, 0) + 1

            # Contar condiciones climáticas
            if condicion:
                condiciones[condicion] = condiciones.get(condicion, 0) + 1

            # Procesar temperaturas (convertir de string a float)
            if temp_str:
                try:
                    temperatura = float(temp_str)
                    todas_las_temperaturas.append(temperatura)

                    # Acumular temperaturas por ciudad
                    if ciudad:
                        if ciudad not in temperaturas_por_ciudad:
                            temperaturas_por_ciudad[ciudad] = []
                        temperaturas_por_ciudad[ciudad].append(temperatura)
                except ValueError:
                    # Ignorar valores de temperatura que no se pueden convertir
                    pass

        # Determinar la ciudad más consultada
        if consultas_por_ciudad:
            ciudad_mas_consultada = max(consultas_por_ciudad, key=consultas_por_ciudad.get)
            consultas_ciudad_max = consultas_por_ciudad[ciudad_mas_consultada]
        else:
            ciudad_mas_consultada = 'N/A'
            consultas_ciudad_max = 0

        # Calcular temperatura promedio global
        if todas_las_temperaturas:
            temperatura_promedio = round(
                sum(todas_las_temperaturas) / len(todas_las_temperaturas), 1
            )
        else:
            temperatura_promedio = 0.0

        # Retornar diccionario con todas las estadísticas
        return {
            'total_consultas': total_consultas,
            'ciudad_mas_consultada': ciudad_mas_consultada,
            'consultas_ciudad_max': consultas_ciudad_max,
            'temperatura_promedio': temperatura_promedio,
            'consultas_por_ciudad': consultas_por_ciudad,
            'condiciones': condiciones,
            'temperaturas_por_ciudad': temperaturas_por_ciudad
        }

    except Exception as e:
        # En caso de error, devolver valores por defecto
        print(f"Error al calcular estadísticas: {e}")
        return {
            'total_consultas': 0,
            'ciudad_mas_consultada': 'N/A',
            'consultas_ciudad_max': 0,
            'temperatura_promedio': 0.0,
            'consultas_por_ciudad': {},
            'condiciones': {},
            'temperaturas_por_ciudad': {}
        }
