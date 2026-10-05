class Cliente:
    """Modelo de cliente. Si algún dato es inválido, el objeto no se crea."""

    # campos que se piden por consola al crear un cliente
    CAMPOS = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")
    # los que no pueden quedar vacíos
    OBLIGATORIOS = ("nombre", "apellido", "email")
    # contador de la clase, lo comparten todos los clientes
    total_creados = 0

    def __init__(self, id_cliente, nombre, apellido, email,
                 telefono="", ciudad="", direccion=""):
        self.__id = id_cliente
        # uso self.nombre (sin __) para que pase por el setter y se valide
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion
        Cliente.total_creados += 1

    # le quita los espacios de los lados al texto
    @staticmethod
    def limpiar(texto):
        return str(texto).strip()

    # validación sencilla: una sola @ y un punto en el dominio
    @staticmethod
    def es_email_valido(texto):
        texto = str(texto).strip()

        if texto.count("@") != 1:
            return False

        usuario, dominio = texto.split("@")

        return (
            len(usuario) > 0
            and "." in dominio
            and not dominio.endswith(".")
        )

    # el id solo se puede leer, no tiene setter
    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    # los setters limpian y validan antes de guardar el dato
    @nombre.setter
    def nombre(self, valor):
        valor = Cliente.limpiar(valor)

        if not valor:
            raise ValueError("El nombre es obligatorio")

        self.__nombre = valor.title()

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = Cliente.limpiar(valor)

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor.title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = Cliente.limpiar(valor)

        if not Cliente.es_email_valido(valor):
            raise ValueError(f"Email inválido: '{valor}'")

        # el email siempre se guarda en minúsculas
        self.__email = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = Cliente.limpiar(valor)

        # el teléfono es opcional, pero si lo escriben deben ser solo números
        if valor and not valor.isdigit():
            raise ValueError("El teléfono solo puede tener números")

        self.__telefono = valor

    @property
    def ciudad(self):
        return self.__ciudad

    @ciudad.setter
    def ciudad(self, valor):
        self.__ciudad = Cliente.limpiar(valor).title()

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        self.__direccion = Cliente.limpiar(valor)

    # propiedades que se calculan al pedirlas, no se guardan
    @property
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"

    @property
    def dominio_email(self):
        return self.__email.split("@")[1]

    # pasa el objeto a diccionario para poder guardarlo en el JSON
    def a_diccionario(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "email": self.__email,
            "telefono": self.__telefono,
            "ciudad": self.__ciudad,
            "direccion": self.__direccion,
        }

    def __str__(self):
        return f"[{self.__id}] {self.nombre_completo} - {self.__email}"

    # lo contrario: arma el cliente a partir de lo que se leyó del JSON
    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos.get("telefono", ""),
            datos.get("ciudad", ""),
            datos.get("direccion", ""),
        )


