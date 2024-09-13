from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def subir_clip(driver, ruta_video):
    try:
        # Localizar el input de archivo oculto y cargar el archivo
        input_file = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-qa-file-selector='qa-videoinput']"))
        )
        input_file.send_keys(ruta_video)
        print(f"Archivo seleccionado: {ruta_video}")

        # Esperar a que se complete la carga
        WebDriverWait(driver, 120).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".upload-progress"))
        )
        print("Video procesado correctamente.")

        # Esperar un poco más para asegurarse de que la interfaz se ha actualizado
        time.sleep(5)

        return True
    except TimeoutException:
        print("Hubo un problema al subir el video o al esperar que se procese.")
        return False
    except Exception as e:
        print(f"Error inesperado al subir el clip: {str(e)}")
        return False
