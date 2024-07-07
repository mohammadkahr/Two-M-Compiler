class GrammarAnalyzer:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.first = {non_terminal: set() for non_terminal in grammar}
        self.follow = {non_terminal: set() for non_terminal in grammar}
        self.follow[start_symbol] = {'$'}

    def compute_first(self):
        for nonterminal in self.grammar:
            for production in self.grammar[nonterminal]:
                for symbol in production:
                    if not symbol[0].isupper():
                        self.first[symbol] = {symbol}

        def first_of(symbol):
            if not symbol[0].isupper():
                return self.first[symbol]
            if not self.first[symbol]:
                for production in self.grammar[symbol]:
                    for sym in production:
                        self.first[symbol] |= first_of(sym) - {'epsilon'}
                        if 'epsilon' not in first_of(sym):
                            break
                    else:
                        self.first[symbol] |= {'epsilon'}
            return self.first[symbol]

        for non_terminal in self.grammar:
            first_of(non_terminal)

        return self.first

    def compute_follow(self):
        self.first = self.compute_first()

        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.grammar.items():
                for production in productions:
                    for symbol in range(len(production)):
                        if not production[symbol][0].isupper():
                            continue
                        before_change = len(self.follow[production[symbol]])
                        if symbol == len(production) - 1:
                            self.follow[production[symbol]] |= self.follow[non_terminal]
                        else:
                            if 'epsilon' in self.first[production[symbol + 1]]:
                                if not production[symbol + 1][0].isupper():
                                    self.follow[production[symbol]] |= production[symbol + 1]
                                else:
                                    self.follow[production[symbol]] |= self.follow[production[symbol + 1]]
                                    self.follow[production[symbol]] |= self.first[production[symbol + 1]] - {'epsilon'}
                            else:
                                self.follow[production[symbol]] |= self.first[production[symbol + 1]]

                        if before_change != len(self.follow[production[symbol]]):
                            changed = True

        return self.follow

    def print_first_sets(self):
        first_sets = self.compute_first()
        print("first sets:")
        for non_terminal, productions in first_sets.items():
            if non_terminal[0].isupper():
                print(f'"{non_terminal}" : {productions},')

    def print_follow_sets(self):
        follow_sets = self.compute_follow()
        print("follow sets:")
        for non_terminal, productions in follow_sets.items():
            print(f'"{non_terminal}" : {productions},')


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

    start_symbol = "Program"

    analyzer = GrammarAnalyzer(grammar, start_symbol)
    analyzer.print_first_sets()
    analyzer.print_follow_sets()
