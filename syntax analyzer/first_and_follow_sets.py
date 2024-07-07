all_first_sets = {
    "Program" : {'t_bool', 't_char', 't_int'},
"Declist" : {'t_char', 't_bool', 't_int'},
"Declist'" : {'epsilon', 't_char', 't_bool', 't_int'},
"Dec" : {'t_bool', 't_char', 't_int'},
"Declaration" : {'t_assign', 't_semicolon', 't_comma', 't_lp', 't_lb'},
"Type" : {'t_char', 't_bool', 't_int'},
"Vardec" : {'t_lb', 't_assign', 't_semicolon', 't_comma'},
"Vardeclist" : {'t_lb', 't_assign', 'epsilon', 't_comma'},
"Vardeclist'" : {'epsilon', 't_comma'},
"VardecInit" : {'t_lb', 't_assign', 'epsilon'},
"VardecInit'" : {'t_assign', 'epsilon'},
"Array" : {'t_lb', 'epsilon'},
"Arraysize" : {'t_id', 't_decimal', 't_string', 'epsilon', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},       
"Funcdec" : {'t_lp'},
"Parameters" : {'epsilon', 't_char', 't_bool', 't_int'},
"ParameterList" : {'t_bool', 't_char', 't_int'},
"ParameterList'" : {'epsilon', 't_comma'},
"Statement" : {'t_continue', 't_id', 't_break', 't_if', 't_for', 't_print', 't_int', 't_bool', 't_lc', 't_return', 't_char'},
"CompoundStmt" : {'t_lc'},
"StatementList" : {'t_continue', 't_id', 't_break', 't_if', 't_for', 't_print', 'epsilon', 't_int', 't_bool', 't_lc', 't_return', 't_char'},
"IfStmt" : {'t_if'},
"ElseStmt" : {'t_else', 'epsilon'},
"LoopStmt" : {'t_for'},
"ForStmt" : {'t_id', 't_bool', 't_semicolon', 't_char', 't_int'},
"LoopVardec" : {'t_id', 't_bool', 'epsilon', 't_char', 't_int'},
"LoopExpr" : {'t_id', 't_decimal', 't_string', 'epsilon', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},        
"LoopStep" : {'t_id', 'epsilon'},
"SimpleStmt" : {'t_id'},
"SimpleStmt2" : {'t_id'},
"SimpleStmt3" : {'t_lp', 't_assign', 'epsilon'},
"Array2" : {'t_lb', 'epsilon'},
"Arraysize2" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},
"VardecStmt" : {'t_bool', 't_char', 't_int'},
"ReturnStmt" : {'t_return'},
"BreakStmt" : {'t_break'},
"ContinueStmt" : {'t_continue'},
"PrintStmt" : {'t_print'},
"PrintRules" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},
"PrintList" : {'epsilon', 't_comma'},
"Expression" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},
"OrExp" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},
"Or" : {'epsilon', 't_lop_or'},
"AndExp" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},
"And" : {'t_lop_and', 'epsilon'},
"NotExp" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},
"CompExp" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_true', 't_char'},
"Comp" : {'t_rop_ge', 't_rop_l', 't_rop_g', 't_rop_ne', 't_rop_le', 'epsilon', 't_rop_e'},
"Comp_OP" : {'t_rop_ge', 't_rop_l', 't_rop_g', 't_rop_ne', 't_rop_le', 't_rop_e'},
"Expr" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_true', 't_char'},
"Arth1" : {'t_aop_pl', 't_aop_mn', 'epsilon'},
"Term" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_true', 't_char'},
"Arth2" : {'t_aop_rm', 't_aop_dv', 't_aop_ml', 'epsilon'},
"Factor" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_true', 't_char'},
"Atom" : {'t_id', 't_hexadecimal', 't_false', 't_decimal', 't_string', 't_true', 't_char'},
"IsFunction" : {'t_lp', 'epsilon'},
"Parameters2" : {'t_id', 't_decimal', 't_string', 'epsilon', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},     
"ParameterList2" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_lop_not', 't_true', 't_char'},
"ParameterList2'" : {'epsilon', 't_comma'},
}

