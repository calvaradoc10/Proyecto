class Cliente:  # Clase (molde) para crear clientes
    """MODELO: un cliente válido. Si los datos están mal, el objeto no se crea."""

    CAMPOS = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")  # Campos que se piden
    OBLIGATORIOS = ("nombre", "apellido", "email")  # Campos que no pueden faltar
    total_creados = 0  # Contador compartido por todos los clientes

    def __init__(self, id_cliente, nombre, apellido, email,  # Constructor: crea el cliente
                 telefono="", ciudad="", direccion=""):  # ="" significa opcional
        self.__id = id_cliente  # ID privado (__ = no se toca desde fuera)
        self.nombre = nombre  # Pasa por el setter (valida)
        self.apellido = apellido  # Pasa por el setter (valida)
        self.email = email  # Pasa por el setter (valida)
        self.telefono = telefono  # Pasa por el setter (valida)
        self.ciudad = ciudad  # Pasa por el setter
        self.direccion = direccion  # Pasa por el setter
        Cliente.total_creados += 1  # Suma 1 al contador

    @staticmethod  # No usa self
    def limpiar(texto):  # Quita espacios al inicio y final
        return str(texto).strip()  # Convierte a texto y limpia

    @staticmethod  # No usa self
    def es_email_valido(texto):  # Revisa si un email es válido
        texto = str(texto).strip()  # Limpia el texto

        if texto.count("@") != 1:  # Debe tener exactamente una @
            return False  # Si no, es inválido

        usuario, dominio = texto.split("@")  # Separa en antes y después de @

        return (  # Es válido si cumple todo:
            len(usuario) > 0  # hay algo antes de @
            and "." in dominio  # el dominio tiene un punto
            and not dominio.endswith(".")  # y no termina en punto
        )

    @property  # Permite leer: cliente.id
    def id(self):  # Getter del ID
        return self.__id  # Devuelve el ID (no tiene setter, no se puede cambiar)

    @property  # Permite leer: cliente.nombre
    def nombre(self):  # Getter
        return self.__nombre  # Devuelve el nombre

    @nombre.setter  # Se ejecuta al hacer: cliente.nombre = ...
    def nombre(self, valor):  # Setter
        valor = Cliente.limpiar(valor)  # Limpia espacios

        if not valor:  # Si quedó vacío
            raise ValueError("El nombre es obligatorio")  # Lanza un error

        self.__nombre = valor.title()  # Guarda con mayúscula inicial

    @property  # Getter de apellido
    def apellido(self):
        return self.__apellido  # Devuelve el apellido

    @apellido.setter  # Setter de apellido
    def apellido(self, valor):
        valor = Cliente.limpiar(valor)  # Limpia

        if not valor:  # Si está vacío
            raise ValueError("El apellido es obligatorio")  # Error

        self.__apellido = valor.title()  # Guarda con mayúscula inicial

    @property  # Getter de email
    def email(self):
        return self.__email  # Devuelve el email

    @email.setter  # Setter de email
    def email(self, valor):
        valor = Cliente.limpiar(valor)  # Limpia

        if not Cliente.es_email_valido(valor):  # Si no es válido
            raise ValueError(f"Email inválido: '{valor}'")  # Error

        self.__email = valor.lower()  # Guarda en minúsculas

    @property  # Getter de teléfono
    def telefono(self):
        return self.__telefono  # Devuelve el teléfono

    @telefono.setter  # Setter de teléfono
    def telefono(self, valor):
        valor = Cliente.limpiar(valor)  # Limpia

        if valor and not valor.isdigit():  # Si hay algo y no son solo números
            raise ValueError("El teléfono solo puede tener números")  # Error

        self.__telefono = valor  # Guarda

    @property  # Getter de ciudad
    def ciudad(self):
        return self.__ciudad  # Devuelve la ciudad

    @ciudad.setter  # Setter de ciudad
    def ciudad(self, valor):
        self.__ciudad = Cliente.limpiar(valor).title()  # Limpia y pone mayúscula inicial

    @property  # Getter de dirección
    def direccion(self):
        return self.__direccion  # Devuelve la dirección

    @direccion.setter  # Setter de dirección
    def direccion(self, valor):
        self.__direccion = Cliente.limpiar(valor)  # Limpia y guarda

    @property  # Propiedad calculada (no se guarda)
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"  # Une nombre y apellido

    @property  # Propiedad calculada
    def dominio_email(self):
        return self.__email.split("@")[1]  # Lo que va después de @

    def a_diccionario(self):  # Convierte el objeto a diccionario (para JSON)
        return {  # Devuelve un diccionario con todos los datos
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "email": self.__email,
            "telefono": self.__telefono,
            "ciudad": self.__ciudad,
            "direccion": self.__direccion,
        }

    def __str__(self):  # Lo que se ve al hacer print(cliente)
        return f"[{self.__id}] {self.nombre_completo} - {self.__email}"  # Texto resumido

    @classmethod  # Recibe la clase (cls) en vez del objeto
    def desde_diccionario(cls, datos):  # Crea un cliente desde un diccionario
        return cls(  # cls(...) = Cliente(...)
            datos["id"],  # [] = campo obligatorio
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos.get("telefono", ""),  # .get = si falta, usa ""
            datos.get("ciudad", ""),
            datos.get("direccion", ""),
        )


