import json
from datetime import datetime, timedelta
import os

ARCHIVO_CALENDARIO = 'calendario_publicaciones.json'
INTERVALO_PUBLICACION = timedelta(hours=1)

def cargar_calendario():
    if not os.path.exists(ARCHIVO_CALENDARIO):
        return {}
    
    with open(ARCHIVO_CALENDARIO, 'r') as f:
        return json.load(f)

def guardar_calendario(calendario):
    with open(ARCHIVO_CALENDARIO, 'w') as f:
        json.dump(calendario, f, indent=2)

def obtener_proxima_fecha_disponible(calendario):
    fechas_programadas = [datetime.fromisoformat(fecha) for fecha in calendario.values()]
    if not fechas_programadas:
        fecha_base = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
        if fecha_base <= datetime.now():
            fecha_base += timedelta(days=1)
        return fecha_base

    ultima_fecha = max(fechas_programadas)
    proxima_fecha = ultima_fecha + timedelta(hours=4)
    
    while True:
        if proxima_fecha.hour not in [13, 19, 23]:
            proxima_fecha = proxima_fecha.replace(hour=13)
        
        fecha_str = proxima_fecha.isoformat()
        if fecha_str not in calendario.values():
            return proxima_fecha
        
        if proxima_fecha.hour == 13:
            proxima_fecha = proxima_fecha.replace(hour=19)
        elif proxima_fecha.hour == 19:
            proxima_fecha = proxima_fecha.replace(hour=23)
        else:  # Si es 23:00, avanzar al siguiente día
            proxima_fecha = (proxima_fecha + timedelta(days=1)).replace(hour=13)

def actualizar_calendario_y_clips():
    calendario = cargar_calendario()
    clips_json = cargar_clips_json()
    
    if clips_json is None:
        print("No se pudo cargar el archivo clips.json. Abortando la actualización.")
        return None

    if isinstance(clips_json, dict):
        clips_lista = clips_json.items()
    else:
        print(f"Error: clips_json no es un diccionario. Tipo: {type(clips_json)}")
        return None

    for clip_key, clip in clips_lista:
        if isinstance(clip, dict):
            if 'fecha_programacion' not in clip:
                fecha_publicacion = obtener_proxima_fecha_disponible(calendario)
                clip['fecha_programacion'] = fecha_publicacion.isoformat()
                
                titulo = clip.get('titulo', 'Sin título')
                calendario_key = f"clip_{fecha_publicacion.strftime('%Y%m%d_%H%M')}_{titulo[:20]}"
                calendario[calendario_key] = fecha_publicacion.isoformat()
            
            # No sobrescribir ruta_video si ya existe
            if 'ruta_video' not in clip:
                print(f"Advertencia: 'ruta_video' no encontrada para el clip: {clip_key}")
        else:
            print(f"Advertencia: Se encontró un clip que no es un diccionario. Tipo: {type(clip)}")

    guardar_calendario(calendario)
    guardar_clips_json(clips_json)
    
    print("Calendario y clips actualizados con fechas de programación.")
    return clips_json

def cargar_clips_json():
    ruta_clips_json = obtener_ruta_clips_json()
    try:
        with open(ruta_clips_json, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: El archivo {ruta_clips_json} no es un JSON válido.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_clips_json}.")
    except Exception as e:
        print(f"Error inesperado al cargar {ruta_clips_json}: {str(e)}")
    return None

def guardar_clips_json(clips_data):
    ruta_clips_json = obtener_ruta_clips_json()
    with open(ruta_clips_json, 'w') as f:
        json.dump(clips_data, f, indent=2)

def obtener_ruta_clips_json():
    ruta_base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'VideoData')
    carpetas = [f for f in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, f))]
    carpeta_reciente = max(carpetas, key=lambda x: os.path.getctime(os.path.join(ruta_base, x)))
    return os.path.join(ruta_base, carpeta_reciente, 'clips.json')

if __name__ == "__main__":
    clips_actualizados = actualizar_calendario_y_clips()
    if clips_actualizados:
        print("Clips actualizados:")
        print(json.dumps(clips_actualizados, indent=2))
    else:
        print("No se pudieron actualizar los clips.")
