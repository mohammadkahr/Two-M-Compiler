from anytree import Node, RenderTree, DoubleStyle
from first_and_follow_sets import all_first_sets, all_follow_sets
from tokenizer import tokenizer


start_symbol = "Program"

rules = {
  "Program": [["Declist"]],

    "Declist": [["Dec", "Declist'"]],
    "Declist'": [["Dec", "Declist'"], ["epsilon"]],

    "Dec": [["Type", "t_id", "Declaration"]],
    "Declaration": [["Vardec"], ["Funcdec"]],

    "Type": [["t_int"], ["t_bool"], ["t_char"]],

    "Vardec": [["Vardeclist", "t_semicolon"]],
    "Vardeclist": [["VardecInit", "Vardeclist'"]],
    "Vardeclist'": [["t_comma", "t_id", "VardecInit", "Vardeclist'"], ["epsilon"]],

    "VardecInit": [["Array", "VardecInit'"]],
    "VardecInit'": [["t_assign", "Expression"], ["epsilon"]],

    "Array": [["t_lb", "Arraysize", "t_rb"], ["epsilon"]],
    "Arraysize": [["Expression"], ["epsilon"]],

    "Funcdec": [["t_lp", "Parameters", "t_rp", "Statement"]],
    "Parameters": [["ParameterList"], ["epsilon"]],
    "ParameterList": [["Type", "t_id", "ParameterList'"]],
    "ParameterList'": [["t_comma", "Type", "t_id", "Array", "ParameterList'"], ["epsilon"]],

    "Statement": [["CompoundStmt"], ["SimpleStmt"], ["IfStmt"],
                  ["LoopStmt"], ["PrintStmt"], ["BreakStmt"],
                  ["ReturnStmt"], ["ContinueStmt"], ["VardecStmt"]
                ],


    "CompoundStmt": [["t_lc", "StatementList", "t_rc"]],
    "StatementList" :[["Statement","StatementList"],["epsilon"]],

    "IfStmt": [["t_if","t_lp", "Expression", "t_rp", "CompoundStmt", "ElseStmt"]],
    "ElseStmt": [["t_else", "CompoundStmt"], ["epsilon"]],

    "LoopStmt": [["t_for", "t_lp", "ForStmt", "t_rp"]],
    "ForStmt": [["LoopVardec", "t_semicolon", "LoopExpr", "t_semicolon", "LoopStep"]],

    "LoopVardec": [["Type", "t_id", "t_assign", "Expression"], ["t_id", "t_assign", "Expression"], ["epsilon"]],
    "LoopExpr": [["Expression"], ["epsilon"]],
    "LoopStep": [["SimpleStmt2"], ["epsilon"]],

    "SimpleStmt": [["t_id", "Array2", "SimpleStmt3", "t_semicolon"]],
    "SimpleStmt2": [["t_id", "Array2", "SimpleStmt3" ]],
    "SimpleStmt3":[["t_assign", "Expression"],["IsFunction"]],
    
    "Array2": [["t_lb", "Arraysize2", "t_rb"], ["epsilon"]],
    "Arraysize2": [["Expression"]],

    "VardecStmt": [["Type", "t_id", "Vardeclist", "t_semicolon"]],

    "ReturnStmt": [["t_return", "t_semicolon"], ["t_return", "Expression", "t_semicolon"]],

    "BreakStmt": [["t_break", "t_semicolon"]],

    "ContinueStmt": [["t_continue", "t_semicolon"]],

    "PrintStmt": [["t_print", "t_lp", "PrintRules", "t_rp", "t_semicolon"]],
    "PrintRules": [["Expression", "PrintList"]],
    "PrintList": [["t_comma", "Expression", "PrintList"], ["epsilon"]],

    "Expression": [["OrExp"]],

    "OrExp": [["AndExp", "Or"]],
    "Or": [["t_lop_or", "AndExp", "Or"], ["epsilon"]],

    "AndExp": [["NotExp", "And"]],
    "And": [["t_lop_and", "NotExp", "And"], ["epsilon"]],

    "NotExp": [["t_lop_not","NotExp"],["CompExp"]],

    "CompExp": [["Expr", "Comp"]],
    "Comp": [["Comp_OP", "Expr", "Comp"], ["epsilon"]],

    "Comp_OP": [["t_rop_l"], ["t_rop_g"], ["t_rop_le"], ["t_rop_ge"], ["t_rop_ne"], ["t_rop_e"]],

    "Expr": [["Term", "Arth1"]],
    "Arth1": [["t_aop_pl", "Term", "Arth1"], ["t_aop_mn", "Term", "Arth1"], ["epsilon"]],

    "Term": [["Factor", "Arth2"]],
    "Arth2": [["t_aop_ml", "Factor", "Arth2"], ["t_aop_dv", "Factor", "Arth2"], ["t_aop_rm", "Factor", "Arth2"], ["epsilon"]],

    "Factor": [["t_aop_pl", "Atom"], ["t_aop_mn", "Atom"], ["Atom"]],

    "Atom": [["t_id", "IsFunction"], ["t_decimal"], ["t_hexadecimal"],
             ["t_string"], ["t_char"], ["t_true"], ["t_false"]],
    
    "IsFunction": [["epsilon"], ["t_lp", "Parameters2", "t_rp"]],

    "Parameters2" : [["ParameterList2"], ["epsilon"]],

    "ParameterList2": [["Expression", "ParameterList2'"]],

    "ParameterList2'": [["t_comma", "Expression", "Array", "ParameterList2'"], ["epsilon"]]
}


def main():
    parsing_table = build_parsing_table(rules)
    print_parsing_table(parsing_table)

    tree_root = predictive_parser(parsing_table, start_symbol)
    # print_parse_tree(tree_root)


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
                print(f"at line {current_token_line}, Extra: {current_token_name}")
                print("Empty table, token discarded")
                current_token = next(token_generator)
                pop_node_stack = False

        else:
            stack.pop()
            print("SYNTAX ERROR!")
            print(f"at line {current_token_line}, Extra: {current_token_name}")

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