class Estudiante:  # Clase (molde) para crear estudiantes
    """MODELO: estudiante con materias y notas."""

    CAMPOS = ("nombre", "apellido", "email", "carnet")  # Campos que se piden
    OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")  # Todos obligatorios

    NOTA_MINIMA = 0  # Nota más baja permitida
    NOTA_MAXIMA = 20  # Nota más alta permitida

    total_creados = 0  # Contador de estudiantes creados

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,  # Constructor
                 notas=None, materias=None):  # Notas y materias son opcionales

        self.__id = id_estudiante  # ID privado

        self.nombre = nombre  # Setter (valida)
        self.apellido = apellido  # Setter (valida)
        self.email = email  # Setter (valida)
        self.carnet = carnet  # Setter (valida)

        self.__notas = dict(notas) if notas else {}  # Copia las notas o crea {} vacío
        self.__materias = set(materias) if materias else set()  # Copia materias o crea set vacío

        Estudiante.total_creados += 1  # Suma 1 al contador

    # ==========================
    # MÉTODOS ESTÁTICOS
    # ==========================

    @staticmethod  # No usa self
    def limpiar(texto):  # Quita espacios
        return str(texto).strip()  # Convierte a texto y limpia

    @staticmethod  # No usa self
    def es_nota_valida(nota):  # Revisa si la nota es válida
        return (  # Es válida si:
            isinstance(nota, (int, float))  # es un número
            and Estudiante.NOTA_MINIMA <= nota <= Estudiante.NOTA_MAXIMA  # y está entre 0 y 20
        )

    # ==========================
    # PROPIEDADES
    # ==========================

    @property  # Getter del ID (sin setter)
    def id(self):
        return self.__id  # Devuelve el ID

    @property  # Getter de nombre
    def nombre(self):
        return self.__nombre  # Devuelve el nombre

    @nombre.setter  # Setter de nombre
    def nombre(self, valor):
        valor = Estudiante.limpiar(valor)  # Limpia

        if not valor:  # Si está vacío
            raise ValueError("El nombre es obligatorio")  # Error

        self.__nombre = valor.title()  # Guarda con mayúscula inicial

    @property  # Getter de apellido
    def apellido(self):
        return self.__apellido  # Devuelve el apellido

    @apellido.setter  # Setter de apellido
    def apellido(self, valor):
        valor = Estudiante.limpiar(valor)  # Limpia

        if not valor:  # Si está vacío
            raise ValueError("El apellido es obligatorio")  # Error

        self.__apellido = valor.title()  # Guarda con mayúscula inicial

    @property  # Getter de email
    def email(self):
        return self.__email  # Devuelve el email

    @email.setter  # Setter de email
    def email(self, valor):
        valor = Estudiante.limpiar(valor)  # Limpia

        if "@" not in valor:  # Solo revisa que tenga @
            raise ValueError(f"Email inválido: '{valor}'")  # Error

        self.__email = valor.lower()  # Guarda en minúsculas

    @property  # Getter de carnet
    def carnet(self):
        return self.__carnet  # Devuelve el carnet

    @carnet.setter  # Setter de carnet
    def carnet(self, valor):
        valor = Estudiante.limpiar(valor).upper()  # Limpia y pasa a MAYÚSCULAS

        if len(valor) < 4:  # Si tiene menos de 4 letras
            raise ValueError("El carnet debe tener al menos 4 caracteres")  # Error

        self.__carnet = valor  # Guarda

    @property  # Getter de materias
    def materias(self):
        return set(self.__materias)  # Devuelve una COPIA (protege el original)

    @property  # Propiedad calculada
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"  # Une nombre y apellido

    @property  # Propiedad calculada
    def promedio(self):  # Promedio de todas las notas
        todas = []  # Lista para juntar todas las notas

        for lista_notas in self.__notas.values():  # Recorre las notas de cada materia
            todas.extend(lista_notas)  # Las agrega a "todas"

        if todas:  # Si hay notas
            return round(sum(todas) / len(todas), 2)  # Suma / cantidad, con 2 decimales

        return 0  # Sin notas, promedio 0

    # PROPIEDAD PEDIDA EN LA TAREA
    @property  # Propiedad calculada
    def estado(self):  # Aprobado o Reprobado
        if self.promedio >= 14:  # Si el promedio es 14 o más
            return "Aprobado"  # Aprobó

        return "Reprobado"  # Si no, reprobó

    # ==========================
    # MÉTODOS DE INSTANCIA
    # ==========================

    def inscribir_materia(self, materia):  # Agrega una materia
        materia = Estudiante.limpiar(materia).title()  # Limpia y pone mayúscula inicial

        if not materia:  # Si está vacía
            raise ValueError("La materia no puede estar vacía")  # Error

        self.__materias.add(materia)  # La agrega al set (no se repite)

        return materia  # Devuelve el nombre limpio

    def agregar_nota(self, materia, nota):  # Agrega una nota a una materia

        if not Estudiante.es_nota_valida(nota):  # Si la nota no es válida
            raise ValueError(  # Error con mensaje
                f"La nota debe estar entre "
                f"{Estudiante.NOTA_MINIMA} y "
                f"{Estudiante.NOTA_MAXIMA}"
            )

        materia = self.inscribir_materia(materia)  # Inscribe la materia (si no estaba)

        self.__notas.setdefault(materia, []).append(nota)  # Crea la lista si no existe y agrega la nota

    def notas_de(self, materia):  # Devuelve las notas de una materia
        materia = Estudiante.limpiar(materia).title()  # Limpia el nombre

        return list(  # Devuelve una copia en lista
            self.__notas.get(materia, [])  # Si no hay notas, lista vacía
        )

    def materias_en_comun(self, otro):  # Materias que comparte con otro estudiante
        return self.__materias & otro.materias  # "&" = intersección de sets

    def a_diccionario(self):  # Convierte a diccionario (para JSON)
        return {  # Devuelve todos los datos
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "email": self.__email,
            "carnet": self.__carnet,
            "notas": self.__notas,
            "materias": sorted(self.__materias),  # Set -> lista ordenada (JSON no acepta sets)
        }

    def __str__(self):  # Lo que se ve al hacer print(estudiante)
        return (  # Texto resumido
            f"[{self.__carnet}] "
            f"{self.nombre_completo} - "
            f"Promedio: {self.promedio} - "
            f"Estado: {self.estado}"
        )

    # ==========================
    # MÉTODO DE CLASE
    # ==========================

    @classmethod  # Recibe la clase (cls)
    def desde_diccionario(cls, datos):  # Crea un estudiante desde un diccionario
        return cls(  # cls(...) = Estudiante(...)
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),  # Si no hay notas, {}
            materias=set(  # Convierte la lista a set
                datos.get("materias", [])  # Si no hay materias, []
            ),
        )


