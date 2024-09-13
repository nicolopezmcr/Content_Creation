import sys
import os
import json
# Añadir el directorio padre al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.file_utils import obtener_ultima_carpeta, obtener_ultimo_archivo

def obtener_info_clips():
    ruta_base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'VideoData')
    print(f"Ruta base: {ruta_base}")
    
    try:
        # Obtenemos la última carpeta
        carpeta_reciente = obtener_ultima_carpeta(ruta_base)
        print(f"Carpeta más reciente: {carpeta_reciente}")
        if not carpeta_reciente:
            print("No se encontró ninguna carpeta en el directorio base.")
            return []

        # Obtenemos la ruta al archivo clips.json más reciente
        ruta_json = obtener_ultimo_archivo(carpeta_reciente, 'clips.json')
        print(f"Ruta del archivo clips.json: {ruta_json}")
        if not ruta_json:
            print("No se encontró el archivo clips.json.")
            return []

        # Leemos la información del JSON
        with open(ruta_json, 'r', encoding='utf-8') as f:
            clips_data = json.load(f)

        # Procesamos la información de los clips y añadimos la ruta_video
        for clip_key, clip in clips_data.items():
            nombre_archivo = f"{clip_key.replace('clip', 'clip_')}.mp4"
            clip['ruta_video'] = os.path.join(carpeta_reciente, 'clips_raw', nombre_archivo)

        # Sobrescribimos el archivo JSON con la nueva información
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(clips_data, f, ensure_ascii=False, indent=2)

        print("Archivo JSON actualizado con las rutas de video.")

        # Creamos la lista de clips_info para devolver
        clips_info = []
        for clip in clips_data.values():
            clips_info.append({
                'titulo': clip.get('titulo', ''),
                'descripcion': clip.get('descripcion', ''),
                'pregunta': clip.get('pregunta', ''),
                'canal': clip.get('canal', ''),
                'tags': clip.get('tags', []),
                'ruta_video': clip.get('ruta_video', '')
            })

        return clips_info

    except Exception as e:
        print(f"Error al obtener la información de los clips: {str(e)}")
        return []

if __name__ == "__main__":
    clips = obtener_info_clips()
    print(json.dumps(clips, indent=2, ensure_ascii=False))
