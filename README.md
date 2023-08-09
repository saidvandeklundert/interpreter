
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

## Tree-walking interpreter:

- `Lexer`: tokenize the source code
- `Parser`: build the AST
- `Evaluator`: gives meaning to the AST:
  - evaluates the AST
  - implements the specification as to how the AST should be evaluated


Interpreted languages can be optimized. Some examples:
- compiling the AST to bytecode so that a virtual machine can execute the program more efficiently
- JIT compiling certain parts of the application to machine code

## Byte-code interpreter:

Compiles source code to bytecode which is then executed by a VM. If the VM is written in a portable language (like C for instance), the advantage is you can run your code on all machines that run that language. Another advantage is that this approach is several times faster when compared to a tree-walking interpreter. In a tree-walking interpreter, each piece of syntax becomes an AST node. Even for simple statements, a lot of objects with pointers and headers are created. This overhead can be reduced by compiling to byte-code.

Compiling to machine code would be even faster. The downside is that every CPU architecture has its own assebly dialect. Getting your language to run on all CPUs is a massive undertaking. A way around this would be using something like LLVM, where you comile to an IR and then let the LLVM backend do the rest.

Bytecode kind of resembles machine code. It forms a dense, linear sequence of binary instructions. Though not as fast as machine code, the instructions are a lot easier to write and maintain.

The VM that executes the bytecode is like a virtual machine that has a simulated chip whose machine code is the byte instructions that are executed. The 'VM' is the interpreter.

Some example languages are Python, Ruby, Lua, OCaml, Erlang and more.

In a byte-code interpreter, we have:
- a front end compiler that turns source code into byte code
- byte code being the representation of the program
- a VM that executes the byte-code

## Compiler:

A compiler is a program that translates code from one language to another language. Oftentimes, what people mean when they say 'compiler' is a program that reads source code in a higher level language and then translates that to machine code or byte code.
### Compiler stages:

- `Lexing`: the Lexer/tokenizer turns source code into a list of tokens. 
- `Parsing`: the parser transforms the list of tokens into an abstract syntax tree (AST). The root of the AST represents the entire program.
- `Code generation`: traverse the AST and generate machine code (or byte code).

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


# General concepts:
Higher-order functions: functions that either return other functions or receive them as arguments.

Closuers: functions that 'close over' the environment they were defined in
## Links:

Statements vs expressions:
https://www.baeldung.com/cs/expression-vs-statement

Compiler and compiler structure:
https://en.wikipedia.org/wiki/Compiler


https://github.com/ThePrimeagen/ts-rust-zig-deez/tree/master
 

https://norasandler.com/2017/11/29/Write-a-Compiler.html