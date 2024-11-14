import json
import datetime


class Auth:
    def __init__(self, code_card, pin):
        self.code_card = code_card
        self.pin = pin
        self.id_usuario = 0

    def autenticar(self):
        with open("clientes.json", "r") as file:
            data = json.load(file)

            for cliente in data["clientes"]:
                if cliente["code-card"] == self.code_card and cliente["pin"] == self.pin:
                    self.id_usuario = cliente["id"]
                    return True

        return False

    def obtener_id_usuario(self):
        return self.id_usuario


class Usuario:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.nombres = ""
        self.apellidos = ""
        self.rol = ""
        self.cel = ""
        self.email = ""
        self.saldo = 0
        self.historial = []
        self.cargar_datos()

    def cargar_datos(self):
        with open("clientes.json", "r") as file:
            data = json.load(file)

            for usuario in data["clientes"]:
                if usuario["id"] == self.id_usuario:
                    self.nombres = usuario["nombres"]
                    self.apellidos = usuario["apellidos"]
                    self.cel = usuario["cel"]
                    self.rol = usuario["rol"]
                    self.email = usuario["email"]
                    self.saldo = usuario["saldo"]
                    self.historial = usuario["historial"]

    def obtener_nombres(self):
        return self.nombres

    def obtener_apellidos(self):
        return self.apellidos

    def obtener_rol(self):
        return self.rol

    def obtener_cel(self):
        return self.cel

    def obtener_email(self):
        return self.email

    def obtener_saldo(self):
        return self.saldo

    def obtener_historial(self):
        return self.historial


class Cajero:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.cliente = {}
        self.cargar_cliente()

    def cargar_cliente(self):
        with open("clientes.json", "r") as file:
            data = json.load(file)
            for cliente in data["clientes"]:
                if cliente["id"] == self.id_usuario:
                    self.cliente = cliente
                    break

    def guardar_cliente(self):
        with open("clientes.json", "r+") as file:
            data = json.load(file)
            for i, cliente in enumerate(data["clientes"]):
                if cliente["id"] == self.id_usuario:
                    data["clientes"][i] = self.cliente

            file.seek(0)
            json.dump(data, file, indent=2)

    def depositar(self, monto):
        self.cliente["saldo"] += monto
        self.cliente["historial"].append({
            "tipo": "deposito",
            "monto": monto,
            "fecha": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
        self.guardar_cliente()
        print(f"Deposito exitoso. Tu nuevo saldo es {self.cliente['saldo']}")

    def retirar(self, monto):
        if monto > self.cliente["saldo"]:
            print("Saldo insuficiente.")
            return
        self.cliente["saldo"] -= monto
        self.cliente["historial"].append({
            "tipo": "retiro",
            "monto": monto,
            "fecha": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
        self.guardar_cliente()
        print(f"Retiro exitoso. Tu nuevo saldo es {self.cliente['saldo']}")


def crear_usuario():
    print("Creando una nueva cuenta de usuario.")
    nombres = input("Ingrese sus nombres: ")
    apellidos = input("Ingrese sus apellidos: ")
    cel = input("Ingrese su número de celular: ")
    email = input("Ingrese su email: ")
    code_card = input("Ingrese un código de tarjeta (único): ")
    pin = input("Ingrese un pin de 4 dígitos: ")

    nuevo_usuario = {
        "id": generar_id(),
        "nombres": nombres,
        "apellidos": apellidos,
        "cel": cel,
        "email": email,
        "rol": "usuario",
        "saldo": 0,
        "historial": [],
        "code-card": code_card,
        "pin": pin,
    }

    with open("clientes.json", "r+") as file:
        data = json.load(file)
        data["clientes"].append(nuevo_usuario)
        file.seek(0)
        json.dump(data, file, indent=2)

    print("Cuenta creada exitosamente.")


def generar_id():

    with open("clientes.json", "r") as file:
        data = json.load(file)
        return len(data["clientes"]) + 1


def login():
    intentos = 0

    while intentos < 3:
        code_card = input("Introduzca su código de tarjeta: ")
        pin = input("Introduzca su pin: ")
        autenticar = Auth(code_card=code_card, pin=pin)

        if autenticar.autenticar():
            return autenticar

        print("Código de tarjeta o pin incorrectos")
        intentos += 1

    print("Demasiados intentos fallidos. El programa se cerrará.")
    return None


def menu(id_usuario: int):
    usuario = Usuario(id_usuario)
    cajero = Cajero(id_usuario)

    menu_normal = """
        1. Depositar
        2. Retirar
        3. Ver saldo
        4. Historial de transacciones
        5. Datos del usuario
        6. Salir
    """
    menu_admin = """
        7. Crear cuenta (Solo Administrador)
    """
    print(menu_normal)

    if usuario.obtener_rol() == "Admin":
        print(menu_admin)

    op = int(input("Elija una opción: "))

    if op == 1:
        monto = int(input("Monto a depositar: "))
        cajero.depositar(monto)
        input()

    elif op == 2:
        monto = int(input("Monto a retirar: "))
        cajero.retirar(monto)
        input()

    elif op == 3:
        print(f"Saldo disponible: {cajero.cliente['saldo']}")
        input()

    elif op == 4:
        for tsc in usuario.obtener_historial():
            print(f"""
            Tipo: {tsc['tipo']}
            Monto: {tsc['monto']}
            Fecha: {tsc['fecha']}""")
    elif op == 5:
        print(f"""
            Nombres: {usuario.obtener_nombres()}
            Apellidos: {usuario.obtener_apellidos()}
            Celular: {usuario.obtener_cel()}
            Email: {usuario.obtener_email()}""")
        input()

    elif op == 7 and usuario.obtener_rol() == "Admin":
        crear_usuario()
        input()

    elif op == 6:
        print("Saliendo del sistema...")
        exit()


def main():
    autenticar = login()
    if autenticar is None:
        return

    id_usuario = autenticar.obtener_id_usuario()
    while True:
        menu(id_usuario)


if __name__ == "__main__":
    main()
