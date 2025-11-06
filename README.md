# 🪶 Marathi Programming Language

A domain-specific programming language designed using Marathi keywords — built with a full compiler pipeline consisting of **Lexical Analysis**, **Syntax Analysis**, **Semantic Analysis**, **Intermediate Representation (IR) Generation**, and **Execution**.

---

## 🚀 Current Capabilities

### 🧱 1. Core Architecture
The language includes:
- **Lexer** → Tokenizes Marathi keywords and symbols  
- **Parser** → Builds an Abstract Syntax Tree (AST)  
- **Semantic Analyzer** → Performs basic type and variable checks  
- **IR Generator** → Converts AST into a lower-level Intermediate Representation  
- **IR Executor** → Executes the IR like a virtual machine  

This makes it a fully working interpreted language with Marathi syntax.

---

## ✨ Supported Features

### 🧮 Arithmetic & Expressions
Supports:
- `+`, `-`, `*`, `/` → Addition, subtraction, multiplication, division  
- `%` → Modulo  
- `^` → Power  
- Parentheses for grouping  
- Full operator precedence  

Example:
```marathi
बदलवा x = 2 + 3 * 4
लिहा x
