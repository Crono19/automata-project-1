class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    
    def next_token(self):
        self.current_token_index += 1
        return self.current_token()

    def raise_error(self, message):
        token = self.current_token()
        if token:
            error_msg = f"Error at line {token['line']}, column {token['column']}: {message}"
        else:
            error_msg = "Error: " + message
        raise SyntaxError(error_msg)

    def parse(self):
        results = []
        while self.current_token() is not None:
            if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] in ['entero', 'decimal', 'booleano', 'cadena']:
                results.append(self.parse_variable_declaration())
            elif self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'si':
                results.append(self.parse_if_statement())
            elif self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'mientras':
                results.append(self.parse_while_loop())
            elif self.current_token()['type'] == 'IDENTIFIER':
                results.append(self.parse_expression())
            else:
                self.raise_error(f"Unexpected token {self.current_token()['value']}")
            # Next token is managed by individual parse functions
        return results
    

    def parse_expression(self):
        if self.current_token()['type'] != 'IDENTIFIER':
            self.raise_error("Expected identifier at start of expression.")

        left = self.current_token()['value']
        self.next_token()

        if self.current_token()['type'] == 'OPERATOR' and self.current_token()['value'] == '=':
            self.next_token()
            expression = self.parse_complex_expression()
        else:
            self.raise_error("Expected '=' after identifier.")

        if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == ';':
            self.next_token()
        else:
            self.raise_error("Expected ';' at end of expression.")

        return {'type': 'assignment', 'identifier': left, 'expression': expression}

    def parse_complex_expression(self):
        elements = []
        if self.current_token()['type'] in ['NUMBER', 'IDENTIFIER']:
            elements.append(self.current_token()['value'])
            self.next_token()
        else:
            self.raise_error("Expected a number or identifier after '='.")

        while self.current_token()['value'] in ['+', '-', '*', '/', '%']:
            operator = self.current_token()['value']
            self.next_token()
            if self.current_token()['type'] in ['NUMBER', 'IDENTIFIER']:
                elements.append(operator)
                elements.append(self.current_token()['value'])
                self.next_token()
            else:
                self.raise_error(f"Expected a number or identifier after operator '{operator}'.")

        return elements

    def parse_variable_declaration(self):
        node = {'type': 'variable_declaration', 'data': {}}
        if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] in ['entero', 'decimal', 'booleano', 'cadena']:
            node['data']['type'] = self.current_token()['value']
            self.next_token()  # move to IDENTIFIER
            if self.current_token()['type'] == 'IDENTIFIER':
                node['data']['identifier'] = self.current_token()['value']
                self.next_token()  # move to OPERATOR(=)
                if self.current_token()['type'] == 'OPERATOR' and self.current_token()['value'] == '=':
                    self.next_token()  # move to VALUE
                    if (self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] in ['verdadero', 'falso']) or (self.current_token()['type'] in ['NUMBER', 'IDENTIFIER']):
                        node['data']['value'] = self.current_token()['value']
                        self.next_token()  # move to SIGN(;)
                        if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == ';':
                            self.next_token()  # Ensure next parsing starts at correct position
                            return node
                        else:
                            self.raise_error("Missing semicolon in variable declaration.")
                    else:
                        self.raise_error("Invalid or missing value in variable declaration.")
                else:
                    self.raise_error("Missing '=' in variable declaration.")
            else:
                self.raise_error("Invalid or missing identifier in variable declaration.")
        return node
    
    def parse_condition(self):
        node = {'type': 'condition', 'data': {}}
        
        if self.current_token()['type'] == 'IDENTIFIER':
            node['data']['identifier'] = self.current_token()['value']
            self.next_token()
            if self.current_token()['type'] == 'OPERATOR' and self.current_token()['value'] in ['==', '<=', '>=', '<', '>']:
                node['data']['operation'] = self.current_token()['value']
                self.next_token()
                if self.current_token()['type'] in ['NUMBER', 'IDENTIFIER']:
                    self.next_token()
                    node['data']['comparison'] = self.current_token()['value']
                    return node
                else:
                    self.raise_error("Missing comparison on the condition.")
            else:
                self.raise_error("Missing operator on the condition.")
        else:
            self.raise_error("Missing identifier on the condition.")

        return node
    
    def parse_statements(self, block_node):
        """Add parsed statements into the statements list of the passed block node."""
        current_statements = block_node['statements']
        if self.current_token()['type'] == 'IDENTIFIER':
            current_statements.append(self.parse_expression())
        elif self.current_token()['type'] == 'KEYWORD':
            if self.current_token()['value'] in ['si', 'mientras']:
                if self.current_token()['value'] == 'si':
                    current_statements.append(self.parse_if_statement())
                else:
                    current_statements.append(self.parse_while_loop())
            elif self.current_token()['value'] in ['entero', 'decimal', 'booleano', 'cadena']:
                current_statements.append(self.parse_variable_declaration())
            else:
                self.raise_error(f"Unexpected keyword {self.current_token()['value']} in statement block.")
        else:
            self.next_token()  # Skip unknown tokens or handle errors
    
    def parse_if_statement(self):
        node = {'type': 'if_statement', 'statements': [], 'data': {}}
        if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'si':
            self.next_token()
            if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '(':
                self.next_token()
                node['data']['condition'] = self.parse_condition()
                if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == ')':
                    self.next_token()
                    if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'entonces':
                        self.next_token()
                        if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '{':
                            self.next_token()
                            while self.current_token() and (self.current_token()['type'] != 'SIGN' or self.current_token()['value'] != '}'):
                                self.parse_statements(node)
                            if self.current_token() and self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '}':
                                self.next_token()
                                return node
                            else:
                                self.raise_error("Expected '}' at the end of the statements block.")
                        else:
                            self.raise_error("Expected '{' after 'entonces'.")
                    else:
                        self.raise_error("Expected 'entonces' after condition.")
                else:
                    self.raise_error("Expected ')' after condition.")
            else:
                self.raise_error("Expected '(' after 'si'.")
        return node

    def parse_while_loop(self):
        node = {'type': 'while_loop', 'statements': [], 'data': {}}
        if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'mientras':
            self.next_token()
            if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '(':
                self.next_token()
                node['data']['condition'] = self.parse_condition()
                if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == ')':
                    self.next_token()
                    if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'hacer':
                        self.next_token()
                        if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '{':
                            self.next_token()
                            while self.current_token() and (self.current_token()['type'] != 'SIGN' or self.current_token()['value'] != '}'):
                                self.parse_statements(node)
                            if self.current_token() and self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '}':
                                self.next_token()
                                return node
                            else:
                                self.raise_error("Expected '}' at the end of statements block.")
                        else:
                            self.raise_error("Expected '{' after 'hacer'.")
                    else:
                        self.raise_error("Expected 'hacer' after condition.")
                else:
                    self.raise_error("Expected ')' after condition.")
            else:
                self.raise_error("Expected '(' after 'mientras'.")
        return node