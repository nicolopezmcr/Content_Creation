import os

def crear_carpeta_clips_raw(ultima_carpeta):
    carpeta_clips = os.path.join(ultima_carpeta, 'clips_raw')
    os.makedirs(carpeta_clips, exist_ok=True)
    return carpeta_clips
