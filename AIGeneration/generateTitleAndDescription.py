import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from Utils.file_utils import obtener_ultimo_archivo

# Cargar variables de entorno
load_dotenv()

# Configurar la API de Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generar_contenido_limpio(ruta_base):
    # Obtener la ruta del archivo datos_video.json
    archivo_datos_video = obtener_ultimo_archivo(ruta_base, 'datos_video.json')
    
    if not archivo_datos_video:
        print("No se encontró el archivo datos_video.json")
        return None

    # Leer el contenido del archivo
    with open(archivo_datos_video, 'r', encoding='utf-8') as f:
        datos_video = json.load(f)

    # Modificar el prompt para Gemini
    prompt = f"""
    Basándote en la siguiente información de un video de YouTube:
    
    Título original: {datos_video.get('titulo', '')}
    Descripción original: {datos_video.get('descripcion', '')}
    Nombre del canal original: {datos_video.get('nombre_canal', '')}
    
    Por favor, realiza las siguientes tareas:
    1. Genera un título mejorado que sea atractivo y optimizado para SEO, manteniendo la esencia del original.
    2. Crea una descripción breve y atractiva, manteniendo la información clave.
    3. Para el nombre del canal, simplemente elimina cualquier carácter extraño o espacio innecesario, sin cambiar su contenido.

    Proporciona la información en el siguiente formato:
    Título: [Título mejorado]
    Descripción: [Descripción breve y atractiva]
    Canal: [Nombre del canal limpio]
    """

    # Generar contenido limpio con Gemini
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Procesar la respuesta
    if response.text:
        print("Respuesta de la IA:", response.text)
        
        try:
            # Intenta extraer la información
            titulo_match = re.search(r'Título:\s*(.*)', response.text, re.IGNORECASE)
            descripcion_match = re.search(r'Descripción:\s*(.*)', response.text, re.IGNORECASE)
            canal_match = re.search(r'Canal:\s*(.*)', response.text, re.IGNORECASE)

            if titulo_match and descripcion_match and canal_match:
                return {
                    'titulo': titulo_match.group(1).strip(),
                    'descripcion': descripcion_match.group(1).strip(),
                    'canal': canal_match.group(1).strip()
                }
            else:
                raise ValueError("No se pudo extraer toda la información necesaria")
        except Exception as e:
            print(f"Error al procesar la respuesta de la IA: {str(e)}")
            return None
    else:
        return None

# Ejemplo de uso
if __name__ == "__main__":
    ruta_base = "/Users/nicolopez/Cursor/Content_Creation/VideoData"
    resultado = generar_contenido_limpio(ruta_base)
    if resultado:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print("No se pudo generar el contenido limpio")
