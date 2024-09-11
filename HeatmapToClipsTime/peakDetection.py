import numpy as np
from scipy.signal import find_peaks

def detectar_picos_con_inicio_fin_respecto_media(señal, altura_minima, distancia_minima):
    picos, _ = find_peaks(señal, height=altura_minima, distance=distancia_minima)
    
    media_señal = np.mean(señal)
    
    resultados = []
    
    for pico in picos:
        inicio = pico
        while inicio > 0 and señal[inicio] > media_señal:
            inicio -= 1
        
        fin = pico
        while fin < len(señal) - 1 and señal[fin] > media_señal:
            fin += 1
        
        resultados.append((inicio, fin))
    
    return resultados, picos
