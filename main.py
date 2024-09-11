import subprocess
import sys

def main():
    # Solicitar la URL del video al usuario
    url_video = input("Por favor, ingresa la URL del video de YouTube: ")

    # Verificar que la URL no esté vacía
    if not url_video:
        print("Error: No se proporcionó una URL válida.")
        sys.exit(1)

    # Ejecutar getHeatmap.py con la URL proporcionada
    try:
        resultado = subprocess.run(["python", "Google/getHeatmap.py", url_video], check=True, text=True, capture_output=True)
        print(resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar getHeatmap.py: {e}")
        print(f"Salida de error: {e.stderr}")
    except FileNotFoundError:
        print("Error: No se pudo encontrar el archivo getHeatmap.py. Asegúrate de que esté en la ruta correcta.")

if __name__ == "__main__":
    main()
