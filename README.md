# APS_logcomp

Alunos: Giovana Cassoni Andrade e Tales Ivalque Taveira de Freitas

## LINGUAGEM

A linguagem de programação criada é para movimentar a garra de um robô, para abrir e fechar, pegando e soltando objetos.

## EBNF

- **PROGRAM**
  - `PROGRAM ::= { DECLARACAO }`

- **DECLARACAO**
  - `DECLARACAO ::= OBJETO_DECLARACAO | VARIAVEL_DECLARACAO | ATRIBUICAO | COMANDO | CONTROLE | COMENTARIO`

- **OBJETO_DECLARACAO**
  - `OBJETO_DECLARACAO ::= "Robo", ID, "=", "Robo", "(", STRING, ")", ";"`

- **VARIAVEL_DECLARACAO**
  - `VARIAVEL_DECLARACAO ::= "var", ID, "=", EXPRESSAO, ";"`

- **ATRIBUICAO**
  - `ATRIBUICAO ::= ID, "=", EXPRESSAO, ";"`

- **COMANDO**
  - `COMANDO ::= "movimentar", "(", ID, ",", EXPRESSAO, ")", ";"` 
  - `| "mostrar", "(", EXPRESSAO, ")", ";"` 
  - `| "abrir", "(", ID, ")", ";"` 
  - `| "fechar", "(", ID, ",", EXPRESSAO, ")", ";"`

- **CONTROLE**
  - `CONTROLE ::= ENQUANTO`

- **ENQUANTO**
  - `ENQUANTO ::= "ENQUANTO", "(", EXPRESSAO, ")", ":", { DECLARACAO }, "FIM", "ENQUANTO", ";"`

- **EXPRESSAO**
  - `EXPRESSAO ::= EXP1, { ("==" | "<" | ">" | "<=" | ">=" | "!="), EXP1 }`

- **EXP1**
  - `EXP1 ::= EXP2, { ("+" | "-"), EXP2 }`

- **EXP2**
  - `EXP2 ::= EXP3, { ("*" | "/"), EXP3 }`

- **EXP3**
  - `EXP3 ::= [ "-" ], ( NUMERO | STRING | "(", EXPRESSAO, ")" | ID, [ ARGUMENTOS ] )`

- **ARGUMENTOS**
  - `ARGUMENTOS ::= ",", EXPRESSAO, { ",", EXPRESSAO }`

- **ID**
  - `ID ::= LETRA, { LETRA | DIGITO | "_" }`

- **NUMERO**
  - `NUMERO ::= DIGITO, { DIGITO }, [ ".", DIGITO, { DIGITO } ]`

- **STRING**
  - `STRING ::= '"', { CARACTERE }, '"'`

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

- **COMENTARIO**
  - `COMENTARIO ::= "//", { ANY_CARACTERE }, "\n"`

- **ANY_CARACTERE**
  - `ANY_CARACTERE ::= LETRA | DIGITO | SIMBOLO`

## EXEMPLOS DE ENTRADA

- entrada 1:

```
// Inicialização do robô
Robo rob1 = Robo("rob1");

// Declaração de variável
var contador = 3;

// Loop para movimentar o robô
ENQUANTO (contador > 0):
    rob1.movimentar(10);
    contador = contador - 1;
FIM ENQUANTO;

// Mostrar o valor de contador
mostrar(contador);
```

- entrada 2:

```
// Inicialização do robô
Robo rob1 = Robo("rob1");

// Declaração de variável
var contador = 3;

// Loop para movimentar o robô
ENQUANTO (contador > 0):
    movimentar(rob1, 10);
    contador = contador - 1;
    mostrar(contador);
FIM ENQUANTO;
```
