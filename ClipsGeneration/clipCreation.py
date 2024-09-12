import os
import subprocess

def generar_clips(video_completo, clips, carpeta_salida, callback=None):
    # Verificar si todos los clips ya existen
    todos_clips_existen = True
    for i in range(1, len(clips) + 1):
        nombre_clip = os.path.join(carpeta_salida, f'clip_{i}.mp4')
        if not os.path.exists(nombre_clip):
            todos_clips_existen = False
            break

    if todos_clips_existen:
        mensaje = "Todos los clips ya existen. Saltando la generación."
        print(mensaje)
        if callback:
            callback(mensaje)
        return False

    # Generar clips solo si no existen
    for i, (inicio, fin) in enumerate(clips, 1):
        nombre_salida = os.path.join(carpeta_salida, f'clip_{i}.mp4')
        if not os.path.exists(nombre_salida):
            duracion = fin - inicio
            comando = [
                'ffmpeg',
                '-y',
                '-ss', str(inicio),
                '-i', video_completo,
                '-t', str(duracion),
                '-c', 'copy',
                '-loglevel', 'error',
                nombre_salida
            ]
            
            try:
                subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                mensaje = f"Clip {i} generado: {nombre_salida}"
                print(mensaje)
                if callback:
                    callback(mensaje)
            except subprocess.CalledProcessError as e:
                mensaje = f"Error al generar el clip {i}: {e}"
                print(mensaje)
                if callback:
                    callback(mensaje)
        else:
            mensaje = f"Clip {i} ya existe: {nombre_salida}"
            print(mensaje)
            if callback:
                callback(mensaje)

    return True
