class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.errors = []
        self.declared_variables = set()

    def current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    
    def next_token(self):
        self.current_token_index += 1
        return self.current_token()
    
    def peek_token(self):
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        return None

    def peek_next_token(self):
        if self.current_token_index + 2 < len(self.tokens):
            return self.tokens[self.current_token_index + 2]
        return None

    def raise_error(self, message):
        token = self.current_token()
        if token:
            error_msg = f"Error at line {token['line']}, column {token['column']}: {message}"
        else:
            error_msg = "Error: " + message
        raise SyntaxError(error_msg)

    def add_error(self, message):
        token = self.current_token()
        if token:
            self.errors.append({
                'value': message,
                'type': 'Error',
                'line': token['line'],
                'column': token['column']
            })
        else:
            self.errors.append({
                'value': message,
                'type': 'Error',
                'line': 'Unknown',
                'column': 'Unknown'
            })

    def parse(self):
        results = []
        while self.current_token() is not None:
            if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] in ['entero', 'decimal', 'booleano', 'cadena']:
                # Peek to see if next token is an identifier followed by `(`, indicates a function declaration
                if self.peek_token() and self.peek_token()['type'] == 'IDENTIFIER' and self.peek_next_token() and self.peek_next_token()['value'] == '(':
                    results.append(self.parse_function_declaration())
                else:
                    results.append(self.parse_variable_declaration())
            elif self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'si':
                results.append(self.parse_if_statement())
            elif self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'mientras':
                results.append(self.parse_while_loop())
            elif self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'retornar':
                results.append(self.parse_while_loop())
            elif self.current_token()['type'] == 'IDENTIFIER':
                results.append(self.parse_expression())
            else:
                self.add_error(f"Unexpected token {self.current_token()['value']}")
                self.raise_error(f"Unexpected token {self.current_token()['value']}")
        return results

    def parse_expression(self):
        if self.current_token()['type'] != 'IDENTIFIER':
            self.add_error("Expected identifier at start of expression.")
            self.raise_error("Expected identifier at start of expression.")

        left = self.current_token()['value']

        # Check if the variable has been declared
        if left not in self.declared_variables:
            self.add_error(f"Variable '{left}' not declared.")
            self.raise_error(f"Variable '{left}' not declared.")

        self.next_token()

        if self.current_token()['type'] == 'OPERATOR' and self.current_token()['value'] == '=':
            self.next_token()
            expression = self.parse_complex_expression()
        else:
            self.add_error("Expected '=' after identifier.")
            self.raise_error("Expected '=' after identifier.")

        if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == ';':
            self.next_token()
        else:
            self.add_error("Expected ';' at end of expression.")
            self.raise_error("Expected ';' at end of expression.")

        return {'type': 'assignment', 'identifier': left, 'expression': expression}

    def parse_complex_expression(self):
        elements = []
        if self.current_token()['type'] in ['NUMBER', 'IDENTIFIER']:
            elements.append(self.current_token()['value'])
            self.next_token()
        else:
            self.add_error("Expected a number or identifier after '='.")
            self.raise_error("Expected a number or identifier after '='.")

        while self.current_token()['value'] in ['+', '-', '*', '/', '%']:
            operator = self.current_token()['value']
            self.next_token()
            if self.current_token()['type'] in ['NUMBER', 'IDENTIFIER']:
                elements.append(operator)
                elements.append(self.current_token()['value'])
                self.next_token()
            else:
                self.add_error(f"Expected a number or identifier after operator '{operator}'.")
                self.raise_error(f"Expected a number or identifier after operator '{operator}'.")
        
        if (self.current_token()['value'] == ';' and self.current_token()['type'] == 'SIGN'):
            return elements    
        else:
            self.add_error("Expected ';' at end of expression.")
            self.raise_error("Expected ';' at end of expression.")

        return elements

    def parse_variable_declaration(self):
        node = {'type': 'variable_declaration', 'data': {}}
        if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] in ['entero', 'decimal', 'booleano', 'cadena']:
            var_type = self.current_token()['value']  # Save the type of the variable
            node['data']['type'] = var_type
            self.next_token()  # move to IDENTIFIER
            if self.current_token()['type'] == 'IDENTIFIER':
                identifier = self.current_token()['value']
                node['data']['identifier'] = identifier
                self.declared_variables.add(identifier)  # Add the variable to declared variables set
                self.next_token()  # move to OPERATOR(=)
                if self.current_token()['type'] == 'OPERATOR' and self.current_token()['value'] == '=':
                    self.next_token()  # move to VALUE
                    value_token = self.current_token()
                    if self.validate_type_value_match(var_type, value_token):
                        node['data']['value'] = value_token['value']
                        self.next_token()  # move to SIGN(;)
                        if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == ';':
                            self.next_token()  # Ensure next parsing starts at correct position
                            return node
                        else:
                            self.add_error("Missing semicolon in variable declaration.")
                            self.raise_error("Missing semicolon in variable declaration.")
                    else:
                        self.add_error(f"Type mismatch: Expected a {var_type} value.")
                        self.raise_error(f"Type mismatch: Expected a {var_type} value.")
                else:
                    self.add_error("Missing '=' in variable declaration.")
                    self.raise_error("Missing '=' in variable declaration.")
            else:
                self.add_error("Invalid or missing identifier in variable declaration.")
                self.raise_error("Invalid or missing identifier in variable declaration.")
        return node

    def validate_type_value_match(self, var_type, value_token):
        """Check if the variable type matches the provided value's type."""
        if var_type == 'entero' and (value_token['type'] == 'NUMBER' and '.' not in value_token['value']):
            return True
        elif var_type == 'decimal'  and value_token['type'] == 'NUMBER':
            self.next_token()
            decimal = self.current_token()['value']
            if (decimal[0] == '.'):
                return True
            
            return True
        elif var_type == 'booleano' and (value_token['type'] == 'KEYWORD' and value_token['value'] in ['verdadero', 'falso']):
            return True
        elif var_type == 'cadena' and (value_token['type'] == 'SIGN' and value_token['value'] == '"'):
            self.next_token()
            if self.current_token()['type'] in ['IDENTIFIER', 'NUMBER', 'KEYWORD']:
                self.next_token()
                if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '"':
                    return True
                
        return False

    
    def parse_condition(self):
            node = {'type': 'condition', 'data': {}}
            
            if self.current_token()['type'] == 'IDENTIFIER':
                node['data']['identifier'] = self.current_token()['value']
                self.next_token()
                if self.current_token()['type'] == 'OPERATOR' and self.current_token()['value'] in ['==', '<=', '>=', '<', '>']:
                    node['data']['operation'] = self.current_token()['value']
                    self.next_token()
                    if (self.current_token()['type'] in ['NUMBER', 'IDENTIFIER']) or (self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] in ['falso', 'verdadero']):
                        self.next_token()
                        node['data']['comparison'] = self.current_token()['value']
                        return node
                    else:
                        self.add_error("Missing comparison on the condition.")
                        self.raise_error("Missing comparison on the condition.")
                else:
                    self.add_error("Missing operator on the condition.")
                    self.raise_error("Missing operator on the condition.")
            else:
                self.add_error("Missing identifier on the condition.")
                self.raise_error("Missing identifier on the condition.")

            return node
    
    def parse_statements(self, block_node):
        """Add parsed statements into the statements list of the passed block node."""
        while self.current_token() and self.current_token()['type'] != 'SIGN' or self.current_token()['value'] != '}':
            if self.current_token()['type'] == 'IDENTIFIER':
                block_node['statements'].append(self.parse_expression())
            elif self.current_token()['type'] == 'KEYWORD':
                if self.current_token()['value'] in ['si', 'mientras']:
                    if self.current_token()['value'] == 'si':
                        block_node['statements'].append(self.parse_if_statement())
                    else:
                        block_node['statements'].append(self.parse_while_loop())
                elif self.current_token()['value'] in ['entero', 'decimal', 'booleano', 'cadena']:
                    block_node['statements'].append(self.parse_variable_declaration())
                elif self.current_token()['value'] == 'retornar':
                    block_node['statements'].append(self.parse_return())
                else:
                    self.add_error(f"Unexpected keyword {self.current_token()['value']} in statement block.")
                    self.raise_error(f"Unexpected keyword {self.current_token()['value']} in statement block.")
            else:
                self.next_token()  # Skip unknown tokens or handle errors
    
    def parse_if_statement(self):
        node = {'type': 'if_statement', 'if_block': {'statements': []}, 'else_block': {'statements': []}}

        if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'si':
            self.next_token()  # Move past 'si'
            if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '(':
                self.next_token()
                condition = self.parse_condition()
                node['if_block']['condition'] = condition
                if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == ')':
                    self.next_token()
                    if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'entonces':
                        self.next_token()
                        if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '{':
                            self.next_token()
                            self.parse_statements(node['if_block'])
                            if self.current_token() and self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '}':
                                self.next_token()
                                # Check for 'sino'
                                if self.current_token() and self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] == 'sino':
                                    self.next_token()
                                    if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '{':
                                        self.next_token()
                                        self.parse_statements(node['else_block'])
                                        if self.current_token() and self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '}':
                                            self.next_token()
                                        else:
                                            self.add_error("Expected '}' at the end of else block.")
                                            self.raise_error("Expected '}' at the end of else block.")
                                    else:
                                        self.add_error("Expected '{' after 'sino'.")
                                        self.raise_error("Expected '{' after 'sino'.")
                                return node
                            else:
                                self.add_error("Expected '}' at the end of if block.")
                                self.raise_error("Expected '}' at the end of if block.")
                        else:
                            self.add_error("Expected '{' after 'entonces'.")
                            self.raise_error("Expected '{' after 'entonces'.")
                    else:
                        self.add_error("Expected 'entonces' after condition.")
                        self.raise_error("Expected 'entonces' after condition.")
                else:
                    self.add_error("Expected ')' after condition.")
                    self.raise_error("Expected ')' after condition.")
            else:
                self.add_error("Expected '(' after 'si'.")
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
                            self.parse_statements(node)
                            if self.current_token() and self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == '}':
                                self.next_token()
                                return node
                            else:
                                self.add_error("Expected '}' at the end of statements block.")
                                self.raise_error("Expected '}' at the end of statements block.")
                        else:
                            self.add_error("Expected '{' after 'hacer'.")
                            self.raise_error("Expected '{' after 'hacer'.")
                    else:
                        self.add_error("Expected 'hacer' after condition.")
                        self.raise_error("Expected 'hacer' after condition.")
                else:
                    self.add_error("Expected ')' after condition.")
                    self.raise_error("Expected ')' after condition.")
            else:
                self.add_error("Expected '(' after 'mientras'.")
                self.raise_error("Expected '(' after 'mientras'.")
        return node
    
    def parse_function_declaration(self):
        node = {'type': 'function_declaration', 'data': {}}
        if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] in ['entero', 'decimal', 'booleano', 'cadena']:
            node['data']['return_type'] = self.current_token()['value']
            self.next_token()  # Move to function name
            if self.current_token()['type'] == 'IDENTIFIER':
                node['data']['function_name'] = self.current_token()['value']
                self.next_token()  # Move to `(`

                if self.current_token()['value'] == '(':
                    self.next_token()  # Skip `(` and check for parameters or `)`
                    node['data']['parameters'] = self.parse_parameters()
                    
                    if self.current_token()['value'] == ')':
                        self.next_token()  # Skip `)` and move to `{`
                        if self.current_token()['value'] == '{':
                            self.next_token()  # Enter function body
                            node['statements'] = []
                            while self.current_token() and self.current_token()['value'] != '}':
                                self.parse_statements(node)
                            if self.current_token() and self.current_token()['value'] == '}':
                                self.next_token()  # Close function body
                                return node
                            else:
                                self.add_error("Expected '}' at the end of function declaration.")
                                self.raise_error("Expected '}' at the end of function declaration.")
                        else:
                            self.add_error("Expected '{' after function parameters.")
                            self.raise_error("Expected '{' after function parameters.")
                    else:
                        self.add_error("Expected ')' after function parameters.")
                        self.raise_error("Expected ')' after function parameters.")
                else:
                    self.add_error("Expected '(' after function name.")
                    self.raise_error("Expected '(' after function name.")
            else:
                self.add_error("Expected function name identifier after return type.")
                self.raise_error("Expected function name identifier after return type.")
        return node

    def parse_parameters(self):
        parameters = []
        if self.current_token()['value'] != ')':  # Check if there are any parameters
            while True:
                if self.current_token()['type'] == 'KEYWORD' and self.current_token()['value'] in ['entero', 'decimal', 'booleano', 'cadena']:
                    param_type = self.current_token()['value']
                    self.next_token()
                    if self.current_token()['type'] == 'IDENTIFIER':
                        param_name = self.current_token()['value']
                        parameters.append({'type': param_type, 'name': param_name})
                        self.next_token()
                        if self.current_token()['value'] == ',':
                            self.next_token()  # Move past the comma for the next parameter
                        elif self.current_token()['value'] == ')':
                            break  # End of parameters list
                        else:
                            self.add_error("Expected ',' or ')' in parameter list.")
                            self.raise_error("Expected ',' or ')' in parameter list.")
                    else:
                        self.add_error("Expected an identifier for parameter name.")
                        self.raise_error("Expected an identifier for parameter name.")
                else:
                    self.add_error("Expected a type keyword in parameters.")
                    self.raise_error("Expected a type keyword in parameters.")
        return parameters
    
    def parse_return(self):
        node = {'type': 'return', 'data': {}}
        self.next_token()
        if self.current_token()['type'] == 'IDENTIFIER':
            node['data']['identifier'] = self.current_token()['value']
            self.next_token()
            if self.current_token()['type'] == 'SIGN' and self.current_token()['value'] == ';':
                self.next_token()
                return node
            else:
                self.add_error("Missing semicolon in function return.")
                self.raise_error("Missing semicolon in function return.")
        else:
            self.add_error("Expected identifier after return.")
            self.raise_error("Expected identifier after return.")
                
        return node
    