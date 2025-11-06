# run.py
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
    mem = {}
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
        elif op == 'binop':
            _, t, bop, a, b = ins
            av = mem[a] if isinstance(a, str) and a in mem else a
            bv = mem[b] if isinstance(b, str) and b in mem else b
            # if a/b are variable names (non-temp), get from mem (variables stored in mem)
            if isinstance(av, str) and av in mem:
                av = mem[av]
            if isinstance(bv, str) and bv in mem:
                bv = mem[bv]
            if bop == 'plus':
                mem[t] = av + bv
            elif bop == 'minus':
                mem[t] = av - bv
            elif bop == 'mul':
                mem[t] = av * bv
            elif bop == 'div':
                mem[t] = av // bv
            elif bop == 'eq':
                mem[t] = 1 if av == bv else 0
        elif op == 'assign':
            _, name, src = ins
            val = mem[src] if isinstance(src, str) and src in mem else src
            # if src is a variable name or temp, pull from mem if present
            if isinstance(val, str) and val in mem:
                val = mem[val]
            mem[name] = val
        elif op == 'print':
            _, src = ins
            val = mem[src] if isinstance(src, str) and src in mem else src
            # if var name is stored in mem
            if isinstance(val, str) and val in mem:
                val = mem[val]
            print(val)
        elif op == 'if_false_goto':
            _, cond, label = ins
            condv = mem[cond] if isinstance(cond, str) and cond in mem else cond
            if isinstance(condv, str) and condv in mem:
                condv = mem[condv]
            if not condv:
                ip = labels[label]
                continue
        elif op == 'goto':
            _, label = ins
            ip = labels[label]
            continue
        # labels and other ops do nothing at runtime (labels handled already)
        ip += 1
    print('--- MEMORY ---')
    print(mem)

def main():
    sample = load_sample()
    if not sample:
        print('No sample.mr found in project folder. Please create sample.mr and run again.')
        sys.exit(1)

    print('--- SOURCE ---')
    print(sample)
    print()
    # tokens
    print_tokens(sample)
    # parse
    ast = parse_code(sample)
    print('\n--- AST ---')
    print(ast)
    # semantic analysis
    sem = SemanticAnalyzer()
    sem.analyze(ast)
    if sem.errors:
        print('\n--- SEMANTIC ERRORS ---')
        for e in sem.errors:
            print(' -', e)
    else:
        print('\nNo semantic errors.')
        # IR generation
        gen = IRGen()
        ir = gen.gen(ast)
        print_ir(ir)
        # interpret IR
        interpret_ir(ir)

if __name__ == '__main__':
    main()
