import re
import argparse

enable_optimization = True
opt_constant_propagation = True
opt_common_subexpression_elimination = True
opt_constant_folding = True
opt_dead_code_elimination = True
opt_multipass_optimization = False
opt_accelerator_reuse = False
opt_accelerator_delegate = False
opt_operator_fusion = True
num_iteration = 3

def is_number(s):
    pattern = r'^-?\d+(\.\d+)?$'
    return bool(re.match(pattern, s))

def look_up_symbol_table(var_name, symbol_tables):
    # traverse in reversed order
    for symbol_table in reversed(symbol_tables):
        if var_name in symbol_table:
            return True
    return False

# AST Nodes
class ASTNode:
    pass

class RegisterOpNode(ASTNode):
    def __init__(self, op_name, props):
        self.op_name = op_name
        self.props = props

    def __repr__(self):
        return f"RegisterOpNode(op_name={self.op_name}, props={self.props})"
    
    def pr(self, depth=0):
        tmp_list = [self.op_name]
        for key, value in self.props.items():
            t_value = tuple(value) 
            tmp_list.append(key)
            tmp_list.append(t_value)

        the_key = tuple(tmp_list) 
        spacex = " " 

        the_key = tuple(tmp_list)  
        print(f"{spacex*depth}if {str(the_key)} in operations:")
        depth += 4
        print(f"{spacex*depth}operations[{str(the_key)}] += 1")
        depth -= 4
        print(f"{spacex*depth}else:")
        depth += 4
        print(f"{spacex*depth}operations[{str(the_key)}] = 1")
        depth -= 4
    
    def write_file(self, depth=0, fout=None):
        tmp_list = [self.op_name]
        for key, value in self.props.items():
            t_value = tuple(value) 
            tmp_list.append(key)
            tmp_list.append(t_value)

        the_key = tuple(tmp_list) 
        spacex = " " 
        fout.write(f"{spacex*depth}if {str(the_key)} in operations:\n")
        depth += 4
        if opt_accelerator_reuse:
            fout.write(f"{spacex*depth}operations[{str(the_key)}] = 1\n")
        else:
            fout.write(f"{spacex*depth}operations[{str(the_key)}] += 1\n")
        depth -= 4
        fout.write(f"{spacex*depth}else:\n")
        depth += 4
        fout.write(f"{spacex*depth}operations[{str(the_key)}] = 1\n")
        depth -= 4


    

class PropNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"PropNode(name={self.name}, value={self.value})"

    


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumberNode(value={self.value})"
    

class TupleNode(ASTNode):
    def __init__(self, values):
        self.values = values
    def __repr__(self):
        return f"TupleNode(values={self.values})"
    

