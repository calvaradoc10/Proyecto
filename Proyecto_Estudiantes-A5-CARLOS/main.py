from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)

from views import ClienteController, EstudianteController


class MenuClientes:
    """Menú de consola para clientes: pide los datos y muestra los resultados."""

    # el menú de estudiantes cambia el título y el ancho de la tabla
    TITULO = "SISTEMA DE GESTIÓN DE CLIENTES"
    ANCHO = 100

    def __init__(self, controlador=ClienteController):
        self._controlador = controlador
        self._activo = True

        # opción -> (texto, método), así el menú se arma solo
        self._opciones = {
            "1": ("Crear", self.crear),
            "2": ("Ver todos", self.listar),
            "3": ("Buscar", self.buscar),
            "4": ("Ver por ID", self.ver_por_id),
            "5": ("Actualizar", self.actualizar),
            "6": ("Eliminar", self.eliminar),
            "7": ("Estadísticas", self.estadisticas),
            "0": ("Salir", self.salir),
        }


    # para que alcance a leer antes de volver al menú
    @staticmethod
    def pausa():
        input("\nPresione Enter para continuar...")

    # devuelve None si lo escrito no es un número entero
    @staticmethod
    def pedir_entero(etiqueta):
        try:
            return int(input(etiqueta))
        except ValueError:
            return None

    # muestra el mensaje en verde o en rojo según cómo salió
    @staticmethod
    def mostrar_resultado(exito, mensaje):
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)


    # imprime los clientes en forma de tabla
    def mostrar_tabla(self, clientes):

        print(
            f"{'ID':<5}"
            f"{'NOMBRE':<25}"
            f"{'EMAIL':<30}"
            f"{'CIUDAD':<20}"
            f"{'TELÉFONO':<15}"
        )

        print("-" * self.ANCHO)

        for cliente in clientes:

            print(
                f"{cliente.id:<5}"
                f"{cliente.nombre_completo:<25}"
                f"{cliente.email:<30}"
                f"{cliente.ciudad:<20}"
                f"{cliente.telefono:<15}"
            )

        print("-" * self.ANCHO)

        imprimir_info(
            f"Total: {len(clientes)} registro(s)"
        )


    def crear(self):

        imprimir_titulo("CREAR NUEVO REGISTRO")

        datos = {}

        # pide un dato por cada campo del modelo
        for campo in self._controlador.MODELO.CAMPOS:

            datos[campo] = input(
                f"{campo.capitalize()}: "
            )

        exito, mensaje = self._controlador.crear(
            datos
        )

        self.mostrar_resultado(
            exito,
            mensaje
        )

        self.pausa()


    def listar(self):

        imprimir_titulo("LISTA DE REGISTROS")

        registros = self._controlador.listar()

        if not registros:

            imprimir_info(
                "Todavía no existen registros."
            )

        else:

            self.mostrar_tabla(
                registros
            )

        self.pausa()


    def buscar(self):

        imprimir_titulo("BUSCAR REGISTRO")

        termino = input(
            "Ingrese el término de búsqueda: "
        )

        encontrados = self._controlador.buscar(
            termino
        )

        if not encontrados:

            imprimir_info(
                f"No se encontraron coincidencias "
                f"para '{termino}'."
            )

        else:

            self.mostrar_tabla(
                encontrados
            )

        self.pausa()


    def ver_por_id(self):

        imprimir_titulo("VER REGISTRO POR ID")

        id_registro = self.pedir_entero(
            "ID: "
        )

        # si no es un entero avisa y vuelve al menú
        if id_registro is None:

            imprimir_error(
                "El ID debe ser un número entero"
            )

            return self.pausa()

        objeto = self._controlador.obtener(
            id_registro
        )

        if objeto is None:

            imprimir_error(
                f"No existe un registro "
                f"con ID {id_registro}"
            )

        else:

            for clave, valor in (
                objeto.a_diccionario().items()
            ):

                print(
                    f"{clave.capitalize():<15}: "
                    f"{valor}"
                )

        self.pausa()


    def actualizar(self):

        imprimir_titulo("ACTUALIZAR REGISTRO")

        id_registro = self.pedir_entero(
            "ID del registro: "
        )

        if id_registro is None:

            imprimir_error(
                "El ID debe ser un número entero"
            )

            return self.pausa()

        objeto = self._controlador.obtener(
            id_registro
        )

        if objeto is None:

            imprimir_error(
                f"No existe un registro "
                f"con ID {id_registro}"
            )

            return self.pausa()

        imprimir_info(
            f"Editando a "
            f"{objeto.nombre_completo}"
        )

        print(
            "\nDeje vacío el campo "
            "que no quiera modificar.\n"
        )

        # lo que se deje vacío no se modifica
        cambios = {}

        for campo in self._controlador.MODELO.CAMPOS:

            actual = getattr(
                objeto,
                campo
            )

            nuevo = input(
                f"{campo.capitalize()} "
                f"[{actual}]: "
            ).strip()

            # solo guarda los campos que sí escribió
            if nuevo:

                cambios[campo] = nuevo

        resultado = self._controlador.actualizar(
            id_registro,
            cambios
        )

        self.mostrar_resultado(
            *resultado
        )

        self.pausa()


    def eliminar(self):

        imprimir_titulo("ELIMINAR REGISTRO")

        id_registro = self.pedir_entero(
            "ID del registro: "
        )

        if id_registro is None:

            imprimir_error(
                "El ID debe ser un número entero"
            )

            return self.pausa()

        objeto = self._controlador.obtener(
            id_registro
        )

        if objeto is None:

            imprimir_error(
                f"No existe un registro "
                f"con ID {id_registro}"
            )

            return self.pausa()

        imprimir_info(
            f"Se eliminará: {objeto}"
        )

        # antes de borrar pide confirmación
        if confirmar(
            "¿Confirma la eliminación?"
        ):

            resultado = (
                self._controlador.eliminar(
                    id_registro
                )
            )

            self.mostrar_resultado(
                *resultado
            )

        else:

            imprimir_info(
                "Operación cancelada"
            )

        self.pausa()


    def estadisticas(self):

        imprimir_titulo("ESTADÍSTICAS")

        datos = self._controlador.estadisticas()

        print(
            f"Total de registros: "
            f"{datos['total']}"
        )

        self.pausa()


    # apaga el bucle principal
    def salir(self):

        self._activo = False

        imprimir_info(
            "Programa finalizado."
        )


    def mostrar_menu(self):

        imprimir_titulo(
            self.TITULO
        )

        for tecla, (
            texto,
            _metodo
        ) in self._opciones.items():

            print(
                f"  {tecla}. {texto}"
            )

        print()


    # bucle principal: muestra el menú y ejecuta la opción elegida
    def ejecutar(self):

        while self._activo:

            self.mostrar_menu()

            tecla = input(
                "Seleccione una opción: "
            ).strip()

            if tecla not in self._opciones:

                imprimir_error(
                    "Opción no válida"
                )

                self.pausa()

                continue

            # saca el método del diccionario y lo ejecuta
            _texto, metodo = (
                self._opciones[tecla]
            )

            metodo()



