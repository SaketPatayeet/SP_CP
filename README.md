# 🪶 Marathi Programming Language

A **Marathi-based programming language** created from scratch — supporting arithmetic, arrays, control flow, loops, and logic in natural Marathi syntax.

It’s built using a complete compiler pipeline:  
**Lexical Analysis → Syntax Analysis → Semantic Analysis → Intermediate Representation (IR) Generation → Execution.**

---

## ⚙️ Architecture Overview

- **Lexer** — Tokenizes Marathi keywords, operators, and literals  
- **Parser** — Builds an Abstract Syntax Tree (AST)  
- **Semantic Analyzer** — Checks variable declarations, assignments, and types  
- **IR Generator** — Converts AST to low-level intermediate code  
- **IR Interpreter** — Executes the IR instructions like a virtual machine  

✅ Fully functional compiler–interpreter hybrid for the Marathi language.

---

## ✨ Supported Features

### 🧮 Arithmetic & Expressions
Supports:
| Operator | Description | Example |
|-----------|--------------|----------|
| `+`, `-`, `*`, `/` | Arithmetic operations | `बदलवा a = 10 + 5 * 2` |
| `%` | Modulo | `बदलवा r = 10 % 3` |
| `^` | Power | `बदलवा p = 2 ^ 3` |
| `()` | Parentheses for precedence | `बदलवा z = (a + b) * c` |

**Example:**
```marathi
बदलवा a = 10
बदलवा b = 5
बदलवा c = (a + b) * 2
लिहा c
```
Output:
```
30
```

---

### 🔢 Variables and Assignment
```marathi
बदलवा x = 5
x = x + 2
लिहा x
```
✔ Variables can be reassigned  
✔ Data types supported: **numbers, strings, and arrays**

---

### 📦 Arrays and Indexing
```marathi
बदलवा arr = [5, 3, 8, 1]
लिहा arr[2]
arr[1] = 10
लिहा arr[1]
```
Output:
```
8
10
```
✔ Supports list creation, index access, and element assignment.

---

### 🧠 Conditional Statements (`जर`, `नाहीतर`)
```marathi
बदलवा a = 10
बदलवा b = 20

जर a < b तर
    लिहा "a लहान आहे"
नाहीतर
    लिहा "b लहान आहे"
संपले
```
Output:
```
a लहान आहे
```

Supports:
- `<`, `>`, `<=`, `>=`, `==`, `!=`
- Nested conditions
- Inline arithmetic inside conditions (`जर (a + b) > 15 तर ...`)

---

### 🧩 Logical Operators
| Marathi Keyword | Meaning | Example |
|------------------|----------|----------|
| `आणि` | AND | `जर (a < 10 आणि b > 5) तर ...` |
| `किंवा` | OR | `जर (a == 10 किंवा b == 10) तर ...` |
| `नाही` | NOT | `जर नाही x तर ...` |

**Example:**
```marathi
बदलवा a = 5
बदलवा b = 10
जर (a < 10 आणि b > 5) तर
    लिहा "योग्य"
नाहीतर
    लिहा "चुकीचे"
संपले
```
Output:
```
योग्य
```

---

### 🔁 Loops

#### 🌀 While Loop (`जोपर्यंत`)
```marathi
बदलवा i = 0
जोपर्यंत i < 5 तर
    लिहा i
    i = i + 1
संपले
```
Output:
```
0
1
2
3
4
```

#### 🔂 For Loop (`साठी`)
```marathi
बदलवा n = 3
साठी i = 0 ते n तर
    लिहा "नमस्कार"
संपले
```
Output:
```
नमस्कार
नमस्कार
नमस्कार
```
Internally expands to a `while` loop with automatic iteration.

---

