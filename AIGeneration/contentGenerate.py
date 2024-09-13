import os
import sys
import json

# Añadir el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.file_utils import obtener_ultima_carpeta, obtener_ultimo_archivo
from generateTitleAndDescription import generar_contenido_limpio
from generateTags import generar_tags_con_gemini
from generateQuestion import generar_pregunta_con_reintento

def generar_y_guardar_contenido():
    ruta_base = "/Users/nicolopez/Cursor/Content_Creation/VideoData"
    ultima_carpeta = obtener_ultima_carpeta(ruta_base)
    
    if not ultima_carpeta:
        print("No se encontró ninguna carpeta de video.")
        return
    
    print(f"Carpeta de trabajo: {ultima_carpeta}")
    
    # Generar contenido limpio
    contenido_limpio = generar_contenido_limpio(ultima_carpeta)
    
    if not contenido_limpio:
        print("No se pudo generar el contenido limpio.")
        return
    
    print("Contenido limpio generado:")
    print(json.dumps(contenido_limpio, indent=2, ensure_ascii=False))
    
    titulo = contenido_limpio['titulo'].strip('* ')
    descripcion = contenido_limpio['descripcion'].strip('* ')
    canal = contenido_limpio['canal'].strip('* ')

    # Generar tags
    tags = generar_tags_con_gemini(ultima_carpeta)
    
    if not tags:
        print("No se pudieron generar los tags.")
        return
    
    print("Tags generados:")
    print(tags)
    
    # Obtener y actualizar clips.json
    archivo_clips = obtener_ultimo_archivo(ultima_carpeta, 'clips.json')
    if not archivo_clips:
        print("No se encontró el archivo clips.json")
        return
    
    print(f"Archivo clips.json: {archivo_clips}")
    
    with open(archivo_clips, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    # Actualizar cada clip con la nueva información
    for clip_key in clips:
        clips[clip_key]['titulo'] = titulo
        clips[clip_key]['descripcion'] = descripcion
        clips[clip_key]['canal'] = canal
        clips[clip_key]['tags'] = tags
        
        # Generar una pregunta única para cada clip
        pregunta = generar_pregunta_con_reintento(ultima_carpeta)
        if pregunta:
            clips[clip_key]['pregunta'] = pregunta
        else:
            print(f"No se pudo generar una pregunta para el clip {clip_key}")
    
    # Guardar los cambios en clips.json
    with open(archivo_clips, 'w', encoding='utf-8') as f:
        json.dump(clips, f, ensure_ascii=False, indent=2)
    
    print("Contenido actualizado:")
    print(json.dumps(clips, ensure_ascii=False, indent=2))
    
    print("Contenido generado y guardado exitosamente en clips.json")

if __name__ == "__main__":
    generar_y_guardar_contenido()
