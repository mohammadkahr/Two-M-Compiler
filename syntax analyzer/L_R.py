class Grammar:
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

    def remove_immediate_left_recursion(self, nonterminal, productions):
        has_left_rec = []
        no_left_rec = []
        for production in productions:
            if production[0] == nonterminal:
                has_left_rec.append(production)
            else:
                no_left_rec.append(production)

        if has_left_rec:
            new_non_terminal = self.get_new_non_terminal(nonterminal)
            new_has_left_rec = []
            new_no_left_rec = []

            if no_left_rec:
                new_no_left_rec = [prod + [new_non_terminal] for prod in no_left_rec]

            if has_left_rec:
                new_has_left_rec = [prod[1:] + [new_non_terminal] for prod in has_left_rec]

            new_has_left_rec.append(["epsilon"])

            if new_no_left_rec:
                updated_productions = {
                    nonterminal: new_no_left_rec,
                    new_non_terminal: new_has_left_rec
                }
            else:
                updated_productions = {
                    nonterminal: [new_non_terminal],
                    new_non_terminal: new_has_left_rec
                }
        else:
            updated_productions = {}

        return updated_productions

    def remove_left_recursion(self):
        non_terminals = list(self.grammar.keys())
        grammar_copy = {k: v[:] for k, v in self.grammar.items()}
        for i in range(len(non_terminals)):
            A_i = non_terminals[i]
            for j in range(i):
                A_j = non_terminals[j]
                new_productions = []
                for production in grammar_copy[A_i]:
                    if production[0] == A_j:
                        for Aj_production in grammar_copy[A_j]:
                            new_productions.append(Aj_production + production[1:])
                    else:
                        new_productions.append(production)
                grammar_copy[A_i] = new_productions
            immediate_left_recursion_removed = self.remove_immediate_left_recursion(A_i, grammar_copy[A_i])
            grammar_copy.update(immediate_left_recursion_removed)
        self.grammar = grammar_copy

    def print_grammar(self):
        print("\nNew set of productions: ")
        for nt, productions in self.grammar.items():
            for prod in productions:
                print(f"{nt} -> {prod}")


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

    g = Grammar(grammar)
    g.remove_left_recursion()
    g.print_grammar()
