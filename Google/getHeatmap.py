from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import sys
import glob
from startSession import iniciar_sesion_chrome
from waitAds import esperar_fin_anuncio
from getVideoLength import obtener_duracion_video
from createVideoDataFolder import obtener_titulo_y_crear_carpeta
from heatmapScreenshot import capturar_mapa_calor
from getVideoInfoScripts import guardar_url_video
from getVideoInfo import obtener_info_video

def obtener_mapa_calor(url_video, intentos=0):
    if intentos >= 5:
        return

    driver = iniciar_sesion_chrome()
    
    try:
        # Carga de la página
        driver.get(url_video)
        
        # Esperar a que termine el anuncio si lo hay
        esperar_fin_anuncio(driver)

        # Obtener el título y crear la carpeta
        carpeta_capturas = obtener_titulo_y_crear_carpeta(driver)
        if not carpeta_capturas:
            raise Exception("No se pudo crear la carpeta para las capturas")
        
        # Borrar contenido de la carpeta si existe
        try:
            # Borrar capturas anteriores si existen
            for archivo in os.listdir(carpeta_capturas):
                ruta_archivo = os.path.join(carpeta_capturas, archivo)
                if os.path.isfile(ruta_archivo):
                    os.remove(ruta_archivo)
        except PermissionError as e:
            print(f"Error de permisos al intentar eliminar archivos: {e}")
            # Aquí puedes decidir si continuar con la ejecución o manejar el error de otra manera
        obtener_info_video(url_video)


        # Encontrar el scrubber
        scrubber = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ytp-scrubber-container"))
        )
        
        # Esperar a que el reproductor de video cargue
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        
        # Dar tiempo para que la página cargue completamente
        time.sleep(5)
        
        # Localizar el scrubber del video
        try:
            scrubber = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ytp-scrubber-button"))
            )
            
            # Interactuar con el scrubber (hacer clic y mantener)
            action = ActionChains(driver)
            action.move_to_element(scrubber)
            action.click_and_hold()
            action.perform()
            
            # Capturar el mapa de calor
            capturar_mapa_calor(driver, carpeta_capturas)

            # Intentar obtener la duración del video
            duracion_video, duracion_segundos = obtener_duracion_video(driver, carpeta_capturas)
            
            if duracion_video:
                if duracion_segundos < 60:
                    driver.quit()
                    obtener_mapa_calor(url_video, intentos + 1)  # Llamada recursiva con contador
                    return  # Salir de la función actual después de la llamada recursiva
            else:
                print("No se pudo obtener la duración del video.")
            
        except Exception as e:
            print(f"Error al procesar el mapa de calor o obtener la duración: {e}")
        
    except Exception as e:
        print(f"Error al procesar el video: {str(e)}")
    finally:
        if driver:
            driver.quit()

# Modificar esta parte al final del script
if __name__ == "__main__":
    if len(sys.argv) > 1:
        url_video = sys.argv[1]
    else:
        print("Por favor, proporciona la URL del video como argumento.")
        sys.exit(1)
    
    tiempo_inicio = time.time()
    obtener_mapa_calor(url_video)
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio

    # Llamar a la función para guardar la URL
    guardar_url_video(url_video)
