import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from Utils.file_utils import obtener_ultimo_archivo
import concurrent.futures
import time
import random
from google.api_core import exceptions

# Cargar variables de entorno
load_dotenv()

# Configurar la API de Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generar_pregunta(ruta_base):
    # Obtener la ruta del archivo datos_video.json
    archivo_datos_video = obtener_ultimo_archivo(ruta_base, 'datos_video.json')
    
    if not archivo_datos_video:
        print("No se encontró el archivo datos_video.json")
        return None

    # Leer el contenido del archivo
    with open(archivo_datos_video, 'r', encoding='utf-8') as f:
        datos_video = json.load(f)

    # Preparar el prompt para Gemini
    prompt = f"""
    Basándote en la siguiente información de un video de YouTube:
    
    Título: {datos_video.get('titulo', '')}
    Descripción: {datos_video.get('descripcion', '')}
    
    Genera una pregunta corta y específica relacionada con el contenido del video. La pregunta debe ser variada y puede ser del estilo:
    - ¿Estuviste en directo viéndolo?
    - ¿Te gusta este artista?
    - ¿Qué opinas de esta mezcla?
    - ¿Cuál es tu parte favorita del video?
    - ¿Has experimentado algo similar?
    - ¿Qué otros artistas te gustaría ver en colaboración?

    Proporciona solo la pregunta, sin ningún texto adicional.
    """

    # Imprimir el prompt que se enviará a Gemini
    print("Prompt enviado a Gemini:")
    print(prompt)

    # Generar pregunta con Gemini
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Procesar la respuesta
    if response.text:
        return response.text.strip()
    else:
        return None

def generar_pregunta_con_reintento(ruta_base, max_intentos=5, espera_inicial=2, factor_espera=2):
    for intento in range(max_intentos):
        try:
            tiempo_espera = espera_inicial * (factor_espera ** intento) + random.uniform(0, 1)
            print(f"Esperando {tiempo_espera:.2f} segundos antes de intentar (intento {intento + 1}/{max_intentos})...")
            time.sleep(tiempo_espera)
            
            pregunta = generar_pregunta(ruta_base)
            if pregunta:
                return pregunta
            else:
                print("No se pudo generar una pregunta. Reintentando...")
        except exceptions.ResourceExhausted:
            print(f"Cuota agotada en el intento {intento + 1}. Reintentando...")
        except Exception as e:
            print(f"Error inesperado en el intento {intento + 1}: {str(e)}. Reintentando...")
    
    print("Se agotaron todos los intentos. No se pudo generar la pregunta.")
    return None

def generar_preguntas_para_clips(ruta_base):
    # Obtener la ruta del archivo clips.json
    archivo_clips = obtener_ultimo_archivo(ruta_base, 'clips.json')
    
    if not archivo_clips:
        print("No se encontró el archivo clips.json")
        return None

    # Leer el contenido del archivo clips.json
    with open(archivo_clips, 'r', encoding='utf-8') as f:
        clips = json.load(f)

    # Crear un pool de workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Crear un diccionario para almacenar los futuros
        future_to_clip = {executor.submit(generar_pregunta_con_reintento, ruta_base): clip_key for clip_key in clips}
        
        # Procesar los resultados a medida que se completan
        for future in concurrent.futures.as_completed(future_to_clip):
            clip_key = future_to_clip[future]
            try:
                pregunta = future.result()
                if pregunta:
                    clips[clip_key]['pregunta'] = pregunta
                else:
                    print(f"No se pudo generar una pregunta para el clip {clip_key}")
            except Exception as exc:
                print(f"El clip {clip_key} generó una excepción: {exc}")

    # Guardar los cambios en clips.json
    with open(archivo_clips, 'w', encoding='utf-8') as f:
        json.dump(clips, f, ensure_ascii=False, indent=2)

    return clips

# Ejemplo de uso
if __name__ == "__main__":
    ruta_base = "/Users/nicolopez/Cursor/Content_Creation/VideoData"
    clips_actualizados = generar_preguntas_para_clips(ruta_base)
    if clips_actualizados:
        print(json.dumps(clips_actualizados, indent=2, ensure_ascii=False))
    else:
        print("No se pudieron generar las preguntas para los clips")
