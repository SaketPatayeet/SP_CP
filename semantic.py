from parser import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}  # name -> type ('int' or 'str' or 'list')
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

    def analyze_Let(self, node):
        t = self.evaluate_type(node.expr)
        
        self.symbols[node.name] = t or 'int'

    def analyze_Print(self, node):
        _ = self.evaluate_type(node.expr)

    def analyze_Assign(self, node):
        # target can be Var or Index
        t = self.evaluate_type(node.expr)
        if isinstance(node.target, Var):
            name = node.target.name
            if name not in self.symbols:
                self.errors.append(f'Use of undeclared variable {name}')
            else:
                if t is None:
                    self.errors.append(f'Cannot determine type of expression assigned to {name}')
                else:
                    self.symbols[name] = t
        elif isinstance(node.target, Index):
            # ensure array exists and is list
            arr_t = self.evaluate_type(node.target.array)
            if arr_t != 'list':
                self.errors.append('Indexing non-list value')
            # index must be int
            idx_t = self.evaluate_type(node.target.index)
            if idx_t != 'int':
                self.errors.append('List index must be integer')

    def analyze_If(self, node):
        cond_t = self.evaluate_type(node.cond)
        if cond_t != 'int':
            self.errors.append('Condition in IF must be numeric (int)')
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
    
        def analyze_ForLoop(self, node):
            # ensure loop variable exists
            if node.var not in self.symbols:
                self.symbols[node.var] = 'int'
            start_t = self.evaluate_type(node.start)
            end_t = self.evaluate_type(node.end)
            if start_t != 'int' or end_t != 'int':
                self.errors.append('For-loop range must be integers')
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
        if isinstance(expr, ArrayLiteral):
            # ensure all elements have type and are same (we'll allow ints/strs, prefer int->list)
            elem_types = []
            for e in expr.elements:
                et = self.evaluate_type(e)
                elem_types.append(et)
            # if any None, return None
            if any(t is None for t in elem_types):
                return None
            # simple policy: if all int -> list of int, else list
            if all(t == 'int' for t in elem_types):
                return 'list'
            else:
                return 'list'
        if isinstance(expr, Index):
            arr_t = self.evaluate_type(expr.array)
            idx_t = self.evaluate_type(expr.index)
            if arr_t != 'list':
                self.errors.append('Indexing non-list value')
                return None
            if idx_t != 'int':
                self.errors.append('List index must be integer')
                return None
            # element type unknown => return int or str? we assume int for arithmetic
            # return 'int' to allow arithmetic on elements that are ints
            return 'int'
        if isinstance(expr, BinOp):
            lt = self.evaluate_type(expr.left)
            rt = self.evaluate_type(expr.right)
            if lt is None or rt is None:
                return None
            if expr.op in ('EQ', 'NE', 'LT', 'GT', 'LE', 'GE'):
                return 'int'
            if lt == 'int' and rt == 'int':
                return 'int'
            if lt == 'str' or rt == 'str':
                self.errors.append('Type error: arithmetic on strings')
                return None
        return None

if __name__ == '__main__':
    from parser import parse_code
    code = 'बदलवा a = [1,2,3]\nलिहा a[1]\n'
    ast = parse_code(code)
    sem = SemanticAnalyzer()
    sem.analyze(ast)
    print('Symbols:', sem.symbols)
    print('Errors:', sem.errors)
