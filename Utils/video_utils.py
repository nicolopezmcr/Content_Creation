import os

def leer_duracion_video(ruta_carpeta):
    ruta_duracion = os.path.join(ruta_carpeta, "duracion_video.txt")
    try:
        with open(ruta_duracion, 'r') as f:
            duracion_str = f.read().strip()
        
        print(f"Contenido del archivo duracion_video.txt: '{duracion_str}'")
        
        partes = duracion_str.replace(',', ':').split(':')
        
        if len(partes) == 3:
            duracion_segundos = int(partes[0]) * 3600 + int(partes[1]) * 60 + int(partes[2])
        elif len(partes) == 2:
            duracion_segundos = int(partes[0]) * 60 + int(partes[1])
        elif len(partes) == 1:
            duracion_segundos = int(partes[0])
        else:
            raise ValueError(f"Formato de tiempo no reconocido: {duracion_str}")
        
        return duracion_segundos
    except FileNotFoundError:
        print(f"No se encontró el archivo de duración del video en: {ruta_duracion}")
        return None
    except Exception as e:
        print(f"Error al leer la duración del video: {e}")
        print(f"Contenido del archivo: {duracion_str}")
        return None
