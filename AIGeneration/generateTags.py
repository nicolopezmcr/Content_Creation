import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from Utils.file_utils import obtener_ultimo_archivo

# Cargar variables de entorno
load_dotenv()

# Configurar la API de Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generar_tags_con_gemini(ruta_base):
    # Obtener la ruta del archivo datos_video.json
    archivo_datos_video = obtener_ultimo_archivo(ruta_base, 'datos_video.json')
    
    if not archivo_datos_video:
        print("No se encontró el archivo datos_video.json")
        return None

    # Leer el contenido del archivo
    with open(archivo_datos_video, 'r', encoding='utf-8') as f:
        datos_video = json.load(f)

    # Modificar el prompt para solicitar tags sin formato de lista
    prompt = f"""
    Basándote en la siguiente información de un video de YouTube, genera 10 tags relevantes:
    
    Título: {datos_video.get('titulo', '')}
    Descripción: {datos_video.get('descripcion', '')}
    Fecha de subida: {datos_video.get('fecha_subida', '')}
    
    Por favor, proporciona los tags separados por comas, sin numeración ni viñetas.
    """

    # Generar tags con Gemini
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Procesar la respuesta
    if response.text:
        # Dividir la respuesta en tags individuales y eliminar espacios en blanco
        tags = [tag.strip() for tag in response.text.split(',')]
        return tags
    else:
        print("No se pudieron generar tags")
        return None

# Agregar esta función a las funciones existentes en file_utils.py
