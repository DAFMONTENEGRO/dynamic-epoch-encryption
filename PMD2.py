import time
import math
import random


def is_prime(num):
    """
    Indica si un numero es primo o no
    :param num: int
        numero
    :return: boolean
        verificacion
    """
    if num > 1:
        for i in range(2, int(math.sqrt(num))+1):
            if not num % i:
                return False
        return True
    else:
        return False


def create_epoch(l_key, l_num, multiplier=2):
    """
    Devuelve un string de los decimales del epoch time
    :param l_key: int
        cantidad de numeros primos en la llave
    :param l_num: int
        maxima cantidad de digitos de un numero en la llave
    :param multiplier: int, optional
        multiplica el intervalo inicial generado para hacer un numero epoch mas grande
        y asegurarse que siempre sea diferente
    :return: str
        decimales del epoch time de longitud 'l_key * l_num * multiplier'
    """
    return str(int((1 + (time.time() % 1)) * 10 ** (l_key * l_num * multiplier)))


def epoch_number_prime(start, l_key, l_num):
    """
    Genera un numero primo por medio de una posicion del epoch time
    :param start: int
        indice inicial del string donde se buscara el numero primo
    :param l_key: int
        cantidad de numeros primos en la llave
    :param l_num: int
        maxima cantidad de digitos de un numero en la llave
    :return: int
        numero primo de maximo l_num digitos y mayor que '5 * 10 ** (l_num-1)' para asegurarse que al
        desencriptar el resultado sea un numero en el rango ASCII
    """
    epoch = create_epoch(l_key, l_num)
    epoch_number = int(epoch[start:start+l_num])
    while not (is_prime(epoch_number) and epoch_number > (5 * 10 ** (l_num-1))):
        epoch = create_epoch(l_key, l_num)
        epoch_number = int(epoch[start:start+l_num])
    return epoch_number


def create_keys(l_key, l_num):
    """
    Crea una llave de numeros primos resultado de la suma de una llave publica y una llave privada
    :param l_key: int
        cantidad de numeros primos en la llave
    :param l_num: int
        maxima cantidad de digitos de un numero en la llave
    :return: tuple(list[int], list[int], list[int])
        tres llaves de l_key elementos
    """
    key = []
    public_key = []
    private_key = []
    for i in range(l_key):
        index = (i * l_num) + 1
        epoch_number = epoch_number_prime(index, l_key, l_num)
        public_key.append(random.randint(0, epoch_number))
        private_key.append(epoch_number-public_key[-1])
        key.append(epoch_number)
    return key, public_key, private_key


def message_to_ascii(message, l_key):
    """
    Convierte un mensaje en una matrix de enteros
    :param message: str
        mensaje a encriptar
    :param l_key: int
        cantidad de numeros primos en la llave
    :return: list[list[int]]
        una matriz de enteros donde la suma de cada fila (representacion de un caracter) es el valor ASCII del caracter
        + 245. Esta suma es necesaria para poder dividir el valor en n enteros y que el maximo valor generado no sea
        superior a 500, esto permite una correcta desencriptacion.
    """
    message_ascii = []
    for char in message:
        sums_ascii = []
        new_ascii = ord(char)+245
        max_random = new_ascii // 2
        for i in range(l_key-1):
            sums_ascii.append(random.randint(1, max_random))
            max_random = (new_ascii-sum(sums_ascii)) // 2
        sums_ascii.append(new_ascii-sum(sums_ascii))
        message_ascii.append(sums_ascii)
    return message_ascii


def verification_sum(key):
    """
    Genera un numero de verificacion para la llave
    :param key: list
        llave de enciptacion de n numeros primos
    :return: int
        el resultado de operar cada elemento de la llave por su indice y hallar el modulo 'len(key)'. Se suma 1 para
        evitar obtener un 0 como numero de verificacion
    """
    verification = 0
    for i, k in enumerate(key):
        verification += (i+1) * k
    return (verification % len(key)) + 1


