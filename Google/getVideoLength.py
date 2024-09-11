from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def obtener_duracion_video(driver, carpeta_capturas=None):
    try:
        # Esperar a que la duración sea visible
        duracion_elemento = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ytp-time-duration"))
        )
        
        duracion_texto = duracion_elemento.text
        if duracion_texto:
            # Convertir la duración a segundos
            duracion_segundos = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duracion_texto.split(':'))))
            
            if carpeta_capturas:
                # Guardar la duración del video en un archivo
                ruta_duracion = os.path.join(carpeta_capturas, "duracion_video.txt")
                with open(ruta_duracion, 'w') as f:
                    f.write(duracion_texto)
            
            return duracion_texto, duracion_segundos
        else:
            raise ValueError("No se pudo obtener la duración del video")
    except Exception as e:
        print(f"Error al obtener la duración del video: {str(e)}")
        return None, None
