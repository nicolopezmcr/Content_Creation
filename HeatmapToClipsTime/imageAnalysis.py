import numpy as np
from PIL import Image

def procesar_mapa_calor(ruta_mapa_calor):
    imagen = Image.open(ruta_mapa_calor).convert('L')
    datos_imagen = np.array(imagen)
    perfil_intensidad = np.mean(datos_imagen, axis=0)
    altura_minima = np.mean(perfil_intensidad)
    ancho_imagen = perfil_intensidad.shape[0]
    
    return perfil_intensidad, altura_minima, ancho_imagen

def calcular_tiempos_clips(resultados, ancho_imagen, duracion_video):
    clips = []
    for i, (inicio, fin) in enumerate(resultados):
        tiempo_inicio = (inicio / ancho_imagen) * duracion_video
        tiempo_fin = (fin / ancho_imagen) * duracion_video
        
        minutos_inicio = int(tiempo_inicio // 60)
        segundos_inicio = int(tiempo_inicio % 60)
        
        minutos_fin = int(tiempo_fin // 60)
        segundos_fin = int(tiempo_fin % 60)
        
        clip = f"Clip {i+1}: Inicio = {minutos_inicio:02d}:{segundos_inicio:02d}, Fin = {minutos_fin:02d}:{segundos_fin:02d}"
        clips.append(clip)
    
    return clips
