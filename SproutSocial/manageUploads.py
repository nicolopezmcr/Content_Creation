from openSproutSocial import abrir_sprout_social
from writePost import escribir_post
from postCalendar import actualizar_calendario_y_clips, cargar_clips_json
from getClipsInfo import obtener_info_clips
import traceback
import time
from datetime import datetime
import json
from chooseCurrentDate import seleccionar_fecha_actual

def gestionar_publicaciones():
    try:
        # Obtener información de los clips
        obtener_info_clips()
        
        # Actualizar el calendario y los clips
        clips_json = actualizar_calendario_y_clips()

        if clips_json is None:
            print("No se pudieron actualizar los clips. Abortando.")
            return

        # Abrir Sprout Social
        driver = abrir_sprout_social()
        print("Sprout Social abierto correctamente.")

        seleccionar_fecha_actual(driver)

        if isinstance(clips_json, dict):
            clips_lista = list(clips_json.values())
        else:
            print(f"Error: clips_json no es un diccionario. Tipo: {type(clips_json)}")
            return

        for clip in clips_lista:
            if isinstance(clip, dict) and 'fecha_programacion' in clip:
                fecha_publicacion = datetime.fromisoformat(clip['fecha_programacion'])
                print(f"Intentando programar el clip: {clip['titulo']} para {fecha_publicacion}")
                print(f"Ruta del video: {clip.get('ruta_video', 'No disponible')}")
                
                if 'ruta_video' not in clip:
                    print(f"Error: 'ruta_video' no encontrada para el clip: {clip['titulo']}")
                    continue

                if escribir_post(driver, clip):
                    print(f"Clip '{clip['titulo']}' programado exitosamente para {fecha_publicacion}.")
                else:
                    print(f"Error al programar el clip '{clip['titulo']}'.")

                # Esperar un poco entre publicaciones
                time.sleep(5)
            else:
                print(f"Advertencia: Clip inválido o sin fecha de programación: {clip}")

    except Exception as e:
        print(f"Error durante la gestión de publicaciones: {str(e)}")
        traceback.print_exc()
    finally:
        if 'driver' in locals():
            driver.quit()
            print("Navegador cerrado.")

if __name__ == "__main__":
    gestionar_publicaciones()