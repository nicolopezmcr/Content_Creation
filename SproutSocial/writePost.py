from uploadFile import subir_clip
from writeContent import escribir_contenido
from pasteDate import pegar_fecha
from datetime import datetime
from sendAndNew import programar_y_nuevo

def escribir_post(driver, clip):
    print(f"Iniciando proceso para el clip: {clip['titulo']}")
    try:
        if subir_clip(driver, clip['ruta_video']):
            print(f"Clip subido exitosamente: {clip['titulo']}")
            
            if escribir_contenido(driver, clip):
                print("Contenido del post escrito correctamente.")
                fecha_publicacion = datetime.fromisoformat(clip['fecha_programacion'])
                pegar_fecha(driver, fecha_publicacion)
                
                # Programar y preparar para el siguiente post
                programar_y_nuevo(driver)
                
                return True
            else:
                print("Error al escribir el contenido del post.")
                return False
        else:
            print(f"Error al subir el clip: {clip['titulo']}")
            return False
    except Exception as e:
        print(f"Error inesperado en escribir_post: {str(e)}")
        return False

# La función gestionar_posts ya no es necesaria aquí, ya que la iteración se realiza en manageUploads.py


