from models import Cliente, Estudiante  # Importa los modelos (moldes de datos)
from shared.json_manager import GestorJSON  # Importa el lector/escritor de JSON


class ClienteController:  # Controlador de clientes
    """CONTROLADOR: realiza las operaciones CRUD. No imprime ni pide datos."""

    MODELO = Cliente  # Clase que usa este controlador
    ARCHIVO = "data/clientes.json"  # Dónde se guardan los datos
    CAMPOS_BUSCABLES = (  # Campos donde se puede buscar
        "nombre",
        "apellido",
        "email",
        "telefono",
        "ciudad"
    )

    _gestor = GestorJSON(ARCHIVO)  # Objeto que lee/guarda el archivo

    # =========================================
    # MÉTODOS DE APOYO
    # =========================================

    @classmethod  # Usa la clase (cls), no un objeto
    def _registros(cls):  # "_" = método de uso interno
        """Devuelve la lista de registros almacenados en JSON."""
        return cls._gestor.leer()  # Lee el archivo y devuelve la lista

    @classmethod  # Método de clase
    def emails_registrados(cls, excepto_id=None):  # Emails ya usados
        """Conjunto de emails ya registrados."""
        return {  # {} con "for" = crea un set (sin repetidos)
            registro["email"].lower()  # Email en minúsculas
            for registro in cls._registros()  # Por cada registro
            if registro["id"] != excepto_id  # Menos el del ID excluido
        }

    @classmethod  # Método de clase
    def siguiente_id(cls):  # Calcula el próximo ID
        """Calcula automáticamente el siguiente ID."""
        ids = [  # Lista con todos los IDs
            registro["id"]
            for registro in cls._registros()
        ]

        return max(ids) + 1 if ids else 1  # El mayor + 1, o 1 si no hay

    @staticmethod  # No usa cls ni self
    def _coincide(registro, termino, campos):  # ¿El término está en algún campo?
        """Comprueba si el término aparece en alguno de los campos."""

        for campo in campos:  # Recorre cada campo

            if termino in str(  # Si el término está dentro del valor...
                registro.get(campo, "")  # Valor del campo (o "" si falta)
            ).lower():  # En minúsculas

                return True  # ...hay coincidencia

        return False  # No coincidió en ningún campo

    # =========================================
    # CREATE - CREAR
    # =========================================

    @classmethod  # Método de clase
    def crear(cls, datos):  # Crea un registro nuevo
        """Crea un nuevo registro."""

        try:  # Intenta crear (el modelo puede lanzar error)

            faltantes = [  # Lista de campos obligatorios vacíos
                campo
                for campo in cls.MODELO.OBLIGATORIOS  # Recorre los obligatorios
                if not str(  # Si está vacío...
                    datos.get(campo, "")
                ).strip()
            ]

            if faltantes:  # Si falta alguno
                return (  # Devuelve (False, mensaje)
                    False,
                    f"Faltan campos obligatorios: "
                    f"{', '.join(faltantes)}"
                )

            email = str(  # Toma el email
                datos.get("email", "")
            ).strip().lower()  # Limpio y en minúsculas

            if email in cls.emails_registrados():  # Si ya existe
                return (  # No se permite repetir
                    False,
                    "Ese email ya está registrado"
                )

            valores = {  # Diccionario solo con los campos del modelo
                campo: datos.get(campo, "")
                for campo in cls.MODELO.CAMPOS
            }

            objeto = cls.MODELO(  # Crea el objeto (aquí se valida)
                cls.siguiente_id(),  # Nuevo ID
                **valores  # "**" pasa el diccionario como nombre=valor
            )

            registros = cls._registros()  # Lee los registros actuales

            registros.append(  # Agrega el nuevo
                objeto.a_diccionario()  # Convertido a diccionario
            )

            if not cls._gestor.guardar(registros):  # Si no se pudo guardar
                return (  # Error
                    False,
                    "No se pudo escribir el archivo"
                )

            return (  # Todo bien
                True,
                f"{objeto.nombre_completo} "
                f"creado con id {objeto.id}"
            )

        except ValueError as error:  # Si el modelo rechazó un dato
            return False, str(error)  # Devuelve el mensaje del error

    # =========================================
    # READ - LEER
    # =========================================

    @classmethod  # Método de clase
    def listar(cls):  # Devuelve todos como objetos
        """Devuelve una lista de objetos."""

        return [  # Lista de objetos
            cls.MODELO.desde_diccionario(registro)  # Diccionario -> objeto
            for registro in cls._registros()  # Por cada registro
        ]

    @classmethod  # Método de clase
    def obtener(cls, id_registro):  # Busca uno por ID
        """Busca un registro por ID."""

        for objeto in cls.listar():  # Recorre todos

            if objeto.id == id_registro:  # Si el ID coincide
                return objeto  # Lo devuelve

        return None  # No lo encontró

    # =========================================
    # SEARCH - BUSCAR
    # =========================================

    @classmethod  # Método de clase
    def buscar(cls, termino):  # Busca por texto
        """Busca coincidencias en varios campos."""

        termino = str(  # Convierte a texto
            termino
        ).strip().lower()  # Limpio y en minúsculas

        if not termino:  # Si está vacío
            return []  # No busca nada

        return [  # Lista de objetos que coinciden
            cls.MODELO.desde_diccionario(registro)  # Diccionario -> objeto
            for registro in cls._registros()  # Por cada registro

            if cls._coincide(  # Solo si coincide
                registro,
                termino,
                cls.CAMPOS_BUSCABLES
            )
        ]

    # =========================================
    # UPDATE - ACTUALIZAR
    # =========================================

    @classmethod  # Método de clase
    def actualizar(cls, id_registro, cambios):  # Modifica un registro
        """Actualiza los datos de un registro."""

        try:  # Intenta actualizar

            desconocidos = (  # Campos que no existen en el modelo
                set(cambios)  # Campos enviados
                - set(cls.MODELO.CAMPOS)  # Menos los válidos
            )

            if desconocidos:  # Si hay campos raros
                return (  # Error
                    False,
                    f"Campos no válidos: "
                    f"{', '.join(sorted(desconocidos))}"
                )

            if not cambios:  # Si no hay cambios
                return (  # Error
                    False,
                    "No se indicó ningún cambio"
                )

            objeto = cls.obtener(id_registro)  # Busca el registro

            if objeto is None:  # Si no existe
                return (  # Error
                    False,
                    f"No existe un registro "
                    f"con id {id_registro}"
                )

            if "email" in cambios:  # Si quiere cambiar el email

                nuevo_email = str(  # Toma el nuevo email
                    cambios["email"]
                ).strip().lower()  # Limpio y en minúsculas

                if nuevo_email in cls.emails_registrados(  # Si otro ya lo usa
                    excepto_id=id_registro  # (sin contar este mismo)
                ):

                    return (  # Error
                        False,
                        "Ese email ya lo usa otro registro"
                    )

            for campo, valor in cambios.items():  # Recorre los cambios

                setattr(  # Hace: objeto.campo = valor (usa el setter)
                    objeto,
                    campo,
                    valor
                )

            registros = cls._registros()  # Lee los registros

            for indice, registro in enumerate(registros):  # enumerate da posición y valor

                if registro["id"] == id_registro:  # Si es el que buscamos

                    registros[indice] = (  # Lo reemplaza
                        objeto.a_diccionario()
                    )

                    break  # Sale del for

            if not cls._gestor.guardar(registros):  # Si no se pudo guardar
                return (  # Error
                    False,
                    "No se pudo guardar la actualización"
                )

            return (  # Todo bien
                True,
                f"Registro {id_registro} actualizado "
                f"({len(cambios)} campo/s)"
            )

        except ValueError as error:  # Si un dato era inválido
            return False, str(error)  # Devuelve el error

    # =========================================
    # DELETE - ELIMINAR
    # =========================================

    @classmethod  # Método de clase
    def eliminar(cls, id_registro):  # Borra un registro
        """Elimina un registro por ID."""

        registros = cls._registros()  # Lee los registros

        quedan = [  # Todos menos el que se borra
            registro
            for registro in registros
            if registro["id"] != id_registro
        ]

        if len(quedan) == len(registros):  # Si no cambió la cantidad
            return (  # No existía
                False,
                f"No existe un registro "
                f"con id {id_registro}"
            )

        if not cls._gestor.guardar(quedan):  # Guarda los que quedan
            return (  # Si falló
                False,
                "No se pudo guardar el archivo"
            )

        return (  # Todo bien
            True,
            f"Registro {id_registro} eliminado"
        )

    # =========================================
    # ESTADÍSTICAS
    # =========================================

    @classmethod  # Método de clase
    def estadisticas(cls):  # Calcula estadísticas de clientes

        registros = cls._registros()  # Lee los registros

        ciudades = {  # Set de ciudades (sin repetir)
            registro.get("ciudad", "")
            for registro in registros
            if registro.get("ciudad")  # Solo si tiene ciudad
        }

        dominios = {  # Set de dominios de email
            registro["email"].split("@")[1]  # Lo que va después de @
            for registro in registros
            if "@" in registro["email"]
        }

        sin_telefono = [  # Nombres de los que no tienen teléfono
            registro["nombre"]
            for registro in registros
            if not registro.get("telefono")
        ]

        return {  # Devuelve todo en un diccionario
            "total": len(registros),
            "ciudades": sorted(ciudades),  # sorted = lista ordenada
            "dominios": sorted(dominios),
            "sin_telefono": sin_telefono,
        }


