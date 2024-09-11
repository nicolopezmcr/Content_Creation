import sys
import os
import numpy as np
from PIL import Image, ImageDraw

# Añadir el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heatmapManage import analizar_mapa_calor
from imageAnalysis import procesar_mapa_calor
from peakDetection import detectar_picos_con_inicio_fin_respecto_media

def marcar_puntos_en_mapa_calor(ruta_mapa_calor, resultados, nombre_salida):
    imagen = Image.open(ruta_mapa_calor)
    draw = ImageDraw.Draw(imagen)
    
    for inicio, fin in resultados:
        draw.line([(inicio, 0), (inicio, imagen.height)], fill=(0, 0, 255, 128), width=2)  # Azul semitransparente
        draw.line([(fin, 0), (fin, imagen.height)], fill=(255, 0, 0, 128), width=2)  # Rojo semitransparente
    
    imagen.save(nombre_salida)

def ejecutar_prueba(ruta_base):
    print("\nEjecutando análisis:")
    resultado = analizar_mapa_calor(ruta_base)
    
    if resultado:
        ruta_carpeta, ruta_mapa_calor, resultados = resultado
        print(f"Ruta del mapa de calor original: {ruta_mapa_calor}")
        
        if not os.path.exists(ruta_mapa_calor):
            print(f"Error: No se encontró el archivo {ruta_mapa_calor}")
            return
        
        print(f"Número de picos detectados: {len(resultados)}")
        
        nombre_salida = os.path.join(os.path.dirname(__file__), "mapa_calor_marcado.png")
        print(f"Intentando guardar mapa de calor marcado en: {nombre_salida}")
        
        try:
            marcar_puntos_en_mapa_calor(ruta_mapa_calor, resultados, nombre_salida)
            if os.path.exists(nombre_salida):
                print(f"Mapa de calor marcado guardado como: {nombre_salida}")
            else:
                print(f"Error: No se pudo guardar el mapa de calor marcado en {nombre_salida}")
        except Exception as e:
            print(f"Error al marcar puntos en el mapa de calor: {str(e)}")
        
        # Guardar resultados en un archivo de texto
        nombre_resultados = os.path.join(os.path.dirname(__file__), "resultados_analisis.txt")
        try:
            with open(nombre_resultados, 'w') as f:
                f.write(f"Análisis del mapa de calor:\n")
                f.write(f"Ruta del mapa de calor: {ruta_mapa_calor}\n")
                f.write(f"Número de picos detectados: {len(resultados)}\n\n")
                for i, (inicio, fin) in enumerate(resultados, 1):
                    f.write(f"Pico {i}: Inicio = {inicio}, Fin = {fin}\n")
            print(f"Resultados guardados en: {nombre_resultados}")
        except Exception as e:
            print(f"Error al guardar los resultados: {str(e)}")
    else:
        print("No se pudo analizar el mapa de calor.")

if __name__ == "__main__":
    ruta_base = "/Users/nicolopez/Cursor/Content_Creation/VideoData"
    ejecutar_prueba(ruta_base)
