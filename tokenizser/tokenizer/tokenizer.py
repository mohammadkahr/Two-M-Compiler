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
def operators(token: str):
    state = 0
    temp = get_token_until_delimiter(token)
    
    if temp == "":
        return False, None

    for char in temp:
        if state == 0:
            if char in "=+-*/%!<>":
                state = 1  
            else:
                return False, None  
        elif state == 1:
            if char in "=+-*/%!<>":
                continue  
            else:
                break  
    
    if temp in tokenMap:
        return True, temp  
    else:
        return False, None  



# Function to check if a token is a hexadecimal number
def hex(s: str) -> bool:
    state = 0
    for char in s.lower():
        if state == 0:
            if char == '0':
                state = 1  # Transition to State 1 upon encountering '0'
            else:
                return False  # Invalid token (does not start with '0')
        elif state == 1:
            if char == 'x':
                state = 2  # Transition to State 2 upon encountering 'x'
            else:
                return False  # Invalid token (missing 'x' after '0')
        elif state == 2:
            if char in "0123456789abcdef":
                continue  # Stay in State 2 for valid hexadecimal digits
            else:
                return False  # Invalid token (encountered non-hexadecimal character)
    return state == 2  # Return True if the final state is 2, indicating a valid hexadecimal number



# Function to remove comments
def comment(token: str):
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

def identifier(token: str):
    state = 0
    temp = get_token_until_delimiter(token)
    if len(temp) == 0:
        return False, None
    
    for char in temp:
        if state == 0:
            if char == '_' or char.isalpha():
                state = 1
            else:
                return False, None
        elif state == 1:
            if char.isalnum() or char == '_':
                continue
            else:
                return False, None
    
    return state == 1, temp if state == 1 else None



# Function to check if a character is a delimiter
def delimiter(token: str):
    token_name = get_token_name(token)
    if (token == '[' or token == ']' or token == '(' or token == ')' or
            token == '{' or token == '}' or token == ';' or token == ','):
        return True, token_name
    else:
        return False, None


# Function to check if a token is a numeric literal
def litnum(token: str):  # in monde
    if token and (token[0].isnumeric() or token[0] == '-'):
        tok = get_token_until_delimiter(token)
        if hex(tok):
            return True, "T_HexaDecimal", tok
        elif token[0] == '-' and len(tok) > 1 and tok[1:].isnumeric():
            return True, "T_Decimal", tok
        elif tok.isnumeric():
            return True, "T_Decimal", tok
    return False, None, None


def bin(s: str) -> bool:
    state = 0
    for c in s.lower():
        if state == 0:
            if c == "0":
                state = 1
            else:
                return False
        elif state == 1:
            if c == "b":
                state = 2
            elif c in "01":
                return False
            else:
                return False
        elif state == 2:
            if c not in "01":
                return False
    return True



# Function to check if a token is a string literal

def litstring(token: str):
    state = 0
    temp = token
    if temp[0] == "'":
        state = 1
    elif temp[0] == '"':
        state = 2
    else:
        return False, None, None
    
    for i in range(1, len(temp)):
        if state == 1:  # Single quotes
            if temp[i] == "'":
                return True, "T_Char", temp[:i+1]
        elif state == 2:  # Double quotes
            if temp[i] == '"':
                return True, "T_String", temp[:i+1]

    return False, None, None



# Function to check if a token is a keyword
def keyword(token: str):
    tok = get_token_until_delimiter(token)
    if tok in KEYWORDS:
        return True, tok.capitalize()
    else:
        return False, None


# Function to check if a character is whitespace
def whitespace(token: str):
    state = 0
    for char in token:
        if state == 0:
            if char.isspace():
                state = 1  
            else:
                return False
        elif state == 1:
            if char.isspace():
                continue  
            else:
                return False  
    return state == 1  


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
def tokenizer():
    count = 0
    for line in read_file_line("test.txt"):
        count += 1
        start = 0
        while start < len(line):
            if comment(line[start:]):
                yield Token("T_Comment", count, line[start + 2:], count)
                start = len(line)
            elif whitespace(line[start:start + 1]):
                yield Token("T_Whitespace", count, line[start:start + 1], count)
            elif delimiter(line[start:start + 1])[0]:
                yield Token(delimiter(line[start:start + 1])[1], count, line[start:start + 1], count)
            elif litnum(line[start:])[0]:
                _, token_name, number = litnum(line[start:])
                yield Token(token_name, count, number, count)
                start += len(number) - 1
            elif keyword(line[start:])[0]:
                yield Token("T_" + keyword(line[start:])[1], count, line[start:start + len(keyword(line[start:])[1])],
                            count)
                start += len(keyword(line[start:])[1]) - 1

            elif identifier(line[start:])[0]:
                yield Token("T_ID", count, identifier(line[start:])[1], count)
                start += len(identifier(line[start:])[1]) - 1
            elif operators(line[start:])[0]:
                operator = operators(line[start:])[1]
                token_name = get_token_name(operator)
                yield Token(token_name, count, operator, count)

            elif litstring(line[start:])[0]:
                _, token_name, word = litstring(line[start:])
                yield Token(token_name, count, word, count)
                start += len(word) - 1
            start += 1


if __name__ == "__main__":
    gen = tokenizer()

    with open("output1.txt", "w") as output_file:
        for token in gen:
            if token.name != "T_Whitespace":
                output_file.write(str(token) + "\n")
