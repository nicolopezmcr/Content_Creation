from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def programar_y_nuevo(driver):
    # Esperar a que el botón de "Más opciones" sea clickable
    boton_mas_opciones = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-qa-button='overflow' and @aria-label='Más opciones para guardar']"))
    )
    boton_mas_opciones.click()
    
    # Esperar a que el elemento "Programar + Nuevo" sea clickable en el desplegable
    opcion_programar_nuevo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@data-qa-menu-item='Programar + NuevoVolver a abrir la ventana Redactar en blanco']"))
    )
    opcion_programar_nuevo.click()
    
    # Hacer clic en el botón "Programar + nuevo"
    boton_programar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@data-qa-button, 'Programar + nuevo')]"))
    )
    boton_programar.click()
    
    # Esperar 5 segundos
    time.sleep(10)
    
    # Comprobar si existe el selector del borrador y desactivarlo si está activado
    try:
        toggle_borrador = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "draft-toggle"))
        )
        
        if toggle_borrador.get_attribute("aria-checked") == "true":
            toggle_borrador.click()
    except:
        print("El toggle de borrador no se encontró o ya está desactivado.")

def seleccionar_fecha(driver, fecha):
    # Abrir el selector de fecha
    selector_fecha = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Fecha']"))
    )
    selector_fecha.click()

    # Esperar a que el calendario esté visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "react-datepicker"))
    )

    # Usar JavaScript para establecer la fecha directamente
    fecha_formateada = fecha.strftime("%Y-%m-%d")
    script = f"arguments[0].value = '{fecha_formateada}'; arguments[0].dispatchEvent(new Event('change'));"
    driver.execute_script(script, selector_fecha)

    # Cerrar el calendario haciendo clic fuera de él
    driver.find_element(By.TAG_NAME, "body").click()

# Asegúrate de llamar a esta función con tu instancia de WebDriver
# Ejemplo: programar_y_nuevo(driver)
