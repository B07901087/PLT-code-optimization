# S -> if_stmt | register_op_stmt | assign_stmt | ε
# if_stmt -> IF condition BLOCK statements BLOCK ELSE BLOCK statements BLOCK
# condition -> ID
# statements -> statement statements | ε
# statement -> BREAK | assignment
# assignment -> ID = expr
# expr -> ID | expr + ID | expr - ID

import argparse

class TokenType:
    IF = 'IF'
    ELSE = 'ELSE'
    ID = 'ID'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    BREAK = 'BREAK'
    EQUALS = 'EQUALS'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    EOF = 'EOF'
    REGISTER_OP = 'REGISTER_OP'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    COLON = 'COLON'
    COMMA = 'COMMA'
    NUM = 'NUM'
    KeyWord = 'KeyWord'
    While = 'While'
    CompEqual = 'CompEqual'
    CompNotEqual = 'CompNotEqual'

file_word_to_tokens = {
    "Keyword": "KeyWord",
    "Identifier": "ID",
    "Number": "NUM",
    "Left Parenthesis": "LPAREN",
    "Right Parenthesis": "RPAREN",
    "Comma": "COMMA",
    "Colon": "COLON",
    "Left Curly Brace": "LBRACE",
    "Right Curly Brace": "RBRACE",
    "Register Operation": "REGISTER_OP",
    "Operator": "Operator"
}

### Here we further convert the some keywords to token type with finer granularity
special_keywords = { "register_op", "if", "else", "break", "while"}
keyword_tokentype_conversion = { 
    "register_op": TokenType.REGISTER_OP, 
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "break": TokenType.BREAK,
    "while": TokenType.While
}

### Here we further convert the some operators to token type with finer granularity
special_operators = { "+", "-", "=", "==", "!="}
operator_tokentype_conversion = { 
    "+": TokenType.PLUS, 
    "-": TokenType.MINUS,
    "=": TokenType.EQUALS, 
    "==": TokenType.CompEqual,
    "!=": TokenType.CompNotEqual
}





class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# AST Nodes
class ASTNode:
    pass

###### for registering operation
class RegisterOpNode(ASTNode):
    def __init__(self, op_name, id_name, props):
        self.op_name = op_name
        self.id_name = id_name
        self.props = props

    def __repr__(self):
        return f"RegisterOpNode(op_name={self.op_name}, id_name={self.id_name}, props={self.props})"
    def print_parse(self, depth=0):
        # node type
        print('  ' * depth + f"RegisterOpNode({self.op_name})")
        depth += 1
        # operator and properties
        print('  ' * depth + f"operation_type:")
        self.id_name.print_parse(depth+1)
        print('  ' * depth + f"properties:")
        for prop in self.props:
            prop.print_parse(depth+1)
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"RegisterOpNode({self.op_name})\n")
        depth += 1
        out_file.write('  ' * depth + f"operation_type:\n")
        self.id_name.output_parse(depth+1, out_file)
        out_file.write('  ' * depth + f"properties:\n")
        for prop in self.props:
            prop.output_parse(depth+1, out_file)

class PropNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"PropNode(name={self.name}, value={self.value})"

    def print_parse(self, depth=0):
        print('  ' * depth + f"PropNode")
        depth += 1
        print('  ' * depth + f"name:")
        self.name.print_parse(depth+1)
        print('  ' * depth + f"value:")
        self.value.print_parse(depth+1)
    
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"PropNode\n")
        depth += 1
        out_file.write('  ' * depth + f"name:\n")
        self.name.output_parse(depth+1, out_file)
        out_file.write('  ' * depth + f"value:\n")
        self.value.output_parse(depth+1, out_file)


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumberNode(value={self.value})"
    def print_parse(self, depth=0):
        print('  ' * depth + f"NumberNode(value={self.value})")
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"NumberNode(value={self.value})\n")

