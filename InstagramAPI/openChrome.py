import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def abrir_chrome():
    # Configurar opciones de Chrome
    chrome_options = Options()
    perfil_dir = os.path.join(os.getcwd(), "perfil_chrome")
    chrome_options.add_argument(f"user-data-dir={perfil_dir}")
    
    # Iniciar el navegador Chrome
    driver = webdriver.Chrome(options=chrome_options)
    return driver
