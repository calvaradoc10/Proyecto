import json  # Módulo para leer y escribir archivos JSON
import os  # Módulo para trabajar con carpetas y rutas


class GestorJSON:  # Clase que maneja un archivo JSON
    """Lee y guarda una lista de diccionarios. Es la única parte que toca el disco."""

    def __init__(self, ruta):  # Constructor: se ejecuta al crear el objeto
        self.__ruta = ruta  # Guarda la ruta como atributo privado (__)

        carpeta = os.path.dirname(ruta)  # Saca la carpeta de la ruta
        if carpeta and not os.path.exists(carpeta):  # Si hay carpeta y no existe...
            os.makedirs(carpeta)  # ...la crea

    @property  # Permite leer la ruta como atributo: gestor.ruta
    def ruta(self):  # Getter de la ruta
        return self.__ruta  # Devuelve la ruta privada

    def leer(self):  # Lee el archivo y devuelve una lista
        if not os.path.exists(self.__ruta):  # Si el archivo no existe...
            return []  # ...devuelve lista vacía

        try:  # Intenta leer (puede fallar)
            with open(self.__ruta, "r", encoding="utf-8") as archivo:  # Abre en modo lectura
                datos = json.load(archivo)  # Convierte el JSON a datos de Python

            return datos if isinstance(datos, list) else []  # Solo acepta listas

        except (json.JSONDecodeError, OSError):  # Si el JSON está mal o hay error al abrir
            return []  # Devuelve lista vacía

    def guardar(self, datos):  # Guarda los datos en el archivo
        try:  # Intenta guardar (puede fallar)
            with open(self.__ruta, "w", encoding="utf-8") as archivo:  # Abre en modo escritura
                json.dump(  # Convierte los datos a JSON y los escribe
                    datos,  # Lo que se va a guardar
                    archivo,  # Dónde se guarda
                    ensure_ascii=False,  # Permite tildes y ñ tal cual
                    indent=2  # Deja el JSON ordenado con sangría
                )

            return True  # Se guardó bien

        except (TypeError, OSError):  # Si el dato no se puede guardar o hay error de disco
            return False  # No se pudo guardar


if __name__ == "__main__":  # Solo se ejecuta si corres este archivo directamente
    gestor = GestorJSON("prueba_temp/estudiantes.json")  # Crea el gestor (y la carpeta)
    print("Ruta:", gestor.ruta)  # Muestra la ruta usando la property

    print("Leer sin archivo:", gestor.leer())  # Aún no existe -> []

    estudiantes = [  # Lista de diccionarios de prueba
        {"nombre": "Ana", "edad": 20},  # Estudiante 1
        {"nombre": "José", "edad": 22},  # Estudiante 2
    ]
    print("Guardar:", gestor.guardar(estudiantes))  # Guarda -> True
    print("Leer:", gestor.leer())  # Lee lo guardado

    print("Guardar dato inválido:", gestor.guardar({1, 2}))  # Un set no es JSON -> False

    os.remove(gestor.ruta)  # Borra el archivo de prueba
    os.rmdir("prueba_temp")  # Borra la carpeta de prueba