##### for while statement 
class WhileNode(ASTNode):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f"WhileNode(condition={self.condition}, statements={self.statements})"
    
    def pr(self, depth=0):
        print('  ' * depth + f"while {self.condition.pv()}:")
        for stmt in self.statements:
            # print(stmt)
            stmt.pr(depth+4)

    def write_file(self, depth=0, fout=None):
        fout.write('  ' * depth + f"while {self.condition.pv()}:\n")
        for stmt in self.statements:
            stmt.write_file(depth+4, fout)

    def forward_propagation(self, symbols=[]):
        # check whether all symbols are defined
        # check condition
        # create symbol table for the local scope

        huan_count = 0

        while huan_count < num_iteration:
            huan_count += 1

            symbols.append({})

            if isinstance(self.condition, BinOpNode):
                if not look_up_symbol_table(self.condition.left, symbols) and not is_number(self.condition.left):
                    raise ValueError(f"Error: {self.condition.left} is not defined in the condition (while)")
                if not look_up_symbol_table(self.condition.right, symbols) and not is_number(self.condition.right):
                    raise ValueError(f"Error: {self.condition.right} is not defined in the condition (while)")


            # do common subexpression elimination and constant propagation
            



            # check statements
            # also perform constant propagation for statements inside while loop
            constant_table = {}
            expression_table = {}
            
            for stmt in self.statements:
                if isinstance(stmt, AssignNode):
                    if isinstance(stmt.expression, BinOpNode):
                        if not look_up_symbol_table(stmt.expression.left, symbols) and not is_number(stmt.expression.left):
                            raise ValueError(f"Error: {stmt.expression.left} is not defined in the expression (assign)")
                        if not look_up_symbol_table(stmt.expression.right, symbols) and not is_number(stmt.expression.right):
                            raise ValueError(f"Error: {stmt.expression.right} is not defined in the expression (assign)")
                        
                        commoned = False
                        if enable_optimization:
                            

                            # # common subexpression elimination
                            if stmt.expression.pv() in expression_table and opt_common_subexpression_elimination:
                                print(f"Replace Common subexpression: {stmt.expression} with {expression_table[stmt.expression.pv()]}")
                                stmt.expression = expression_table[stmt.expression.pv()]
                                commoned = True
                            else:
                                # constant propagation
                                if stmt.expression.left in constant_table and opt_constant_propagation:
                                    stmt.expression.left = constant_table[stmt.expression.left]
                                if stmt.expression.right in constant_table and opt_constant_propagation:
                                    stmt.expression.right = constant_table[stmt.expression.right]

                            # update common subexpression table
                            if not commoned:
                                # print(f"this is the expression: {stmt.expression}")
                                if stmt.expression not in expression_table:
                                    expression_table[stmt.expression.pv()] = stmt.variable
                                    print(f"expression_table: {expression_table}")

                    elif not look_up_symbol_table(stmt.expression, symbols) and not is_number(stmt.expression):
                        raise ValueError(f"Error: {stmt.expression} is not defined in the expression (while)")
                    else:
                        # try to replace the variable with the constant
                        #TPH: here
                        if enable_optimization and stmt.expression in constant_table:
                            stmt.expression = constant_table[stmt.expression]
                        # if enable_optimization and stmt.expression in expression_table:
                        #     stmt.expression = expression_table[stmt.expression]
                        pass
                    # define variable in the local symbol table if it's not defined
                    if not look_up_symbol_table(stmt.variable, symbols):
                        symbols[-1][stmt.variable] = stmt.expression
                    # needed by constant propagation
                    if not isinstance(stmt.expression, BinOpNode) and is_number(stmt.expression):
                        constant_table[stmt.variable] = stmt.expression
                    print(f"constant_table: {constant_table}")
                elif isinstance(stmt, IfNode):
                    stmt.forward_propagation(symbols)
                elif isinstance(stmt, WhileNode):
                    stmt.forward_propagation(symbols)
                else:
                    pass

            # backward propagation for dead code elimination (currently only support assignment)
            # applied use/def chain
            print("start dead code elimination...")
            live_vars = set()
            if enable_optimization:
                for stmt in reversed(self.statements):
                    if isinstance(stmt, AssignNode):
                        # remove the variable from the live_vars
                        if stmt.variable in live_vars:
                            live_vars.remove(stmt.variable)
                        else:
                            # dead code, only consider removing local variables
                            if stmt.variable in symbols[-1]:
                                print(f"Dead code: {stmt}")
                                self.statements.remove(stmt)

                        # add the experssion to the live_vars
                        if isinstance(stmt.expression, BinOpNode):
                            print(f"this is the current expression: {stmt.expression}")
                            if stmt.expression.left in constant_table or not is_number(stmt.expression.left): 
                                live_vars.add(stmt.expression.left)
                            if stmt.expression.right in constant_table or not is_number(stmt.expression.right):
                                live_vars.add(stmt.expression.right)
                        else:
                            # print(f"this is the current expression (else): {stmt.expression}")
                            live_vars.add(stmt.expression)
                    
            # a final pass for constant folding
            if enable_optimization and opt_constant_folding:
                for stmt in self.statements:
                    if isinstance(stmt, AssignNode):
                        if isinstance(stmt.expression, BinOpNode):
                            print(f"this is the current expression (constant folding): {stmt.expression}")
                            if is_number(stmt.expression.left) and is_number(stmt.expression.right):
                                left_num = float(stmt.expression.left)
                                right_num = float(stmt.expression.right)
                                if stmt.expression.operator == "PLUS":
                                    stmt.expression = str(left_num + right_num)
                                elif stmt.expression.operator == "CompEqual":
                                    stmt.expression = str(left_num == right_num)
                                elif stmt.expression.operator == "CompNotEqual":
                                    stmt.expression = str(left_num != right_num)



            # remove the symbol table for the local scope
            symbols.pop()
            if not opt_multipass_optimization:
                break


