package repl

import (
	"bufio"
	"fmt"
	"io"

	"github.com/saidvandeklundert/interpreter/lexer"
	"github.com/saidvandeklundert/interpreter/parser"
	"github.com/saidvandeklundert/interpreter/evaluator"
)

const PROMPT = ">> "

func Start(in io.Reader, out io.Writer) {
	scanner := bufio.NewScanner(in)
	for {
		fmt.Printf(PROMPT)
		scanned := scanner.Scan()
		if !scanned {
			return
		}
		line := scanner.Text()
		l := lexer.New(line)
		p := parser.New(l)
		program := p.ParseProgram()
		if len(p.Errors()) != 0 {
			printParserErrors(out, p.Errors())
			continue
		}
		evaluated := evaluator.Eval(program)
		if evaluated !=nil{
			io.WriteString(out, evaluated.Inspect())
			io.WriteString(out, "\n")
		}

	}
}

const MONKEY_FACE = ` __,__
.-"-.            .-"-.            .-"-.           .-"-.
_/_-.-_\_        _/.-.-.\_        _/.-.-.\_       _/.-.-.\_
/ __} {__ \      /|( o o )|\      ( ( o o ) )     ( ( o o ) )
/ //  "  \\ \    | //  "  \\ |      |/  "  \|       |/  "  \|
/ / \'---'/ \ \  / / \'---'/ \ \      \'/^\'/         \ .-. /
\ \_/'"""'\\_/ /  \\ \\_/'"""'\_/ /   /'\ /'\         /'"""'\\
\\           /    \\           /    /  /|\\  \\      /       \\

-={ see no evil }={ hear no evil }={ speak no evil }={ have no fun }=-
`

func printParserErrors(out io.Writer, errors []string) {
	io.WriteString(out, MONKEY_FACE)
	io.WriteString(out, "Woops! We ran into some monkey business here!\n")
	io.WriteString(out, " parser errors:\n")
	for _, msg := range errors {
		io.WriteString(out, "\t"+msg+"\n")
	}
}
