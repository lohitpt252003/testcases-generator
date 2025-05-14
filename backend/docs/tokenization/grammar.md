****# Grammar

## Terminals
- `"var"`, `"int"`, `"float"`, `"char"`, `"string"`
- `INTEGER = [0-9]+`
- `NUMBER = [INTEGER](.[INTEGER])`
- `IDENTIFIER = [a-zA-Z_][a-zA-Z0-9_]*`
- `(`, `)`, `:`, `;`, `+`

## Non-Terminals
```ebnf
Program = { VariableDecl };
VariableDecl = "var" IDENTIFIER ":" ("int" |"float" | "char" | "string") [Params] ";"
Params = "(" ("IntParams" | "FloatParams" | "CharParams" |  "StringParams") ")";
Intparams = (NUMBER | NUMBER_IDENTIFIER) "," (NUMBER | NUMBER_IDENTIFIER) ;
floatParams = (intparams | intparams "," (0, 1, 2, 3, 4, 5, 6));
charparams = [set];
stringparams = (INT, INT_IDENTIFIER) "," charparams;
set = ["lower", "upper", "special", "digit"];
`**``**