import os  # Módulo para usar comandos del sistema operativo

# DICCIONARIO de colores de consola
COLORES = {  # Diccionario: nombre del color -> código de color
    "ROJO": "\033[91m",  # Código para texto rojo
    "VERDE": "\033[92m",  # Código para texto verde
    "AZUL": "\033[94m",  # Código para texto azul
    "AMARILLO": "\033[93m",  # Código para texto amarillo
    "CYAN": "\033[96m",  # Código para texto cyan
    "BLANCO": "\033[97m",  # Código para texto blanco
    "RESET": "\033[0m",  # Vuelve al color normal
}  # Fin del diccionario

# TUPLA: respuestas afirmativas aceptadas
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")  # Tupla (lista que no cambia)


def limpiar_pantalla():  # Define la función para limpiar la consola
    os.system("clear" if os.name == "posix" else "cls")  # "clear" en Linux/Mac, "cls" en Windows


def imprimir_color(texto, color):  # Imprime un texto con color
    codigo = COLORES.get(color, COLORES["BLANCO"])  # Busca el color; si no existe usa blanco
    print(f"{codigo}{texto}{COLORES['RESET']}")  # Imprime color + texto + reset


def imprimir_titulo(texto):  # Imprime un título decorado
    limpiar_pantalla()  # Limpia la pantalla primero
    imprimir_color("=" * 60, "AZUL")  # Línea de 60 "=" en azul
    print(f"  {texto}".center(60))  # Texto centrado en 60 espacios
    imprimir_color("=" * 60, "AZUL")  # Otra línea azul
    print()  # Línea en blanco


def imprimir_exito(mensaje):  # Muestra un mensaje de éxito
    imprimir_color(f"✓ {mensaje}", "VERDE")  # En verde con un check


def imprimir_error(mensaje):  # Muestra un mensaje de error
    imprimir_color(f"✗ {mensaje}", "ROJO")  # En rojo con una X


def imprimir_info(mensaje):  # Muestra un mensaje informativo
    imprimir_color(f"ℹ {mensaje}", "CYAN")  # En cyan con una "i"


def confirmar(pregunta):  # Pregunta algo y devuelve True o False
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()  # Lee, quita espacios y pasa a minúsculas
    return respuesta in RESPUESTAS_SI  # True si la respuesta está en la tupla


if __name__ == "__main__":  # Solo se ejecuta si corres este archivo directamente
    imprimir_titulo("PRUEBA DE HERRAMIENTAS")  # Limpia pantalla y muestra el título
    imprimir_color("Texto en amarillo", "AMARILLO")  # Prueba un color
    imprimir_color("Color inexistente", "ROSA")  # Color que no existe -> sale blanco
    imprimir_exito("Operación correcta")  # Prueba mensaje de éxito
    imprimir_error("Algo salió mal")  # Prueba mensaje de error
    imprimir_info("Esto es información")  # Prueba mensaje de info
    if confirmar("¿Te gustó la prueba?"):  # Pregunta al usuario
        imprimir_exito("¡Genial!")  # Si respondió que sí
    else:  # Si respondió otra cosa
        imprimir_info("Ok, seguiremos mejorando")  # Mensaje alternativo