def encrypt(message, l_key=12, l_num=3, step=1, max_l_key=24):
    """
    Encripta un mensaje recibido
    :param message: str
        mensaje a encriptar
    :param l_key: int, optional
        cantidad de numeros primos en la llave
    :param l_num: int, optional
        maxima cantidad de digitos de un numero en la llave
    :param step: int, optional
        paso dinamico de enciptacion. Es una constante de cambio que controla el crecimiento del numero de verificacion
        en cada suma parcial de la encriptacion.
    :param max_l_key: int, optional
        valor por defecto del algoritmo que limita la longitud de las llaves
    :return: tuple(list[str], int, list[int], list[int], list[int])
        list[str] (enconding) paquetes resultado de la encriptacion de cada caracter
        int (verification)  numero verificacion. Ver algoritmo 'verification_sum(key)'
        list[int] (key, public_key, private_key) Llaves de encriptacion. Ver algoritmo 'create_keys(l_key, l_num)'
    """
    if l_num < 3:
        l_num = 3
    l_key = l_key % max_l_key
    message_ascii = message_to_ascii(message, l_key)
    key, public_key, private_key = create_keys(l_key, l_num)
    verification = verification_sum(key)
    enconding = []
    for char in message_ascii:
        code = ""
        for i, k in enumerate(key):
            code += str((verification * char[i]) % k) + "."  # 2.2.1. Pequeño teorema de Fermat de README
            verification += step
        enconding.append(code)
    verification -= len(message) * l_key
    return enconding, verification, key, public_key, private_key


def enconding_to_numbers(enconding):
    """
    Convierte los paquetes de la encriptacion en su correspondiente lista de enteros
    :param enconding: list[str]
        paquetes resultado de la encriptacion de cada caracter
    :return: list[list[int]]
        la matrix correspondiente a los enteros de todos los paquetes. Cada paquete es la representacion de un caracter
    """
    numbers = []
    for code in enconding:
        char_number = [int(num) for num in code[:-1].split(".")]
        numbers.append(char_number)
    return numbers


def decrypt(enconding, public_key, private_key, step=1):
    """
    Desencripta el mensaje cifrado
    :param enconding: list[str]
        paquetes resultado de la encriptacion de cada caracter
    :param public_key: list[int]
        llave publica que genera el encriptador
    :param private_key: list[int]
        llave privada que genera el encriptador (llave local)
    :param step: int, optional
        paso dinamico de enciptacion. Es una constante de cambio que controla el crecimiento del numero de verificacion
        en cada suma parcial de la encriptacion.
    :return: str
        mensaje original
    """
    key = [public_key[i] + private_key[i] for i in range(len(private_key))]
    verification = verification_sum(key)
    enconding_numbers = enconding_to_numbers(enconding)
    message = ""
    for char in enconding_numbers:
        sums_ascii = 0
        for i, number in enumerate(char):
            inv_mod_verf = pow(verification, -1, key[i])
            sums_ascii += (inv_mod_verf * number) % key[i]
            verification += step
        message += chr(sums_ascii-245)
    return message


# ------------------------ CONFIGURACION EXPERIMENTAL ------------------------ #

stp = 1  # Paso dinamico del encriptador
length_key = 12  # Longitud que tendran las claves
length_numbers = 4  # Longitud maxima de digitos que tendran los primos en la clave
msg = "HACKEADO"  # Mensaje que se encriptara

encding, verf, prime_key, publi_key, priv_key = encrypt(msg, length_key, length_numbers, stp)
print("\nINFORMACION ENCRIPTACION:")
print("    Paso dinamico:", stp)
print("    Longitud de la clave:", length_key)
print("    Cantidad maxima de digitos en los primos:", length_numbers)
print("    Mensaje a encriptar: '{}'".format(msg))
print("    Numero de verificacion de la clave:", verf)
print("    Clave de encriptacion:", prime_key)
print("    Clave privada generada:", priv_key)
print("    Clave publica generada:", publi_key)
print("\nDETALLE ENCRIPTACION:")
for ic, cod in enumerate(encding):
    print("    Caracter #{} '{}': {}".format(ic+1, msg[ic], cod))

dcrypt = decrypt(encding, publi_key, priv_key, stp)
print("\nDETALLE DESENCRIPTACION:")
print("    Mensaje a desencriptar: #{} paquetes".format(len(encding)))
for cod in encding:
    print("        +", cod)
print("    Paso dinamico:", stp)
print("    Clave privada local:", priv_key)
print("    Clave publica obtenida:", publi_key)
print("    Mensaje desencriptado:", dcrypt)

# ------------------------ CONFIGURACION EXPERIMENTAL ------------------------ #
