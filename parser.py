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
    def __init__(self, target, expr):
        # target may be a Var(name) or Index(array_expr, index_expr)
        self.target = target
        self.expr = expr
    def __repr__(self):
        return f'Assign({self.target}, {self.expr})'

class Let(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def __repr__(self):
        return f'Let({self.name}, {self.expr})'

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

class ForLoop(ASTNode):
    def __init__(self, var, start, end, body):
        self.var = var
        self.start = start
        self.end = end
        self.body = body
    def __repr__(self):
        return f"ForLoop({self.var}, {self.start}, {self.end}, {self.body})"

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

class ArrayLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f'Array({self.elements})'

class Index(ASTNode):
    def __init__(self, array_expr, index_expr):
        self.array = array_expr
        self.index = index_expr
    def __repr__(self):
        return f'Index({self.array}, {self.index})'


class Parser:
    def __init__(self, tokens):
        # Remove NEWLINEs for simpler parsing
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
            # Check for array indexing
            if self.peek()[0] == 'LBRACK':
                self.next()
                idx = self.expr()
                self.expect('RBRACK')
                target = Index(Var(name), idx)
            else:
                target = Var(name)
            self.expect('ASSIGN')
            expr = self.expr()
            return Assign(target, expr)

        elif tok[0] == 'LET':
            self.next()
            id_tok = self.expect('ID')
            self.expect('ASSIGN')
            expr = self.expr()
            return Let(id_tok[1], expr)

        elif tok[0] == 'IF':
            self.next()
            cond = self.expr()
            self.expect('THEN')
            then_block = []
            while self.peek()[0] not in ('ELSE', 'END', 'EOF'):
                then_block.append(self.statement())

            else_block = None
            if self.peek()[0] == 'ELSE':
                self.next()
                else_block = []
                while self.peek()[0] not in ('END', 'EOF'):
                    else_block.append(self.statement())

            if self.peek()[0] == 'END':
                self.next()
            return If(cond, then_block, else_block)

        elif tok[0] == 'WHILE':
            self.next()
            cond = self.expr()
            self.expect('THEN')
            body = []
            while self.peek()[0] not in ('END', 'EOF'):
                body.append(self.statement())
            if self.peek()[0] == 'END':
                self.next()
            return While(cond, body)

        elif tok[0] == 'FOR':
            # साठी i = start ते end तर
            self.next()
            var_name = self.expect('ID')[1]
            self.expect('ASSIGN')
            start_expr = self.expr()
            self.expect('TO')
            end_expr = self.expr()
            self.expect('THEN')

            body = []
            while self.peek()[0] not in ('END', 'EOF'):
                body.append(self.statement())
            if self.peek()[0] == 'END':
                self.next()
            return ForLoop(var_name, start_expr, end_expr, body)

        else:
            raise SyntaxError(f'Unknown statement starting with {tok[0]} at {tok[2]}')

    # ---------- EXPRESSION PARSING ----------

    def expr(self):
        return self.parse_or()

    def parse_or(self):
        node = self.parse_and()
        while self.peek()[0] == 'OR':
            self.next()
            right = self.parse_and()
            node = BinOp(node, 'OR', right)
        return node

    def parse_and(self):
        node = self.parse_not()
        while self.peek()[0] == 'AND':
            self.next()
            right = self.parse_not()
            node = BinOp(node, 'AND', right)
        return node

    def parse_not(self):
        if self.peek()[0] == 'NOT':
            self.next()
            operand = self.parse_comparison()
            return BinOp(Num(0), 'EQ', operand)
        return self.parse_comparison()

    def parse_comparison(self):
        node = self.parse_addsub()
        while self.peek()[0] in ('EQ', 'NE', 'LT', 'GT', 'LE', 'GE'):
            op = self.next()[0]
            right = self.parse_addsub()
            node = BinOp(node, op, right)
        return node

    def parse_addsub(self):
        node = self.parse_muldivmod()
        while self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.next()[0]
            right = self.parse_muldivmod()
            node = BinOp(node, op, right)
        return node

    def parse_muldivmod(self):
        node = self.parse_power()
        while self.peek()[0] in ('MUL', 'DIV', 'MOD'):
            op = self.next()[0]
            right = self.parse_power()
            node = BinOp(node, op, right)
        return node

    def parse_power(self):
        node = self.factor()
        while self.peek()[0] == 'POW':
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
            name = self.next()[1]
            node = Var(name)
            if self.peek()[0] == 'LBRACK':
                self.next()
                idx = self.expr()
                self.expect('RBRACK')
                node = Index(node, idx)
            return node
        if tok[0] == 'LPAREN':
            self.next()
            node = self.expr()
            self.expect('RPAREN')
            return node
        if tok[0] == 'LBRACK':
            self.next()
            elems = []
            if self.peek()[0] != 'RBRACK':
                elems.append(self.expr())
                while self.peek()[0] == 'COMMA':
                    self.next()
                    elems.append(self.expr())
            self.expect('RBRACK')
            return ArrayLiteral(elems)
        raise SyntaxError(f'Unexpected token in factor: {tok[0]} at {tok[2]}:{tok[3]}')

def parse_code(code):
    toks = list(tokenize(code))
    p = Parser(toks + [('EOF', '', 0, 0)])
    return p.parse()

if __name__ == '__main__':
    s = 'बदलवा a = [1,2,3]\nलिहा a[1]\n'
    ast = parse_code(s)
    print(ast)
