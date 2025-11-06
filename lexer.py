import re

# Token specification (order matters: longer first)
TOKEN_SPEC = [
    ('COMMENT',   r'\#.*'),
    ('STRING',    r'"[^"\n]*"'),
    ('NUMBER',    r'\d+'),
    ('EQ',        r'=='),
    ('NE',        r'!='),
    ('LE',        r'<='),
    ('GE',        r'>='),
    ('LT',        r'<'),
    ('GT',        r'>'),
    ('ASSIGN',    r'='),
    ('PLUS',      r'\+'),
    ('MINUS',     r'-'),
    ('MUL',       r'\*'),
    ('DIV',       r'/'),
    ('MOD',       r'%'),
    ('POW',       r'\^'),
    ('LBRACK',    r'\['),
    ('RBRACK',    r'\]'),
    ('COMMA',     r','),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('NEWLINE',   r'\n'),
    ('SKIP',      r'[ \t]+'),
    ('ID', r'[A-Za-z\u0900-\u097F_][A-Za-z0-9\u0900-\u097F_]*'),
    ('MISMATCH',  r'.'),
]


# Map Marathi keywords (Devanagari) to token types
KEYWORDS = {
    'जर': 'IF',
    'तर': 'THEN',
    'नाहीतर': 'ELSE',
    'जोपर्यंत': 'WHILE',
    'साठी': 'FOR', 
    'लिहा': 'PRINT',
    'बदलवा': 'LET',
    'आणि': 'AND',
    'किंवा': 'OR',
    'नाही': 'NOT',
    'संपले': 'END',
    'ते': 'TO',
}

master_pat = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC))

def tokenize(code):
    """Yield tokens as tuples: (type, value, lineno, col)"""
    lineno = 1
    line_start = 0
    for mo in master_pat.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1
        if kind == 'NUMBER':
            yield ('NUMBER', int(value), lineno, column)
        elif kind == 'STRING':
            yield ('STRING', value[1:-1], lineno, column)
        elif kind == 'ID':
            if value in KEYWORDS:
                yield (KEYWORDS[value], value, lineno, column)
            else:
                yield ('ID', value, lineno, column)
        elif kind == 'NEWLINE':
            lineno += 1
            line_start = mo.end()
            yield ('NEWLINE', '\n', lineno-1, column)
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character {value!r} at line {lineno} col {column}')
        else:
            yield (kind, value, lineno, column)

if __name__ == '__main__':
    sample = 'बदलवा a = 5\nलिहा "नमस्कार"\n'
    for t in tokenize(sample):
        print(t)