### 📚 Nested Control Flow (Example: Bubble Sort)
```marathi
बदलवा arr = [5, 3, 8, 1]
बदलवा n = 4

बदलवा i = 0
जोपर्यंत i < n तर
    बदलवा j = 0
    जोपर्यंत j < n - i - 1 तर
        जर arr[j] > arr[j+1] तर
            बदलवा temp = arr[j]
            arr[j] = arr[j+1]
            arr[j+1] = temp
        संपले
        j = j + 1
    संपले
    i = i + 1
संपले

लिहा arr[0]
लिहा arr[1]
लिहा arr[2]
लिहा arr[3]
```
Output:
```
1
3
5
8
```

---

### 🖨️ Output
```marathi
लिहा "नमस्कार जग"
लिहा x
```
✔ Prints strings and variables directly.  
✔ Strings can be enclosed in quotes `" "` for Marathi text.

---

### 🧮 Advanced Expressions
You can mix logical, arithmetic, and comparison operations freely:
```marathi
जर 2 + 3 * 4 > 10 तर
    लिहा "होय"
नाहीतर
    लिहा "नाही"
संपले
```
Output:
```
होय
```

---

### 💡 Boolean Logic Example
```marathi
बदलवा x = 0
जर नाही x तर
    लिहा "नकार सत्य आहे"
संपले
```
Output:
```
नकार सत्य आहे
```

---

### 💥 Error Handling
- Detects invalid tokens (`Unexpected character`)  
- Reports missing keywords (`संपले` not found)  
- Shows **line and column numbers** for debugging  
- Stops at first major syntax error for clarity

---

## 🧩 Intermediate Representation (IR)
The parser compiles Marathi source into a three-address style **Intermediate Representation (IR)**:
```
('const', 't0', 5)
('assign', 'a', 't0')
('binop', 't1', 'lt', 'a', 'b')
('if_false_goto', 't1', 'L0')
('print', 't2')
('goto', 'L1')
('label', 'L0')
('label', 'L1')
```
This IR is then executed line-by-line by a custom interpreter.

---

## 🧭 Language Summary

| Feature | Status |
|----------|---------|
| Arithmetic & Variables | ✅ |
| Strings | ✅ |
| Arrays | ✅ |
| Conditionals (`जर`, `नाहीतर`) | ✅ |
| Loops (`जोपर्यंत`, `साठी`) | ✅ |
| Nested Loops / Conditionals | ✅ |
| Logical Ops (`आणि`, `किंवा`, `नाही`) | ✅ |
| Comparison Ops (`<`, `>`, `==`, etc.) | ✅ |
| Printing (`लिहा`) | ✅ |
| Boolean Logic | ✅ |
| Operator Precedence | ✅ |
| Functions | ❌ (Coming Soon) |
| Input (`वाचा`) | ❌ |
| Step in Loops (`पाऊल`) | 🔜 |
| Comments | ❌ |
| Type System | Basic (int, str, list) |
| Semantic Checks | Partial |

---

## 🧩 Planned Enhancements

### 🪄 Next Steps
- Add **`पाऊल` (step)** in `साठी` loop  
- Add **user-defined functions** (`कार्य ... संपले`)  
- Add **input** keyword (`वाचा`)  
- Add **break (`थांबा`)** and **continue (`पुढे जा`)**  
- Add **comments** (`#` or `/* ... */`)  
- Add **float and boolean** types  
- Introduce **scoping and return statements**

---

### 🌱 Long-Term Goals
- File handling (`उघडा`, `वाचा`, `लिहा`)  
- Library functions (`वर्गमूळ`, `जास्तीतजास्त`, etc.)  
- For-each loop (`प्रत्येक घटकासाठी`)  
- REPL mode (interactive shell)  
- Bytecode / Python backend compilation  
- Module imports and standard libraries

---

## 🧠 Example: Combining All Features
```marathi
बदलवा n = 5
बदलवा sum = 0

साठी i = 0 ते n तर
    जर i % 2 == 0 तर
        लिहा "सम संख्या:"
        लिहा i
        sum = sum + i
    संपले
संपले

लिहा "बेरीज आहे:"
लिहा sum
```
Output:
```
सम संख्या:
0
सम संख्या:
2
सम संख्या:
4
बेरीज आहे:
6
```


