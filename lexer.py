key_words = ['entero', 'decimal', 'booleano', 'cadena', 'sino', 'si', 'mientras', 
             'hacer', 'verdadero', 'falso', 'entonces']
operators = ['+', '-', '*', '/', '%', '==', '<=', '>=', '<', '>', '=']
signs = ['(', ')', '{', '}', '"', ';', ',']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
identifiers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_']

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.token_counts = {}
        self.errors = []

    def next_char(self):
        if self.position < len(self.text):
            result = self.text[self.position]
            self.position += 1
            self.column += 1
            if result == '\n':
                self.line += 1
                self.column = 1
            return result
        return None

    def peek(self):
        if self.position < len(self.text):
            return self.text[self.position]
        return None

    def add_token(self, type, value):
        if type == 'ERROR':
            self.errors.append({
                'type': type,
                'value': value,
                'line': self.line,
                'column': self.column - 1  # Error at the current column
            })
        else:
            if value in self.token_counts:
                self.token_counts[value]['count'] += 1
                # Keep the line and column of the first occurrence
            else:
                self.tokens.append({'type': type, 'value': value, 'line': self.line, 'column': self.column - len(value)})
                self.token_counts[value] = {
                    'type': type,
                    'count': 1,
                    'line': self.line,
                    'column': self.column - len(value)  # Token starts at current column minus its length
                }

    def tokenize(self):
        current_char = self.next_char()

        while current_char is not None:
            if current_char.isspace():
                current_char = self.next_char()
                continue

            if current_char.isalpha() or current_char == '_':
                start_pos = self.position - 1
                while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
                    self.next_char()
                value = self.text[start_pos:self.position].lower()
                token_type = 'KEYWORD' if value in key_words else 'IDENTIFIER'
                self.add_token(token_type, value)

            elif current_char.isdigit():
                start_pos = self.position - 1
                while self.peek() and self.peek().isdigit():
                    self.next_char()
                value = self.text[start_pos:self.position]
                self.add_token('NUMBER', value)

            elif current_char in operators:
                start_pos = self.position - 1
                while self.peek() and (self.text[start_pos:self.position + 1] in operators):
                    self.next_char()
                value = self.text[start_pos:self.position]
                self.add_token('OPERATOR', value)

            elif current_char in signs:
                self.add_token('SIGN', current_char)

            else:
                self.add_token('ERROR', current_char)

            current_char = self.next_char()

        self.tokens.extend(self.errors)
        return self.tokens, self.token_counts
    
    def add_token_in_order(self, type, value):
        if type == 'ERROR':
            self.errors.append({
                'type': type,
                'value': value,
                'line': self.line,
                'column': self.column - 1  # Error at the current column
            })
        else:
            self.tokens.append({'type': type, 'value': value, 'line': self.line, 'column': self.column - len(value)})
            self.token_counts[value] = {
                'type': type,
                'count': 1,
                'line': self.line,
                'column': self.column - len(value)  # Token starts at current column minus its length
            }

    def tokenize_in_order(self):
        current_char = self.next_char()

        while current_char is not None:
            if current_char.isspace():
                current_char = self.next_char()
                continue

            if current_char.isalpha() or current_char == '_':
                start_pos = self.position - 1
                while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
                    self.next_char()
                value = self.text[start_pos:self.position].lower()
                token_type = 'KEYWORD' if value in key_words else 'IDENTIFIER'
                self.add_token_in_order(token_type, value)

            elif current_char.isdigit():
                start_pos = self.position - 1
                while self.peek() and self.peek().isdigit():
                    self.next_char()
                value = self.text[start_pos:self.position]
                self.add_token_in_order('NUMBER', value)

            elif current_char in operators:
                start_pos = self.position - 1
                while self.peek() and (self.text[start_pos:self.position + 1] in operators):
                    self.next_char()
                value = self.text[start_pos:self.position]
                self.add_token_in_order('OPERATOR', value)

            elif current_char in signs:
                self.add_token_in_order('SIGN', current_char)

            else:
                self.add_token_in_order('ERROR', current_char)

            current_char = self.next_char()

        return self.tokens
