# irgen.py
from parser import *

class IRGen:
    def __init__(self):
        self.code = []     # list of instructions (tuples)
        self.temp_id = 0
        self.label_id = 0

    def new_temp(self):
        name = f't{self.temp_id}'
        self.temp_id += 1
        return name

    def new_label(self):
        lab = f'L{self.label_id}'
        self.label_id += 1
        return lab

    def gen(self, node):
        method = 'gen_' + node.__class__.__name__
        if hasattr(self, method):
            return getattr(self, method)(node)
        else:
            raise NotImplementedError(f'No gen for {node.__class__.__name__}')

    def gen_Program(self, node):
        for s in node.statements:
            self.gen(s)
        return self.code

    def gen_Print(self, node):
        src = self.gen(node.expr)
        self.code.append(('print', src))

    def gen_Assign(self, node):
        rhs = self.gen(node.expr)
        self.code.append(('assign', node.name, rhs))

    def gen_Num(self, node):
        t = self.new_temp()
        self.code.append(('const', t, node.value))
        return t

    def gen_Str(self, node):
        t = self.new_temp()
        self.code.append(('const_str', t, node.value))
        return t

    def gen_Var(self, node):
        return node.name

    def gen_BinOp(self, node):
        l = self.gen(node.left)
        r = self.gen(node.right)
        t = self.new_temp()
        op = node.op.lower()  # PLUS -> plus, EQ -> eq
        self.code.append(('binop', t, op, l, r))
        return t

    def gen_If(self, node):
        # generate cond
        cond = self.gen(node.cond)
        label_else = self.new_label()
        label_end = self.new_label()
        # if cond == 0 goto else
        self.code.append(('if_false_goto', cond, label_else))
        # then-block
        for s in node.then_block:
            self.gen(s)
        self.code.append(('goto', label_end))
        # else label
        self.code.append(('label', label_else))
        if node.else_block:
            for s in node.else_block:
                self.gen(s)
        self.code.append(('label', label_end))

    def gen_While(self, node):
        start = self.new_label()
        end = self.new_label()
        self.code.append(('label', start))
        cond = self.gen(node.cond)
        self.code.append(('if_false_goto', cond, end))
        for s in node.body:
            self.gen(s)
        self.code.append(('goto', start))
        self.code.append(('label', end))
