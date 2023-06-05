package token

type TokenType string

type Token struct {
	Type    TokenType
	Literal string
}

const (
	ILLEGAL = "ILLEGAL"
	EOF     = "EOF"

	// identifiers + literals
	IDENT = "IDENT" // add, foobar, x, y,...
	INT   = "INT"   //134345

	// Operators
	ASSIGN = "="
	PLUS   = "+"

	// Delimers
	COMMA     = ","
	SEMICOLON = ";"

	LPAREN = "()"
	RPAREN = ")"
	LBRACE = "{"
	RBRACE = "}"

	// Keywords
	FUNCTION = "FUNCTION"
	LET      = "LET"
)