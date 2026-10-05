from models import Cliente, Estudiante
from shared.json_manager import GestorJSON


class ClienteController:
    """Controlador: hace el CRUD sobre el JSON. No imprime ni pide nada por consola."""

    # estas variables de clase son las que cambia el controlador hijo
    MODELO = Cliente
    ARCHIVO = "data/clientes.json"
    CAMPOS_BUSCABLES = (
        "nombre",
        "apellido",
        "email",
        "telefono",
        "ciudad"
    )

    # el gestor es el único que lee y escribe el archivo
    _gestor = GestorJSON(ARCHIVO)


    @classmethod
    def _registros(cls):
        """Lee todos los registros del archivo."""
        return cls._gestor.leer()

    @classmethod
    def emails_registrados(cls, excepto_id=None):
        """Emails que ya existen (al editar se puede excluir un id)."""
        return {
            registro["email"].lower()
            for registro in cls._registros()
            if registro["id"] != excepto_id
        }

    @classmethod
    def siguiente_id(cls):
        """Siguiente id libre: el mayor que hay + 1."""
        ids = [
            registro["id"]
            for registro in cls._registros()
        ]

        return max(ids) + 1 if ids else 1

    @staticmethod
    def _coincide(registro, termino, campos):
        """True si el texto buscado está en alguno de los campos."""

        for campo in campos:

            if termino in str(
                registro.get(campo, "")
            ).lower():

                return True

        return False


    @classmethod
    def crear(cls, datos):
        """Valida y guarda un registro nuevo. Devuelve (éxito, mensaje)."""

        try:

            # revisa que no falte ningún campo obligatorio
            faltantes = [
                campo
                for campo in cls.MODELO.OBLIGATORIOS
                if not str(
                    datos.get(campo, "")
                ).strip()
            ]

            if faltantes:
                return (
                    False,
                    f"Faltan campos obligatorios: "
                    f"{', '.join(faltantes)}"
                )

            email = str(
                datos.get("email", "")
            ).strip().lower()

            # el email no se puede repetir
            if email in cls.emails_registrados():
                return (
                    False,
                    "Ese email ya está registrado"
                )

            # arma el objeto con los campos del modelo; si algo está mal, el modelo lanza ValueError
            valores = {
                campo: datos.get(campo, "")
                for campo in cls.MODELO.CAMPOS
            }

            objeto = cls.MODELO(
                cls.siguiente_id(),
                **valores
            )

            # se agrega al final de la lista y se guarda el archivo completo
            registros = cls._registros()

            registros.append(
                objeto.a_diccionario()
            )

            if not cls._gestor.guardar(registros):
                return (
                    False,
                    "No se pudo escribir el archivo"
                )

            return (
                True,
                f"{objeto.nombre_completo} "
                f"creado con id {objeto.id}"
            )

        # error de validación que viene del modelo
        except ValueError as error:
            return False, str(error)


    @classmethod
    def listar(cls):
        """Todos los registros convertidos a objetos."""

        return [
            cls.MODELO.desde_diccionario(registro)
            for registro in cls._registros()
        ]

    @classmethod
    def obtener(cls, id_registro):
        """Devuelve el objeto con ese id, o None si no existe."""

        for objeto in cls.listar():

            if objeto.id == id_registro:
                return objeto

        return None


    @classmethod
    def buscar(cls, termino):
        """Busca el texto en los campos permitidos para buscar."""

        termino = str(
            termino
        ).strip().lower()

        if not termino:
            return []

        return [
            cls.MODELO.desde_diccionario(registro)
            for registro in cls._registros()

            if cls._coincide(
                registro,
                termino,
                cls.CAMPOS_BUSCABLES
            )
        ]


    @classmethod
    def actualizar(cls, id_registro, cambios):
        """Cambia solo los campos indicados de un registro."""

        try:

            # no se aceptan campos que el modelo no tiene
            desconocidos = (
                set(cambios)
                - set(cls.MODELO.CAMPOS)
            )

            if desconocidos:
                return (
                    False,
                    f"Campos no válidos: "
                    f"{', '.join(sorted(desconocidos))}"
                )

            if not cambios:
                return (
                    False,
                    "No se indicó ningún cambio"
                )

            objeto = cls.obtener(id_registro)

            if objeto is None:
                return (
                    False,
                    f"No existe un registro "
                    f"con id {id_registro}"
                )

            # si cambia el email, que no lo esté usando otro registro
            if "email" in cambios:

                nuevo_email = str(
                    cambios["email"]
                ).strip().lower()

                if nuevo_email in cls.emails_registrados(
                    excepto_id=id_registro
                ):

                    return (
                        False,
                        "Ese email ya lo usa otro registro"
                    )

            # setattr pasa por los setters, así cada cambio se valida
            for campo, valor in cambios.items():

                setattr(
                    objeto,
                    campo,
                    valor
                )

            registros = cls._registros()

            # cambia el registro viejo por el actualizado
            for indice, registro in enumerate(registros):

                if registro["id"] == id_registro:

                    registros[indice] = (
                        objeto.a_diccionario()
                    )

                    break

            if not cls._gestor.guardar(registros):
                return (
                    False,
                    "No se pudo guardar la actualización"
                )

            return (
                True,
                f"Registro {id_registro} actualizado "
                f"({len(cambios)} campo/s)"
            )

        except ValueError as error:
            return False, str(error)


    @classmethod
    def eliminar(cls, id_registro):
        """Borra un registro por su id."""

        registros = cls._registros()

        # me quedo con todos menos el que se va a borrar
        quedan = [
            registro
            for registro in registros
            if registro["id"] != id_registro
        ]

        # si el tamaño no cambió, ese id no existía
        if len(quedan) == len(registros):
            return (
                False,
                f"No existe un registro "
                f"con id {id_registro}"
            )

        if not cls._gestor.guardar(quedan):
            return (
                False,
                "No se pudo guardar el archivo"
            )

        return (
            True,
            f"Registro {id_registro} eliminado"
        )


    @classmethod
    def estadisticas(cls):

        registros = cls._registros()

        # conjuntos para que no se repitan ciudades ni dominios
        ciudades = {
            registro.get("ciudad", "")
            for registro in registros
            if registro.get("ciudad")
        }

        dominios = {
            registro["email"].split("@")[1]
            for registro in registros
            if "@" in registro["email"]
        }

        sin_telefono = [
            registro["nombre"]
            for registro in registros
            if not registro.get("telefono")
        ]

        return {
            "total": len(registros),
            "ciudades": sorted(ciudades),
            "dominios": sorted(dominios),
            "sin_telefono": sin_telefono,
        }