class Estudiante:
    """Modelo de estudiante, con sus materias y sus notas."""

    CAMPOS = ("nombre", "apellido", "email", "carnet")
    OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")

    # rango de notas permitido
    NOTA_MINIMA = 0
    NOTA_MAXIMA = 20

    total_creados = 0

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 notas=None, materias=None):

        self.__id = id_estudiante

        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        # notas = {materia: [notas]}, materias = conjunto para que no se repitan
        self.__notas = dict(notas) if notas else {}
        self.__materias = set(materias) if materias else set()

        Estudiante.total_creados += 1


    @staticmethod
    def limpiar(texto):
        return str(texto).strip()

    # la nota debe ser un número dentro del rango
    @staticmethod
    def es_nota_valida(nota):
        return (
            isinstance(nota, (int, float))
            and Estudiante.NOTA_MINIMA <= nota <= Estudiante.NOTA_MAXIMA
        )


    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = Estudiante.limpiar(valor)

        if not valor:
            raise ValueError("El nombre es obligatorio")

        self.__nombre = valor.title()

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = Estudiante.limpiar(valor)

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor.title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = Estudiante.limpiar(valor)

        # aquí el email se valida más simple que en Cliente
        if "@" not in valor:
            raise ValueError(f"Email inválido: '{valor}'")

        self.__email = valor.lower()

    @property
    def carnet(self):
        return self.__carnet

    @carnet.setter
    def carnet(self, valor):
        # el carnet se guarda en mayúsculas
        valor = Estudiante.limpiar(valor).upper()

        if len(valor) < 4:
            raise ValueError("El carnet debe tener al menos 4 caracteres")

        self.__carnet = valor

    # devuelve una copia para que no la cambien desde afuera
    @property
    def materias(self):
        return set(self.__materias)

    @property
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"

    @property
    def promedio(self):
        # junta las notas de todas las materias y saca un solo promedio
        todas = []

        for lista_notas in self.__notas.values():
            todas.extend(lista_notas)

        if todas:
            return round(sum(todas) / len(todas), 2)

        return 0

    @property
    def estado(self):
        # 14 es la nota mínima para aprobar
        if self.promedio >= 14:
            return "Aprobado"

        return "Reprobado"


    # si la materia ya estaba, el conjunto no la repite
    def inscribir_materia(self, materia):
        materia = Estudiante.limpiar(materia).title()

        if not materia:
            raise ValueError("La materia no puede estar vacía")

        self.__materias.add(materia)

        return materia

    def agregar_nota(self, materia, nota):

        if not Estudiante.es_nota_valida(nota):
            raise ValueError(
                f"La nota debe estar entre "
                f"{Estudiante.NOTA_MINIMA} y "
                f"{Estudiante.NOTA_MAXIMA}"
            )

        materia = self.inscribir_materia(materia)

        # setdefault crea la lista si es la primera nota de esa materia
        self.__notas.setdefault(materia, []).append(nota)

    # devuelve una copia de las notas de la materia
    def notas_de(self, materia):
        materia = Estudiante.limpiar(materia).title()

        return list(
            self.__notas.get(materia, [])
        )

    # intersección de los dos conjuntos de materias
    def materias_en_comun(self, otro):
        return self.__materias & otro.materias

    def a_diccionario(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "email": self.__email,
            "carnet": self.__carnet,
            "notas": self.__notas,
            # un set no se guarda en JSON, por eso va como lista ordenada
            "materias": sorted(self.__materias),
        }

    def __str__(self):
        return (
            f"[{self.__carnet}] "
            f"{self.nombre_completo} - "
            f"Promedio: {self.promedio} - "
            f"Estado: {self.estado}"
        )


    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(
                datos.get("materias", [])
            ),
        )


# pruebas rápidas, solo corren si ejecuto este archivo
if __name__ == "__main__":

    print("===== CLIENTE =====")
    c = Cliente(1, "  ana ", "lopez", "ANA@Mail.com", "555123", "lima", "Av. Sol 1")
    print(c)
    print("Nombre completo:", c.nombre_completo)
    print("Dominio:", c.dominio_email)
    print("Email válido 'a@b.com':", Cliente.es_email_valido("a@b.com"))
    print("Email válido 'malo':", Cliente.es_email_valido("malo"))
    d = c.a_diccionario()
    print("Diccionario:", d)
    print("Copia:", Cliente.desde_diccionario(d))

    try:
        c.telefono = "abc"
    except ValueError as e:
        print("Error esperado:", e)

    print("Clientes creados:", Cliente.total_creados)

    print("\n===== ESTUDIANTE =====")
    e1 = Estudiante(1, "juan", "perez", "juan@mail.com", "a001")
    e2 = Estudiante(2, "maria", "diaz", "maria@mail.com", "b002")

    e1.agregar_nota("matematica", 18)
    e1.agregar_nota("fisica", 15)
    e2.agregar_nota("Matematica", 10)
    e2.inscribir_materia("historia")

    print(e1)
    print(e2)
    print("Notas de e1 en matemática:", e1.notas_de("matematica"))
    print("Materias de e2:", e2.materias)
    print("En común:", e1.materias_en_comun(e2))
    print("Nota 25 válida?", Estudiante.es_nota_valida(25))

    try:
        e1.agregar_nota("fisica", 25)
    except ValueError as e:
        print("Error esperado:", e)

    try:
        Estudiante(3, "luis", "ruiz", "luis@mail.com", "ab")
    except ValueError as e:
        print("Error esperado:", e)

    d2 = e1.a_diccionario()
    print("Diccionario:", d2)
    print("Copia:", Estudiante.desde_diccionario(d2))
    print("Estudiantes creados:", Estudiante.total_creados)
