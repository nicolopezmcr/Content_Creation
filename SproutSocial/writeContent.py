from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from prepareText import preparar_texto

def escribir_contenido(driver, clip_info):
    try:
        # Esperar a que la página se cargue completamente
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ComposeEditor-body"))
        )
        print("Página cargada completamente.")

        # Esperar a que el área de texto sea interactuable
        area_texto = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.public-DraftEditor-content[contenteditable='true']"))
        )
        print("Área de texto encontrada y clickeable.")

        # Esperar un poco más para asegurarnos de que todo esté listo
        time.sleep(5)

        contenido = preparar_texto(clip_info)
        
        # Usar JavaScript para pegar el contenido
        script = """
        var element = arguments[0];
        element.focus();
        const dataTransfer = new DataTransfer();
        dataTransfer.setData('text/plain', arguments[1]);
        element.dispatchEvent(new ClipboardEvent('paste', {
            clipboardData: dataTransfer,
            bubbles: true,
            cancelable: true
        }));
        """
        driver.execute_script(script, area_texto, contenido)
        print("Contenido de texto pegado.")

        # Esperar un poco más después de pegar el contenido
        time.sleep(3)

        return True
    except TimeoutException:
        print("No se pudo encontrar o interactuar con el área de texto.")
        return False
    except Exception as e:
        print(f"Error inesperado al escribir contenido: {str(e)}")
        return False

