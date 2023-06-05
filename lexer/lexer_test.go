package lexer

import (
	"monkey/token"
	"testing"
)

func TestNextToken(t *testing.T) {
	input := `=+(){},;`

	tests := []struct {
		expextedType    token.TokenType
		expectedLiteral string
	}{
		{token.ASSIGN, "="},
		{token.PLUS, "+"},
		{token.LPAREN, "("},
		{token.RPAREN, ")"},
		{token.LBRACE, "{"},
		{token.COMMA, ","},
		{token.SEMICOLON, ";"},
		{token.EOF, ""},
	}
}

l := New(input)

for i, tt := range tests {
	tok := l.NextToken()

	if tok.Type != tt.expextedType{
		t.Fatalf("tests[%d] - tokentype wrong. expected=%q, got %q",
	i,tt.expextedType, tok.Type)
	}

	if tok.Literal!= tt.expectedLiteral {
		t.Fatal("tests[%d] - literal wrong. expected=%q, got=%q",
	i, tt.expectedLiteral, tok.Literal)
	}
}