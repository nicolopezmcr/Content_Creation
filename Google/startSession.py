from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def iniciar_sesion_chrome():
    chrome_options = Options()
    
    # Crear un directorio para el perfil si no existe
    perfil_dir = os.path.join(os.getcwd(), "perfil_chrome")
    if not os.path.exists(perfil_dir):
        os.makedirs(perfil_dir)
    
    # Usar el perfil creado
    chrome_options.add_argument(f"user-data-dir={perfil_dir}")
    
    # Iniciar el navegador Chrome
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver

# Ejemplo de uso:
# driver = iniciar_sesion_chrome()
# ... usar el driver ...
# driver.quit()
