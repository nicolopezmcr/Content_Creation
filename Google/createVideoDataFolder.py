from getVideoInfoScripts import obtener_titulo_video, obtener_fecha_subida
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re

def obtener_titulo_y_crear_carpeta(driver):
    try:
        titulo_limpio = obtener_titulo_video(driver)
        if not titulo_limpio:
            return None

        # Esperar y hacer clic en el botón "...más"
        try:
            boton_mas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-paper-button#expand"))
            )
            boton_mas.click()
        except Exception as e:
            print(f"Error al hacer clic en el botón '...más': {str(e)}")

        fecha_subida = obtener_fecha_subida(driver)
        

        # Crear el nombre de la carpeta incluyendo la fecha
        nombre_carpeta = f"{titulo_limpio}-{fecha_subida}" if fecha_subida else titulo_limpio

        # Crear la ruta completa de la carpeta
        ruta_carpeta = os.path.join(os.getcwd(), "VideoData", nombre_carpeta)

        # Crear la carpeta si no existe
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
        else:
            print(f"La carpeta ya existe: {ruta_carpeta}")

        return ruta_carpeta
    except Exception as e:
        print(f"Error al obtener el título y crear la carpeta: {str(e)}")
        return None
