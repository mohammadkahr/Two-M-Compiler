from syntax import *
from tokenizer import *
from anytree import NodeMixin, RenderTree, AsciiStyle

# class ASTNode:
#     def __init__(self, node_type, value=None, children=None):
#         self.node_type = node_type  # var - func
#         self.value = value
#         self.children = children if children else []
class ASTNode(NodeMixin):
    def __init__(self, node_type, value=None, children=None, parent=None):
        self.node_type = node_type
        self.value = value
        self.parent = parent
        if children:
            self.children = children
        else:
            self.children = []

    def __repr__(self):
        return f"ASTNode(type={self.node_type}, value={self.value}, children={len(self.children)})"

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = []
        self.errors = []

    def analyze(self, ast):
        self._analyze_node(ast)

    def _analyze_node(self, node, scope=None):
        if node.node_type == 'variable_declaration':
            self._handle_variable_declaration(node, scope)
        elif node.node_type == 'function_declaration':
            self._handle_function_declaration(node, scope)
        elif node.node_type == 'assignment':
            self._handle_assignment(node, scope)
        elif node.node_type == 'if_statement':
            self._handle_if_statement(node, scope)
        elif node.node_type == 'function_call':
            self._handle_function_call(node, scope)
        elif node.node_type == 'return_statement':
            self._handle_return_statement(node, scope)
        elif node.node_type == 'block':
            self._handle_block(node, scope)
        elif node.node_type == 'while_statement':
            self._handle_while_statement(node, scope)
        elif node.node_type == 'for_statement':
            self._handle_for_statement(node, scope)
        elif node.node_type == 'else_statement':
            self._handle_else_statement(node, scope)
        elif node.node_type == 'expression':
            self._evaluate_expression(node, scope)
        # and other type

        # check other children
        for child in node.children:
            self._analyze_node(child, scope)
        

    def _handle_while_statement(self, node, scope):
        condition_node = node.children[0]
        condition_type = self._evaluate_expression(condition_node, scope)
        if condition_type != 'bool':
            self.errors.append("Error: Conditional expression type in while statement must be bool.")
        self._analyze_node(node.children[1], scope)

    def _handle_for_statement(self, node, scope):
        initialization_node = node.children[0]
        condition_node = node.children[1]
        increment_node = node.children[2]
        self._analyze_node(initialization_node, scope)
        condition_type = self._evaluate_expression(condition_node, scope)
        if condition_type != 'bool':
            self.errors.append("Error: Conditional expression type in for statement must be bool.")
        self._analyze_node(increment_node, scope)
        self._analyze_node(node.children[3], scope)

    def _handle_else_statement(self, node, scope):
        self._analyze_node(node.children[0], scope)

    def _handle_variable_declaration(self, node, scope):
        variable_name = node.value
        variable_type = node.children[0].value  # We assume that the type of the variable in the first child is 90

        if self._is_variable_defined(variable_name, scope):
            self.errors.append(f"Error, var '{variable_name}' already defined in this scope.")
        else:
            self._define_variable(variable_name, variable_type, scope)

    def _handle_function_declaration(self, node, scope):
        function_name = node.value
        return_type = node.children[0].value
        parameters = node.children[1].children

        if self._is_function_defined(function_name):
            self.errors.append(f"Error, function '{function_name}' already defined.")
        else:
            self._define_function(function_name, return_type, parameters, scope)

        self._analyze_node(node.children[2], function_name)

    def _handle_assignment(self, node, scope):
        variable_name = node.children[0].value
        expression_type = self._evaluate_expression(node.children[1], scope)
        variable_type = self._get_variable_type(variable_name, scope)
        if variable_type != expression_type:
            self.errors.append(f"Error, variable '{variable_name}' does not match the type of the assigned expression.")

    def _handle_if_statement(self, node, scope):
        condition_type = self._evaluate_expression(node.children[0], scope)
        if condition_type != 'bool':
            self.errors.append(f"Error: The condition of the if statement must be of bool type.")

        self._analyze_node(node.children[1], scope)  # body of if
        if len(node.children) > 2:
            self._analyze_node(node.children[2], scope)  # body of else

    def _handle_function_call(self, node, scope):
        function_name = node.value
        arguments = node.children
        function = self._get_function(function_name)
        if not function:
            self.errors.append(f"Error, function '{function_name}' is not defined.")
        else:
            expected_params = function['parameters']
            if len(arguments) != len(expected_params):
                self.errors.append(f"Error: The number of arguments does not match the number of parameters for "
                                   f"function '{function_name}'.")
            for arg, param in zip(arguments, expected_params):
                arg_type = self._evaluate_expression(arg, scope)
                if arg_type != param['type']:
                    self.errors.append(f"Error: The type of the arguments does not match the type of the parameters "
                                       f"of the function '{function_name}'.")

    def _handle_return_statement(self, node, scope):
        expression_type = self._evaluate_expression(node.children[0], scope)
        function = self._get_function(scope)
        if function['return_type'] != expression_type:
            self.errors.append(f"Error: The return type of function '{scope}' does not match the return type of "
                               f"expression.")

    def _handle_block(self, node, scope):
        new_scope = scope + '{}'
        for child in node.children:
            self._analyze_node(child, new_scope)

    def _is_variable_defined(self, name, scope):
        for entry in self.symbol_table:
            if entry['name'] == name and entry['scope'] == scope:
                return True
        return False

    def _define_variable(self, name, var_type, scope):
        self.symbol_table.append({'name': name, 'type': var_type, 'scope': scope})

    def _is_function_defined(self, name):
        for entry in self.symbol_table:
            if entry['name'] == name and entry['type'] == 'function':
                return True
        return False

    def _define_function(self, name, return_type, parameters, scope):
        self.symbol_table.append(
            {'name': name, 'type': 'function', 'return_type': return_type, 'parameters': parameters, 'scope': scope})

    def _get_variable_type(self, name, scope):
        for entry in self.symbol_table:
            if entry['name'] == name and entry['scope'] == scope:
                return entry['type']
        return None

    def _get_function(self, name):
        for entry in self.symbol_table:
            if entry['name'] == name and entry['type'] == 'function':
                return entry
        return None

    def _evaluate_expression(self, node, scope):
        if node.node_type == 'literal':
            return node.value_type
        elif node.node_type == 'variable':
            return self._get_variable_type(node.value, scope)
        elif node.node_type == 'binary_operation':
            left_type = self._evaluate_expression(node.children[0], scope)
            right_type = self._evaluate_expression(node.children[1], scope)
            if node.value in ['+', '-', '*', '/']:
                if left_type == 'int' and right_type == 'int':
                    return 'int'
                else:
                    self.errors.append(f"Error: operands of operator '{node.value}' must be of type int.")
            elif node.value in ['&&', '||']:
                if left_type == 'bool' and right_type == 'bool':
                    return 'bool'
                else:
                    self.errors.append(f"Error: Operands of operator '{node.value}' must be of type bool.")

        # and other

        return None


