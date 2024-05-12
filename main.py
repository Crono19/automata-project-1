from parse import Parser
from lexer import Lexer


# Example code text
code_text = """
cadena string = "hi world";
entero contador2 = 1;
mientras ( contador == 1 ) hacer {
    contador = contador + 1;
    si ( contador == 1 ) entonces {
        contador = contador - 1;
    }
    entero contador3 = 50;
}

cadena string = "hi world";
booleano flag = verdadero;
si ( flag == falso ) entonces {
    mientras ( contador >= 5 ) hacer {
        contador = contador - 1;
    }
    cadena string = "hi world";
    booleano flag = verdadero;
}

entero funcion(booleano flag, entero a, decimal q) {
    contador = 2 * 5 + 9 - 1;
}
"""

# Initialize the lexer with the code text
lexer = Lexer(code_text)

# Generate tokens
tokens = lexer.tokenize_in_order()

# Assuming the Parser class has been appropriately defined and imported
parser = Parser(tokens)

# Parse the tokens
try:
    print("Parsing completed successfully.")
except SyntaxError as e:
    print("Error during parsing:")
    print(e)
