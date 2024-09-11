from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from getVideoInfoScripts import (
    obtener_titulo_video, obtener_fecha_subida, guardar_url_video,
    obtener_descripcion_video, guardar_descripcion_video,
    obtener_nombre_canal, guardar_nombre_canal, guardar_datos_video_json
)

def obtener_info_video(url):
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless

    # Inicializar el driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navegar a la URL del video
        driver.get(url)

        # Obtener el título del video
        titulo = obtener_titulo_video(driver)
      
        # Obtener la descripción del video
        descripcion = obtener_descripcion_video(driver)
       
        # Obtener el nombre del canal
        nombre_canal = obtener_nombre_canal(driver)
       

        # Guardar la URL del video
        guardar_url_video(url)

        # Guardar todos los datos en un archivo JSON
        guardar_datos_video_json(url, titulo, descripcion, nombre_canal)

        return titulo, descripcion, nombre_canal

    except Exception as e:
        print(f"Error al obtener la información del video: {str(e)}")
        return None, None, None, None

    finally:
        # Cerrar el navegador
        driver.quit()

# Ejemplo de uso
if __name__ == "__main__":
    url_video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Reemplaza con la URL real del video
    titulo, fecha, descripcion, canal = obtener_info_video(url_video)
    if titulo and fecha and descripcion and canal:
        print("Información obtenida con éxito y guardada en JSON")
    else:
        print("No se pudo obtener toda la información del video")
