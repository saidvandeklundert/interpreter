# interpreter
Writing an interpreter in Go


```
go run .
go test ./...
```


`AST`: abstract syntax tree: a tree representation of the abstract syntactic structure of text (often source code) written in a formal language. Each node of the tree denotes a construct occurring in the text. ~wikipedia

Expressions produce values, statements don’t. 

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

 ### Adding an integer literal"

 Integer literals are expressions. The value they produce is the integer itself. 





 Compiler and compiler structure:
 https://en.wikipedia.org/wiki/Compiler


 https://github.com/ThePrimeagen/ts-rust-zig-deez/tree/master
 