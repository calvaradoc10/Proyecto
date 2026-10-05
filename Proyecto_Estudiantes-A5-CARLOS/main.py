from shared.herramientas import (  # Importa funciones de ayuda para la consola
    imprimir_titulo,  # Limpia pantalla y muestra un título
    imprimir_exito,  # Mensaje verde
    imprimir_error,  # Mensaje rojo
    imprimir_info,  # Mensaje cyan
    confirmar  # Pregunta si/no
)

from views import ClienteController, EstudianteController  # Importa los controladores (hacen el CRUD)


class MenuClientes:  # Clase del menú de clientes
    """VISTA: muestra información y recoge datos del usuario."""

    TITULO = "SISTEMA DE GESTIÓN DE CLIENTES"  # Título del menú
    ANCHO = 100  # Ancho de las líneas de la tabla

    def __init__(self, controlador=ClienteController):  # Constructor; por defecto usa clientes
        self._controlador = controlador  # Guarda el controlador a usar
        self._activo = True  # Mientras sea True, el menú sigue

        self._opciones = {  # Diccionario: tecla -> (texto, método)
            "1": ("Crear", self.crear),  # Opción 1
            "2": ("Ver todos", self.listar),  # Opción 2
            "3": ("Buscar", self.buscar),  # Opción 3
            "4": ("Ver por ID", self.ver_por_id),  # Opción 4
            "5": ("Actualizar", self.actualizar),  # Opción 5
            "6": ("Eliminar", self.eliminar),  # Opción 6
            "7": ("Estadísticas", self.estadisticas),  # Opción 7
            "0": ("Salir", self.salir),  # Opción 0
        }

    # =====================================================
    # MÉTODOS ESTÁTICOS DE APOYO
    # =====================================================

    @staticmethod  # No necesita "self"
    def pausa():  # Espera a que el usuario presione Enter
        input("\nPresione Enter para continuar...")  # Pausa el programa

    @staticmethod  # No necesita "self"
    def pedir_entero(etiqueta):  # Pide un número entero
        try:  # Intenta convertir
            return int(input(etiqueta))  # Lee y convierte a entero
        except ValueError:  # Si no era un número...
            return None  # ...devuelve None

    @staticmethod  # No necesita "self"
    def mostrar_resultado(exito, mensaje):  # Muestra éxito o error
        if exito:  # Si salió bien
            imprimir_exito(mensaje)  # Mensaje verde
        else:  # Si salió mal
            imprimir_error(mensaje)  # Mensaje rojo

    # =====================================================
    # MOSTRAR TABLA
    # =====================================================

    def mostrar_tabla(self, clientes):  # Imprime una lista en forma de tabla

        print(  # Imprime los encabezados
            f"{'ID':<5}"  # "<5" = alinear a la izquierda en 5 espacios
            f"{'NOMBRE':<25}"
            f"{'EMAIL':<30}"
            f"{'CIUDAD':<20}"
            f"{'TELÉFONO':<15}"
        )

        print("-" * self.ANCHO)  # Línea separadora

        for cliente in clientes:  # Recorre cada cliente

            print(  # Imprime una fila con sus datos
                f"{cliente.id:<5}"
                f"{cliente.nombre_completo:<25}"
                f"{cliente.email:<30}"
                f"{cliente.ciudad:<20}"
                f"{cliente.telefono:<15}"
            )

        print("-" * self.ANCHO)  # Línea separadora final

        imprimir_info(  # Muestra cuántos hay
            f"Total: {len(clientes)} registro(s)"  # len() cuenta elementos
        )

    # =====================================================
    # CREAR
    # =====================================================

    def crear(self):  # Crea un registro nuevo

        imprimir_titulo("CREAR NUEVO REGISTRO")  # Título

        datos = {}  # Diccionario vacío para los datos

        for campo in self._controlador.MODELO.CAMPOS:  # Recorre los campos del modelo

            datos[campo] = input(  # Pide cada campo y lo guarda
                f"{campo.capitalize()}: "  # Ej: "Nombre: "
            )

        exito, mensaje = self._controlador.crear(  # Pide al controlador crear
            datos  # Le pasa los datos
        )

        self.mostrar_resultado(  # Muestra si funcionó
            exito,
            mensaje
        )

        self.pausa()  # Espera Enter

    # =====================================================
    # LISTAR
    # =====================================================

    def listar(self):  # Muestra todos los registros

        imprimir_titulo("LISTA DE REGISTROS")  # Título

        registros = self._controlador.listar()  # Obtiene la lista

        if not registros:  # Si está vacía

            imprimir_info(  # Avisa
                "Todavía no existen registros."
            )

        else:  # Si hay registros

            self.mostrar_tabla(  # Los muestra en tabla
                registros
            )

        self.pausa()  # Espera Enter

    # =====================================================
    # BUSCAR
    # =====================================================

    def buscar(self):  # Busca registros por texto

        imprimir_titulo("BUSCAR REGISTRO")  # Título

        termino = input(  # Pide qué buscar
            "Ingrese el término de búsqueda: "
        )

        encontrados = self._controlador.buscar(  # Busca coincidencias
            termino
        )

        if not encontrados:  # Si no encontró nada

            imprimir_info(  # Avisa
                f"No se encontraron coincidencias "
                f"para '{termino}'."
            )

        else:  # Si encontró

            self.mostrar_tabla(  # Muestra resultados
                encontrados
            )

        self.pausa()  # Espera Enter

    # =====================================================
    # VER POR ID
    # =====================================================

    def ver_por_id(self):  # Muestra un registro según su ID

        imprimir_titulo("VER REGISTRO POR ID")  # Título

        id_registro = self.pedir_entero(  # Pide el ID
            "ID: "
        )

        if id_registro is None:  # Si no escribió un número

            imprimir_error(  # Muestra error
                "El ID debe ser un número entero"
            )

            return self.pausa()  # Pausa y sale del método

        objeto = self._controlador.obtener(  # Busca el registro
            id_registro
        )

        if objeto is None:  # Si no existe

            imprimir_error(  # Muestra error
                f"No existe un registro "
                f"con ID {id_registro}"
            )

        else:  # Si existe

            for clave, valor in (  # Recorre cada dato (clave: valor)
                objeto.a_diccionario().items()  # Convierte el objeto a diccionario
            ):

                print(  # Imprime cada dato
                    f"{clave.capitalize():<15}: "
                    f"{valor}"
                )

        self.pausa()  # Espera Enter

    # =====================================================
    # ACTUALIZAR
    # =====================================================

    def actualizar(self):  # Modifica un registro

        imprimir_titulo("ACTUALIZAR REGISTRO")  # Título

        id_registro = self.pedir_entero(  # Pide el ID
            "ID del registro: "
        )

        if id_registro is None:  # Si no es número

            imprimir_error(  # Error
                "El ID debe ser un número entero"
            )

            return self.pausa()  # Pausa y sale

        objeto = self._controlador.obtener(  # Busca el registro
            id_registro
        )

        if objeto is None:  # Si no existe

            imprimir_error(  # Error
                f"No existe un registro "
                f"con ID {id_registro}"
            )

            return self.pausa()  # Pausa y sale

        imprimir_info(  # Muestra a quién edita
            f"Editando a "
            f"{objeto.nombre_completo}"
        )

        print(  # Instrucción para el usuario
            "\nDeje vacío el campo "
            "que no quiera modificar.\n"
        )

        cambios = {}  # Aquí se guardan solo los cambios

        for campo in self._controlador.MODELO.CAMPOS:  # Recorre cada campo

            actual = getattr(  # Obtiene el valor actual del campo
                objeto,
                campo
            )

            nuevo = input(  # Pide el valor nuevo
                f"{campo.capitalize()} "
                f"[{actual}]: "  # Muestra el actual entre []
            ).strip()  # Quita espacios

            if nuevo:  # Si escribió algo

                cambios[campo] = nuevo  # Lo guarda como cambio

        resultado = self._controlador.actualizar(  # Aplica los cambios
            id_registro,
            cambios
        )

        self.mostrar_resultado(  # Muestra resultado
            *resultado  # "*" separa la tupla en (exito, mensaje)
        )

        self.pausa()  # Espera Enter

    # =====================================================
    # ELIMINAR
    # =====================================================

    def eliminar(self):  # Borra un registro

        imprimir_titulo("ELIMINAR REGISTRO")  # Título

        id_registro = self.pedir_entero(  # Pide el ID
            "ID del registro: "
        )

        if id_registro is None:  # Si no es número

            imprimir_error(  # Error
                "El ID debe ser un número entero"
            )

            return self.pausa()  # Pausa y sale

        objeto = self._controlador.obtener(  # Busca el registro
            id_registro
        )

        if objeto is None:  # Si no existe

            imprimir_error(  # Error
                f"No existe un registro "
                f"con ID {id_registro}"
            )

            return self.pausa()  # Pausa y sale

        imprimir_info(  # Muestra qué se borrará
            f"Se eliminará: {objeto}"
        )

        if confirmar(  # Pide confirmación
            "¿Confirma la eliminación?"
        ):

            resultado = (  # Si dijo que sí, elimina
                self._controlador.eliminar(
                    id_registro
                )
            )

            self.mostrar_resultado(  # Muestra resultado
                *resultado
            )

        else:  # Si dijo que no

            imprimir_info(  # Avisa que se canceló
                "Operación cancelada"
            )

        self.pausa()  # Espera Enter

    # =====================================================
    # ESTADÍSTICAS DE CLIENTES
    # =====================================================

    def estadisticas(self):  # Muestra estadísticas

        imprimir_titulo("ESTADÍSTICAS")  # Título

        datos = self._controlador.estadisticas()  # Pide los datos al controlador

        print(  # Muestra el total
            f"Total de registros: "
            f"{datos['total']}"
        )

        self.pausa()  # Espera Enter

    # =====================================================
    # SALIR
    # =====================================================

    def salir(self):  # Termina el programa

        self._activo = False  # Esto detiene el bucle while

        imprimir_info(  # Mensaje de despedida
            "Programa finalizado."
        )

    # =====================================================
    # MOSTRAR MENÚ
    # =====================================================

    def mostrar_menu(self):  # Dibuja el menú

        imprimir_titulo(  # Título del menú
            self.TITULO
        )

        for tecla, (  # Recorre cada opción
            texto,  # Texto de la opción
            _metodo  # "_" = no se usa aquí
        ) in self._opciones.items():

            print(  # Imprime la opción
                f"  {tecla}. {texto}"
            )

        print()  # Línea en blanco

    # =====================================================
    # EJECUTAR
    # =====================================================

    def ejecutar(self):  # Bucle principal del menú

        while self._activo:  # Repite hasta elegir Salir

            self.mostrar_menu()  # Muestra el menú

            tecla = input(  # Pide la opción
                "Seleccione una opción: "
            ).strip()  # Quita espacios

            if tecla not in self._opciones:  # Si la opción no existe

                imprimir_error(  # Error
                    "Opción no válida"
                )

                self.pausa()  # Espera Enter

                continue  # Vuelve al inicio del while

            _texto, metodo = (  # Saca el método de la opción
                self._opciones[tecla]
            )

            metodo()  # Ejecuta el método elegido


