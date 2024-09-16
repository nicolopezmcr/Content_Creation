from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def verificar_selector_mobile_publisher(driver):
    try:
        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-qa-name='mobile-publisher']"))
        )
        print("El selector 'mobile-publisher' existe.")
        
        # Hacer clic en el elemento
        elemento.click()
        print("Se ha hecho clic en el selector 'mobile-publisher'.")
        
        # Buscar y hacer clic en el elemento Techno Lovers
        techno_lovers = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Techno Lovers')]"))
        )
        techno_lovers.click()
        print("Se ha hecho clic en 'Techno Lovers'.")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        print("El selector 'mobile-publisher' no se encontró o no se pudo interactuar con él.")
        return False

