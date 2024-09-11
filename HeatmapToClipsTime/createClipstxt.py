import os
from Utils.file_utils import obtener_ultima_carpeta
from Utils.video_utils import leer_duracion_video

def escribir_clips_a_archivo(ruta_carpeta, clips):
    ruta_archivo_clips = os.path.join(ruta_carpeta, "Clips.txt")
    
    with open(ruta_archivo_clips, 'w') as archivo_clips:
        archivo_clips.write(f"Se encontraron {len(clips)} picos en el mapa de calor:\n")
        for clip in clips:
            archivo_clips.write(f"{clip}\n")
    
    print(f"\nSe ha creado el archivo Clips.txt en: {ruta_archivo_clips}")

# Aquí puedes incluir las funciones obtener_ultima_carpeta y leer_duracion_video
# si no están disponibles en Utils.file_utils y Utils.video_utils respectivamente
