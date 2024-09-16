import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openChrome import abrir_chrome
from loginInstagram import iniciar_sesion_instagram
from postHistory import registrar_clip_subido, verificar_clip_subido
import json
def obtener_info_clip():
    video_data_path = "/Users/nicolopez/Cursor/Content_Creation/VideoData"
    
    carpetas = [f for f in os.listdir(video_data_path) if os.path.isdir(os.path.join(video_data_path, f))]
    ultima_carpeta = max(carpetas, key=lambda x: os.path.getctime(os.path.join(video_data_path, x)))
    
    clips_json_path = os.path.join(video_data_path, ultima_carpeta, "clips.json")
    
    print(f"Buscando clips en: {clips_json_path}")
    
    with open(clips_json_path, 'r') as f:
        clips = json.load(f)
    
    for clip_key, clip_info in clips.items():
        clip_number = int(clip_key.replace('clip', ''))
        if not verificar_clip_subido(clip_number):
            ruta_video = clip_info['ruta_video']
            if os.path.exists(ruta_video):
                print(f"Clip encontrado para subir: {clip_key}")
                return {
                    'numero_clip': clip_number,
                    **clip_info
                }
    
    print("No hay clips nuevos para subir.")
    return None

def subir_post(driver):
    try:
        clip_info = obtener_info_clip()
        if not clip_info:
            return False
        
        ruta_archivo = clip_info['ruta_video']
        numero_clip = clip_info['numero_clip']
        print(f"Intentando subir: {ruta_archivo}")
        
        # Esperar a que el botón "Crear" esté presente y visible
        crear_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@role='link']//span[contains(text(), 'Crear')]/ancestor::a"))
        )
        
        # Usar JavaScript para hacer clic en el botón
        driver.execute_script("arguments[0].click();", crear_button)
        print("Se hizo clic en el botón 'Crear'")
        
        # Esperar a que aparezca el input de tipo file
        input_file = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        
        # Cargar el archivo directamente
        input_file.send_keys(ruta_archivo)
        print(f"Se seleccionó el archivo: {ruta_archivo}")
        
        # Esperar a que se cargue el video
        time.sleep(5)  # Ajusta este tiempo según sea necesario
        
        # Esperar a que aparezca el primer botón "Siguiente" y hacer clic
        siguiente_button1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(text(), 'Siguiente')]"))
        )
        siguiente_button1.click()
        print("Se hizo clic en el primer botón 'Siguiente'")
        
        # Esperar un momento después de hacer clic en el primer "Siguiente"
        time.sleep(3)
        
        # Esperar a que aparezca el segundo botón "Siguiente" y hacer clic
        siguiente_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(text(), 'Siguiente')]"))
        )
        siguiente_button2.click()
        print("Se hizo clic en el segundo botón 'Siguiente'")
        
        # Esperar un momento después de hacer clic en el segundo "Siguiente"
        time.sleep(3)

        # Esperar a que aparezca el campo de texto para el pie de foto
        pie_foto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Escribe un pie de foto o vídeo…']"))
        )
        
        # Preparar el contenido del pie de foto
        titulo = clip_info['titulo']
        descripcion = clip_info['descripcion']
        pregunta = clip_info['pregunta']
        canal = clip_info['canal']
        tags = ' '.join([f"#{tag}" for tag in clip_info['tags']])
        
        contenido_pie_foto = f"{titulo}\n\n{descripcion}\n\n{pregunta}\n\nCanal: {canal}\n\n{tags}"
        
        # Introducir el contenido en el campo de texto
        pie_foto.send_keys(contenido_pie_foto)
        print("Se ha introducido el pie de foto")
        
        # Esperar un momento después de introducir el texto
        time.sleep(3)
        
        # Esperar a que aparezca el botón "Compartir" y hacer clic
        compartir_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(text(), 'Compartir')]"))
        )
        compartir_button.click()
        print("Se hizo clic en el botón 'Compartir'")
        
        # Esperar a que aparezca el mensaje de confirmación
        mensaje_confirmacion = WebDriverWait(driver, 500).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Se ha compartido tu reel.')]"))
        )
        
        if mensaje_confirmacion:
            print(f"El post del clip {numero_clip} se ha compartido exitosamente")
            registrar_clip_subido(numero_clip, clip_info['titulo'])
            return True
        else:
            print("No se pudo confirmar la publicación del post")
            return False

    except Exception as e:
        print(f"Error al intentar subir el post: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    driver = abrir_chrome()
    iniciar_sesion_instagram(driver)
    
    if subir_post(driver):
        print("Post subido exitosamente.")
    else:
        print("No se pudo subir el post o no hay clips nuevos.")
    
    driver.quit()
