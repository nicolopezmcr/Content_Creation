from uploadFile import subir_clip
from writeContent import escribir_contenido

def escribir_post(driver, clip_info):
    print(f"Iniciando proceso para el clip: {clip_info['titulo']}")
    try:
        if subir_clip(driver, clip_info['ruta_video']):
            print(f"Clip subido exitosamente: {clip_info['titulo']}")
            
            if escribir_contenido(driver, clip_info):
                print("Contenido del post escrito correctamente.")
                return True
            else:
                print("Error al escribir el contenido del post.")
                return False
        else:
            print(f"Error al subir el clip: {clip_info['titulo']}")
            return False
    except Exception as e:
        print(f"Error inesperado en escribir_post: {str(e)}")
        return False

def gestionar_posts(driver):
    from getClipsInfo import obtener_info_clips
    clips_info = obtener_info_clips()
    if clips_info:
        print(f"Se encontraron {len(clips_info)} clips para procesar.")
        for clip in clips_info:
            if escribir_post(driver, clip):
                print(f"Post creado exitosamente para el clip: {clip['titulo']}")
            else:
                print(f"Error al crear el post para el clip: {clip['titulo']}")
    else:
        print("No se encontraron clips para procesar.")