# def parse_output_to_ast(parser_output):
#     lines = parser_output.strip().split('\n')
#     stack = []
#     root = None
#     current_node = None

#     for line in lines:
#         if line.startswith("Action:"):
#             parts = line.split('->')
#             action = parts[1].strip().split()
#             node_type = action[0]
#             new_node = Node(node_type)

#             if root is None:
#                 root = new_node
#             else:
#                 current_node.add_child(new_node)

#             stack.append(new_node)
#             current_node = new_node

#         elif line.startswith("Matched Token:") or line.startswith("Current Token:"):
#             token_info = line.split('Value:')[1].strip()
#             if current_node is not None:
#                 current_node.value = token_info

#         elif line.startswith("Stack:"):
#             while len(stack) > 1 and not stack[-1].children:
#                 stack.pop()
#             if stack:
#                 current_node = stack[-1]

#     return root



def convert_parser_tree_to_syntax_tree(parser_tree_root):
    # Recursive function to traverse and convert the tree
    def traverse_and_convert(node, parent=None):
        if not node.children:
            # It's a leaf node, keep it as it is
            return ASTNode(node.node_type, node.value, parent=parent)

        # Filter out nodes that are not meaningful for the syntax tree
        meaningful_children = [child for child in node.children if child.node_type not in ['epsilon']]

        if not meaningful_children:
            return None

        new_node = ASTNode(node.node.name, node.name, parent=parent)
        for child in meaningful_children:
            new_child = traverse_and_convert(child, new_node)
            if new_child:
                new_child.parent = new_node

        return new_node

    # Start conversion from the root of the parser tree
    syntax_tree_root = traverse_and_convert(parser_tree_root)

    return syntax_tree_root

class Node2:
    def __init__(self, node_type, value=None, parent=None):
        self.node_type = node_type
        self.value = value
        self.children = []
        if parent:
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value}, children={len(self.children)})"


def print_tree(node, level=0):
    print(node)
    print(' ' * level * 2 + f'{node.node_type}: {node.value}')
    for child in node.children:
        print_tree(child, level + 1)


if __name__ == '__main__':
    parsing_table = build_parsing_table(rules)
    ast_root = predictive_parser(parsing_table, 'Program')
    print_tree(ast_root)
   # Example usage
    # Assuming 'root' is the root node of the parser tree generated by the predictive parser
    syntax_tree_root = convert_parser_tree_to_syntax_tree(ast_root)
    # Visualize the syntax tree
    for pre, fill, node in RenderTree(syntax_tree_root, style=AsciiStyle()):
        print("%s%s" % (pre, node.node_type))

    # ast_root = parse_output_to_ast(ast_root)
    # semantic_analyzer = SemanticAnalyzer()
    # semantic_analyzer.analyze(ast_root)
    # for error in semantic_analyzer.errors:
    #     print(error)

# if __name__ == "__main__":
#     tokens = list(tokenizer())
#     # input_code = ' '.join([token.name for token in tokens if token.name != 'T_Whitespace'])
#     parsing_table = build_parsing_table(rules)
#
#     try:
#         parser_output = predictive_parser(tokens, parsing_table)
#         # print(parser_output)
#
#         ast = parse_output_to_ast(parser_output)  # parser_output باید یک رشته باشد
#         # print_tree(ast)
#
#         semantic_analyzer = SemanticAnalyzer()
#         semantic_analyzer.analyze(ast)
#
#         for error in semantic_analyzer.errors:
#             print(error)
#     except SyntaxError as e:
#         print(f"Syntax error: {e}")