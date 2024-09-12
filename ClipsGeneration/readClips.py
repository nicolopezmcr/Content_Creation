import os
import json

def obtener_archivo_clips(ultima_carpeta):
    archivo_clips = os.path.join(ultima_carpeta, 'clips.json')
    if os.path.exists(archivo_clips):
        return archivo_clips
    else:
        raise FileNotFoundError(f"No se encontró el archivo clips.json en {ultima_carpeta}")

def leer_tiempos_clips(ruta_archivo):
    clips = []
    with open(ruta_archivo, 'r') as f:
        clips_data = json.load(f)
    
    for clip_info in clips_data.values():
        inicio = convertir_a_segundos(clip_info['inicio'])
        fin = convertir_a_segundos(clip_info['fin'])
        clips.append((inicio, fin))
    return clips

def convertir_a_segundos(tiempo):
    minutos, segundos = map(int, tiempo.split(':'))
    return minutos * 60 + segundos
