import os

def obtener_ultima_carpeta(ruta_base):
    carpetas = [os.path.join(ruta_base, d) for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]
    return max(carpetas, key=os.path.getmtime) if carpetas else None

def obtener_ultimo_archivo(ruta_base, extension):
    archivos = [os.path.join(ruta_base, f) for f in os.listdir(ruta_base) if os.path.isfile(os.path.join(ruta_base, f)) and f.endswith(extension)]
    return max(archivos, key=os.path.getmtime) if archivos else None

def obtener_ultimo_archivo_json_video(ruta_base):
    return obtener_ultimo_archivo(ruta_base, 'info_video.json')

def obtener_ultimo_archivo_txt_clips(ruta_base):
    return obtener_ultimo_archivo(ruta_base, 'Clips.txt')

def obtener_ruta_a_clips_en_ultima_carpeta(ruta_base):
    ultima_carpeta = obtener_ultima_carpeta(ruta_base)
    if ultima_carpeta:
        return os.path.join(ultima_carpeta,'clips_raw','Clips.txt')
    return None