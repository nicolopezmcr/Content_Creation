import os

def analizar_clips(ruta_carpeta):
    ruta_archivo = os.path.join(ruta_carpeta, 'Clips.txt')
    clips_unicos = []
    
    if not os.path.exists(ruta_archivo):
        print(f"No se encontró el archivo Clips.txt en {ruta_carpeta}")
        return []

    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        encabezado = lineas[0]  # Guardamos el encabezado
        for linea in lineas[1:]:
            partes = linea.strip().split(': ', 1)
            if len(partes) == 2:
                _, datos_clip = partes
                if datos_clip not in clips_unicos:
                    clips_unicos.append(datos_clip)
    
    # Sobrescribir el archivo con los clips únicos
    with open(ruta_archivo, 'w') as archivo:
        archivo.write(encabezado)
        for i, clip in enumerate(clips_unicos, 1):
            archivo.write(f"Clip {i}: {clip}\n")
    
    print(f"Se han eliminado las repeticiones. Ahora hay {len(clips_unicos)} clips únicos.")
    return clips_unicos

