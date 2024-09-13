from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time

def seleccionar_fecha_actual(driver):
    print("Iniciando seleccionar_fecha_actual...")
    
    try:
        print("Buscando el botón del día actual...")
        boton_dia_actual = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.CalendarWeekBody-headerDay--today button"))
        )
        print(f"Botón del día actual encontrado: {boton_dia_actual.text}")
        
        print("Intentando hacer clic en el botón del día actual...")
        boton_dia_actual.click()
        print("Clic exitoso en el botón del día actual")
        
        # Esperar un momento para que la página se actualice
        time.sleep(1)
        
        print("Buscando el menú 'Programar una publicación'...")
        menu_item = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-qa-menu-item='Programar una publicación']"))
        )
        
        print("Intentando hacer clic usando JavaScript...")
        driver.execute_script("arguments[0].click();", menu_item)
        
        # Verificar si el menú desaparece
        try:
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "li[data-qa-menu-item='Programar una publicación']"))
            )
            print("El menú 'Programar una publicación' desapareció, indicando un cambio en la interfaz.")
            return True
        except TimeoutException:
            print("El menú 'Programar una publicación' sigue visible.")
        
        print("No se detectó ningún cambio después de intentar hacer clic.")
        return False
        
    except Exception as e:
        print(f"Error inesperado en seleccionar_fecha_actual: {str(e)}")
        return False

if __name__ == "__main__":
    from manageUploads import abrir_sprout_social
    driver = abrir_sprout_social()
    seleccionar_fecha_actual(driver)
    driver.quit()