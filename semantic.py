
from lark import Tree


class SemanticError(Exception):
    """Representa un error semantico."""
    pass


# Tabla de simbolos
tabla_simbolos = {}


def verificar_expresion(nodo):
    """

    """

    if not isinstance(nodo, Tree):
        return None

    tipo_nodo = str(nodo.data)

    # Numeros
    if tipo_nodo == "number":
        return "number"

    # Cadenas de texto
    elif tipo_nodo == "string":
        return "string"

    # Variables
    elif tipo_nodo == "variable":
        nombre = str(nodo.children[0])

        if nombre not in tabla_simbolos:
            raise SemanticError(
                f"La variable '{nombre}' no ha sido declarada."
            )

        return tabla_simbolos[nombre]

    # Negacion numerica
    elif tipo_nodo == "neg":
        tipo = verificar_expresion(nodo.children[0])

        if tipo != "number":
            raise SemanticError(
                "La negacion solo puede utilizarse con numeros."
            )

        return "number"

    # Operaciones aritmeticas
    elif tipo_nodo in ("add", "sub", "mul", "div"):

        izquierda = verificar_expresion(nodo.children[0])
        derecha = verificar_expresion(nodo.children[1])

        if izquierda != "number" or derecha != "number":
            raise SemanticError(
                "Las operaciones aritmeticas solo admiten numeros."
            )

        return "number"

    # Comparaciones
    elif tipo_nodo == "comparison":

        izquierda = verificar_expresion(nodo.children[0])
        derecha = verificar_expresion(nodo.children[2])

        if izquierda != derecha:
            raise SemanticError(
                "No se pueden comparar tipos de datos diferentes."
            )

        return "boolean"

    return None


def analizar_sentencia(nodo):
    """Analiza las instrucciones del programa."""

    tipo_nodo = str(nodo.data)

    # Declaracion de variables
    if tipo_nodo == "var_decl":

        nombre = str(nodo.children[0])
        expresion = nodo.children[1]

        if nombre in tabla_simbolos:
            raise SemanticError(
                f"La variable '{nombre}' ya fue declarada."
            )

        tipo = verificar_expresion(expresion)

        tabla_simbolos[nombre] = tipo

    # Impresion de resultados
    elif tipo_nodo == "print_stmt":

        expresion = nodo.children[0]
        verificar_expresion(expresion)

    # Condicionales
    elif tipo_nodo == "if_stmt":

        condicion = nodo.children[0]
        tipo = verificar_expresion(condicion)

        if tipo != "boolean":
            raise SemanticError(
                "La condicion debe ser una comparacion."
            )

        for hijo in nodo.children[1:]:
            if isinstance(hijo, Tree):
                analizar_sentencia(hijo)

    # Bloques de instrucciones
    elif tipo_nodo in ("start", "block"):

        for hijo in nodo.children:
            if isinstance(hijo, Tree):
                analizar_sentencia(hijo)


def analizar_semantica(arbol):
    """Punto de entrada del analisis semantico."""

    tabla_simbolos.clear()

    analizar_sentencia(arbol)

    print("Analisis semantico correcto")

    print("\nTabla de simbolos:")

    for nombre, tipo in tabla_simbolos.items():
        print(f"{nombre}: {tipo}")
