from parse import Parser
from lexer import Lexer


# Example code text
code_text = """
entero contador = 0;
entero contador2 = 1;
mientras ( contador < 10 ) hacer {
    contador = contador + 1;
    si ( contador == 1 ) entonces {
        contador = contador - 1;
    }
    entero contador3 = 50;
}

booleano flag = verdadero;
si ( flag == 10 ) entonces {
    mientras ( contador >= 5 ) hacer {
        contador = contador - 1;
    }
    booleano flag = verdadero;
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
    parser.parse()
    print("Parsing completed successfully.")
except SyntaxError as e:
    print("Error during parsing:")
    print(e)
