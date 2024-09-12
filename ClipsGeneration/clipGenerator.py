import os
import re
import sys
# Añadir el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from videoDownload import descargar_video_completo
from clipCreation import generar_clips
from readClips import obtener_archivo_clips, leer_tiempos_clips
from Utils.file_utils import obtener_ultima_carpeta
from createClipsFolder import crear_carpeta_clips_raw

def extract_number(filename):
    return int(re.search(r'clip_(\d+)', filename).group(1))

def main(callback=None):
    ruta_base = "/Users/nicolopez/Cursor/Content_Creation/VideoData"
    mensajes = []
    try:
        ultima_carpeta = obtener_ultima_carpeta(ruta_base)
        carpeta_clips_raw = crear_carpeta_clips_raw(ultima_carpeta)
        
        ruta_clips = obtener_archivo_clips(ultima_carpeta)
        ruta_url = os.path.join(ultima_carpeta, 'url_video.txt')
        
        if not os.path.exists(ruta_url):
            mensaje = f"Error: No se encontró el archivo url_video.txt en {ultima_carpeta}"
            mensajes.append(mensaje)
            if callback:
                callback(mensaje)
            return False, mensajes

        with open(ruta_url, 'r') as f:
            url = f.read().strip()

        if not url:
            mensaje = "Error: El archivo url_video.txt está vacío"
            mensajes.append(mensaje)
            print(mensaje)
            if callback:
                callback(mensaje)
            return False, mensajes
        
        clips = leer_tiempos_clips(ruta_clips)
        
        # Forzar la descarga del video completo
        video_completo = descargar_video_completo(url, carpeta_clips_raw, callback)
        if not video_completo:
            mensaje = "Error: No se pudo descargar el video completo"
            mensajes.append(mensaje)
            if callback:
                callback(mensaje)
            return False, mensajes
        
        clips_generados = generar_clips(video_completo, clips, carpeta_clips_raw, callback)
        
        mensaje_final = "Proceso de generación de clips completado."
        mensajes.append(mensaje_final)
        if callback:
            callback(mensaje_final)
        return clips_generados, mensajes
    except FileNotFoundError as e:
        mensaje = f"Error: {e}"
        mensajes.append(mensaje)
        if callback:
            callback(mensaje)
    except Exception as e:
        mensaje = f"Error inesperado: {str(e)}"
        mensajes.append(mensaje)
        if callback:
            callback(mensaje)
    return False, mensajes

if __name__ == "__main__":
    success, messages = main()
    for message in messages:
        print(message)