class EstudianteController(ClienteController):
    """Controlador de estudiantes: reutiliza el CRUD del de clientes y suma lo de notas y materias."""

    # cambia el modelo y el archivo, el resto del CRUD se reutiliza
    MODELO = Estudiante

    ARCHIVO = "data/estudiantes.json"

    CAMPOS_BUSCABLES = (
        "nombre",
        "apellido",
        "email",
        "carnet"
    )

    _gestor = GestorJSON(ARCHIVO)


    @classmethod
    def carnets_registrados(cls, excepto_id=None):
        """Carnets ya usados, en mayúsculas."""

        return {
            registro["carnet"].upper()
            for registro in cls._registros()
            if registro["id"] != excepto_id
        }


    @classmethod
    def crear(cls, datos):

        carnet = str(
            datos.get("carnet", "")
        ).strip().upper()

        # reviso el carnet aquí y dejo que el padre valide lo demás
        if carnet in cls.carnets_registrados():

            return (
                False,
                "Ese carnet ya está registrado"
            )

        return super().crear(datos)


    @classmethod
    def actualizar(cls, id_registro, cambios):

        # el carnet tampoco se puede repetir
        if "carnet" in cambios:

            nuevo_carnet = str(
                cambios["carnet"]
            ).strip().upper()

            if nuevo_carnet in cls.carnets_registrados(
                excepto_id=id_registro
            ):

                return (
                    False,
                    "Ese carnet ya lo usa otro estudiante"
                )

        return super().actualizar(
            id_registro,
            cambios
        )


    @classmethod
    def agregar_nota(
        cls,
        id_estudiante,
        materia,
        nota
    ):

        estudiante = cls.obtener(
            id_estudiante
        )

        if estudiante is None:

            return (
                False,
                f"No existe un estudiante "
                f"con id {id_estudiante}"
            )

        try:

            estudiante.agregar_nota(
                materia,
                nota
            )

            registros = cls._registros()

            # guarda al estudiante con la nota ya agregada
            for indice, registro in enumerate(registros):

                if registro["id"] == id_estudiante:

                    registros[indice] = (
                        estudiante.a_diccionario()
                    )

                    break

            if not cls._gestor.guardar(registros):

                return (
                    False,
                    "No se pudo guardar la nota"
                )

            return (
                True,
                f"Nota {nota} agregada en "
                f"{materia}"
            )

        except ValueError as error:

            return (
                False,
                str(error)
            )


    @classmethod
    def materias_ofertadas(cls):
        """Todas las materias de los estudiantes, sin repetir."""

        materias = set()

        for estudiante in cls.listar():

            materias.update(
                estudiante.materias
            )

        return materias


    # devuelve None si alguno de los dos estudiantes no existe
    @classmethod
    def materias_en_comun(
        cls,
        id_a,
        id_b
    ):

        estudiante_a = cls.obtener(id_a)
        estudiante_b = cls.obtener(id_b)

        if estudiante_a is None:
            return None

        if estudiante_b is None:
            return None

        return estudiante_a.materias_en_comun(
            estudiante_b
        )


    @classmethod
    def estadisticas(cls):

        estudiantes = cls.listar()

        # cuenta cuántos hay en cada estado
        aprobados = [
            estudiante
            for estudiante in estudiantes
            if estudiante.estado == "Aprobado"
        ]

        reprobados = [
            estudiante
            for estudiante in estudiantes
            if estudiante.estado == "Reprobado"
        ]

        return {
            "total": len(estudiantes),
            "aprobados": len(aprobados),
            "reprobados": len(reprobados),
            "materias": sorted(
                cls.materias_ofertadas()
            ),
        }


