class GrammarProcessor:
    def __init__(self, grammar):
        self.grammar = grammar
        self.counter = 1

    def get_new_non_terminal(self, base):
        if self.counter == 1:
            new_non_terminal = base + str(self.counter)
        else:
            base = base[:-1]
            new_non_terminal = base + str(self.counter)
        self.counter += 1
        return new_non_terminal

    def factor_once(self, grammar):
        new_grammar = {}
        changes_made = False

        for non_terminal, productions in grammar.items():
            grouped = {}
            for prod in productions:
                first = prod[0]
                if first not in grouped:
                    grouped[first] = []
                grouped[first].append(prod)

            new_grammar[non_terminal] = []

            for first, group in grouped.items():
                if len(group) > 1:
                    changes_made = True
                    new_non_terminal = self.get_new_non_terminal(non_terminal)
                    new_grammar[non_terminal].append([first, new_non_terminal])
                    new_grammar[new_non_terminal] = []

                    for prod in group:
                        suffix = prod[1:] if len(prod) > 1 else ["epsilon"]
                        new_grammar[new_non_terminal].append(suffix)
                else:
                    new_grammar[non_terminal].append(group[0])

        return new_grammar, changes_made

    def left_factor(self):
        current_grammar = self.grammar
        while True:
            current_grammar, changes_made = self.factor_once(current_grammar)
            if not changes_made:
                break
        return current_grammar


if __name__ == "__main__":
    grammar = {
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
                      ["ReturnStmt"], ["ContinueStmt"], ["VardecStmt"]],
        "CompoundStmt": [["t_lc", "StatementList", "t_rc"]],
        "StatementList": [["Statement", "StatementList"], ["epsilon"]],
        "IfStmt": [["t_if", "t_lp", "Expression", "t_rp", "CompoundStmt", "ElseStmt"]],
        "ElseStmt": [["t_else", "CompoundStmt"], ["epsilon"]],
        "LoopStmt": [["t_for", "t_lp", "ForStmt", "t_rp"]],
        "ForStmt": [["LoopVardec", "t_semicolon", "LoopExpr", "t_semicolon", "LoopStep"]],
        "LoopVardec": [["Type", "t_id", "t_assign", "Expression"], ["t_id", "t_assign", "Expression"], ["epsilon"]],
        "LoopExpr": [["Expression"], ["epsilon"]],
        "LoopStep": [["SimpleStmt2"], ["epsilon"]],
        "SimpleStmt": [["t_id", "Array2", "SimpleStmt3", "t_semicolon"]],
        "SimpleStmt2": [["t_id", "Array2", "SimpleStmt3"]],
        "SimpleStmt3": [["t_assign", "Expression"], ["IsFunction"]],
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
        "NotExp": [["t_lop_not", "NotExp"], ["CompExp"]],
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
        "Parameters2": [["ParameterList2"], ["epsilon"]],
        "ParameterList2": [["Expression", "ParameterList2'"]],
        "ParameterList2'": [["t_comma", "Expression", "Array", "ParameterList2'"], ["epsilon"]]
    }

    processor = GrammarProcessor(grammar)
    factored_grammar = processor.left_factor()
    print(factored_grammar)
