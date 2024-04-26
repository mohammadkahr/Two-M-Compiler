# Constants
KEYWORDS = {"bool", "break", "char", "continue", "else", "false",
            "for", "if", "int", "print", "return", "true"}
ARITHMETIC_OPERATORS = {"+", "-", "*", "/", "%"}
RELATIONAL_OPERATORS = {">", ">=", "<", "<=", "==", "!="}
LOGICAL_OPERATORS = {"&&", "||", "!", "="}
SINGS_OPERATORS = {"{", "}", "(", ")", "[", "]", ",", ";"}

# Token mapping
tokenMap = {'bool': 'T_Bool', 'break': 'T_Break', 'char': 'T_Char', 'continue': 'T_Continue',
            'else': 'T_Else', 'false': 'T_False', 'for': 'T_For', 'if': 'T_If', 'int': 'T_Int',
            'print': 'T_Print', 'return': 'T_Return', 'true': 'T_True', '+': 'T_AOp_P',
            '-': 'T_AOp_M', '*': 'T_AOp_T', '/': 'T_AOp_D', '%': 'T_AOp_R', '>': 'T_ROp_GT',
            '>=': 'T_ROp_GE', '<': 'T_ROp_LT', '<=': 'T_ROp_LE', '==': 'T_ROp_EQ', '!=': 'T_ROp_NE',
            '&&': 'T_LOp_AND', '||': 'T_LOp_OR', '!': 'T_LOp_NOT', '=': 'T_Assign', '{': 'T_LCurly',
            '}': 'T_RCurly', '(': 'T_LParen', ')': 'T_RParen', '[': 'T_LSquare', ']': 'T_RSqaure',
            ',': 'T_Comma', ';': 'T_Semicolon'
            }


# Function to get the token name
def get_token_name(token: str):
    token_name = ''
    if token in tokenMap.keys():
        token_name = tokenMap[token]
    return token_name


# Function to get token until delimiters or whitespace
def get_token_until_delimiter(token: str) -> str:
    index = 0
    for i, char in enumerate(token):
        if char in SINGS_OPERATORS or char.isspace():
            index = i
            break
    return token[:index]


# Function to check if a character is an operator
def is_operator(string: str):
    operators = ['=', '+', '-', '*', '/', '%', '!', '<', '>']
    if string[0] in operators:
        return True, string[0]
    return False, None


# Function to check if a token is a hexadecimal number
def is_hex(s: str) -> bool:
    return s.lower().startswith("0x") and all(c in "0123456789abcdef" for c in s[2:].lower())


# Function to remove comments
def is_comment(token: str):
    state = 0
    for char in token:
        if state == 0:
            if char == "/":
                state = 1
        elif state == 1:
            if char == "/":
                state = 2
        elif state == 2:
            return True
    return False


# Function to check if a token is an identifier
def is_identifier(token: str):
    temp = get_token_until_delimiter(token)
    if len(temp) == 0:
        return False, None
    if temp[0] == '_' or temp[0].isalpha():
        for char in temp:
            if not char.isalnum() and char != '_':
                return False, None
        return True, temp
    return False, None


# Function to check if a character is a delimiter
def is_delimiter(token: str):
    token_name = get_token_name(token)
    if (token == '[' or token == ']' or token == '(' or token == ')' or
            token == '{' or token == '}' or token == ';' or token == ','):
        return True, token_name
    else:
        return False, None


# Function to check if a token is a numeric literal
def is_litnum(token: str):  # in monde
    if token and (token[0].isnumeric() or token[0] == '-'):
        tok = get_token_until_delimiter(token)
        if is_hex(tok):
            return True, "T_HexaDecimal", tok
        elif token[0] == '-' and len(tok) > 1 and tok[1:].isnumeric():
            return True, "T_Decimal", tok
        elif tok.isnumeric():
            return True, "T_Decimal", tok
    return False, None, None


# Function to check if a token is a string literal
def is_litstring(token: str):
    if token[0] == "'":
        if len(token) >= 3 and token[2] == "'":
            return True, "T_Char", token[:3]
        elif len(token) >= 4 and token[1] == '\\' and token[3] == "'":
            return True, "T_Char", token[:4]
    elif token[0] == '"':
        index = 1
        while index < len(token):
            if token[index] == '"':
                if token[index - 1] != '\\':
                    return True, "T_String", token[:index + 1]
            index += 1
    return False, None, None


# Function to check if a token is a keyword
def is_keyword(token: str):
    tok = get_token_until_delimiter(token)
    if tok in KEYWORDS:
        return True, tok.capitalize()
    else:
        return False, None


# Function to check if a character is whitespace
def is_whitespace(token: str):
    if ord(token) == 32 or ord(token) == 10 or ord(token) == 9:
        return True
    else:
        return False


# Function to read file line by line
def read_file_line(file_name: str):
    with open(file_name, "r") as file:
        for line in file:
            yield line


# Class to represent tokens
class Token:
    def __init__(self, name, line_num, value, count):
        self.name = name
        self.line_num = line_num
        self.value = value
        self.count = count

    def __str__(self) -> str:
        return f"{repr(self.value)} -> {self.name} in line: {self.line_num}"


# Function to generate tokens
def get_tokens():
    count = 0
    for line in read_file_line("tokens.txt"):
        count += 1
        beg = 0
        while beg < len(line):
            if is_comment(line[beg:]):
                yield Token("T_Comment", count, line[beg + 2:], count)
                beg = len(line)
            elif is_whitespace(line[beg:beg + 1]):
                yield Token("T_Whitespace", count, line[beg:beg + 1], count)
            elif is_delimiter(line[beg:beg + 1])[0]:
                yield Token(is_delimiter(line[beg:beg + 1])[1], count, line[beg:beg + 1], count)
            elif is_litnum(line[beg:])[0]:
                _, token_name, number = is_litnum(line[beg:])
                yield Token(token_name, count, number, count)
                beg += len(number) - 1
            elif is_keyword(line[beg:])[0]:
                yield Token("T_" + is_keyword(line[beg:])[1], count, line[beg:beg + len(is_keyword(line[beg:])[1])],
                            count)
                beg += len(is_keyword(line[beg:])[1]) - 1

            elif is_identifier(line[beg:])[0]:
                yield Token("T_ID", count, is_identifier(line[beg:])[1], count)
                beg += len(is_identifier(line[beg:])[1]) - 1
            elif is_operator(line[beg:])[0]:
                operator = is_operator(line[beg:])[1]
                token_name = get_token_name(operator)
                yield Token(token_name, count, operator, count)

            elif is_litstring(line[beg:])[0]:
                _, token_name, word = is_litstring(line[beg:])
                yield Token(token_name, count, word, count)
                beg += len(word) - 1
            beg += 1


if __name__ == "__main__":
    gen = get_tokens()

    with open("output.txt", "w") as output_file:
        for token in gen:
            if token.name != "T_Whitespace":
                output_file.write(str(token) + "\n")
