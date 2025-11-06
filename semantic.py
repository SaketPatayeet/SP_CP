# semantic.py
from parser import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}  # name -> type ('int' or 'str')
        self.errors = []

    def analyze(self, node):
        method = 'analyze_' + node.__class__.__name__
        if hasattr(self, method):
            return getattr(self, method)(node)
        else:
            # generic traversal
            for child in getattr(node, '__dict__', {}).values():
                if isinstance(child, list):
                    for c in child:
                        if isinstance(c, ASTNode):
                            self.analyze(c)
                elif isinstance(child, ASTNode):
                    self.analyze(child)

    def analyze_Program(self, node):
        for s in node.statements:
            self.analyze(s)

    def analyze_Print(self, node):
        _ = self.evaluate_type(node.expr)

    def analyze_Assign(self, node):
        t = self.evaluate_type(node.expr)
        if t is None:
            self.errors.append(f'Cannot determine type of expression assigned to {node.name}')
        else:
            if node.name in self.symbols and self.symbols[node.name] != t:
                self.errors.append(f'Type error: variable {node.name} previously {self.symbols[node.name]} now {t}')
            self.symbols[node.name] = t

    # ✅ Added support for Marathi 'बदलवा' (let declaration)
    def analyze_let(self, node):
        t = self.evaluate_type(node[2]) if isinstance(node, tuple) else None
        var_name = node[1] if isinstance(node, tuple) else None
        if var_name:
            if var_name in self.symbols:
                self.errors.append(f'Variable {var_name} already declared')
            else:
                self.symbols[var_name] = t or 'int'

    def analyze_If(self, node):
        cond_t = self.evaluate_type(node.cond)
        # ✅ Allow comparison operations too
        if cond_t != 'int':
            if not (isinstance(node.cond, BinOp) and node.cond.op in ('EQ', 'NE', 'LT', 'GT', 'LE', 'GE')):
                self.errors.append('Condition in IF must be numeric or comparison')
        for s in node.then_block:
            self.analyze(s)
        if node.else_block:
            for s in node.else_block:
                self.analyze(s)

    def analyze_While(self, node):
        cond_t = self.evaluate_type(node.cond)
        if cond_t != 'int':
            self.errors.append('Condition in WHILE must be numeric (0=false, non-zero=true)')
        for s in node.body:
            self.analyze(s)

    def evaluate_type(self, expr):
        if isinstance(expr, Num):
            return 'int'
        if isinstance(expr, Str):
            return 'str'
        if isinstance(expr, Var):
            if expr.name not in self.symbols:
                self.errors.append(f'Use of undeclared variable {expr.name}')
                return None
            return self.symbols[expr.name]
        if isinstance(expr, BinOp):
            lt = self.evaluate_type(expr.left)
            rt = self.evaluate_type(expr.right)
            if lt is None or rt is None:
                return None
            # ✅ EQ, NE, LT, GT etc always return int (boolean)
            if expr.op in ('EQ', 'NE', 'LT', 'GT', 'LE', 'GE'):
                return 'int'
            if lt == 'int' and rt == 'int':
                return 'int'
            # arithmetic on strings -> error
            if lt == 'str' or rt == 'str':
                self.errors.append('Type error: arithmetic on strings')
                return None
        return None


# self-test
if __name__ == '__main__':
    from parser import parse_code
    code = 'बदलवा a = 5\nजर a == 5 तर\n    लिहा "ok"\nनाहीतर\n    लिहा "no"\n'
    ast = parse_code(code)
    sem = SemanticAnalyzer()
    sem.analyze(ast)
    print('Symbols:', sem.symbols)
    print('Errors:', sem.errors)
