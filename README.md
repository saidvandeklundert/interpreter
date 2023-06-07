# interpreter
Writing an interpreter in Go


```
go run .
go test ./...
```



Expressions produce values, statements don’t. 

What an expression is and what a statement is can vary from programming language to programming language.

Example statement: `let x = 5;`
Example expression: `5`

Prefix operator: operator 'in front of' its operand: `--5`
Postfix operator: operator 'after' its operand: `5++`
Infix operators: operator sits in between operands: `5 * 5`

Binary expression: two operands separated by 1 infix operator.

Operator precedence: some operators have a 'higher 'rank' and get to go first: `2 + 5 * 5` gives 27 for that reason.

Adding a statement to the parser:
- add to the AST
- enable the parser to detect the token for the statement. For instance,
 add code to enable the parser to detect the `return` token.

 This interpreter has only the `let` and `return` statement.