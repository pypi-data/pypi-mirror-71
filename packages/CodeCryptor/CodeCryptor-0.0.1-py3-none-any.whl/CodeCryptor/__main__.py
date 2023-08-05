import argparse
import getpass
import pickle
import sys
from os import listdir, path
from os import remove as rmfile
from time import time

import nacl.secret
import nacl.utils
import nacl.pwhash


def checkfile(filename):
    try:
        # OSError if file exists or is invalid
        with open(filename, 'x') as tempfile:
            pass
        rmfile(filename)
        return True
    except OSError:
        return False


def encrypt(file_in, password, file_out, key_file,use_key=False) -> None:
    if not use_key:
        password = password.encode('utf-8')
        kdf = nacl.pwhash.argon2i.kdf
        salt = nacl.utils.random(nacl.pwhash.argon2i.SALTBYTES)
        key = kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt)
        key_file.write(key)
    else:
        key = key_file.read()
    box = nacl.secret.SecretBox(key)
    encrypted = box.encrypt(file_in.read())
    file_out.write(encrypted)


def decrypt(file_in, file_out,key_file) -> None:
    key = key_file.read()
    box = nacl.secret.SecretBox(key)
    file_out.write(box.decrypt(file_in.read()))

def main(args=None):

    #TODO: Add encrypt with Key
    parser = argparse.ArgumentParser()
    parser.add_argument("--decrypt", help="La acción del CodeCryptor",
                        action="store_true", default=False)
    parser.add_argument("--encrypt", help="La acción del CodeCryptor",
                        action="store_true", default=False)
    parser.add_argument("-v", "--verbose", help="Aumenta la información de salida",
                        action="store_true", default=False)
    parser.add_argument("-i", "--input", help="Input file",
                        type=str, default=None)
    parser.add_argument(
        "-o", "--output", help="Output file", type=str, default=None)
    parser.add_argument("--password",
                        help="Llave para encryptar", type=str, default=None)
    parser.add_argument("--key",
                        help="Llave para decryptar", type=str, default=None)
    args = parser.parse_args()

    verbose = args.verbose
    _encrypt = args.encrypt
    _decrypt = args.decrypt
    input_file = args.input
    out_file = args.output
    password = args.password
    key_file = args.key
    use_key = False

    assert (_decrypt or _encrypt
            ), "No se selecciono la acción --decrypt o --encrypt!"
    assert not(_decrypt and _encrypt
               ), "No se puede seleccionar --decrypt y --encrypt al mismo tiempo!"
    assert not(password and key_file
               ), "No se puede seleccionar --pasword y --key al mismo tiempo!"

    assert input_file is not None, "No se selecciono un archivo de entrada"

    if _encrypt:
        assert out_file is not None, "No se selecciono un archivo de salida"
        if password is None:
            print("No se escogió una contraseña para encryptar")
            sys.exit(1)
        if key_file is None and password is not None:
            print("Usando contraseña para encriptar...")
            key_file = "key.key"
        elif key_file is not None and password is None:
            print("Usando llave para encriptar")
            password=None
            use_key = True
            key_file = path.abspath(key_file)
        else:
            key_file = path.abspath(key_file)
            if path.exists(key_file):
                print(
                    "El Archivo de llave de salida ya existe, cuidado con sobreescribirlo!")
                sys.exit(1)
            if not checkfile(key_file):
                print("El Archivo de llave de salida es invalido")
                sys.exit(1)
    elif _decrypt:
        assert key_file is not None, "No se selecciono un archivo de llave para decryptar"
        key_file = path.abspath(key_file)

    input_file = path.abspath(input_file)
    out_file = path.abspath(out_file)

    if not path.isfile(input_file):
        print("El Archivo de entrada no existe o es invalido")
        sys.exit(1)
    if path.exists(out_file):
        print("El Archivo de salida ya existe")
        sys.exit(1)
    if not checkfile(out_file):
        print("El Archivo de salida es invalido")
        sys.exit(1)

    time_start = 0
    if(verbose):
        time_start = time()
    try:
        with open(input_file, 'rb') as in_file, open(out_file, 'wb') as o_file, open(key_file, 'wb' if _encrypt else 'rb') as keyf:
            if(_encrypt):
                encrypt(in_file, password, o_file, keyf,use_key)
                print(
                    "NO OLVIDES GUARDAR EL ARCHIVO {} PARA LUEGO DECRYPTAR EL ARCHIVO".format(key_file))
            elif(_decrypt):
                decrypt(in_file, o_file,keyf)
            else:
                raise "No se selecciono una opción"
    except Exception as e:
        if(verbose):
            print(str(e))
        print("Ocurrio un error durante la operación para {}".format(
            "encryptar" if _encrypt else "decryptar"))
        rmfile(out_file)
        if(_encrypt):
            rmfile(key_file)
        sys.exit(1)

    if(verbose):
        time_end = time()
        print("Operación finalizada en {} segundos".format(time_end-time_start))

if __name__ == "__main__":
    main()