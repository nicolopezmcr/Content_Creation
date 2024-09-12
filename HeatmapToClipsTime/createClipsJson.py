import os
import json
import re
from Utils.file_utils import obtener_ultima_carpeta
from Utils.video_utils import leer_duracion_video

def escribir_clips_a_archivo(ruta_carpeta, clips):
    ruta_archivo_clips = os.path.join(ruta_carpeta, "clips.json")
    
    # Función para extraer inicio y fin de cada clip
    def extraer_tiempos(clip_str):
        match = re.search(r"Inicio = (\d+:\d+), Fin = (\d+:\d+)", clip_str)
        if match:
            return {"inicio": match.group(1), "fin": match.group(2)}
        return None

    datos_clips = {
        f"clip{i + 1}": extraer_tiempos(clip)
        for i, clip in enumerate(clips)
        if extraer_tiempos(clip)
    }
    
    with open(ruta_archivo_clips, 'w', encoding='utf-8') as archivo_clips:
        json.dump(datos_clips, archivo_clips, ensure_ascii=False, indent=4)
    
    print(f"\nSe ha creado el archivo clips.json en: {ruta_archivo_clips}")

# Aquí puedes incluir las funciones obtener_ultima_carpeta y leer_duracion_video
# si no están disponibles en Utils.file_utils y Utils.video_utils respectivamente
