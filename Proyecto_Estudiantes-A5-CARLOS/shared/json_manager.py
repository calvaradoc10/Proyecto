# este módulo es el único que lee y escribe el archivo
import json
import os


class GestorJSON:
    """Lee y guarda una lista de diccionarios en un archivo JSON."""

    def __init__(self, ruta):
        self.__ruta = ruta

        # si la carpeta no existe, la crea
        carpeta = os.path.dirname(ruta)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    # la ruta solo se puede leer, no cambiar
    @property
    def ruta(self):
        return self.__ruta

    # si el archivo no existe o está dañado devuelve una lista vacía
    def leer(self):
        if not os.path.exists(self.__ruta):
            return []

        try:
            with open(self.__ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            return datos if isinstance(datos, list) else []

        except (json.JSONDecodeError, OSError):
            return []

    # devuelve True si guardó bien y False si falló
    def guardar(self, datos):
        try:
            with open(self.__ruta, "w", encoding="utf-8") as archivo:
                json.dump(
                    datos,
                    archivo,
                    # para que las tildes y la ñ se guarden bien
                    ensure_ascii=False,
                    indent=2
                )

            return True

        except (TypeError, OSError):
            return False


# prueba rápida con una carpeta temporal
if __name__ == "__main__":
    gestor = GestorJSON("prueba_temp/estudiantes.json")
    print("Ruta:", gestor.ruta)

    print("Leer sin archivo:", gestor.leer())

    estudiantes = [
        {"nombre": "Ana", "edad": 20},
        {"nombre": "José", "edad": 22},
    ]
    print("Guardar:", gestor.guardar(estudiantes))
    print("Leer:", gestor.leer())

    # un set no es JSON, tiene que dar False
    print("Guardar dato inválido:", gestor.guardar({1, 2}))

    os.remove(gestor.ruta)
    os.rmdir("prueba_temp")