all_follow_sets = {
    "Program" : {'$'},
"Declist" : {'$'},
"Declist'" : {'$'},
"Dec" : {'t_bool', '$', 't_char', 't_int'},
"Declaration" : {'t_int', 't_bool', '$', 't_char'},
"Type" : {'t_id'},
"Vardec" : {'t_int', 't_bool', '$', 't_char'},
"Vardeclist" : {'t_semicolon'},
"Vardeclist'" : {'t_semicolon'},
"VardecInit" : {'t_semicolon', 't_comma'},
"VardecInit'" : {'t_semicolon', 't_comma'},
"Array" : {'t_rp', 't_assign', 't_semicolon', 't_comma'},
"Arraysize" : {'t_rb'},
"Funcdec" : {'t_int', 't_bool', '$', 't_char'},
"Parameters" : {'t_rp'},
"ParameterList" : {'t_rp'},
"ParameterList'" : {'t_rp'},
"Statement" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"CompoundStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', '$', 't_bool', 't_else', 't_char'},"StatementList" : {'t_rc'},
"IfStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"ElseStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"LoopStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"ForStmt" : {'t_rp'},
"LoopVardec" : {'t_semicolon'},
"LoopExpr" : {'t_semicolon'},
"LoopStep" : {'t_rp'},
"SimpleStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"SimpleStmt2" : {'t_rp'},
"SimpleStmt3" : {'t_rp', 't_semicolon'},
"Array2" : {'t_rp', 't_assign', 't_semicolon', 't_lp'},
"Arraysize2" : {'t_rb'},
"VardecStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"ReturnStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"BreakStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"ContinueStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"PrintStmt" : {'t_id', 't_for', 't_int', 't_lc', 't_return', 't_continue', 't_rc', 't_break', 't_if', 't_print', 't_bool', '$', 't_char'},
"PrintRules" : {'t_rp'},
"PrintList" : {'t_rp'},
"Expression" : {'t_comma', 't_lb', 't_rp', 't_assign', 't_semicolon', 't_rb'},
"OrExp" : {'t_comma', 't_lb', 't_rp', 't_assign', 't_semicolon', 't_rb'},
"Or" : {'t_comma', 't_lb', 't_rp', 't_assign', 't_semicolon', 't_rb'},
"AndExp" : {'t_lop_or', 't_comma', 't_lb', 't_rp', 't_assign', 't_semicolon', 't_rb'},
"And" : {'t_lop_or', 't_comma', 't_lb', 't_rp', 't_assign', 't_semicolon', 't_rb'},
"NotExp" : {'t_lop_or', 't_comma', 't_lb', 't_rp', 't_assign', 't_semicolon', 't_lop_and', 't_rb'},
"CompExp" : {'t_lop_or', 't_comma', 't_lb', 't_rp', 't_assign', 't_semicolon', 't_lop_and', 't_rb'},
"Comp" : {'t_lop_or', 't_comma', 't_lb', 't_rp', 't_assign', 't_semicolon', 't_lop_and', 't_rb'},
"Comp_OP" : {'t_id', 't_decimal', 't_string', 't_aop_pl', 't_aop_mn', 't_false', 't_hexadecimal', 't_true', 't_char'},
"Expr" : {'t_rop_l', 't_comma', 't_lop_and', 't_rop_ge', 't_lop_or', 't_rop_ne', 't_rop_le', 't_lb', 't_rop_e', 't_rp', 't_assign', 't_semicolon', 't_rop_g', 't_rb'},
"Arth1" : {'t_rop_l', 't_comma', 't_lop_and', 't_rop_ge', 't_lop_or', 't_rop_ne', 't_rop_le', 't_lb', 't_rop_e', 't_rp', 't_assign', 't_semicolon', 't_rop_g', 't_rb'},
"Term" : {'t_rop_l', 't_comma', 't_lop_and', 't_rop_ge', 't_lop_or', 't_rop_ne', 't_rop_le', 't_lb', 't_rop_e', 't_aop_pl', 't_aop_mn', 't_rp', 't_assign', 't_semicolon', 't_rop_g', 't_rb'},
"Arth2" : {'t_rop_l', 't_comma', 't_lop_and', 't_rop_ge', 't_lop_or', 't_rop_ne', 't_rop_le', 't_lb', 't_rop_e', 't_aop_pl', 't_aop_mn', 't_rp', 't_assign', 't_semicolon', 't_rop_g', 't_rb'},
"Factor" : {'t_rop_l', 't_comma', 't_aop_rm', 't_aop_ml', 't_lop_and', 't_rop_ge', 't_aop_dv', 't_lop_or', 't_rop_ne', 't_rop_le', 't_lb', 't_rop_e', 't_aop_pl', 't_aop_mn', 't_rp', 't_assign', 't_semicolon', 't_rop_g', 't_rb'},
"Atom" : {'t_rop_l', 't_aop_rm', 't_lop_and', 't_lop_or', 't_rop_le', 't_lb', 't_assign', 't_comma', 't_aop_ml', 't_rop_ge', 't_aop_dv', 't_rop_ne', 't_rop_e', 't_aop_pl', 't_aop_mn', 't_rp', 't_semicolon', 't_rop_g', 't_rb'},
"IsFunction" : {'t_rop_l', 't_aop_rm', 't_lop_and', 't_lop_or', 't_rop_le', 't_lb', 't_assign', 't_comma', 't_aop_ml', 't_rop_ge', 't_aop_dv', 't_rop_ne', 't_rop_e', 't_aop_pl', 't_aop_mn', 't_rp', 't_semicolon', 't_rop_g', 't_rb'},
"Parameters2" : {'t_rp'},
"ParameterList2" : {'t_rp'},
"ParameterList2'" : {'t_rp'},
}