# pruebas rápidas con una carpeta temporal para no tocar los datos reales
if __name__ == "__main__":
    import shutil

    ClienteController._gestor = GestorJSON("prueba_temp/clientes.json")
    EstudianteController._gestor = GestorJSON("prueba_temp/estudiantes.json")

    print("===== CLIENTES =====")
    print(ClienteController.crear({"nombre": "ana", "apellido": "lopez", "email": "ana@mail.com",
                                   "telefono": "555", "ciudad": "lima"}))
    print(ClienteController.crear({"nombre": "luis", "apellido": "ruiz", "email": "luis@gmail.com"}))
    print(ClienteController.crear({"nombre": "otra", "apellido": "x", "email": "ana@mail.com"}))
    print(ClienteController.crear({"nombre": "", "apellido": "x", "email": "x@mail.com"}))
    print("Emails:", ClienteController.emails_registrados())
    print("Siguiente ID:", ClienteController.siguiente_id())
    print("Listar:", [str(c) for c in ClienteController.listar()])
    print("Obtener 1:", ClienteController.obtener(1))
    print("Buscar 'lima':", [str(c) for c in ClienteController.buscar("lima")])
    print(ClienteController.actualizar(2, {"ciudad": "cusco"}))
    print(ClienteController.actualizar(2, {"edad": 5}))
    print("Estadísticas:", ClienteController.estadisticas())
    print(ClienteController.eliminar(2))
    print(ClienteController.eliminar(99))

    print("\n===== ESTUDIANTES =====")
    print(EstudianteController.crear({"nombre": "juan", "apellido": "perez",
                                      "email": "juan@mail.com", "carnet": "a001"}))
    print(EstudianteController.crear({"nombre": "maria", "apellido": "diaz",
                                      "email": "maria@mail.com", "carnet": "b002"}))
    print(EstudianteController.crear({"nombre": "pepe", "apellido": "x",
                                      "email": "pepe@mail.com", "carnet": "A001"}))
    print("Carnets:", EstudianteController.carnets_registrados())
    print(EstudianteController.agregar_nota(1, "matematica", 18))
    print(EstudianteController.agregar_nota(1, "fisica", 16))
    print(EstudianteController.agregar_nota(2, "matematica", 9))
    print(EstudianteController.agregar_nota(2, "fisica", 30))
    print(EstudianteController.agregar_nota(99, "fisica", 10))
    print(EstudianteController.actualizar(2, {"carnet": "A001"}))
    print(EstudianteController.actualizar(2, {"apellido": "gomez"}))
    print("Buscar 'b002':", [str(e) for e in EstudianteController.buscar("b002")])
    print("Materias ofertadas:", EstudianteController.materias_ofertadas())
    print("En común 1 y 2:", EstudianteController.materias_en_comun(1, 2))
    print("En común 1 y 99:", EstudianteController.materias_en_comun(1, 99))
    print("Estadísticas:", EstudianteController.estadisticas())

    # borra la carpeta de prueba
    shutil.rmtree("prueba_temp")
