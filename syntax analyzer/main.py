from anytree import Node, RenderTree, DoubleStyle
from first_and_follow_sets import all_first_sets, all_follow_sets
from tokenizer import tokenizer


start_symbol = "Program"

rules = {
    "Program": [["DeclarationBlock"]],

    "DeclarationBlock": [["SingleDec", "DeclarationExtension"]],
    "DeclarationExtension": [["SingleDec", "DeclarationExtension"], ["epsilon"]],

    "SingleDec": [["DataType", "t_id", "DeclarationType"]],
    "DeclarationType": [["VariableDeclaration"], ["FunctionDeclaration"]],

    "DataType": [["t_int"], ["t_bool"], ["t_char"]],

    "VariableDeclaration": [["VariableList", "t_semicolon"]],
    "VariableList": [["VariableInitializer", "VariableListExtension"]],
    "VariableListExtension": [["t_comma", "t_id", "VariableInitializer", "VariableListExtension"], ["epsilon"]],

    "VariableInitializer": [["ArrayDeclaration", "VarInitializerExtension"]],
    "VarInitializerExtension": [["t_assign", "ExpressionStructure"], ["epsilon"]],

    "ArrayDeclaration": [["t_lb", "ArrayDimension", "t_rb"], ["epsilon"]],
    "ArrayDimension": [["ExpressionStructure"], ["epsilon"]],

    "FunctionDeclaration": [["t_lp", "FunctionParameters", "t_rp", "ActionStatement"]],
    "FunctionParameters": [["ParametersList"], ["epsilon"]],
    "ParametersList": [["DataType", "t_id", "ParametersExtension"]],
    "ParametersExtension": [["t_comma", "DataType", "t_id", "ArrayDeclaration", "ParametersExtension"], ["epsilon"]],

    "ActionStatement": [["CompoundStatement"], ["SimpleAction"], ["ConditionStatement"],
                        ["IterationStatement"], ["OutputStatement"], ["BreakAction"],
                        ["ReturnAction"], ["ContinueAction"], ["VariableDeclarationStatement"]
                       ],

    "CompoundStatement": [["t_lc", "StatementSequence", "t_rc"]],
    "StatementSequence": [["ActionStatement", "StatementSequence"], ["epsilon"]],

    "ConditionStatement": [["t_if", "ExpressionStructure", "CompoundStatement", "AlternativeStatement"]],
    "AlternativeStatement": [["t_else", "CompoundStatement"], ["epsilon"]],

    "IterationStatement": [["t_for", "t_lp", "ForInitialization", "t_rp"]],
    "ForInitialization": [["LoopVarInitialization", "t_semicolon", "LoopExpression", "t_semicolon", "LoopStep"]],

    "LoopVarInitialization": [["DataType", "t_id", "t_assign", "ExpressionStructure"], ["t_id", "t_assign", "ExpressionStructure"], ["epsilon"]],
    "LoopExpression": [["ExpressionStructure"], ["epsilon"]],
    "LoopStep": [["SimpleAction2"], ["epsilon"]],

    "SimpleAction": [["t_id", "ArrayAccess", "t_assign", "ExpressionStructure", "t_semicolon"]],
    "SimpleAction2": [["t_id", "ArrayAccess", "t_assign", "ExpressionStructure"]],
    "ArrayAccess": [["t_lb", "ArrayDimension2", "t_rb"], ["epsilon"]],
    "ArrayDimension2": [["ExpressionStructure"]],

    "VariableDeclarationStatement": [["DataType", "t_id", "VariableList", "t_semicolon"]],

    "ReturnAction": [["t_return", "t_semicolon"], ["t_return", "ExpressionStructure", "t_semicolon"]],

    "BreakAction": [["t_break", "t_semicolon"]],

    "ContinueAction": [["t_continue", "t_semicolon"]],

    "OutputStatement": [["t_print", "t_lp", "OutputRules", "t_rp", "t_semicolon"]],
    "OutputRules": [["ExpressionStructure", "PrintExtension"]],
    "PrintExtension": [["t_comma", "ExpressionStructure", "PrintExtension"], ["epsilon"]],

    "ExpressionStructure": [["LogicalExpression"]],

    "LogicalExpression": [["AndExpression", "OrExtension"]],
    "OrExtension": [["t_lop_or", "AndExpression", "OrExtension"], ["epsilon"]],

    "AndExpression": [["NegationExpression", "AndChain"]],
    "AndChain": [["t_lop_and", "NegationExpression", "AndChain"], ["epsilon"]],

    "NegationExpression": [["t_lop_not", "NegationExpression"], ["ComparisonExpression"]],

    "ComparisonExpression": [["SimpleExpression", "ComparisonExtension"]],
    "ComparisonExtension": [["ComparisonOps", "SimpleExpression", "ComparisonExtension"], ["epsilon"]],

    "ComparisonOps": [["t_rop_l"], ["t_rop_g"], ["t_rop_le"], ["t_rop_ge"], ["t_rop_ne"], ["t_rop_e"]],

    "SimpleExpression": [["ArithmeticTerm", "ArithmeticChain1"]],
    "ArithmeticChain1": [["t_aop_pl", "ArithmeticTerm", "ArithmeticChain1"], ["t_aop_mn", "ArithmeticTerm", "ArithmeticChain1"], ["epsilon"]],

    "ArithmeticTerm": [["ArithmeticFactor", "ArithmeticChain2"]],
    "ArithmeticChain2": [["t_aop_ml", "ArithmeticFactor", "ArithmeticChain2"], ["t_aop_dv", "ArithmeticFactor", "ArithmeticChain2"], ["t_aop_rm", "ArithmeticFactor", "ArithmeticChain2"], ["epsilon"]],

    "ArithmeticFactor": [["t_aop_pl", "Elementary"], ["t_aop_mn", "Elementary"], ["Elementary"]],

    "Elementary": [["t_id", "FunctionOrArrayAccess"], ["t_decimal"], ["t_hexadecimal"],
                   ["t_string"], ["t_char"], ["t_true"], ["t_false"],
                   ["t_lp", "ExpressionStructure", "t_rp"]],
    
    "FunctionOrArrayAccess": [["epsilon"], ["t_lp", "DetailedParameters", "t_rp"]],

    "DetailedParameters": [["ParametersList2"], ["epsilon"]],

    "ParametersList2": [["t_id", "ParametersTail"]],

    "ParametersTail": [["t_comma", "t_id", "ArrayDeclaration", "ParametersTail"], ["epsilon"]]
}


