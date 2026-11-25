import sys
from pathlib import Path
from lark import Lark
from lark.exceptions import LarkError

from semantic import analizar_semantica, SemanticError
from translator import traducir_programa

BASE_DIR = Path(__file__).resolve().parent


def crear_analizador():
    """Carga la gramatica formal y crea el parser LALR."""
    ruta_gramatica = BASE_DIR / "grammar.lark"
    with open(ruta_gramatica, "r", encoding="utf-8") as archivo:
        gramatica = archivo.read()
    return Lark(gramatica, parser="lalr", start="start")


def compilar(archivo_entrada: Path, archivo_salida: Path = None) -> bool:
    """Ejecuta el pipeline completo de compilacion."""
    if archivo_salida is None:
        archivo_salida = BASE_DIR / "salida.py"

    if not archivo_entrada.exists():
        print(f"Error: El archivo de entrada '{archivo_entrada}' no existe.")
        return False

    with open(archivo_entrada, "r", encoding="utf-8") as archivo:
        codigo = archivo.read()

    try:
        # 1. Analisis sintactico (Lexer + Parser)
        parser = crear_analizador()
        arbol = parser.parse(codigo)
        print("1. Analisis sintactico: Correcto")

        # 2. Analisis semantico (Tabla de simbolos y chequeo de tipos)
        analizar_semantica(arbol)

        # 3. Generacion de codigo (Traduccion a Python)
        codigo_python = traducir_programa(arbol)
        print("\n2. Traduccion a Python: Correcta")
        print("\nCodigo Python generado:")
        print(codigo_python)

        # 4. Guardar archivo generado
        with open(archivo_salida, "w", encoding="utf-8") as archivo:
            archivo.write(codigo_python)

        print(f"Archivo {archivo_salida.name} generado correctamente.")
        return True

    except LarkError as error:
        print("\nError sintactico:")
        print(error)
        return False

    except SemanticError as error:
        print("\nError semantico:")
        print(error)
        return False

    except Exception as error:
        print("\nError durante el procesamiento:")
        print(error)
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.mini>")
        print("Ejemplo: python main.py ejemplos/edades.mini")
        sys.exit(1)

    archivo = Path(sys.argv[1])
    if not archivo.is_absolute():
        archivo = BASE_DIR / archivo

    exito = compilar(archivo)
    if not exito:
        sys.exit(1)
