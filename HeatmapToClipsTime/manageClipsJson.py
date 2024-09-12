import os
import json
from math import ceil

def tiempo_a_segundos(tiempo):
    m, s = map(int, tiempo.split(':'))
    return m * 60 + s

def segundos_a_tiempo(segundos):
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02d}:{segundos:02d}"

def ajustar_clip(inicio, fin):
    duracion = tiempo_a_segundos(fin) - tiempo_a_segundos(inicio)
    if duracion < 30:
        return None
    elif 30 <= duracion < 60:
        tiempo_adicional = 60 - duracion
        nuevo_inicio = max(0, tiempo_a_segundos(inicio) - tiempo_adicional // 2)
        nuevo_fin = tiempo_a_segundos(fin) + (tiempo_adicional - (tiempo_adicional // 2))
        return segundos_a_tiempo(nuevo_inicio), segundos_a_tiempo(nuevo_fin)
    elif duracion > 180:
        num_partes = ceil(duracion / 180)
        duracion_parte = duracion / num_partes
        clips_divididos = []
        for i in range(num_partes):
            inicio_parte = tiempo_a_segundos(inicio) + int(i * duracion_parte)
            fin_parte = min(tiempo_a_segundos(fin), inicio_parte + int(duracion_parte))
            clips_divididos.append((segundos_a_tiempo(inicio_parte), segundos_a_tiempo(fin_parte)))
        return clips_divididos
    else:
        return inicio, fin

def analizar_clips(ruta_carpeta):
    ruta_archivo = os.path.join(ruta_carpeta, 'clips.json')
    
    if not os.path.exists(ruta_archivo):
        print(f"No se encontró el archivo clips.json en {ruta_carpeta}")
        return {}

    print(f"Leyendo el archivo: {ruta_archivo}")
    with open(ruta_archivo, 'r') as archivo:
        clips_data = json.load(archivo)
    
    print(f"Número de clips originales: {len(clips_data)}")

    clips_procesados = {}
    clips_unicos = set()

    for clip_info in clips_data.values():
        tiempo_inicio = clip_info['inicio']
        tiempo_fin = clip_info['fin']
        
        resultado_ajuste = ajustar_clip(tiempo_inicio, tiempo_fin)
        
        if resultado_ajuste is None:
            continue
        elif isinstance(resultado_ajuste, list):
            for inicio, fin in resultado_ajuste:
                if (inicio, fin) not in clips_unicos:
                    clips_unicos.add((inicio, fin))
                    clips_procesados[f"clip{len(clips_procesados) + 1}"] = {
                        "inicio": inicio,
                        "fin": fin,
                        "duracion": tiempo_a_segundos(fin) - tiempo_a_segundos(inicio)
                    }
        else:
            inicio, fin = resultado_ajuste
            if (inicio, fin) not in clips_unicos:
                clips_unicos.add((inicio, fin))
                clips_procesados[f"clip{len(clips_procesados) + 1}"] = {
                    "inicio": inicio,
                    "fin": fin,
                    "duracion": tiempo_a_segundos(fin) - tiempo_a_segundos(inicio)
                }

    print(f"Número de clips después del procesamiento: {len(clips_procesados)}")
    print(f"Sobrescribiendo el archivo: {ruta_archivo}")
    
    with open(ruta_archivo, 'w') as archivo:
        json.dump(clips_procesados, archivo, ensure_ascii=False, indent=4)
    
    print(f"Archivo sobrescrito exitosamente.")
    
    return clips_procesados

# Ejemplo de uso
if __name__ == "__main__":
    ruta_carpeta = "Content_Creation/VideoData/Fatima Hajji _ Aniversario CODE - Fabrik Madrid 19 11 2022-15 dic 2022"
    clips_procesados = analizar_clips(ruta_carpeta)
    print("Proceso completado.")

