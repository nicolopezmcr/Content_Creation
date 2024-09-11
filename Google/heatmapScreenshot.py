from selenium.webdriver.common.by import By
import os

def capturar_mapa_calor(driver, carpeta_capturas):
    # Capturar la pantalla completa mientras se muestra el mapa de calor
    driver.save_screenshot(os.path.join(carpeta_capturas, "mapa_calor_completo.png"))
    
    # Buscar elementos del mapa de calor
    elementos_heatmap = driver.find_elements(By.XPATH, "//div[contains(@class, 'ytp-heat-map-container')]")
    
    if elementos_heatmap:
        for i, elemento in enumerate(elementos_heatmap):
            try:
                # Verificar si el elemento es visible y tiene dimensiones
                if elemento.is_displayed():
                    tamaño = elemento.size
                    if tamaño['width'] > 0 and tamaño['height'] > 0:
                        # Capturar el elemento individual
                        elemento.screenshot(os.path.join(carpeta_capturas, f"mapa_calor_{i}.png"))
                    else:
                        print(f"El elemento del mapa de calor {i} tiene dimensiones de 0, no se puede capturar.")
                else:
                    print(f"El elemento del mapa de calor {i} no está visible, no se puede capturar.")
            except Exception as e:
                print(f"No se pudo capturar el elemento del mapa de calor {i}: {str(e)}")
    else:
        print("\nNo se encontraron elementos del mapa de calor.")
