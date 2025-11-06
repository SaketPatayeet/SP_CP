# parser.py
from lexer import tokenize

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f'Program({self.statements})'

class Print(ASTNode):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f'Print({self.expr})'

class Assign(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def __repr__(self):
        return f'Assign({self.name}, {self.expr})'

class If(ASTNode):
    def __init__(self, cond, then_block, else_block=None):
        self.cond = cond
        self.then_block = then_block
        self.else_block = else_block
    def __repr__(self):
        return f'If({self.cond}, then={self.then_block}, else={self.else_block})'

class While(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    def __repr__(self):
        return f'While({self.cond}, body={self.body})'

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f'BinOp({self.left}, {self.op}, {self.right})'

class Num(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Num({self.value})'

class Str(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Str({self.value!r})'

class Var(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Var({self.name})'

class Parser:
    def __init__(self, tokens):
        # filter out NEWLINE tokens for simplicity in this parser
        self.tokens = [t for t in tokens if t[0] != 'NEWLINE']
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '', 0, 0)

    def next(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def expect(self, kind):
        tok = self.peek()
        if tok[0] != kind:
            raise SyntaxError(f'Expected {kind} but got {tok[0]} at {tok[2]}:{tok[3]}')
        return self.next()

    def parse(self):
        stmts = []
        while self.peek()[0] != 'EOF':
            stmts.append(self.statement())
        return Program(stmts)

    def statement(self):
        tok = self.peek()
        if tok[0] == 'PRINT':
            self.next()
            expr = self.expr()
            return Print(expr)
        elif tok[0] == 'ID':
            name = self.next()[1]
            if self.peek()[0] == 'ASSIGN':
                self.next()
                expr = self.expr()
                return Assign(name, expr)
            else:
                raise SyntaxError(f'Expected = after identifier at {tok[2]}:{tok[3]}')
        elif tok[0] == 'IF':
            self.next()
            cond = self.expr()
            self.expect('THEN')
            then_block = []
            # parse until ELSE or EOF (note: simple block handling)
            while self.peek()[0] not in ('ELSE', 'EOF'):
                then_block.append(self.statement())
            else_block = None
            if self.peek()[0] == 'ELSE':
                self.next()
                else_block = []
                while self.peek()[0] != 'EOF':
                    else_block.append(self.statement())
            return If(cond, then_block, else_block)
        elif tok[0] == 'WHILE':
            self.next()
            cond = self.expr()
            body = []
            while self.peek()[0] != 'EOF':
                body.append(self.statement())
            return While(cond, body)
        elif tok[0] == 'LET':
            # LET <ID> = <expr>
            self.next()  # consume LET
            id_tok = self.expect('ID')
            self.expect('ASSIGN')
            expr = self.expr()
            return ('let', id_tok[1], expr)
        else:
            raise SyntaxError(f'Unknown statement starting with {tok[0]} at {tok[2]}')
        

    # expression: handles +, -, == (left associative)
    def expr(self):
        node = self.term()
        while self.peek()[0] in ('PLUS', 'MINUS', 'EQ'):
            op = self.next()[0]
            right = self.term()
            node = BinOp(node, op, right)
        return node

    # term: handles * and /
    def term(self):
        node = self.factor()
        while self.peek()[0] in ('MUL', 'DIV'):
            op = self.next()[0]
            right = self.factor()
            node = BinOp(node, op, right)
        return node

    def factor(self):
        tok = self.peek()
        if tok[0] == 'NUMBER':
            self.next()
            return Num(tok[1])
        if tok[0] == 'STRING':
            self.next()
            return Str(tok[1])
        if tok[0] == 'ID':
            self.next()
            return Var(tok[1])
        if tok[0] == 'LPAREN':
            self.next()
            node = self.expr()
            self.expect('RPAREN')
            return node
        raise SyntaxError(f'Unexpected token in factor: {tok[0]} at {tok[2]}:{tok[3]}')

def parse_code(code):
    toks = list(tokenize(code))
    p = Parser(toks + [('EOF', '', 0, 0)])
    return p.parse()

# quick self-test
if __name__ == '__main__':
    s = 'बदलवा a = 5\nलिहा a\n'
    ast = parse_code(s)
    print(ast)
