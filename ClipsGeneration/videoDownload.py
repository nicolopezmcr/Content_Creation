import os
import yt_dlp

def descargar_video_completo(url, carpeta_salida, callback=None):
    nombre_salida = os.path.join(os.path.dirname(carpeta_salida), 'video_completo.mp4')
    if os.path.exists(nombre_salida):
        mensaje = f"El video completo ya existe: {nombre_salida}"
        print(mensaje)
        if callback:
            callback(mensaje)
        return nombre_salida
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': nombre_salida,
        'concurrent_fragment_downloads': 10,
        'retries': 10,
        'fragment_retries': 10,
        'http_chunk_size': 10485760,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        mensaje = f"Video completo descargado: {nombre_salida}"
        print(mensaje)
        if callback:
            callback(mensaje)
        return nombre_salida
    except Exception as e:
        mensaje = f"Error al descargar el video completo: {str(e)}"
        print(mensaje)
        if callback:
            callback(mensaje)
        return None
