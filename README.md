# Interpreters and compilers


`AST`: abstract syntax tree: a tree representation of the abstract syntactic structure of text (often source code) written in a formal language. Each node of the tree denotes a construct occurring in the text. ~wikipedia A parser takes source code as input (tokens or text) and produces the AST.

`Expression`: produces a value, or put otherwise, expressions evaluate to a value.

`Statement`: code that executes a specific instruction or tells the computer to complete a task. For instance, control statements, assignments, import statements, etc. Statements do not produce a value.

`Identifiers`/`Symbols`: names for variables, types, functions, and labels in a program.
What an expression is and what a statement is can vary from programming language to programming language.

Example statement: `let x = 5;`
Example expression: `5`

Prefix operator: operator 'in front of' its operand: `--5`
Postfix operator: operator 'after' its operand: `5++`
Infix operators: operator sits in between operands: `5 * 5`

Unary expressions: there is 1 operand
Binary expression: two operands separated by 1 infix operator.

Operator precedence: some operators have a 'higher 'rank' and get to go first: `2 + 5 * 5` gives 27 for that reason.

Adding a statement to the parser:
- add to the AST
- enable the parser to detect the token for the statement. For instance,
 add code to enable the parser to detect the `return` token.

This interpreter has only the `let` and `return` statement.



Assembler and linker transform assembly into an executable.

## Compiler:

A compiler is a program that translates code from one language to another language. Oftentimes, what people mean when they say 'compiler' is a program that reads source code in a higher level language and then translates that to machine code or byte code.
### Compiler stages:

- Lexing: the Lexer/tokenizer turns source code into a list of tokens. 
- Parsing: the parser transforms the list of tokens into an abstract syntax tree (AST). The root of the AST represents the entire program.
- Code generation: traverse the AST and generate machine code (or byte code).

The 6 compiler stages:
- lexical analysis
- semantic analysis
- intermediate code generation
- code optimization
- code generation
### Language processing system:

- Preprocessor: macro-expansion, #include, etc.
- Compiler: takes source code and targets an assembly language (typially described as something done in 6 phases)
- Assembler: translates assembly code to machine code. The output is object code (an exe).
- Linker: link all programs (such as modules) together to create a final executable
- Loader: loads final executable into memory

## Links:

Statements vs expressions:
https://www.baeldung.com/cs/expression-vs-statement

Compiler and compiler structure:
https://en.wikipedia.org/wiki/Compiler


https://github.com/ThePrimeagen/ts-rust-zig-deez/tree/master
 

https://norasandler.com/2017/11/29/Write-a-Compiler.html