class TupleNode(ASTNode):
    def __init__(self, values):
        self.values = values
    def __repr__(self):
        return f"TupleNode(values={self.values})"
    def print_parse(self, depth=0):
        print('  ' * depth + f"TupleNode")
        depth += 1
        print('  ' * depth + f"values:")
        for value in self.values:
            value.print_parse(depth+1)
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"TupleNode\n")
        depth += 1
        out_file.write('  ' * depth + f"values:\n")
        for value in self.values:
            value.output_parse(depth+1, out_file)

##### for while statement 
class WhileNode(ASTNode):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f"WhileNode(condition={self.condition}, statements={self.statements})"

    def print_parse(self, depth=0):
        print('  ' * depth + f"WhileNode")
        depth += 1
        print('  ' * depth + f"condition:")
        self.condition.print_parse(depth+1)
        print('  ' * depth + f"statements:")
        for stmt in self.statements:
            stmt.print_parse(depth+1)
    
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"WhileNode\n")
        depth += 1
        out_file.write('  ' * depth + f"condition:\n")
        self.condition.output_parse(depth+1, out_file)
        out_file.write('  ' * depth + f"statements:\n")
        for stmt in self.statements:
            stmt.output_parse(depth+1, out_file)

##### for if else statement
class IfNode(ASTNode):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"IfNode(condition={self.condition}, true_branch={self.true_branch}, false_branch={self.false_branch})"
    def print_parse(self, depth=0):
        print('  ' * depth + f"IfNode")
        depth += 1
        print('  ' * depth + f"condition:")
        self.condition.print_parse(depth+1)
        print('  ' * depth + f"true_branch:")
        for stmt in self.true_branch:
            stmt.print_parse(depth+1)
        print('  ' * depth + f"false_branch:")
        for stmt in self.false_branch:
            stmt.print_parse(depth+1)
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"IfNode\n")
        depth += 1
        out_file.write('  ' * depth + f"condition:\n")
        self.condition.output_parse(depth+1, out_file)
        out_file.write('  ' * depth + f"true_branch:\n")
        for stmt in self.true_branch:
            stmt.output_parse(depth+1, out_file)
        out_file.write('  ' * depth + f"false_branch:\n")
        for stmt in self.false_branch:
            stmt.output_parse(depth+1, out_file)

class BreakNode(ASTNode):
    def __repr__(self):
        return "BreakNode()"
    def print_parse(self, depth=0):
        print('  ' * depth + f"BreakNode()")
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"BreakNode()\n")

class AssignNode(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
    def __repr__(self):
        return f"AssignNode(variable={self.variable}, expression={self.expression})"
    def print_parse(self, depth=0):
        print('  ' * depth + f"AssignNode(=)")
        depth += 1
        print('  ' * depth + f"variable:")
        self.variable.print_parse(depth+1)
        print('  ' * depth + f"expression:")
        self.expression.print_parse(depth+1)
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"AssignNode(=)\n")
        depth += 1
        out_file.write('  ' * depth + f"variable:\n")
        self.variable.output_parse(depth+1, out_file)
        out_file.write('  ' * depth + f"expression:\n")
        self.expression.output_parse(depth+1, out_file)

class BinOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinOpNode(left={self.left}, operator={self.operator}, right={self.right})"
    
    def print_parse(self, depth=0):
        print('  ' * depth + f"BinOpNode(operator={self.operator})")
        depth += 1
        print('  ' * depth + f"left:")
        self.left.print_parse(depth+1)
        print('  ' * depth + f"right:")
        self.right.print_parse(depth+1)
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"BinOpNode(operator={self.operator})\n")
        depth += 1
        out_file.write('  ' * depth + f"left:\n")
        self.left.output_parse(depth+1, out_file)
        out_file.write('  ' * depth + f"right:\n")
        self.right.output_parse(depth+1, out_file)

class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"VarNode(name={self.name})"
    def print_parse(self, depth=0):
        print('  ' * depth + f"VarNode(name={self.name})")
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"VarNode(name={self.name})\n")

class KeyWordNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"KeyWordNode(name={self.name})"
    def print_parse(self, depth=0):
        print('  ' * depth + f"KeyWordNode(name={self.name})")
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"KeyWordNode(name={self.name})\n")

class IDNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"IDNode(name={self.name})"
    def print_parse(self, depth=0):
        print('  ' * depth + f"IDNode(name={self.name})")
    def output_parse(self, depth=0, out_file=None):
        out_file.write('  ' * depth + f"IDNode(name={self.name})\n")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF)

    def expect(self, token_type):
        if isinstance(token_type, list):
            if self.current_token.type in token_type:
                self.advance()
            else:
                raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")
                # exit(0)
                # raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")
        else:
            if self.current_token.type == token_type:
                self.advance()
            else:
                raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")
                # exit(0)
                # raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")

    def parse(self):
        # program_statements -> statement statements | ε
        # program_statement -> reg_stmt | if_stmt | while_stmt
        ##### these are the supported starting keywords
        supported_starting_types = {TokenType.REGISTER_OP, TokenType.IF, TokenType.While, TokenType.ID}
        
        statements = []
        while self.current_token.type in supported_starting_types:
            if self.current_token.type == TokenType.REGISTER_OP:
                statements.append(self.parse_reg())
            elif self.current_token.type == TokenType.IF:
                statements.append(self.parse_if_stmt())
            elif self.current_token.type == TokenType.While:
                statements.append(self.parse_while_stmt())
            elif self.current_token.type == TokenType.ID:
                statements.append(self.parse_assignment())
            else:
                raise SyntaxError("Expected 'register_op', 'if', 'while', or 'ID'")
                # exit(0)
                # raise SyntaxError("Expected 'register_op', 'if', 'while', or 'ID")
        return statements

    ### this is for registering operation
    def parse_reg(self):
        # reg_stmt -> register_op ID (tu_prop_a)
        if self.current_token.type == TokenType.REGISTER_OP:
            op_name = self.current_token.value
            self.expect(TokenType.REGISTER_OP)
            id_name = IDNode(self.current_token.value)
            self.expect(TokenType.ID)
            self.expect(TokenType.LPAREN)
            props = self.parse_tu_prop_a()
            self.expect(TokenType.RPAREN)
            return RegisterOpNode(op_name, id_name, props)
        else:
            raise SyntaxError("Expected 'register_op'")
            # exit(0)
            # raise SyntaxError("Expected 'register_op'")

    def parse_tu_prop_a(self):
        # tu_prop_a -> prop tu_prop_b
        prop = self.parse_prop()
        more_props = self.parse_tu_prop_b()
        return [prop] + more_props

    def parse_tu_prop_b(self):
        # tu_prop_b -> $ | , prop tu_prop_b
        if self.current_token.type == TokenType.COMMA:
            self.expect(TokenType.COMMA)
            prop = self.parse_prop()
            return [prop] + self.parse_tu_prop_b()
        else:
            return []

    def parse_prop(self):
        # prop -> ID: num_or_tuple
        prop_name = IDNode(self.current_token.value)
        self.expect(TokenType.ID)
        self.expect(TokenType.COLON)
        value = self.parse_num_or_tuple()
        return PropNode(prop_name, value)

    def parse_num_or_tuple(self):
        # num_or_tuple -> num | (list_num_a)
        if self.current_token.type == TokenType.NUM:
            value = float(self.current_token.value)
            self.expect(TokenType.NUM)
            return NumberNode(value)
        elif self.current_token.type == TokenType.LPAREN:
            self.expect(TokenType.LPAREN)
            values = self.parse_list_num_a()
            self.expect(TokenType.RPAREN)
            return TupleNode(values)
        else:
            raise SyntaxError("Expected a number or '('")
            # exit(0)
            # raise SyntaxError("Expected a number or '('")

    def parse_list_num_a(self):
        # list_num_a -> num list_num_b
        num = float(self.current_token.value)
        self.expect(TokenType.NUM)
        more_nums = self.parse_list_num_b()
        return [NumberNode(num)] + more_nums

    def parse_list_num_b(self):
        # list_num_b -> $ | , num list_num_b
        if self.current_token.type == TokenType.COMMA:
            self.expect(TokenType.COMMA)
            num = float(self.current_token.value)
            self.expect(TokenType.NUM)
            return [NumberNode(num)] + self.parse_list_num_b()
        else:
            return []

    #### this is for while statement
    def parse_while_stmt(self):
        # while_stmt -> WHILE condition {general_statements}
        # general_statements -> general_statement general_statements | ε
        # general_statement -> if_stmt | BREAK | assignment | reg_stmt
        self.expect(TokenType.While)
        condition = self.parse_condition()
        self.expect(TokenType.LBRACE)
        statements = self.parse_general_statements()
        self.expect(TokenType.RBRACE)
        return WhileNode(condition, statements)
    
    def parse_general_statements(self):
        # general_statements -> general_statement general_statements | ε
        statements = []
        while self.current_token.type in {TokenType.BREAK, TokenType.ID, TokenType.IF, TokenType.REGISTER_OP}:
            statements.append(self.parse_general_statement())
        return statements

    def parse_general_statement(self):
        # general_statement -> if_stmt | BREAK | assignment | reg_stmt
        if self.current_token.type == TokenType.BREAK:
            self.advance()
            return BreakNode()
        elif self.current_token.type == TokenType.ID:
            return self.parse_assignment()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_stmt()
        elif self.current_token.type == TokenType.REGISTER_OP:
            return self.parse_reg()
        else:
            raise SyntaxError("Expected either 'break', 'ID', 'if', or 'register_op'")
            # exit(0)
            # raise SyntaxError("Expected either 'break', 'ID', 'if', or 'register_op'")

    #### this is for if else statement
    def parse_if_stmt(self):
        # if_stmt -> IF condition {statements} else_stmt
        # else_stmt -> ELSE {statements} | ε
        self.expect(TokenType.IF)
        condition = self.parse_condition()
        self.expect(TokenType.LBRACE)
        true_branch = self.parse_statements()
        self.expect(TokenType.RBRACE)
        # optional else branch
        if self.current_token.type == TokenType.ELSE:
            self.expect(TokenType.ELSE)
            self.expect(TokenType.LBRACE)
            false_branch = self.parse_statements()
            self.expect(TokenType.RBRACE)
        else:
            false_branch = []
        return IfNode(condition, true_branch, false_branch)

    def parse_condition(self):
        # condition -> ID | NUM | ID/NUM ==/!= ID/NUM | KeyWord

        if self.current_token.type == TokenType.KeyWord:
            condition = KeyWordNode(self.current_token.value)
        elif self.current_token.type == TokenType.NUM:
            condition = NumberNode(float(self.current_token.value))
        elif self.current_token.type == TokenType.ID:
            condition = IDNode(self.current_token.value)
        else:
            pass
        last_token_type = self.current_token.type
        self.expect([TokenType.ID, TokenType.NUM, TokenType.KeyWord])
        # Currently we don't support multiple conditions or comparison with complex expressions
        if last_token_type in {TokenType.ID, TokenType.NUM} and self.current_token.type in {TokenType.CompEqual, TokenType.CompNotEqual}:
            operator = self.current_token.type
            self.advance()
            if self.current_token.type == TokenType.ID:
                right = IDNode(self.current_token.value)
            elif self.current_token.type == TokenType.NUM:
                right = NumberNode(float(self.current_token.value))
            else:
                pass
            self.expect([TokenType.ID, TokenType.NUM])
            condition = BinOpNode(condition, operator, right)
        elif last_token_type in {TokenType.KeyWord} and self.current_token.type in {TokenType.CompEqual, TokenType.CompNotEqual}:
            raise SyntaxError("Expected ID or NUM before comparison operator")
            # exit(0)
            # raise SyntaxError("Expected ID or NUM before comparison operator")
        else:
            # print("No comparison operator")
            pass
        return condition

    def parse_statements(self):
        # statements -> statement statements | ε
        statements = []
        while self.current_token.type in {TokenType.BREAK, TokenType.ID, TokenType.REGISTER_OP}:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        # statement -> BREAK | assignment | reg_stmt
        if self.current_token.type == TokenType.BREAK:
            self.advance()
            return BreakNode()
        elif self.current_token.type == TokenType.ID:
            return self.parse_assignment()
        elif self.current_token.type == TokenType.REGISTER_OP:
            return self.parse_reg()
        else:
            raise SyntaxError("Expected 'break', 'ID', or 'register_op'")
            # exit(0)
            # raise SyntaxError("Expected statement")

    def parse_assignment(self):
        # assignment -> ID = expr
        variable = IDNode(self.current_token.value)
        self.expect(TokenType.ID)
        self.expect(TokenType.EQUALS)
        expression = self.parse_expr()
        return AssignNode(variable, expression)

    def parse_expr(self):
        # expr -> ID | expr + ID | expr + NUM | NUM
        # currently only support addition
        if self.current_token.type == TokenType.ID:
            left = IDNode(self.current_token.value)
        elif self.current_token.type == TokenType.NUM:
            left = NumberNode(float(self.current_token.value))
        else:
            pass
        self.expect([TokenType.ID, TokenType.NUM])
        while self.current_token.type == TokenType.PLUS:
            operator = self.current_token.type
            self.advance()
            # right = VarNode(self.current_token.value)
            # self.expect(TokenType.ID)
            if self.current_token.type == TokenType.ID:
                right = IDNode(self.current_token.value)
            elif self.current_token.type == TokenType.NUM:
                right = NumberNode(float(self.current_token.value))
            else:
                pass
            self.expect([TokenType.ID, TokenType.NUM])
            left = BinOpNode(left, operator, right)
        return left




