# funciones de ayuda para la consola: colores, títulos y mensajes
import os

# códigos ANSI para pintar el texto en la terminal
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# respuestas que cuentan como un sí
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


# cls en Windows, clear en Linux y Mac
def limpiar_pantalla():
    os.system("clear" if os.name == "posix" else "cls")


# si el color no existe usa blanco
def imprimir_color(texto, color):
    codigo = COLORES.get(color, COLORES["BLANCO"])
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    imprimir_color(f"ℹ {mensaje}", "CYAN")


# True si responde que sí, False con cualquier otra cosa
def confirmar(pregunta):
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


# prueba rápida de las funciones
if __name__ == "__main__":
    imprimir_titulo("PRUEBA DE HERRAMIENTAS")
    imprimir_color("Texto en amarillo", "AMARILLO")
    imprimir_color("Color inexistente", "ROSA")
    imprimir_exito("Operación correcta")
    imprimir_error("Algo salió mal")
    imprimir_info("Esto es información")
    if confirmar("¿Te gustó la prueba?"):
        imprimir_exito("¡Genial!")
    else:
        imprimir_info("Ok, seguiremos mejorando")
