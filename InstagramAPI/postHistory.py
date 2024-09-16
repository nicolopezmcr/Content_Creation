import json
import os
from datetime import datetime

class PostHistory:
    def __init__(self, history_file='post_history.json'):
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_to_history(self, clip_number, titulo):
        self.history.append({
            'clip': f'clip{clip_number}',
            'titulo': titulo,
            'fecha_subido': datetime.now().isoformat()
        })
        self.save_history()

    def is_clip_uploaded(self, clip_number):
        return any(item['clip'] == f'clip{clip_number}' for item in self.history)

def registrar_clip_subido(clip_number, titulo):
    history = PostHistory()
    if not history.is_clip_uploaded(clip_number):
        history.add_to_history(clip_number, titulo)
        print(f"Clip {clip_number} - '{titulo}' añadido al historial de publicaciones.")
    else:
        print(f"El clip {clip_number} ya está en el historial de publicaciones.")

def verificar_clip_subido(clip_number):
    history = PostHistory()
    return history.is_clip_uploaded(clip_number)

# Eliminamos las funciones que no se utilizan
# def obtener_proximo_clip():
# def marcar_clip_como_subido():

# Ejemplo de uso
if __name__ == "__main__":
    # Simular registro de clips subidos
    registrar_clip_subido(1, "Título del clip 1")
    registrar_clip_subido(2, "Título del clip 2")
    registrar_clip_subido(1, "Título del clip 1")  # Intentar registrar duplicado

    # Verificar si un clip está subido
    print(f"¿El clip 1 está subido? {verificar_clip_subido(1)}")
    print(f"¿El clip 3 está subido? {verificar_clip_subido(3)}")
