from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import dotenv

def abrir_sprout_social():
    chrome_options = Options()
    
    # Crear un directorio para el perfil si no existe
    perfil_dir = os.path.join(os.getcwd(), "perfil_chrome")
    if not os.path.exists(perfil_dir):
        os.makedirs(perfil_dir)
    
    # Usar el perfil creado
    chrome_options.add_argument(f"user-data-dir={perfil_dir}")
    
    # Añadir opciones adicionales
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    
    # Usar webdriver_manager para manejar la instalación del ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    print("Iniciando Chrome...")
    # Inicializar el driver de Chrome con las opciones y el servicio
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Chrome iniciado correctamente.")
    
    url_inicial = "https://app.sproutsocial.com/publishing/calendar/"
    print(f"Accediendo a la URL inicial: {url_inicial}")
    driver.get(url_inicial)
    print("URL cargada. Esperando elementos...")
    
    # Esperar 3 segundos para ver si se carga la página principal
    time.sleep(3)
    
    # Verificar si es necesario iniciar sesión
    if driver.current_url.startswith("https://app.sproutsocial.com/login"):
        print("Es necesario iniciar sesión.")
        
        # Cargar variables de entorno
        dotenv.load_dotenv()
        
        # Esperar y completar el campo de correo electrónico
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(os.getenv("MAIL_SPROUT"))
        
        # Completar el campo de contraseña
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(os.getenv("PASSWORD_SPROUT"))
        
        # Marcar la casilla "Recuérdame" si no está marcada
        remember_me = driver.find_element(By.ID, "rememberMe")
        if not remember_me.is_selected():
            remember_me.click()
        
        # Hacer clic en el botón de inicio de sesión
        login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Log In')]")
        login_button.click()
        
        print("Inicio de sesión completado. Esperando carga de la página...")
        time.sleep(2)  # Esperar a que se cargue la página después del inicio de sesión
        
        # Intentar ir a la URL inicial después de iniciar sesión
        print(f"Intentando acceder nuevamente a la URL inicial: {url_inicial}")
        driver.get(url_inicial)
        print("URL inicial cargada después del inicio de sesión.")
    
    else:
        print("Ya se ha iniciado sesión. Continuando...")
    
    print("Sprout Social abierto y listo para usar.")
    return driver

if __name__ == "__main__":
    driver = abrir_sprout_social()
    try:
        print("Manteniendo la sesión de Chrome abierta. Presiona Ctrl+C para cerrar.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCerrando el navegador...")
    finally:
        driver.quit()
