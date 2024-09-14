from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import locale
import time

# Configurar el locale para español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def pegar_fecha(driver, fecha):
    try:
        print(f"Intentando pegar la fecha: {fecha}")

        # Encontrar el input de fecha
        fecha_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='M/D/YYYY']"))
        )
        
        # Formatear la fecha como "sáb., sep. 14, 2024"
        fecha_formateada = fecha.strftime("%a., %b. %d, %Y").lower()
        
        # Corregir abreviaturas de meses en español
        meses_abreviados = {
            "ene.": "ene", "feb.": "feb", "mar.": "mar", "abr.": "abr",
            "may.": "may", "jun.": "jun", "jul.": "jul", "ago.": "ago",
            "sep.": "sep", "oct.": "oct", "nov.": "nov", "dic.": "dic"
        }
        for mes_esp, mes_abr in meses_abreviados.items():
            fecha_formateada = fecha_formateada.replace(mes_esp, mes_abr)
        
        # Ingresar la fecha
        fecha_input.clear()
        fecha_input.send_keys(fecha_formateada)
        print(f"Fecha ingresada: {fecha_formateada}")
        
        # Seleccionar la hora
        hora_24 = int(fecha.strftime("%H"))
        hora_12 = str(((hora_24 - 1) % 12) + 1)  # Convertir a formato 12h
        minutos = fecha.strftime("%M")
        am_pm = "am" if hora_24 < 12 else "pm"

        print(f"Intentando seleccionar hora: {hora_12} {am_pm}")
        
        # Esperar a que el selector de horas tenga opciones válidas
        def horas_cargadas(driver):
            selector = Select(driver.find_element(By.CSS_SELECTOR, "select[id^='hours-time_picker']"))
            return len(selector.options) > 1 and selector.options[0].text != '-'

        WebDriverWait(driver, 20).until(horas_cargadas)
        
        selector_hora = Select(driver.find_element(By.CSS_SELECTOR, "select[id^='hours-time_picker']"))
        
        # Obtener todas las opciones disponibles
        opciones = selector_hora.options
        print(f"Opciones de hora disponibles: {[option.text for option in opciones]}")
        
        # Encontrar la opción correcta
        hora_correcta = None
        for opcion in opciones:
            if opcion.text == hora_12:
                hora_correcta = opcion
                break
        
        if hora_correcta:
            selector_hora.select_by_visible_text(hora_correcta.text)
            print(f"Hora seleccionada: {hora_correcta.text}")
        else:
            print(f"No se pudo encontrar la opción para la hora {hora_12}")
            return False

        print(f"Intentando seleccionar minutos: {minutos}")
        selector_minutos = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[id^='minutes-time_picker']"))
        )
        Select(selector_minutos).select_by_value(minutos)
        print(f"Minutos seleccionados: {minutos}")

        print(f"Intentando seleccionar AM/PM: {am_pm}")
        selector_ampm = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[id^='meridiem-time_picker']"))
        )
        Select(selector_ampm).select_by_value(am_pm)
        print(f"AM/PM seleccionado: {am_pm}")
        
        print(f"Fecha y hora pegadas completamente: {fecha_formateada} {hora_12}:{minutos} {am_pm}")
        return True
    except Exception as e:
        print(f"Error al pegar la fecha: {str(e)}")
        return False