def parse_file(file_path):
    with open(file_path, 'r') as file:
        tokens = []
        for line in file:
            # print(f"line: [{line}]")
            parts = line[1:-2].split(", ")
            # print(f"parts: {parts}")
            if parts[0] in file_word_to_tokens:
                token_name = file_word_to_tokens[parts[0]]
                token_value = parts[1][1:-1]
                #### token type conversion to support finer granularity
                if token_name == "KeyWord":
                    if token_value in special_keywords:
                        tokens.append(Token(keyword_tokentype_conversion[token_value], token_value))
                    else:
                        tokens.append(Token(TokenType.KeyWord, token_value))
                elif token_name == "Operator":
                    if token_value in special_operators:
                        tokens.append(Token(operator_tokentype_conversion[token_value], token_value))
                    else:
                        tokens.append(Token(TokenType.Operator, token_value))
                else:
                    ### other token types
                    tokens.append(Token(file_word_to_tokens[parts[0]], token_value))
            else:
                print("Unknown token:", parts[0])
                exit(0)
    return tokens

if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser(description="A simple argument parser example")

    ####### using parser
    arg_parse.add_argument("-o", "--output", type=str, help="Output file name")
    arg_parse.add_argument("filename", nargs="?", type=str, help="Input file")

    input_file_name = arg_parse.parse_args().filename
    output_file_name = arg_parse.parse_args().output

    if input_file_name is None:
        input_file_name = "simple1.txt"
    
    print("beginning parsing file:", input_file_name)
    my_tokens= parse_file(input_file_name)

    # read tokens and parse
    parser = Parser(my_tokens)
    ast = parser.parse()
    
    # print the AST
    if output_file_name is not None:
        with open(output_file_name, 'w') as out_file:
            for node in ast:
                node.output_parse(0, out_file)
                # out_file.write("\n")
    else:
        for node in ast:
            node.print_parse(0)
            print("")
