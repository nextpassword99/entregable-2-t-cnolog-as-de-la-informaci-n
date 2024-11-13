# Sistema de Cajero Automático

Este es un sistema de cajero automático simple que permite a los usuarios realizar transacciones básicas como depósitos, retiros y consultar su saldo. Además, los usuarios pueden ver su historial de transacciones y datos personales. Los administradores tienen la capacidad de crear nuevas cuentas de usuario.

## Estructura del Proyecto

El sistema está compuesto por varias clases que gestionan la autenticación, la información del usuario, las operaciones bancarias y el flujo general del programa.

### Clases

#### 1. `Auth`

La clase `Auth` se encarga de la autenticación de los usuarios mediante un código de tarjeta y un PIN.

##### Atributos:

- `code_card`: Código único de la tarjeta del usuario.
- `pin`: PIN de 4 dígitos asociado a la tarjeta del usuario.
- `id_usuario`: Identificador único del usuario autenticado.

##### Métodos:

- `__init__(self, code_card, pin)`: Constructor que inicializa el código de tarjeta, el PIN y el ID de usuario.
- `autenticar()`: Verifica si el código de tarjeta y el PIN coinciden con los datos almacenados en el archivo JSON. Si los datos son correctos, asigna un `id_usuario` y retorna `True`, de lo contrario retorna `False`.
- `obtener_id_usuario()`: Devuelve el ID del usuario autenticado.

#### 2. `Usuario`

La clase `Usuario` maneja la información personal, el saldo y el historial de transacciones de cada usuario.

##### Atributos:

- `id_usuario`: ID único del usuario.
- `nombres`: Nombre del usuario.
- `apellidos`: Apellidos del usuario.
- `rol`: Rol del usuario (ej. "usuario" o "admin").
- `cel`: Número de celular del usuario.
- `email`: Correo electrónico del usuario.
- `saldo`: Saldo disponible en la cuenta del usuario.
- `historial`: Historial de transacciones del usuario.

##### Métodos:

- `__init__(self, id_usuario)`: Constructor que inicializa el ID del usuario y carga los datos desde el archivo `clientes.json`.
- `cargar_datos()`: Carga los datos del usuario desde el archivo JSON.
- Métodos `obtener_*()`: Métodos para obtener los datos personales del usuario: `nombres`, `apellidos`, `rol`, `cel`, `email`, `saldo`, `historial`.

#### 3. `Cajero`

La clase `Cajero` gestiona las operaciones bancarias como depósitos y retiros, y actualiza el saldo y el historial del cliente en el archivo JSON.

##### Atributos:

- `id_usuario`: ID único del usuario.
- `cliente`: Diccionario que contiene los datos del cliente (información personal y saldo).

##### Métodos:

- `__init__(self, id_usuario)`: Constructor que inicializa el ID de usuario y carga los datos del cliente.
- `cargar_cliente()`: Carga los datos del cliente desde el archivo `clientes.json`.
- `guardar_cliente()`: Guarda los datos actualizados del cliente en el archivo JSON.
- `depositar(monto)`: Realiza un depósito en la cuenta del usuario y agrega la transacción al historial.
- `retirar(monto)`: Realiza un retiro de la cuenta del usuario si tiene saldo suficiente. Si no hay suficiente saldo, muestra un mensaje de error.

#### 4. Funciones Auxiliares

- **`crear_usuario()`**: Permite a un administrador crear una nueva cuenta de usuario. Solicita los datos necesarios (nombres, apellidos, celular, email, código de tarjeta, PIN) y guarda la nueva cuenta en el archivo JSON.
- **`generar_id()`**: Genera un ID único para un nuevo usuario basado en el número total de usuarios en el archivo JSON.

- **`login()`**: Maneja el proceso de autenticación del usuario. Permite hasta tres intentos para ingresar el código de tarjeta y PIN correctamente.

- **`menu()`**: Muestra el menú principal del sistema. Dependiendo del rol del usuario (usuario normal o administrador), se muestran diferentes opciones (por ejemplo, crear cuenta solo para administradores).

- **`main()`**: Controla el flujo principal del programa, iniciando el proceso de autenticación y mostrando el menú para el usuario una vez autenticado.

## Estructura de Datos

El sistema guarda la información de los usuarios en un archivo JSON llamado `clientes.json`. El formato del archivo es el siguiente:

```json
{
  "clientes": [
    {
      "id": 1,
      "nombres": "Jorge",
      "apellidos": "Alfaraz Fernandez",
      "rol": "Admin",
      "cel": "999999999",
      "email": "c3wQ2@example.com",
      "code-card": "123456789",
      "pin": "1234",
      "saldo": 1110,
      "historial": [
        {
          "tipo": "deposito",
          "monto": 500,
          "fecha": "2023-01-01"
        },
        {
          "tipo": "retiro",
          "monto": 100,
          "fecha": "2023-01-04"
        }
        {...}
      ]
    },
    {
      "id": 2,
      "nombres": "Alex",
      "apellidos": "Gomez Aroni",
      "cel": "123123123",
      "email": "alex@gmail.com",
      "rol": "usuario",
      "saldo": 0,
      "historial": [],
      "code-card": "123123123",
      "pin": "1234"
    },
    {...}
  ]
}
```
