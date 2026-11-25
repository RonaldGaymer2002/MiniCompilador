
import sys
from pathlib import Path
from lark import Lark

from semantic import analizar_semantica, SemanticError
from translator import traducir_programa


# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Verificar que se haya indicado un archivo
if len(sys.argv) < 2:
    print("Error: Debes indicar un archivo .mini")
    sys.exit(1)

# Obtener el archivo de entrada
ARCHIVO_ENTRADA = Path(sys.argv[1])

if not ARCHIVO_ENTRADA.is_absolute():
    ARCHIVO_ENTRADA = BASE_DIR / ARCHIVO_ENTRADA

# Archivo de salida
ARCHIVO_SALIDA = BASE_DIR / "salida.py"


# 1. Cargar la gramatica
with open(BASE_DIR / "grammar.lark", "r", encoding="utf-8") as archivo:
    gramatica = archivo.read()


# 2. Crear el analizador
parser = Lark(
    gramatica,
    parser="lalr",
    start="start"
)


try:
    # Leer el codigo fuente
    with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as archivo:
        codigo = archivo.read()

    # 3. Analisis sintactico
    arbol = parser.parse(codigo)
    

    print("1. Analisis sintactico: Correcto")

    # 4. Analisis semantico
    analizar_semantica(arbol)

    # 5. Traduccion
    codigo_python = traducir_programa(arbol)

    print("\n2. Traduccion a Python: Correcta")
    print("\nCodigo Python generado:")
    print(codigo_python)

    # 6. Guardar el resultado
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as archivo:
        archivo.write(codigo_python)

    print("Archivo salida.py generado correctamente.")

except SemanticError as error:
    print("\nError semantico:")
    print(error)

except Exception as error:
    print("\nError durante el procesamiento:")
    print(error)