def main():
    parsing_table = build_parsing_table(rules)
    print_parsing_table(parsing_table)

    tree_root = predictive_parser(parsing_table, start_symbol)
    print_parse_tree(tree_root)


def predictive_parser(parsing_table, start_symbol):
    #tajzieh konnade pish bini konandeh
    #ll(1)
    stack = ['$', start_symbol]
    root = Node(start_symbol)
    parent_stack = [root]
    token_generator = tokenizer()
    current_token = next(token_generator)
    pop_node_stack = True

    while stack:
        print(f"**********************")
        print(f"Stack: {stack}")
        print(f"Current Token: {current_token}")

        top = stack[-1]
        if stack != ["$"] and pop_node_stack:
            current_node = parent_stack.pop() #end and return
        else:
            pop_node_stack = True

        if current_token == "$" and top == "$":
            break
        elif current_token == "$":
            current_token_name = "$"
            current_token_value = "$"
            current_token_line = "End of Tokens"
        else:
            current_token_name = current_token.name
            current_token_value = current_token.value
            current_token_line = current_token.line_num

        if top == current_token_name:
            stack.pop()
            current_token = next(token_generator)
            if current_token_value != None:
                Node(current_token_value, parent=current_node)

            print(f"Matched Token: {current_token_name.upper()}, Value: {current_token_value}")
        elif top[0].isupper():  #captal
            if top in parsing_table.keys() and current_token_name in parsing_table[top].keys():
                if parsing_table[top][current_token_name] != "synch":
                    production = parsing_table[top][current_token_name][0]
                else:
                    production = parsing_table[top][current_token_name]

                print(f"Action: {top} -> {production}")

                if production == "synch":
                    print(f"Synch")
                    stack.pop()
                elif production != ['epsilon']:
                    stack.pop()
                    for symbol in reversed(production):
                        stack.append(symbol)

                        child_node = Node(symbol.upper(), parent=current_node)
                        parent_stack.append(child_node)
                else:
                    child_node = Node("epsilon", parent=current_node)
                    stack.pop()
            else:
                print(f"SYNTAX ERROR!")
                print("at line #{current_token_line}, Extra: {current_token_name}")
                print("Empty table, token discarded")
                current_token = next(token_generator)
                pop_node_stack = False

        else:
            stack.pop()
            print(f"SYNTAX ERROR!")
            print("at line #{current_token_line}, Extra: {current_token_name}")

    return root


