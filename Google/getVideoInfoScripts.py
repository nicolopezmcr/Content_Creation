from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import glob
import re
import json

def obtener_titulo_video(driver):
    try:
        # Esperar a que el título sea visible
        titulo_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ytd-watch-metadata yt-formatted-string"))
        )
        
        titulo = titulo_elemento.text
        # Limpiar el título para usarlo como nombre de carpeta
        titulo_limpio = re.sub(r'[^\w\-_\. ]', '_', titulo)
        return titulo_limpio
    except Exception as e:
        print(f"Error al obtener el título del video: {str(e)}")
        return None

def obtener_fecha_subida(driver):
    try:
        # Lista de meses en español
        meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

        # Construir la expresión XPath para buscar el span específico
        fecha_xpath = "//span[@dir='auto' and @class='style-scope yt-formatted-string bold' and @style-target='bold']"

        # Buscar todos los elementos que coincidan con el XPath
        elementos_fecha = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, fecha_xpath))
        )

        for elemento in elementos_fecha:
            texto = elemento.text
            for mes in meses:
                if mes in texto:
                    return texto
        
        print("No se encontró la fecha de subida")
        return None
    except Exception as e:
        print(f"Error al obtener la fecha de subida: {str(e)}")
        return None

def guardar_url_video(url_video):
    # Definir la ruta base como una variable
    ruta_base = os.path.join(os.getcwd(), "VideoData")

    # Encontrar la última carpeta creada o actualizada
    ultima_carpeta = max(glob.glob(os.path.join(ruta_base, "*")), key=os.path.getmtime)

    # Guardar la URL en la última carpeta
    ruta_url = os.path.join(ultima_carpeta, "url_video.txt")
    with open(ruta_url, 'w') as f:
        f.write(url_video)

def obtener_descripcion_video(driver):
    try:
        # Esperar a que la descripción sea visible
        descripcion_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap"))
        )
        
        descripcion = descripcion_elemento.text
        return descripcion
    except Exception as e:
        print(f"Error al obtener la descripción del video: {str(e)}")
        return None

def guardar_descripcion_video(descripcion):
    # Definir la ruta base como una variable
    ruta_base = os.path.join(os.getcwd(), "VideoData")

    # Encontrar la última carpeta creada o actualizada
    ultima_carpeta = max(glob.glob(os.path.join(ruta_base, "*")), key=os.path.getmtime)

    # Guardar la descripción en la última carpeta
    ruta_descripcion = os.path.join(ultima_carpeta, "descripcion_video.txt")
    with open(ruta_descripcion, 'w', encoding='utf-8') as f:
        f.write(descripcion)

def obtener_nombre_canal(driver):
    try:
        # Esperar a que el nombre del canal sea visible
        nombre_canal_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#text-container yt-formatted-string#text"))
        )
        
        nombre_canal = nombre_canal_elemento.text
        return nombre_canal
    except Exception as e:
        print(f"Error al obtener el nombre del canal: {str(e)}")
        return None

def guardar_nombre_canal(nombre_canal):
    # Definir la ruta base como una variable
    ruta_base = os.path.join(os.getcwd(), "VideoData")

    # Encontrar la última carpeta creada o actualizada
    ultima_carpeta = max(glob.glob(os.path.join(ruta_base, "*")), key=os.path.getmtime)

    # Guardar el nombre del canal en la última carpeta
    ruta_nombre_canal = os.path.join(ultima_carpeta, "nombre_canal.txt")
    with open(ruta_nombre_canal, 'w', encoding='utf-8') as f:
        f.write(nombre_canal)

def guardar_datos_video_json(url, titulo, descripcion, nombre_canal):
    # Definir la ruta base como una variable
    ruta_base = os.path.join(os.getcwd(), "VideoData")

    # Encontrar la última carpeta creada o actualizada
    ultima_carpeta = max(glob.glob(os.path.join(ruta_base, "*")), key=os.path.getmtime)

    # Crear un diccionario con los datos del video
    datos_video = {
        'url': url,
        'titulo': titulo,
        'descripcion': descripcion,
        'nombre_canal': nombre_canal
    }

    # Guardar los datos en un archivo JSON en la última carpeta
    ruta_json = os.path.join(ultima_carpeta, "datos_video.json")
    try:
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(datos_video, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar los datos en JSON: {str(e)}")
       




# Esta función se puede llamar desde getHeatmap.py
