C_KEYWORDS = {
    'int': 'TOK_INT', 
    'float': 'TOK_FLOAT', 
    'double': 'TOK_DOUBLE',
    'char': 'TOK_CHAR', 
    'void': 'TOK_VOID', 
    'short': 'TOK_SHORT', 
    'long': 'TOK_LONG', 
    'signed': 'TOK_SIGNED', 
    'unsigned': 'TOK_UNSIGNED', 
    'if': 'TOK_IF', 
    'else': 'TOK_ELSE', 
    'for': 'TOK_FOR', 
    'while': 'TOK_WHILE', 
    'do': 'TOK_DO', 
    'switch': 'TOK_SWITCH', 
    'case': 'TOK_CASE', 
    'default': 'TOK_DEFAULT', 
    'break': 'TOK_BREAK', 
    'continue': 'TOK_CONTINUE', 
    'return': 'TOK_RETURN', 
    'static': 'TOK_STATIC', 
    'extern': 'TOK_EXTERN', 
    'auto': 'TOK_AUTO', 
    'register': 'TOK_REGISTER', 
    'const': 'TOK_CONST', 
    'volatile': 'TOK_VOLATILE', 
    'restrict': 'TOK_RESTRICT', 
    'struct': 'TOK_STRUCT', 
    'union': 'TOK_UNION', 
    'typedef': 'TOK_TYPEDEF', 
    'enum': 'TOK_ENUM', 
    'sizeof': 'TOK_SIZEOF'
}

PYTHON_KEYWORDS = {
    'if': 'TOK_IF',
    'elif': 'TOK_ELIF',
    'else': 'TOK_ELSE',
    'for': 'TOK_FOR',
    'while': 'TOK_WHILE',
    'break': 'TOK_BREAK',
    'continue': 'TOK_CONTINUE',
    'return': 'TOK_RETURN',
    'pass': 'TOK_PASS',
    'yield': 'TOK_YIELD',
    'raise': 'TOK_RAISE',
    'def': 'TOK_DEF',
    'class': 'TOK_CLASS',
    'lambda': 'TOK_LAMBDA',
    'with': 'TOK_WITH',
    'as': 'TOK_AS',
    'try': 'TOK_TRY',
    'except': 'TOK_EXCEPT',
    'finally': 'TOK_FINALLY',
    'import': 'TOK_IMPORT',
    'from': 'TOK_FROM',
    'global': 'TOK_GLOBAL',
    'nonlocal': 'TOK_NONLOCAL',
    'True': 'TOK_TRUE',
    'False': 'TOK_FALSE',
    'None': 'TOK_NONE',
    'and': 'TOK_AND',
    'or': 'TOK_OR',
    'not': 'TOK_NOT',
    'in': 'TOK_IN',
    'is': 'TOK_IS',
    'del': 'TOK_DEL',
    'assert': 'TOK_ASSERT',
    'async': 'TOK_ASYNC',
    'await': 'TOK_AWAIT'
}

TOKEN_TO_KEYWORD_C = {v : k for k, v in C_KEYWORDS.items()}

TOKEN_TO_KEYWORD_PY = {v : k for k, v in PYTHON_KEYWORDS.items()}

def is_c_keyword(word):
    return word in C_KEYWORDS

def is_py_keyword(word):
    return word in PYTHON_KEYWORDS

def is_keyword(word, language):
    if language == 'C':
        return is_c_keyword(word)
    elif language == 'Python':
        return is_py_keyword(word)
    else:
        raise ValueError("Unsupported language: {}".format(language))

def get_token_type(word, language):

    if language == 'C':
        return C_KEYWORDS.get(word, 'TOK_IDENTIFIER')
    elif language == 'Python':
        return PYTHON_KEYWORDS.get(word, 'TOK_IDENTIFIER')
    else:
        raise ValueError("Unsupported language: {}".format(language))