##### for if else statement
class IfNode(ASTNode):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"IfNode(condition={self.condition}, true_branch={self.true_branch}, false_branch={self.false_branch})"
    
    def pr(self, depth=0):
        print(' ' * depth + f"if {self.condition.pv()}:")
        for stmt in self.true_branch:
            stmt.pr(depth+4)
        if self.false_branch:
            print('  ' * depth + f"else:")
            for stmt in self.false_branch:
                stmt.pr(depth+4)
    
    def write_file(self, depth=0, fout=None):
        fout.write(' ' * depth + f"if {self.condition.pv()}:\n")
        for stmt in self.true_branch:
            stmt.write_file(depth+4, fout)
        if self.false_branch:
            fout.write('  ' * depth + f"else:\n")
            for stmt in self.false_branch:
                stmt.write_file(depth+4, fout)

    def forward_propagation(self, symbols=[]):
        # check whether all symbols are defined
        # check condition
        # create symbol table for the local scope
        symbols.append({})

        # check the condition
        if isinstance(self.condition, BinOpNode):
            if not look_up_symbol_table(self.condition.left, symbols) and not is_number(self.condition.left):
                raise ValueError(f"Error: {self.condition.left} is not defined in the condition (if)")
            if not look_up_symbol_table(self.condition.right, symbols) and not is_number(self.condition.right):
                raise ValueError(f"Error: {self.condition.right} is not defined in the condition (if)")

        # check true branch
        for stmt in self.true_branch:
            if isinstance(stmt, AssignNode):
                if isinstance(stmt.expression, BinOpNode):
                    if not look_up_symbol_table(stmt.expression.left, symbols) and not is_number(stmt.expression.left):
                        raise ValueError(f"Error: {stmt.expression.left} is not defined in the true (if)")
                    if not look_up_symbol_table(stmt.expression.right, symbols) and not is_number(stmt.expression.right):
                        raise ValueError(f"Error: {stmt.expression.right} is not defined in the true (if)")
                elif not look_up_symbol_table(stmt.expression, symbols) and not is_number(stmt.expression):
                    raise ValueError(f"Error: {stmt.expression} is not defined in the expression (if)")
                else:
                    pass
                # define variable in the local symbol table if it's not defined
                if not look_up_symbol_table(stmt.variable, symbols):
                    symbols[-1][stmt.variable] = stmt.expression
            elif isinstance(stmt, IfNode):
                stmt.forward_propagation(symbols)
            elif isinstance(stmt, WhileNode):
                stmt.forward_propagation(symbols)
            else:
                pass

        # check false branch
        for stmt in self.false_branch:
            if isinstance(stmt, AssignNode):
                if isinstance(stmt.expression, BinOpNode):
                    if not look_up_symbol_table(stmt.expression.left, symbols) and not is_number(stmt.expression.left):
                        raise ValueError(f"Error: {stmt.expression.left} is not defined in the true (if)")
                    if not look_up_symbol_table(stmt.expression.right, symbols) and not is_number(stmt.expression.right):
                        raise ValueError(f"Error: {stmt.expression.right} is not defined in the true (if)")
                elif not look_up_symbol_table(stmt.expression, symbols) and not is_number(stmt.expression):
                    raise ValueError(f"Error: {stmt.expression} is not defined in the expression (if)")
                else:
                    pass
                # define variable in the local symbol table if it's not defined
                if not look_up_symbol_table(stmt.variable, symbols):
                    symbols[-1][stmt.variable] = stmt.expression
            elif isinstance(stmt, IfNode):
                stmt.forward_propagation(symbols)
            elif isinstance(stmt, WhileNode):
                stmt.forward_propagation(symbols)
            else:
                pass

        # remove the symbol table for the local scope
        symbols.pop()

class BreakNode(ASTNode):
    def __repr__(self):
        return "BreakNode()"
    def pr(self, depth=0):
        print(' ' * depth + "break")

    def write_file(self, depth=0, fout=None):
        fout.write(' ' * depth + "break\n")
    