def print_parse_tree(root: Node):
    for pre, fill, node in RenderTree(root, style=DoubleStyle):
        print(f"{pre}{node.name}")


def build_parsing_table(grammar_rules):
    syntax_table = {symbol: {} for symbol in grammar_rules}

    for symbol, expansions in grammar_rules.items():
        for expansion in expansions:
            first_symbols = compute_first_set(expansion, all_first_sets)

            for first_symbol in first_symbols:
                if first_symbol != 'epsilon':
                    if first_symbol not in syntax_table[symbol]:
                        syntax_table[symbol][first_symbol] = []
                    syntax_table[symbol][first_symbol].append(expansion)
                else:
                    for terminal in all_follow_sets[symbol]:
                        if terminal not in syntax_table[symbol]:
                            syntax_table[symbol][terminal] = []
                        syntax_table[symbol][terminal].append(expansion)
                        if "$" in all_follow_sets[symbol]:
                            syntax_table[symbol]["$"] = []
                            syntax_table[symbol]["$"].append(expansion)

    for symbol, follow_set in all_follow_sets.items():
        for terminal in follow_set:
            if terminal not in syntax_table[symbol]:
                syntax_table[symbol][terminal] = "synch"

    return syntax_table


# def add_epsilon_productions(symbol, syntax_table, expansion):
#     for terminal in all_follow_sets[symbol]:
#         if terminal not in syntax_table[symbol]:
#             syntax_table[symbol][terminal] = []
#         syntax_table[symbol][terminal].append(expansion)
#         if "$" in all_follow_sets[symbol] and "$" not in syntax_table[symbol]:
#             syntax_table[symbol]["$"] = [expansion]

# def fill_synch_entries(syntax_table, follow_sets):
#     for symbol, follow_set in follow_sets.items():
#         for terminal in follow_set:
#             if terminal not in syntax_table[symbol]:
#                 syntax_table[symbol][terminal] = "synch"


def compute_first_set(production, all_first_sets):
    result = set()
    if not production:
        result.add('epsilon')
    else:
        for symbol in production:
            if symbol in all_first_sets:
                result.update(all_first_sets[symbol])
                if 'epsilon' not in all_first_sets[symbol]:
                    break
            else:
                result.add(symbol)
                break
    return result


def print_parsing_table(parsing_table):
    for nonterminal, rules in parsing_table.items():
        ambiguous = False 
        for terminal, production in rules.items():
            print(f"M[{nonterminal}, {terminal}] = {production}")
            if len(production) > 1 and production != "synch" and not ambiguous:
                ambiguous = True

        if ambiguous:
            print(f"ERROR: The Grammar for '{nonterminal}' is Ambiguous.")
            


if __name__ == "__main__":
    main()
