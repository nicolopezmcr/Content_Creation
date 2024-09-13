from openSproutSocial import abrir_sprout_social
from chooseCurrentDate import seleccionar_fecha_actual
from writePost import escribir_post
from getClipsInfo import obtener_info_clips
import traceback
import time

def gestionar_publicaciones():
    
    try:
        driver = abrir_sprout_social()
        print("Sprout Social abierto correctamente.")
        
        if seleccionar_fecha_actual(driver):
            print("Fecha actual seleccionada correctamente.")
            time.sleep(5)  # Esperar 5 segundos adicionales
            
            clips_info = obtener_info_clips()
            if clips_info:
                print(f"Se encontraron {len(clips_info)} clips para subir.")
                # Procesar solo el primer clip
                clip = clips_info[0]
                print(f"Intentando subir el clip: {clip['titulo']}")
                
                if escribir_post(driver, clip):
                    print(f"Clip '{clip['titulo']}' subido exitosamente.")
                else:
                    print(f"Error al subir el clip '{clip['titulo']}'.")
            else:
                print("No se encontraron clips para subir.")
        else:
            print("No se pudo seleccionar la fecha actual.")
    except Exception as e:
        print(f"Error durante la gestión de publicaciones: {str(e)}")
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
            print("Navegador cerrado.")

if __name__ == "__main__":
    gestionar_publicaciones()