class AssignNode(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
    def __repr__(self):
        return f"AssignNode(variable={self.variable}, expression={self.expression})"
    
    def pr(self, depth=0):
        if not isinstance(self.expression, BinOpNode):
            print(' ' * depth + f"{self.variable} = {self.expression}")
        else:
            print(' ' * depth + f"{self.variable} = {self.expression.pv()}")

    def write_file(self, depth=0, fout=None):
        if not isinstance(self.expression, BinOpNode):
            fout.write(' ' * depth + f"{self.variable} = {self.expression}\n")
        else:
            fout.write(' ' * depth + f"{self.variable} = {self.expression.pv()}\n")
    
class BinOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinOpNode(left={self.left}, operator={self.operator}, right={self.right})"
    
    def pv(self, depth=0):
        if self.operator == "PLUS":
            return f"{self.left} + {self.right}"
        elif self.operator == "CompEqual":
            return f"{self.left} == {self.right}"
        elif self.operator == "CompNotEqual":
            return f"{self.left} != {self.right}"
        else:
            return f"{self.left} {self.operator} {self.right}"

    def pr(self, depth=0):
        if self.operator == "PLUS":
            print(' ' * depth + f"{self.left.pr()} + {self.right.pr()}")
        elif self.operator == "CompEqual":
            print(' ' * depth + f"{self.left.pr()} == {self.right.pr()}")
        elif self.operator == "CompNotEqual":
            print(' ' * depth + f"{self.left.pr()} != {self.right.pr()}")
        else:
            print(' ' * depth + f"{self.left.pr()} {self.operator} {self.right.pr()}")
    
    def write_file(self, depth=0, fout=None):
        if self.operator == "PLUS":
            fout.write(' ' * depth + f"{self.left.pv()} + {self.right.pv()}\n")
        elif self.operator == "CompEqual":
            fout.write(' ' * depth + f"{self.left.pv()} == {self.right.pv()}\n")
        elif self.operator == "CompNotEqual":
            fout.write(' ' * depth + f"{self.left.pv()} != {self.right.pv()}\n")
        else:
            fout.write(' ' * depth + f"{self.left.pv()} {self.operator} {self.right.pv()}\n")

class KeyWordNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"KeyWordNode(name={self.name})"

class IDNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"IDNode(name={self.name})"



class ast_parser:
    def __init__(self, filename):
        self.filename = filename
        self.ast = []
        self.lines = []
        self.current_pos = 0
        self.statements = []
        self.parse_file()

    def dump_common_end(self):
        print("FC_list = []")
        print("Conv_list = []")
        print(f"for key, value in operations.items():")
        # parse the content of key
        # op name: currently only support Conv
        print(f"    op_name = key[0]")
        print(f"    props = key[1:]")
        print(f"    if op_name == 'Conv':")
        print(f"        for i in range(0, len(props), 2):")
        print(f"            prop_name = props[i]")
        print(f"            prop_value = props[i+1]")
        print(f"            if prop_name == 'kernel':")
        print(f"                width = prop_value[0]")
        print(f"                height = prop_value[1]")
        print(f"            elif prop_name == 'channels':")
        print(f"                in_chan = prop_value[0]")
        print(f"                out_chan = prop_value[1]")
        print(f"            else:")
        print(f"                print(f'Unknown property: {{prop_name}}')")
        print(f"        for t in range(value):")
        print(f"            Conv_list.append((width, height, in_chan, out_chan))")
        # this is the FC part
        print(f"    if op_name == 'FC':")
        print(f"        for i in range(0, len(props), 2):")
        print(f"            prop_name = props[i]")
        print(f"            prop_value = props[i+1]")
        print(f"            if prop_name == 'in':")
        print(f"                rows = prop_value[0]")
        print(f"            elif prop_name == 'out':")
        print(f"                loaded_cols = prop_value[0]")
        print(f"            else:")
        print(f"                print(f'Unknown property: {{prop_name}}')")
        print(f"        for t in range(value):")
        print(f"            FC_list.append((rows, loaded_cols))")
        print(f"    else:")
        print(f"        print(f'Unknown operator: {{op_name}}')")

        # code generation for the systemC with the targeted kernel
        # perform some runs to change the corresponding lines of the systemC code
        # TODO
        # Let's just call shell script to do this
        # No, I think we can use Python

        # First, we need to calculate the number of accelerators we need to generate
        print("num_fc_accelerators = len(FC_list)")
        print("file_numbers = [i for i in range(len(FC_list))]")
        # create the directory
        print("for i in file_numbers:")
        print("    if not os.path.exists(f\"FC_{i}\"):")
        print("        os.makedirs(f\"FC_{i}\")")
        
        # print("    with open('../../code_template/generator_template.py', 'r') as file:")
        # print("        content = file.read()")
        # print("    content = content.replace('rows = 2', f\"rows = {int(float(FC_list[i][1]))}\")")
        # print("    content = content.replace('loaded_cols = 4', f\"loaded_cols = {int(float(FC_list[i][0]))}\")")
        # print("    with open(f'FC_{i}/generator.py', 'w') as file:")
        # print("        file.write(content)")
        # print("    os.chdir(f'FC_{i}')")
        # print("    os.system(f'python3 generator.py')")
        # print("    os.chdir(f'..')")

        # create the hpp generator and execute it
        print("    with open('../../code_template/generator_template.py', 'r') as file:")
        print("        content = file.read()")
        print("    content = content.replace('rows = 2', f\"rows = {int(float(FC_list[i][1]))}\")")
        print("    content = content.replace('loaded_cols = 4', f\"loaded_cols = {int(float(FC_list[i][0]))}\")")
        print("    with open(f'FC_{i}/generator.py', 'w') as file:")
        print("        file.write(content)")
        print("    os.chdir(f'FC_{i}')")
        print("    os.system(f'python3 generator.py')")
        print("    os.chdir(f'..')")
        # generate the memlist
        print("    with open('../../code_template/memlist.txt', 'r') as file:")
        print("        content = file.read()")
        print("    content = content.replace('65536', f\"{int(float(FC_list[i][0]))*int(float(FC_list[i][1]))}\")")
        print("    content = content.replace('256', f\"{int(float(FC_list[i][1]))}\")")
        print("    with open(f'FC_{i}/memlist.txt', 'w') as file:")
        print("        file.write(content)")
        # generate the systemC code
        print("    with open('../../code_template/huangemmplt.hpp', 'r') as file:")
        print("        content = file.read()")
        print("    content = content.replace('PLM_IN_WORD 65536', f\"PLM_IN_WORD {int(float(FC_list[i][0]))*int(float(FC_list[i][1]))}\")")
        print("    content = content.replace('PLM_OUT_WORD 256', f\"PLM_OUT_WORD {int(float(FC_list[i][1]))}\")")
        print("    with open(f'FC_{i}/huangemmplt.hpp', 'w') as file:")
        print("        file.write(content)")



    def write_common_end(self, fout):
        fout.write("FC_list = []\n")
        fout.write("Conv_list = []\n")
        fout.write(f"for key, value in operations.items():\n")
        # parse the content of key
        # op name: currently only support Conv
        fout.write(f"    op_name = key[0]\n")
        fout.write(f"    props = key[1:]\n")
        fout.write(f"    if op_name == 'Conv':\n")
        fout.write(f"        for i in range(0, len(props), 2):\n")
        fout.write(f"            prop_name = props[i]\n")
        fout.write(f"            prop_value = props[i+1]\n")
        fout.write(f"            if prop_name == 'kernel':\n")
        fout.write(f"                width = prop_value[0]\n")
        fout.write(f"                height = prop_value[1]\n")
        fout.write(f"            elif prop_name == 'channels':\n")
        fout.write(f"                in_chan = prop_value[0]\n")
        fout.write(f"                out_chan = prop_value[1]\n")
        fout.write(f"            else:\n")
        fout.write(f"                print(f'Unknown property: {{prop_name}}')\n")
        fout.write(f"        for t in range(value):\n")
        fout.write(f"            Conv_list.append((width, height, in_chan, out_chan))\n")
        # this is the FC part
        fout.write(f"    if op_name == 'FC':\n")
        fout.write(f"        for i in range(0, len(props), 2):\n")
        fout.write(f"            prop_name = props[i]\n")
        fout.write(f"            prop_value = props[i+1]\n")
        fout.write(f"            if prop_name == 'in':\n")
        fout.write(f"                rows = prop_value[0]\n")
        fout.write(f"            elif prop_name == 'out':\n")
        fout.write(f"                loaded_cols = prop_value[0]\n")
        fout.write(f"            else:\n")
        fout.write(f"                print(f'Unknown property: {{prop_name}}')\n")
        fout.write(f"        for t in range(value):\n")
        fout.write(f"            FC_list.append((float(rows), float(loaded_cols)))\n")
        fout.write(f"    else:\n")
        fout.write(f"        print(f'Unknown operator: {{op_name}}')\n")

        # code generation for the systemC with the targeted kernel
        # perform some runs to change the corresponding lines of the systemC code
        # TODO
        # Let's just call shell script to do this
        # No, I think we can use Python

        # accelerator delegate optimization
        if opt_accelerator_delegate:
            # fout.write("for row, loaded_col in FC_list:\n")
            fout.write("points = sorted(FC_list, key=lambda p: (p[0], p[1]))\n")
            fout.write("result = []\n")
            fout.write("for i, (x1, y1) in enumerate(points):\n")
            fout.write("    dominated = False\n")
            fout.write("    for x2, y2 in points[i + 1:]:\n")
            fout.write("        if x1 < x2 and y1 < y2:\n")
            fout.write("            dominated = True\n")
            fout.write("            break\n")
            fout.write("    if not dominated:\n")
            fout.write("        result.append((x1, y1))\n")
            fout.write("FC_list = result\n")


        # First, we need to calculate the number of accelerators we need to generate
        fout.write("num_fc_accelerators = len(FC_list)\n")
        fout.write("file_numbers = [i for i in range(len(FC_list))]\n")
        # create the directory
        fout.write("for i in file_numbers:\n")
        fout.write("    if not os.path.exists(f\"FC_{i}\"):\n")
        fout.write("        os.makedirs(f\"FC_{i}\")\n")
        # create the hpp generator and execute it
        fout.write("    with open('../../code_template/generator_template.py', 'r') as file:\n")
        fout.write("        content = file.read()\n")
        fout.write("    content = content.replace('rows = 2', f\"rows = {int(float(FC_list[i][1]))}\")\n")
        fout.write("    content = content.replace('loaded_cols = 4', f\"loaded_cols = {int(float(FC_list[i][0]))}\")\n")
        fout.write("    with open(f'FC_{i}/generator.py', 'w') as file:\n")
        fout.write("        file.write(content)\n")
        fout.write("    os.chdir(f'FC_{i}')\n")
        fout.write("    os.system(f'python3 generator.py')\n")
        fout.write("    os.chdir(f'..')\n")
        # generate the memlist
        fout.write("    with open('../../code_template/memlist.txt', 'r') as file:\n")
        fout.write("        content = file.read()\n")
        fout.write("    content = content.replace('65536', f\"{int(float(FC_list[i][0]))*int(float(FC_list[i][1]))}\")\n")
        fout.write("    content = content.replace('256', f\"{int(float(FC_list[i][1]))}\")\n")
        fout.write("    with open(f'FC_{i}/memlist.txt', 'w') as file:\n")
        fout.write("        file.write(content)\n")
        # generate the systemC code
        fout.write("    with open('../../code_template/huangemmplt.hpp', 'r') as file:\n")
        fout.write("        content = file.read()\n")
        fout.write("    content = content.replace('PLM_IN_WORD 65536', f\"PLM_IN_WORD {int(float(FC_list[i][0]))*int(float(FC_list[i][1]))}\")\n")
        fout.write("    content = content.replace('PLM_OUT_WORD 256', f\"PLM_OUT_WORD {int(float(FC_list[i][1]))}\")\n")
        fout.write("    with open(f'FC_{i}/huangemmplt.hpp', 'w') as file:\n")
        fout.write("        file.write(content)\n")
        



    def dump_common_start(self):
        print("import os")

    def write_common_start(self, fout):
        fout.write("import os\n")
        

    def dump(self):
        self.dump_common_start()
        current_depth = 0
        spacex = " "
        print(f"{spacex*current_depth}operations = {{}}")

        # Let's perform some optimization here
        # 1. constant propagation
        available_constants = {}
        symbols = [{}]
        for statement in self.statements:
            # first check whether we can replace the variable with the constant, and also check whether the variable is defined
            if isinstance(statement, AssignNode):
                if isinstance(statement.expression, BinOpNode):
                    if not look_up_symbol_table(statement.expression.left, symbols) and not is_number(statement.expression.left):
                        raise ValueError(f"Error: {statement.expression.left} is not defined in the true (if)")
                    if not look_up_symbol_table(statement.expression.right, symbols) and not is_number(statement.expression.right):
                        raise ValueError(f"Error: {statement.expression.right} is not defined in the true (if)")
                elif not look_up_symbol_table(statement.expression, symbols) and not is_number(statement.expression):
                    raise ValueError(f"Error: {statement.expression} is not defined in the expression (if)")
                else:
                    pass
                # define variable in the local symbol table if it's not defined
                if not look_up_symbol_table(statement.variable, symbols):
                    symbols[0][statement.variable] = statement.expression

            elif isinstance(statement, IfNode):
                statement.forward_propagation(symbols)
            elif isinstance(statement, WhileNode):
                statement.forward_propagation(symbols)

        # 2. dead code elimination

        # here we are parsing the statements, the generated code will extract operations
        # print(f"output statements: {self.statements}")
        for statement in self.statements:
            statement.pr(current_depth)
        
        self.dump_common_end()

    def write_file(self, fout):
        self.write_common_start(fout)
        current_depth = 0
        spacex = " "
        fout.write(f"{spacex*current_depth}operations = {{}}\n")

        # Let's perform some optimization here
        # 1. constant propagation
        available_constants = {}
        symbols = [{}]
        for statement in self.statements:
            # first check whether we can replace the variable with the constant, and also check whether the variable is defined
            if isinstance(statement, AssignNode):
                if isinstance(statement.expression, BinOpNode):
                    if not look_up_symbol_table(statement.expression.left, symbols) and not is_number(statement.expression.left):
                        raise ValueError(f"Error: {statement.expression.left} is not defined in the true (if)")
                    if not look_up_symbol_table(statement.expression.right, symbols) and not is_number(statement.expression.right):
                        raise ValueError(f"Error: {statement.expression.right} is not defined in the true (if)")
                elif not look_up_symbol_table(statement.expression, symbols) and not is_number(statement.expression):
                    raise ValueError(f"Error: {statement.expression} is not defined in the expression (if)")
                else:
                    pass
                # define variable in the local symbol table if it's not defined
                if not look_up_symbol_table(statement.variable, symbols):
                    symbols[0][statement.variable] = statement.expression

            elif isinstance(statement, IfNode):
                statement.forward_propagation(symbols)
            elif isinstance(statement, WhileNode):
                statement.forward_propagation(symbols)

        # 2. dead code elimination

        # here we are parsing the statements, the generated code will extract operations
        # print(f"output statements: {self.statements}")
        for statement in self.statements:
            statement.write_file(current_depth, fout)
        
        self.write_common_end(fout)



    def count_leading_spaces(self, input_string):
        return len(input_string) - len(input_string.lstrip())

    def extract_id_name(self, input_string):
        bracket_content = re.search(r'\((.*?)\)', input_string)
        if bracket_content:
            bracket_content = bracket_content.group(1)  

            # get operator type (IDNode(name=Conv))
            equal_content = re.search(r'=(.+)', bracket_content)
            if equal_content:
                result = equal_content.group(1)  
                return result
                # print("Extracted content:", result)
            else:
                raise ValueError(f"error when parsing getting id name: {input_string}")
        else:
            raise ValueError(f"error when parsing getting id name: {input_string}")

    
    def parse_file(self):
        with open(self.filename) as f:
            self.lines = f.readlines()
        while self.current_pos < len(self.lines):
            line = self.lines[self.current_pos]
            self.current_pos += 1
            if line.startswith("RegisterOpNode"):
                self.statements.append(self.parse_register_op_node())
            elif line.startswith("IfNode"):
                self.statements.append(self.parse_if_node())
            elif line.startswith("WhileNode"):
                self.statements.append(self.parse_while_node())
            elif line.startswith("AssignNode"):
                self.statements.append(self.parse_assign_node())
            else:
                raise ValueError(f"Unsupported node type: {line}")

    def parse_register_op_node(self):
        # first parse the operation_type:
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "operation_type:":
            raise ValueError(f"error when parsing register_op: {line}")
        
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1

        operator_name = self.extract_id_name(line)
        

        # get properties
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "properties:":
            raise ValueError(f"error when parsing register_op (get property): {line}")

        # line = self.lines[self.current_pos]
        # depth = self.count_leading_spaces(line)

        # keep getting PropNode
        props = {}
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        # print(line)
        while line.startswith("PropNode"):
            # print(line)
            # self.current_pos += 1
            line = self.lines[self.current_pos].strip()
            self.current_pos += 1
            # print(line)
            # name:
            #     IDNode(name=kernel)
            if not line.startswith("name:"):
                raise ValueError(f"error when parsing register_op (get property): {line}")
            line = self.lines[self.current_pos].strip()
            self.current_pos += 1

            prop_name = self.extract_id_name(line)
            line = self.lines[self.current_pos].strip()
            self.current_pos += 1

            value_list = []
            # value:
            if not line.startswith("value:"):
                raise ValueError(f"error when parsing register_op (get property): {line}")
            line = self.lines[self.current_pos].strip()
            self.current_pos += 1

            # TupleNode
            if not line.startswith("TupleNode"):
                # just one value
                if line.startswith("NumberNode"):
                    print(f"line: {line}")
                    value = self.extract_id_name(line)
                    value_list.append(value)
                    if self.current_pos < len(self.lines):
                        line = self.lines[self.current_pos].strip()
                    else:
                        props[prop_name] = value_list
                        self.current_pos += 1
                        break
                    # line = self.lines[self.current_pos].strip()
                    # print(f"next line: {line}")
                    # exit(0)
                    self.current_pos += 1
                    # line = self.lines[self.current_pos].strip()
                    # print(f"next line: {line}")
                else:
                    raise ValueError(f"error when parsing register_op (get property with one value): {line}")
            else:
                line = self.lines[self.current_pos].strip()
                self.current_pos += 1

                # value
                if not line.startswith("values:"):
                    raise ValueError(f"error when parsing register_op (get property): {line}")
                line = self.lines[self.current_pos].strip()
                self.current_pos += 1

                while line.startswith("NumberNode"):
                    value = self.extract_id_name(line)
                    value_list.append(value)
                    line = self.lines[self.current_pos].strip()
                    self.current_pos += 1
            # self.current_pos -= 1
            props[prop_name] = value_list
        
        self.current_pos -= 1
        print(f"operator_name: {operator_name}")
        print(f"props: {props}")
        return RegisterOpNode(operator_name, props)
    
    def parse_assign_node(self):
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "variable:":
            raise ValueError(f"error when parsing assign_node: {line}")
        
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        variable = self.extract_id_name(line)

        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "expression:":
            raise ValueError(f"error when parsing assign_node: {line}")
        
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line.startswith("BinOpNode"):
            self.current_pos -= 1
            expression = self.parse_bin_op_node()
        elif line.startswith("IDNode"):
            expression = self.extract_id_name(line)
        elif line.startswith("NumberNode"):
            expression = self.extract_id_name(line)
        else:
            raise ValueError(f"error when parsing assign_node (expression): {line}")
        
        return AssignNode(variable, expression)
    
    def parse_if_node(self):
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "condition:":
            raise ValueError(f"error when parsing if_node: {line}")
        
        # parse binary node (condition)
        line = self.lines[self.current_pos].strip()
        # self.current_pos += 1
        if line.startswith("BinOpNode"):
            condition = self.parse_bin_op_node()
        else:
            raise ValueError(f"error when parsing if_node (bin_op): {line}")
        
        # parse true branch
        
        true_depth = self.count_leading_spaces(self.lines[self.current_pos])
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "true_branch:":
            raise ValueError(f"error when parsing if_node (true_branch): {line}")
        
        true_branch = []

        print(f"true_depth: {true_depth}")
        # possible statements: assign and register
        while self.current_pos < len(self.lines) and self.count_leading_spaces(self.lines[self.current_pos]) > true_depth:
            line = self.lines[self.current_pos].strip()
            if line.startswith("AssignNode"):
                self.current_pos += 1
                true_branch.append(self.parse_assign_node())
            elif line.startswith("RegisterOpNode"):
                self.current_pos += 1
                true_branch.append(self.parse_register_op_node())
            elif line.startswith("BreakNode"):
                self.current_pos += 1
                true_branch.append(BreakNode())
            else:
                print(f"error in true_branch: {line}")
                exit(0)

        
        # parse false branch
        line = self.lines[self.current_pos].strip()
        false_depth = self.count_leading_spaces(self.lines[self.current_pos])
        self.current_pos += 1
        if line != "false_branch:":
            raise ValueError(f"error when parsing if_node (false_branch): {line}")
        
        false_branch = []
        

        # it's possible that there is no false branch (2 cases)

        # scenario 1: no false branch
        if self.current_pos >= len(self.lines):
            return IfNode(condition, true_branch, false_branch)
        # scenario 2: other statements
        line = self.lines[self.current_pos].strip()
        if not self.count_leading_spaces(self.lines[self.current_pos]) > false_depth:
            print(f"no false branch, the next line: {line}")
            return IfNode(condition, true_branch, false_branch)

        while self.current_pos < len(self.lines) and self.count_leading_spaces(self.lines[self.current_pos]) > false_depth:
            line = self.lines[self.current_pos].strip()
            if line.startswith("AssignNode"):
                self.current_pos += 1
                false_branch.append(self.parse_assign_node())
            elif line.startswith("RegisterOpNode"):
                self.current_pos += 1
                false_branch.append(self.parse_register_op_node())
            elif line.startswith("BreakNode"):
                self.current_pos += 1
                false_branch.append(BreakNode())
            else:
                print(f"error in false_branch: {line}")
                raise ValueError(f"error when parsing if_node (false_branch): {line}")
                # exit(0)
        
        return IfNode(condition, true_branch, false_branch)


    def parse_bin_op_node(self):
        line = self.lines[self.current_pos].strip()
        bin_op_name = self.extract_id_name(line)
        self.current_pos += 1

        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "left:":
            raise ValueError(f"error when parsing bin_op_node (left): {line}")
        
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        left = self.extract_id_name(line)

        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "right:":
            raise ValueError(f"error when parsing bin_op_node (right): {line}")
        
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        right = self.extract_id_name(line)
        return BinOpNode(left, bin_op_name, right)
    

    def parse_while_node(self):
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "condition:":
            raise ValueError(f"error when parsing while_node: {line}")
        
        # parse binary node (condition)
        line = self.lines[self.current_pos].strip()
        # self.current_pos += 1
        if line.startswith("BinOpNode"):
            condition = self.parse_bin_op_node()
        else:
            raise ValueError(f"error when parsing while_node (bin_op): {line}")
        
        # parse true branch
        
        true_depth = self.count_leading_spaces(self.lines[self.current_pos])
        line = self.lines[self.current_pos].strip()
        self.current_pos += 1
        if line != "statements:":
            raise ValueError(f"error when parsing while_node (statements): {line}")
        
        statements = []

        print(f"true_depth: {true_depth}")
        # possible statements: assign and register
        while self.current_pos < len(self.lines) and self.count_leading_spaces(self.lines[self.current_pos]) > true_depth:
            line = self.lines[self.current_pos].strip()
            if line.startswith("AssignNode"):
                self.current_pos += 1
                statements.append(self.parse_assign_node())
            elif line.startswith("RegisterOpNode"):
                self.current_pos += 1
                statements.append(self.parse_register_op_node())
            elif line.startswith("IfNode"):
                self.current_pos += 1
                statements.append(self.parse_if_node())
            else:
                print(f"error in true_branch: {line}")
                exit(0)
        
        return WhileNode(condition, statements)


if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser(description="A simple argument parser example")

    ####### using parser
    arg_parse.add_argument("-o", "--output", type=str, help="Output file name")
    arg_parse.add_argument("filename", nargs="?", type=str, help="Input file")

    input_file_name = arg_parse.parse_args().filename
    output_file_name = arg_parse.parse_args().output

    if input_file_name is None:
        input_file_name = "ast_outputs/output1.txt"

    if "2" in input_file_name:
        opt_constant_propagation = False
    if "3" in input_file_name:
        opt_multipass_optimization = True

    ast = ast_parser(input_file_name)
    print(ast.statements)

    if output_file_name is None:
        ast.dump()
    else:
        with open(output_file_name, "w") as foutt:
            ast.write_file(foutt)