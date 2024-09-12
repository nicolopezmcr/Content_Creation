import os
import sys

# Añadir el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.file_utils import obtener_ultima_carpeta
from Utils.video_utils import leer_duracion_video
from imageAnalysis import procesar_mapa_calor, calcular_tiempos_clips
from peakDetection import detectar_picos_con_inicio_fin_respecto_media
from createClipsJson import escribir_clips_a_archivo
from manageClipsJson import analizar_clips
def analizar_mapa_calor(ruta_base, nombre_archivo_mapa_calor='mapa_calor_0.png', distancia_minima=20):
    ruta_carpeta = obtener_ultima_carpeta(ruta_base)
    
    if not ruta_carpeta:
        print("No se encontró ninguna carpeta en la ruta especificada.")
        return None
    
    print(f"Analizando la carpeta: {ruta_carpeta}")
    
    ruta_mapa_calor = os.path.join(ruta_carpeta, nombre_archivo_mapa_calor)
    
    if not os.path.exists(ruta_mapa_calor):
        print(f"No se encontró el archivo {nombre_archivo_mapa_calor} en la carpeta: {ruta_carpeta}")
        print("Contenido de la carpeta:")
        for archivo in os.listdir(ruta_carpeta):
            print(f"- {archivo}")
        return None
    
    perfil_intensidad, altura_minima, ancho_imagen = procesar_mapa_calor(ruta_mapa_calor)
    
    resultados, picos = detectar_picos_con_inicio_fin_respecto_media(perfil_intensidad, altura_minima, distancia_minima)
    
    duracion_video = leer_duracion_video(ruta_carpeta)
    if not duracion_video:
        print("No se pudo obtener la duración del video.")
        return None
    
    clips = calcular_tiempos_clips(resultados, ancho_imagen, duracion_video)
    
    for clip in clips:
        print(clip)

    escribir_clips_a_archivo(ruta_carpeta, clips)
    analizar_clips(ruta_carpeta)
    
    return ruta_carpeta, ruta_mapa_calor, resultados

def main():
    ruta_base = "/Users/nicolopez/Cursor/Content_Creation/VideoData"
    analizar_mapa_calor(ruta_base)

if __name__ == "__main__":
    main()
