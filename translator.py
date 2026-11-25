
from lark import Tree


def traducir_expresion(nodo):
    """
    Convierte una expresion de UTEPSA
    a una expresion equivalente en Python.
    """

    tipo = str(nodo.data)

    # Numeros
    if tipo == "number":
        return str(nodo.children[0])

    # Cadenas de texto
    elif tipo == "string":
        return str(nodo.children[0])

    # Variables
    elif tipo == "variable":
        return str(nodo.children[0])

    # Suma
    elif tipo == "add":
        izquierda = traducir_expresion(nodo.children[0])
        derecha = traducir_expresion(nodo.children[1])
        return f"({izquierda} + {derecha})"

    # Resta
    elif tipo == "sub":
        izquierda = traducir_expresion(nodo.children[0])
        derecha = traducir_expresion(nodo.children[1])
        return f"({izquierda} - {derecha})"

    # Multiplicacion
    elif tipo == "mul":
        izquierda = traducir_expresion(nodo.children[0])
        derecha = traducir_expresion(nodo.children[1])
        return f"({izquierda} * {derecha})"

    # Division
    elif tipo == "div":
        izquierda = traducir_expresion(nodo.children[0])
        derecha = traducir_expresion(nodo.children[1])
        return f"({izquierda} / {derecha})"

    # Negacion numerica
    elif tipo == "neg":
        expresion = traducir_expresion(nodo.children[0])
        return f"(-{expresion})"

    # Comparaciones
    elif tipo == "comparison":
        izquierda = traducir_expresion(nodo.children[0])
        operador = str(nodo.children[1])
        derecha = traducir_expresion(nodo.children[2])

        return f"{izquierda} {operador} {derecha}"

    raise ValueError(f"Expresion no reconocida: {tipo}")


def traducir_sentencia(nodo, nivel=0):
    """
    Traduce las instrucciones de UTEPSA.
    """

    tipo = str(nodo.data)
    espacio = "    " * nivel

    # Declaracion de variables
    if tipo == "var_decl":
        nombre = str(nodo.children[0])
        expresion = traducir_expresion(nodo.children[1])

        return [f"{espacio}{nombre} = {expresion}"]

    # Impresion de resultados
    elif tipo == "print_stmt":
        expresion = traducir_expresion(nodo.children[0])

        return [f"{espacio}print({expresion})"]

    # Condicionales
    elif tipo == "if_stmt":
        condicion = traducir_expresion(nodo.children[0])

        lineas = [f"{espacio}if {condicion}:"]

        bloque_if = nodo.children[1]
        contenido_if = traducir_bloque(bloque_if, nivel + 1)

        lineas.extend(contenido_if)

        # Comprobar si existe una alternativa
        if len(nodo.children) > 2 and nodo.children[2] is not None:
            lineas.append(f"{espacio}else:")

            bloque_else = nodo.children[2]
            contenido_else = traducir_bloque(
                bloque_else, nivel + 1
            )

            lineas.extend(contenido_else)

        return lineas

    raise ValueError(f"Instruccion no reconocida: {tipo}")


def traducir_bloque(nodo, nivel=0):
    """
    Traduce todas las instrucciones de un bloque.
    """

    lineas = []

    for hijo in nodo.children:
        lineas.extend(traducir_sentencia(hijo, nivel))

    # Python necesita pass si el bloque esta vacio
    if not lineas:
        lineas.append("    " * nivel + "pass")

    return lineas


def traducir_programa(arbol):
    """
    Punto de entrada del traductor.
    """

    lineas = []

    for instruccion in arbol.children:
        lineas.extend(traducir_sentencia(instruccion))

    return "\n".join(lineas) + "\n"