# hereda el menú de clientes y le suma las opciones de notas
class MenuEstudiantes(MenuClientes):

    TITULO = "SISTEMA DE GESTIÓN DE ESTUDIANTES"
    ANCHO = 115

    def __init__(self):

        # le pasa al padre el controlador de estudiantes
        super().__init__(
            EstudianteController
        )

        # opciones propias, incluyen notas, promedio y materias
        self._opciones = {
            "1": (
                "Crear estudiante",
                self.crear
            ),
            "2": (
                "Ver todos los estudiantes",
                self.listar
            ),
            "3": (
                "Buscar estudiante",
                self.buscar
            ),
            "4": (
                "Ver estudiante por ID",
                self.ver_por_id
            ),
            "5": (
                "Actualizar estudiante",
                self.actualizar
            ),
            "6": (
                "Eliminar estudiante",
                self.eliminar
            ),
            "7": (
                "Estadísticas",
                self.estadisticas
            ),
            "8": (
                "Agregar nota",
                self.agregar_nota
            ),
            "9": (
                "Ver promedio",
                self.ver_promedio
            ),
            "10": (
                "Materias en común",
                self.ver_materias_en_comun
            ),
            "0": (
                "Salir",
                self.salir
            ),
        }


    # esta tabla muestra carnet, promedio y estado
    def mostrar_tabla(self, estudiantes):

        print(
            f"{'ID':<5}"
            f"{'CARNET':<15}"
            f"{'NOMBRE':<25}"
            f"{'EMAIL':<30}"
            f"{'PROMEDIO':<15}"
            f"{'ESTADO':<15}"
        )

        print("-" * self.ANCHO)

        for estudiante in estudiantes:

            print(
                f"{estudiante.id:<5}"
                f"{estudiante.carnet:<15}"
                f"{estudiante.nombre_completo:<25}"
                f"{estudiante.email:<30}"
                f"{estudiante.promedio:<15}"
                f"{estudiante.estado:<15}"
            )

        print("-" * self.ANCHO)

        imprimir_info(
            f"Total: "
            f"{len(estudiantes)} estudiante(s)"
        )


    def ver_por_id(self):

        imprimir_titulo(
            "DATOS DEL ESTUDIANTE"
        )

        id_estudiante = self.pedir_entero(
            "ID del estudiante: "
        )

        if id_estudiante is None:

            imprimir_error(
                "El ID debe ser un número entero"
            )

            return self.pausa()

        estudiante = (
            self._controlador.obtener(
                id_estudiante
            )
        )

        if estudiante is None:

            imprimir_error(
                f"No existe un estudiante "
                f"con ID {id_estudiante}"
            )

        else:

            datos = (
                estudiante.a_diccionario()
            )

            print(
                f"ID        : "
                f"{estudiante.id}"
            )

            print(
                f"Nombre    : "
                f"{estudiante.nombre_completo}"
            )

            print(
                f"Email     : "
                f"{estudiante.email}"
            )

            print(
                f"Carnet    : "
                f"{estudiante.carnet}"
            )

            materias = datos["materias"]

            if materias:

                print(
                    f"Materias  : "
                    f"{', '.join(materias)}"
                )

            else:

                print(
                    "Materias  : "
                    "Sin materias registradas"
                )

            print(
                f"Notas     : "
                f"{datos['notas']}"
            )

            print(
                f"Promedio  : "
                f"{estudiante.promedio}"
            )

            print(
                f"Estado    : "
                f"{estudiante.estado}"
            )

        self.pausa()


    def agregar_nota(self):

        imprimir_titulo(
            "AGREGAR NOTA"
        )

        id_estudiante = self.pedir_entero(
            "ID del estudiante: "
        )

        if id_estudiante is None:

            imprimir_error(
                "El ID debe ser un número entero"
            )

            return self.pausa()

        materia = input(
            "Materia: "
        ).strip()

        try:

            # float para aceptar notas con decimales
            nota = float(
                input("Nota (0 a 20): ")
            )

        except ValueError:

            imprimir_error(
                "La nota debe ser un número"
            )

            return self.pausa()

        resultado = (
            self._controlador.agregar_nota(
                id_estudiante,
                materia,
                nota
            )
        )

        self.mostrar_resultado(
            *resultado
        )

        self.pausa()


    def ver_promedio(self):

        imprimir_titulo(
            "PROMEDIO DEL ESTUDIANTE"
        )

        id_estudiante = self.pedir_entero(
            "ID del estudiante: "
        )

        if id_estudiante is None:

            imprimir_error(
                "El ID debe ser un número entero"
            )

            return self.pausa()

        estudiante = (
            self._controlador.obtener(
                id_estudiante
            )
        )

        if estudiante is None:

            imprimir_error(
                f"No existe un estudiante "
                f"con ID {id_estudiante}"
            )

        else:

            print(
                f"Estudiante : "
                f"{estudiante.nombre_completo}"
            )

            print(
                f"Carnet     : "
                f"{estudiante.carnet}"
            )

            print(
                f"Promedio   : "
                f"{estudiante.promedio}"
            )

            print(
                f"Estado     : "
                f"{estudiante.estado}"
            )

        self.pausa()


    def ver_materias_en_comun(self):

        imprimir_titulo(
            "MATERIAS EN COMÚN"
        )

        id_a = self.pedir_entero(
            "ID del primer estudiante: "
        )

        id_b = self.pedir_entero(
            "ID del segundo estudiante: "
        )

        if id_a is None or id_b is None:

            imprimir_error(
                "Los ID deben ser números enteros"
            )

            return self.pausa()

        materias = (
            self._controlador.materias_en_comun(
                id_a,
                id_b
            )
        )

        # None = uno de los dos no existe; vacío = no comparten materias
        if materias is None:

            imprimir_error(
                "Uno o ambos estudiantes "
                "no existen"
            )

        elif not materias:

            imprimir_info(
                "Los estudiantes no tienen "
                "materias en común"
            )

        else:

            imprimir_exito(
                "Materias en común: "
                + ", ".join(
                    sorted(materias)
                )
            )

        self.pausa()


    def estadisticas(self):

        imprimir_titulo(
            "ESTADÍSTICAS DE ESTUDIANTES"
        )

        datos = (
            self._controlador.estadisticas()
        )

        print(
            f"Estudiantes registrados : "
            f"{datos['total']}"
        )

        print(
            f"Aprobados                : "
            f"{datos['aprobados']}"
        )

        print(
            f"Reprobados               : "
            f"{datos['reprobados']}"
        )

        materias = datos["materias"]

        if materias:

            print(
                f"Materias ofertadas        : "
                f"{', '.join(materias)}"
            )

        else:

            print(
                "Materias ofertadas        : "
                "Ninguna"
            )

        self.pausa()



# punto de entrada del programa
if __name__ == "__main__":

    try:

        MenuEstudiantes().ejecutar()

    # por si lo cierran con Ctrl+C
    except KeyboardInterrupt:

        print(
            "\nPrograma interrumpido "
            "por el usuario."
        )