# =========================================================
# CONTROLADOR DE ESTUDIANTES
# =========================================================

class EstudianteController(ClienteController):  # Hereda todo de ClienteController
    """
    Hereda las operaciones CRUD de ClienteController
    y agrega las operaciones propias de Estudiante.
    """

    MODELO = Estudiante  # Usa el modelo Estudiante

    ARCHIVO = "data/estudiantes.json"  # Su propio archivo

    CAMPOS_BUSCABLES = (  # Campos donde buscar
        "nombre",
        "apellido",
        "email",
        "carnet"
    )

    _gestor = GestorJSON(ARCHIVO)  # Su propio gestor de archivo

    # =========================================
    # CARNETS
    # =========================================

    @classmethod  # Método de clase
    def carnets_registrados(cls, excepto_id=None):  # Carnets ya usados
        """Devuelve un SET con todos los carnets registrados."""

        return {  # Set de carnets
            registro["carnet"].upper()  # En mayúsculas
            for registro in cls._registros()
            if registro["id"] != excepto_id  # Menos el excluido
        }

    # =========================================
    # CREAR ESTUDIANTE
    # =========================================

    @classmethod  # Método de clase
    def crear(cls, datos):  # Sobrescribe crear del padre

        carnet = str(  # Toma el carnet
            datos.get("carnet", "")
        ).strip().upper()  # Limpio y en mayúsculas

        if carnet in cls.carnets_registrados():  # Si ya existe

            return (  # Error
                False,
                "Ese carnet ya está registrado"
            )

        return super().crear(datos)  # Si no, usa el crear del padre

    # =========================================
    # ACTUALIZAR ESTUDIANTE
    # =========================================

    @classmethod  # Método de clase
    def actualizar(cls, id_registro, cambios):  # Sobrescribe actualizar

        if "carnet" in cambios:  # Si cambia el carnet

            nuevo_carnet = str(  # Toma el nuevo carnet
                cambios["carnet"]
            ).strip().upper()  # Limpio y en mayúsculas

            if nuevo_carnet in cls.carnets_registrados(  # Si otro lo usa
                excepto_id=id_registro
            ):

                return (  # Error
                    False,
                    "Ese carnet ya lo usa otro estudiante"
                )

        return super().actualizar(  # Usa el actualizar del padre
            id_registro,
            cambios
        )

    # =========================================
    # AGREGAR NOTA
    # =========================================

    @classmethod  # Método de clase
    def agregar_nota(  # Agrega una nota a un estudiante
        cls,
        id_estudiante,
        materia,
        nota
    ):

        estudiante = cls.obtener(  # Busca el estudiante
            id_estudiante
        )

        if estudiante is None:  # Si no existe

            return (  # Error
                False,
                f"No existe un estudiante "
                f"con id {id_estudiante}"
            )

        try:  # Intenta agregar la nota

            estudiante.agregar_nota(  # El modelo valida la nota
                materia,
                nota
            )

            registros = cls._registros()  # Lee los registros

            for indice, registro in enumerate(registros):  # Busca su posición

                if registro["id"] == id_estudiante:  # Si es él

                    registros[indice] = (  # Lo reemplaza con la nota nueva
                        estudiante.a_diccionario()
                    )

                    break  # Sale del for

            if not cls._gestor.guardar(registros):  # Si no se pudo guardar

                return (  # Error
                    False,
                    "No se pudo guardar la nota"
                )

            return (  # Todo bien
                True,
                f"Nota {nota} agregada en "
                f"{materia}"
            )

        except ValueError as error:  # Si la nota era inválida

            return (  # Devuelve el error
                False,
                str(error)
            )

    # =========================================
    # MATERIAS OFERTADAS
    # =========================================

    @classmethod  # Método de clase
    def materias_ofertadas(cls):  # Todas las materias
        """Devuelve todas las materias sin repetir."""

        materias = set()  # Set vacío

        for estudiante in cls.listar():  # Recorre los estudiantes

            materias.update(  # Agrega sus materias al set
                estudiante.materias
            )

        return materias  # Devuelve el set

    # =========================================
    # MATERIAS EN COMÚN
    # =========================================

    @classmethod  # Método de clase
    def materias_en_comun(  # Materias que comparten 2 estudiantes
        cls,
        id_a,
        id_b
    ):

        estudiante_a = cls.obtener(id_a)  # Busca al primero
        estudiante_b = cls.obtener(id_b)  # Busca al segundo

        if estudiante_a is None:  # Si no existe el primero
            return None  # Devuelve None

        if estudiante_b is None:  # Si no existe el segundo
            return None  # Devuelve None

        return estudiante_a.materias_en_comun(  # Usa el método del modelo
            estudiante_b
        )

    # =========================================
    # ESTADÍSTICAS PARA ESTUDIANTES
    # =========================================

    @classmethod  # Método de clase
    def estadisticas(cls):  # Sobrescribe estadísticas

        estudiantes = cls.listar()  # Todos los estudiantes

        aprobados = [  # Solo los aprobados
            estudiante
            for estudiante in estudiantes
            if estudiante.estado == "Aprobado"
        ]

        reprobados = [  # Solo los reprobados
            estudiante
            for estudiante in estudiantes
            if estudiante.estado == "Reprobado"
        ]

        return {  # Devuelve todo en un diccionario
            "total": len(estudiantes),
            "aprobados": len(aprobados),
            "reprobados": len(reprobados),
            "materias": sorted(  # Materias ordenadas
                cls.materias_ofertadas()
            ),
        }


