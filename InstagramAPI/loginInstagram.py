import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time

# Cargar variables de entorno
load_dotenv()

def iniciar_sesion_instagram(driver):
    # Navegar a Instagram
    driver.get("https://www.instagram.com/")
    
    # Verificar si el botón "Crear" está presente
    try:
        crear_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@role='link']//span[contains(text(), 'Crear')]"))
        )
        print("El botón 'Crear' está presente. La sesión ya está iniciada.")
        return True
    except:
        print("El botón 'Crear' no está presente. Procediendo con el inicio de sesión.")

    # Esperar a que aparezca el formulario de inicio de sesión
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginForm"))
        )
        
        # Ingresar credenciales
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        
        username.send_keys(os.getenv("INSTAGRAM_USERNAME"))
        password.send_keys(os.getenv("INSTAGRAM_PASSWORD"))
        
        # Enviar el formulario
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        time.sleep(3)
        
        print("Inicio de sesión exitoso en Instagram")
        return True
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return False
