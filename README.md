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

## Mudanças na linguagem

- **Declaração de objetos**
  - `Robo nome_var = Robo("Nome do Robô");`
  A ideia aqui é criar uma variável para representar o robô, e inicializá-la com um nome único. Para o usuário, a implementação é transparente, mas para o compilador, a variável é tratada como um objeto.

- **Métodos reservados**
  - `move_frente(Robo rob1, int i);`
  - `move_tras(Robo rob1, int i);`
  - `move_esquerda(Robo rob1, int i);`
  - `move_direita(Robo rob1, int i);`
  - `gira(Robo rob1, int i);`
  - `abre(Robo rob1);`
  - `fecha(Robo rob1);`
  - `sobe(Robo rob1);`
  - `desce(Robo rob1);`
  - `ver_x(Robo rob1);`
  - `ver_y(Robo rob1);`
  - `ver_angulo(Robo rob1);`
  - `ver_garra(Robo rob1);`
  - `ver_braco(Robo rob1);`

  Esses métodos são os comandos básicos que o robô pode executar. Eles são chamados dentro de funções do tipo "comando" e são responsáveis por movimentar o robô, abrir e fechar a garra, subir e descer o braço, e visualizar informações sobre o robô.

- **Declaração de comandos**
  - `girar(expressão);`
  - `comando expr(Robo rob1, int a);`
  Como estamos criado uma linguagem para operar um robô, é elementar que seja possível criar comando específicos para realizar as mais diversas ações com menos linhas de código. Para isso, foi craido o tipo de função "comando", que deve receber um objeto do tipo Robo e possivelmente outros argumentos, e executa uma ação específica, derivada de uma sequência de outros comandos.
  Exemplo [test_comando](testes/test_comando.txt)

- **Linguagem clara**
  O nome dos comandos e funções foram escolhidos de forma a serem intuitivos, facilitando o entendimento do código, além das regras de construção da sintaxe, que não possui regras rígidas como identação, por exemplo.

## EXEMPLOS DE ENTRADA

Os exemplos de entrada podem ser vistos na pasta "testes".