if __name__ == "__main__":  # Solo se ejecuta si corres este archivo directamente
    import shutil  # Módulo para borrar carpetas

    # Usamos archivos de prueba para NO tocar los datos reales
    ClienteController._gestor = GestorJSON("prueba_temp/clientes.json")  # Archivo temporal de clientes
    EstudianteController._gestor = GestorJSON("prueba_temp/estudiantes.json")  # Archivo temporal de estudiantes

    print("===== CLIENTES =====")  # Separador
    print(ClienteController.crear({"nombre": "ana", "apellido": "lopez", "email": "ana@mail.com",
                                   "telefono": "555", "ciudad": "lima"}))  # Crear -> True
    print(ClienteController.crear({"nombre": "luis", "apellido": "ruiz", "email": "luis@gmail.com"}))  # Crear sin teléfono
    print(ClienteController.crear({"nombre": "otra", "apellido": "x", "email": "ana@mail.com"}))  # Email repetido -> False
    print(ClienteController.crear({"nombre": "", "apellido": "x", "email": "x@mail.com"}))  # Falta nombre -> False
    print("Emails:", ClienteController.emails_registrados())  # Set de emails
    print("Siguiente ID:", ClienteController.siguiente_id())  # 3
    print("Listar:", [str(c) for c in ClienteController.listar()])  # Todos
    print("Obtener 1:", ClienteController.obtener(1))  # Uno por ID
    print("Buscar 'lima':", [str(c) for c in ClienteController.buscar("lima")])  # Búsqueda
    print(ClienteController.actualizar(2, {"ciudad": "cusco"}))  # Actualizar -> True
    print(ClienteController.actualizar(2, {"edad": 5}))  # Campo inválido -> False
    print("Estadísticas:", ClienteController.estadisticas())  # Estadísticas
    print(ClienteController.eliminar(2))  # Eliminar -> True
    print(ClienteController.eliminar(99))  # No existe -> False

    print("\n===== ESTUDIANTES =====")  # Separador
    print(EstudianteController.crear({"nombre": "juan", "apellido": "perez",
                                      "email": "juan@mail.com", "carnet": "a001"}))  # Crear
    print(EstudianteController.crear({"nombre": "maria", "apellido": "diaz",
                                      "email": "maria@mail.com", "carnet": "b002"}))  # Crear
    print(EstudianteController.crear({"nombre": "pepe", "apellido": "x",
                                      "email": "pepe@mail.com", "carnet": "A001"}))  # Carnet repetido -> False
    print("Carnets:", EstudianteController.carnets_registrados())  # Set de carnets
    print(EstudianteController.agregar_nota(1, "matematica", 18))  # Nota -> True
    print(EstudianteController.agregar_nota(1, "fisica", 16))  # Nota -> True
    print(EstudianteController.agregar_nota(2, "matematica", 9))  # Nota -> True
    print(EstudianteController.agregar_nota(2, "fisica", 30))  # Nota inválida -> False
    print(EstudianteController.agregar_nota(99, "fisica", 10))  # No existe -> False
    print(EstudianteController.actualizar(2, {"carnet": "A001"}))  # Carnet de otro -> False
    print(EstudianteController.actualizar(2, {"apellido": "gomez"}))  # Actualizar -> True
    print("Buscar 'b002':", [str(e) for e in EstudianteController.buscar("b002")])  # Búsqueda
    print("Materias ofertadas:", EstudianteController.materias_ofertadas())  # Todas las materias
    print("En común 1 y 2:", EstudianteController.materias_en_comun(1, 2))  # Materias compartidas
    print("En común 1 y 99:", EstudianteController.materias_en_comun(1, 99))  # None
    print("Estadísticas:", EstudianteController.estadisticas())  # Estadísticas

    shutil.rmtree("prueba_temp")  # Borra la carpeta de prueba