if __name__ == "__main__":  # Solo se ejecuta si corres este archivo directamente

    print("===== CLIENTE =====")  # Separador
    c = Cliente(1, "  ana ", "lopez", "ANA@Mail.com", "555123", "lima", "Av. Sol 1")  # Crea un cliente
    print(c)  # Usa __str__
    print("Nombre completo:", c.nombre_completo)  # Propiedad calculada
    print("Dominio:", c.dominio_email)  # Propiedad calculada
    print("Email válido 'a@b.com':", Cliente.es_email_valido("a@b.com"))  # True
    print("Email válido 'malo':", Cliente.es_email_valido("malo"))  # False
    d = c.a_diccionario()  # Objeto -> diccionario
    print("Diccionario:", d)  # Lo muestra
    print("Copia:", Cliente.desde_diccionario(d))  # Diccionario -> objeto

    try:  # Prueba un error
        c.telefono = "abc"  # Teléfono con letras
    except ValueError as e:  # Atrapa el error
        print("Error esperado:", e)  # Lo muestra

    print("Clientes creados:", Cliente.total_creados)  # Contador de clase

    print("\n===== ESTUDIANTE =====")  # Separador
    e1 = Estudiante(1, "juan", "perez", "juan@mail.com", "a001")  # Estudiante 1
    e2 = Estudiante(2, "maria", "diaz", "maria@mail.com", "b002")  # Estudiante 2

    e1.agregar_nota("matematica", 18)  # Nota de e1
    e1.agregar_nota("fisica", 15)  # Otra nota de e1
    e2.agregar_nota("Matematica", 10)  # Nota de e2
    e2.inscribir_materia("historia")  # Materia sin nota

    print(e1)  # Usa __str__
    print(e2)  # Usa __str__
    print("Notas de e1 en matemática:", e1.notas_de("matematica"))  # [18]
    print("Materias de e2:", e2.materias)  # Set de materias
    print("En común:", e1.materias_en_comun(e2))  # {'Matematica'}
    print("Nota 25 válida?", Estudiante.es_nota_valida(25))  # False

    try:  # Prueba un error
        e1.agregar_nota("fisica", 25)  # Nota fuera de rango
    except ValueError as e:  # Atrapa el error
        print("Error esperado:", e)  # Lo muestra

    try:  # Prueba otro error
        Estudiante(3, "luis", "ruiz", "luis@mail.com", "ab")  # Carnet muy corto
    except ValueError as e:  # Atrapa el error
        print("Error esperado:", e)  # Lo muestra

    d2 = e1.a_diccionario()  # Objeto -> diccionario
    print("Diccionario:", d2)  # Lo muestra
    print("Copia:", Estudiante.desde_diccionario(d2))  # Diccionario -> objeto
    print("Estudiantes creados:", Estudiante.total_creados)  # Contador de clase
