# APS_logcomp

Alunos: Giovana Cassoni Andrade e Tales Ivalque Taveira de Freitas

## LINGUAGEM

A linguagem de programação criada é para operar um robô, movimentando-o para frente, trás, lados, girando, abrindo e fechando a garra, movimentando o braço do robô, e visualizando diversas informações referentes a ele. A ideia dessa linguagem foi inspirada em uma disciplina passada na qual um robô deve realizar determinadas tarefas, e um código que facilite a execução seria muito beneficial para os alunos.

## EBNF

- **PROGRAM**
  - `PROGRAM ::= { FUNC_COMAND }`

- **FUNC_COMAND**
  - `FUNC_COMAND ::= VARIAVEIS_FUNC, ID, "(", [ VARIAVEIS, ID, { ",", VARIAVEIS, ID } ], ")", BLOCO`

- **BLOCO**
  - `BLOCO ::= ":", { DECLARACAO }, "FIM", ";"`

- **DECLARACAO**
  - `DECLARACAO ::= OBJETO_DECLARACAO | VARIAVEL_DECLARACAO | ATRIBUICAO | COMANDO | ENQUANTO | SE | COMENTARIO`

- **OBJETO_DECLARACAO**
  - `OBJETO_DECLARACAO ::= "Robo", ID, "=", "Robo", "(", STRING, ")", ";"`

- **VARIAVEL_DECLARACAO**
  - `VARIAVEL_DECLARACAO ::= VARIAVEIS, ID, { [ "=", EXPRESSAO ], { ",", ID } }, ";"`

- **VARIAVEIS_FUNC**
  - `VARIAVEIS_FUNC ::= "void" | "int" | "bool" | "str" | "comando"`

- **VARIAVEIS**
  - `VARIAVEIS ::= "int" | "bool" | "str"`

- **ATRIBUICAO**
  - `ATRIBUICAO ::= ID, ( "=", EXPRESSAO, ";" | "(", [ EXPRESSAO, { ",", EXPRESSAO } ], ")", ";" )`

- **COMANDO**
  - `COMANDO ::= "mostrar", "(", EXPRESSAO, ")", ";"` 
  - `| "return", "(", EXPRESSAO, ")", ";"`

- **SE**
  - `SE ::= "SE", "(", EXPRESSAO, ")", BLOCO, [ SENAO ]`

- **SENAO**
  - `SENAO ::= "SENAO", BLOCO`

- **ENQUANTO**
  - `ENQUANTO ::= "ENQUANTO", "(", EXPRESSAO, ")", BLOCO`

- **EXPRESSAO**
  - `EXPRESSAO ::= EXP1, { ("==" | "<" | ">" | "<=" | ">=" | "!="), EXP1 }`

- **EXP1**
  - `EXP1 ::= EXP2, { ("+" | "-" | "||"), EXP2 }`

- **EXP2**
  - `EXP2 ::= EXP3, { ("*" | "/" | "&&"), EXP3 }`

- **EXP3**
  - `EXP3 ::= [ "-" | "+" | "!"], NUMERO | STRING | "(", EXPRESSAO, ")" | ( ID | METODOS_RESERVADOS ), [ "(", [ ARGUMENTOS ], ")" ]`

- **ARGUMENTOS**
  - `ARGUMENTOS ::= EXPRESSAO, { ",", EXPRESSAO }`

- **ID**
  - `ID ::= LETRA, { LETRA | DIGITO | "_" }`

- **NUMERO**
  - `NUMERO ::= DIGITO, { DIGITO }, [ ".", DIGITO, { DIGITO } ]`

- **STRING**
  - `STRING ::= '"', { CARACTERE }, '"'`

- **COMENTARIO**
  - `COMENTARIO ::= "//", { CARACTERE }, "\n"`

- **CARACTERE**
  - `CARACTERE ::= LETRA | DIGITO | SIMBOLO`

- **LETRA**
  - `LETRA ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" |`
  - `         "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" |`
  - `         "u" | "v" | "w" | "x" | "y" | "z" |`
  - `         "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" |`
  - `         "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" |`
  - `         "U" | "V" | "W" | "X" | "Y" | "Z"`

- **DIGITO**
  - `DIGITO ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"`

- **SIMBOLO**
  - `SIMBOLO ::= "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" |`
  - `           "-" | "_" | "=" | "+" | "[" | "]" | "{" | "}" | "|" |`
  - `           "\\" | ":" | ";" | "'" | "\"" | "," | "." | "/" |`
  - `           "<" | ">" | "?" | " " | "\t"`

- **BOOLEANOS**
  - `BOOLEANOS ::= "true" | "false"`

- **METODOS_RESERVADOS**
  - `METODOS_RESERVADOS ::= "move_frente" | "move_tras" | "move_esquerda" |`
  - `"move_direita" | "gira" | "abre" | "fecha" | "sobe" | "desce" | "ver_x" |`
  - `"ver_y" | "ver_angulo" | "ver_garra" | "ver_braco"`

## EXEMPLOS DE ENTRADA

Os exemplos de entrada podem ser vistos na pasta "testes".