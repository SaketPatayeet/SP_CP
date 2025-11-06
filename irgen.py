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
        # target may be Var or Index
        if isinstance(node.target, Var):
            self.code.append(('assign', node.target.name, rhs))
        elif isinstance(node.target, Index):
            # generate index and emit index_set
            arr = self.gen(node.target.array)
            idx = self.gen(node.target.index)
            self.code.append(('index_set', arr, idx, rhs))
        else:
            raise NotImplementedError('Unknown assign target')

    def gen_Let(self, node):
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

    def gen_ArrayLiteral(self, node):
        # generate each element and produce a const_list
        elem_temps = []
        for e in node.elements:
            et = self.gen(e)
            elem_temps.append(et)
        t = self.new_temp()
        self.code.append(('const_list', t, elem_temps))
        return t

    def gen_Var(self, node):
        return node.name

    def gen_Index(self, node):
        arr = self.gen(node.array)
        idx = self.gen(node.index)
        t = self.new_temp()
        self.code.append(('index_get', t, arr, idx))
        return t

    def gen_BinOp(self, node):
        l = self.gen(node.left)
        r = self.gen(node.right)
        t = self.new_temp()
        op = node.op.lower()

        # map logical and arithmetic ops
        self.code.append(('binop', t, op, l, r))
        return t


    def gen_If(self, node):
        cond = self.gen(node.cond)
        label_else = self.new_label()
        label_end = self.new_label()
        self.code.append(('if_false_goto', cond, label_else))
        for s in node.then_block:
            self.gen(s)
        self.code.append(('goto', label_end))
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

    def gen_ForLoop(self, node):
        # साठी i = start ते end तर ... संपले
        start_val = self.gen(node.start)
        end_val = self.gen(node.end)
        self.code.append(('assign', node.var, start_val))

        loop_label = self.new_label()
        end_label = self.new_label()

        self.code.append(('label', loop_label))

        cond_temp = self.new_temp()
            # Check i < end
        self.code.append(('binop', cond_temp, 'lt', node.var, end_val))
        self.code.append(('if_false_goto', cond_temp, end_label))

            # loop body
        for s in node.body:
            self.gen(s)

            # increment i = i + 1
        one_temp = self.new_temp()
        self.code.append(('const', one_temp, 1))
        add_temp = self.new_temp()
        self.code.append(('binop', add_temp, 'plus', node.var, one_temp))
        self.code.append(('assign', node.var, add_temp))

        self.code.append(('goto', loop_label))
        self.code.append(('label', end_label))

