from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def esperar_fin_anuncio(driver, timeout=15):
    try:
        anuncio_presente = EC.presence_of_element_located((By.CLASS_NAME, "ad-showing"))
        WebDriverWait(driver, 3).until(anuncio_presente)
        print("Anuncio detectado, esperando a que termine...")
        boton_saltar = EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-skip-ad-button"))
        fin_anuncio = EC.invisibility_of_element_located((By.CLASS_NAME, "ad-showing"))
        
        
        WebDriverWait(driver, timeout).until(EC.any_of(fin_anuncio, boton_saltar))
        
        try:
            driver.find_element(By.CSS_SELECTOR, "button.ytp-skip-ad-button").click()
            print("Botón 'Saltar anuncio' clickeado.")
        except:
            pass

        print("Anuncio terminado o saltado.")
        return True
    except:
        print("No se detectó anuncio.")
        return False