# =========================================================
# MENÚ DE ESTUDIANTES
# =========================================================

class MenuEstudiantes(MenuClientes):  # Hereda todo de MenuClientes

    TITULO = "SISTEMA DE GESTIÓN DE ESTUDIANTES"  # Cambia el título
    ANCHO = 115  # Tabla más ancha

    def __init__(self):  # Constructor

        super().__init__(  # Llama al constructor del padre
            EstudianteController  # Usa el controlador de estudiantes
        )

        self._opciones = {  # Reemplaza las opciones con más opciones
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
            "8": (  # Opción nueva
                "Agregar nota",
                self.agregar_nota
            ),
            "9": (  # Opción nueva
                "Ver promedio",
                self.ver_promedio
            ),
            "10": (  # Opción nueva
                "Materias en común",
                self.ver_materias_en_comun
            ),
            "0": (
                "Salir",
                self.salir
            ),
        }

    # =====================================================
    # TABLA DE ESTUDIANTES
    # =====================================================

    def mostrar_tabla(self, estudiantes):  # Sobrescribe la tabla del padre

        print(  # Encabezados
            f"{'ID':<5}"
            f"{'CARNET':<15}"
            f"{'NOMBRE':<25}"
            f"{'EMAIL':<30}"
            f"{'PROMEDIO':<15}"
            f"{'ESTADO':<15}"
        )

        print("-" * self.ANCHO)  # Separador

        for estudiante in estudiantes:  # Recorre cada estudiante

            print(  # Imprime su fila
                f"{estudiante.id:<5}"
                f"{estudiante.carnet:<15}"
                f"{estudiante.nombre_completo:<25}"
                f"{estudiante.email:<30}"
                f"{estudiante.promedio:<15}"
                f"{estudiante.estado:<15}"
            )

        print("-" * self.ANCHO)  # Separador final

        imprimir_info(  # Total de estudiantes
            f"Total: "
            f"{len(estudiantes)} estudiante(s)"
        )

    # =====================================================
    # VER ESTUDIANTE
    # =====================================================

    def ver_por_id(self):  # Sobrescribe ver_por_id del padre

        imprimir_titulo(  # Título
            "DATOS DEL ESTUDIANTE"
        )

        id_estudiante = self.pedir_entero(  # Pide el ID
            "ID del estudiante: "
        )

        if id_estudiante is None:  # Si no es número

            imprimir_error(  # Error
                "El ID debe ser un número entero"
            )

            return self.pausa()  # Pausa y sale

        estudiante = (  # Busca el estudiante
            self._controlador.obtener(
                id_estudiante
            )
        )

        if estudiante is None:  # Si no existe

            imprimir_error(  # Error
                f"No existe un estudiante "
                f"con ID {id_estudiante}"
            )

        else:  # Si existe

            datos = (  # Lo convierte a diccionario
                estudiante.a_diccionario()
            )

            print(  # ID
                f"ID        : "
                f"{estudiante.id}"
            )

            print(  # Nombre
                f"Nombre    : "
                f"{estudiante.nombre_completo}"
            )

            print(  # Email
                f"Email     : "
                f"{estudiante.email}"
            )

            print(  # Carnet
                f"Carnet    : "
                f"{estudiante.carnet}"
            )

            materias = datos["materias"]  # Lista de materias

            if materias:  # Si tiene materias

                print(  # Las une con comas
                    f"Materias  : "
                    f"{', '.join(materias)}"
                )

            else:  # Si no tiene

                print(  # Avisa
                    "Materias  : "
                    "Sin materias registradas"
                )

            print(  # Notas
                f"Notas     : "
                f"{datos['notas']}"
            )

            print(  # Promedio
                f"Promedio  : "
                f"{estudiante.promedio}"
            )

            print(  # Aprobado / Reprobado
                f"Estado    : "
                f"{estudiante.estado}"
            )

        self.pausa()  # Espera Enter

    # =====================================================
    # AGREGAR NOTA
    # =====================================================

    def agregar_nota(self):  # Agrega una nota a un estudiante

        imprimir_titulo(  # Título
            "AGREGAR NOTA"
        )

        id_estudiante = self.pedir_entero(  # Pide el ID
            "ID del estudiante: "
        )

        if id_estudiante is None:  # Si no es número

            imprimir_error(  # Error
                "El ID debe ser un número entero"
            )

            return self.pausa()  # Pausa y sale

        materia = input(  # Pide la materia
            "Materia: "
        ).strip()  # Quita espacios

        try:  # Intenta convertir la nota

            nota = float(  # float = número con decimales
                input("Nota (0 a 20): ")
            )

        except ValueError:  # Si no es número

            imprimir_error(  # Error
                "La nota debe ser un número"
            )

            return self.pausa()  # Pausa y sale

        resultado = (  # Pide al controlador guardar la nota
            self._controlador.agregar_nota(
                id_estudiante,
                materia,
                nota
            )
        )

        self.mostrar_resultado(  # Muestra resultado
            *resultado
        )

        self.pausa()  # Espera Enter

    # =====================================================
    # VER PROMEDIO
    # =====================================================

    def ver_promedio(self):  # Muestra el promedio de un estudiante

        imprimir_titulo(  # Título
            "PROMEDIO DEL ESTUDIANTE"
        )

        id_estudiante = self.pedir_entero(  # Pide el ID
            "ID del estudiante: "
        )

        if id_estudiante is None:  # Si no es número

            imprimir_error(  # Error
                "El ID debe ser un número entero"
            )

            return self.pausa()  # Pausa y sale

        estudiante = (  # Busca el estudiante
            self._controlador.obtener(
                id_estudiante
            )
        )

        if estudiante is None:  # Si no existe

            imprimir_error(  # Error
                f"No existe un estudiante "
                f"con ID {id_estudiante}"
            )

        else:  # Si existe

            print(  # Nombre
                f"Estudiante : "
                f"{estudiante.nombre_completo}"
            )

            print(  # Carnet
                f"Carnet     : "
                f"{estudiante.carnet}"
            )

            print(  # Promedio
                f"Promedio   : "
                f"{estudiante.promedio}"
            )

            print(  # Estado
                f"Estado     : "
                f"{estudiante.estado}"
            )

        self.pausa()  # Espera Enter

    # =====================================================
    # MATERIAS EN COMÚN
    # =====================================================

    def ver_materias_en_comun(self):  # Compara materias de 2 estudiantes

        imprimir_titulo(  # Título
            "MATERIAS EN COMÚN"
        )

        id_a = self.pedir_entero(  # ID del primero
            "ID del primer estudiante: "
        )

        id_b = self.pedir_entero(  # ID del segundo
            "ID del segundo estudiante: "
        )

        if id_a is None or id_b is None:  # Si alguno no es número

            imprimir_error(  # Error
                "Los ID deben ser números enteros"
            )

            return self.pausa()  # Pausa y sale

        materias = (  # Pide las materias en común
            self._controlador.materias_en_comun(
                id_a,
                id_b
            )
        )

        if materias is None:  # None = algún estudiante no existe

            imprimir_error(  # Error
                "Uno o ambos estudiantes "
                "no existen"
            )

        elif not materias:  # Conjunto vacío = nada en común

            imprimir_info(  # Avisa
                "Los estudiantes no tienen "
                "materias en común"
            )

        else:  # Sí hay materias en común

            imprimir_exito(  # Las muestra ordenadas
                "Materias en común: "
                + ", ".join(  # Une con comas
                    sorted(materias)  # Ordena alfabéticamente
                )
            )

        self.pausa()  # Espera Enter

    # =====================================================
    # ESTADÍSTICAS DE ESTUDIANTES
    # =====================================================

    def estadisticas(self):  # Sobrescribe estadísticas del padre

        imprimir_titulo(  # Título
            "ESTADÍSTICAS DE ESTUDIANTES"
        )

        datos = (  # Pide las estadísticas
            self._controlador.estadisticas()
        )

        print(  # Total
            f"Estudiantes registrados : "
            f"{datos['total']}"
        )

        print(  # Aprobados
            f"Aprobados                : "
            f"{datos['aprobados']}"
        )

        print(  # Reprobados
            f"Reprobados               : "
            f"{datos['reprobados']}"
        )

        materias = datos["materias"]  # Lista de materias

        if materias:  # Si hay materias

            print(  # Las muestra
                f"Materias ofertadas        : "
                f"{', '.join(materias)}"
            )

        else:  # Si no hay

            print(  # Avisa
                "Materias ofertadas        : "
                "Ninguna"
            )

        self.pausa()  # Espera Enter


# =========================================================
# INICIO DEL PROGRAMA
# =========================================================

if __name__ == "__main__":  # Solo se ejecuta si corres este archivo directamente

    try:  # Intenta correr el programa

        MenuEstudiantes().ejecutar()  # Crea el menú y lo arranca

    except KeyboardInterrupt:  # Si el usuario presiona Ctrl+C

        print(  # Mensaje de salida
            "\nPrograma interrumpido "
            "por el usuario."
        )
