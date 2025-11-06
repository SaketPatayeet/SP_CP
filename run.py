from lexer import tokenize
from parser import parse_code
from semantic import SemanticAnalyzer
from irgen import IRGen
import sys

def load_sample(path='sample.mr'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''

def print_tokens(code):
    print('--- TOKENS ---')
    for t in tokenize(code):
        print(t)

def print_ir(ir):
    print('--- IR ---')
    for instr in ir:
        print(instr)

def interpret_ir(ir):
    print('--- IR EXECUTION OUTPUT ---')
    mem = {}   # variables and temps stored here
    labels = {}
    # first pass: collect labels -> index
    for i, ins in enumerate(ir):
        if ins[0] == 'label':
            labels[ins[1]] = i
    ip = 0
    while ip < len(ir):
        ins = ir[ip]
        op = ins[0]
        if op == 'const':
            _, temp, val = ins
            mem[temp] = val
        elif op == 'const_str':
            _, temp, val = ins
            mem[temp] = val
        elif op == 'const_list':
            _, temp, elem_temps = ins
            # resolve element values (either temp names or literals - we always store temps)
            lst = []
            for et in elem_temps:
                val = mem.get(et, et)
                if isinstance(val, str) and val in mem:
                    val = mem[val]
                lst.append(val)
            mem[temp] = lst
        elif op == 'binop':
            _, t, bop, a, b = ins
            # resolve operands (temp names or variable names or literal numbers)
            av = mem.get(a, a)
            bv = mem.get(b, b)
            # if still a name and in mem, resolve
            if isinstance(av, str) and av in mem:
                av = mem[av]
            if isinstance(bv, str) and bv in mem:
                bv = mem[bv]
            # arithmetic / comparisons
            if bop == 'plus':
                mem[t] = av + bv
            elif bop == 'minus':
                mem[t] = av - bv
            elif bop == 'mul':
                mem[t] = av * bv
            elif bop == 'div':
                # integer division
                mem[t] = av // bv
            elif bop == 'eq':
                mem[t] = 1 if av == bv else 0
            elif bop == 'ne':
                mem[t] = 1 if av != bv else 0
            elif bop == 'lt':
                mem[t] = 1 if av < bv else 0
            elif bop == 'gt':
                mem[t] = 1 if av > bv else 0
            elif bop == 'le':
                mem[t] = 1 if av <= bv else 0
            elif bop == 'ge':
                mem[t] = 1 if av >= bv else 0
            elif bop == 'mod':
                mem[t] = av % bv
            elif bop == 'pow':
                mem[t] = av ** bv
            elif bop == 'and':
                mem[t] = 1 if av and bv else 0
            elif bop == 'or':
                mem[t] = 1 if av or bv else 0
            else:
                raise RuntimeError('Unknown binop ' + bop)
        elif op == 'assign':
            _, name, src = ins
            # src may be temp or literal; resolvex
            val = mem.get(src, src)
            if isinstance(val, str) and val in mem:
                val = mem[val]
            mem[name] = val
        elif op == 'index_get':
            _, t, arr, idx = ins
            arrv = mem.get(arr, arr)
            if isinstance(arrv, str) and arrv in mem:
                arrv = mem[arrv]
            idxv = mem.get(idx, idx)
            if isinstance(idxv, str) and idxv in mem:
                idxv = mem[idxv]
            # fetch element
            mem[t] = arrv[idxv]
        elif op == 'index_set':
            _, arr, idx, src = ins
            arrv = mem.get(arr, arr)
            if isinstance(arrv, str) and arrv in mem:
                arrv = mem[arrv]
            idxv = mem.get(idx, idx)
            if isinstance(idxv, str) and idxv in mem:
                idxv = mem[idxv]
            val = mem.get(src, src)
            if isinstance(val, str) and val in mem:
                val = mem[val]
            # write into list in-place; ensure arr variable points to actual list
            if isinstance(arrv, list):
                arrv[idxv] = val
                # if arr was a variable name, ensure mem stores updated list (already stored)
            else:
                raise RuntimeError('Indexing into non-list')
        elif op == 'print':
            _, src = ins
            val = mem.get(src, src)
            if isinstance(val, str) and val in mem:
                val = mem[val]
            print(val)
        elif op == 'if_false_goto':
            _, cond, label = ins
            condv = mem.get(cond, cond)
            if isinstance(condv, str) and condv in mem:
                condv = mem[condv]
            if not condv:
                ip = labels[label]
                continue
        elif op == 'goto':
            _, label = ins
            ip = labels[label]
            continue
        # label does nothing at runtime
        ip += 1
    print('--- MEMORY ---')
    print(mem)

def main():
    code = load_sample()
    if not code:
        print('No sample.mr found!')
        sys.exit(1)

    print('--- SOURCE ---')
    print(code)
    print()

    # tokens (optional)
    print_tokens(code)

    ast = parse_code(code)
    print('\n--- AST ---')
    print(ast)

    sem = SemanticAnalyzer()
    sem.analyze(ast)
    if sem.errors:
        print('\n--- SEMANTIC ERRORS ---')
        for e in sem.errors:
            print(' -', e)
        return

    print('\nNo semantic errors.')
    gen = IRGen()
    ir = gen.gen(ast)
    print_ir(ir)
    interpret_ir(ir)

if __name__ == '__main__':
    main()
