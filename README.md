# APS_logcomp

Alunos: Giovana Cassoni Andrade e Tales Ivalque Taveira de Freitas

## LINGUAGEM

A linguagem de programação criada é para movimentar a garra de um robô, para abrir e fechar, pegando e soltando objetos.

## EBNF

- DECLARACAO = { IDENTIFICADOR | MOSTRAR | SE | ENQUANTO } ;
- IDENTIFICADOR = ID, "=", EXPRESSAO ;
- INSERIR = "inserir", "(", ")" ;
- MOSTRAR = "mostrar", "(", EXPRESSAO, ")" ;
- SE = "SE", EXPRESSAO, ":", DECLARACAO, "FIM", "SE", ( λ | CONTRARIO ) ;
- CONTRARIO = "CONTRARIO", ":", DECLARACAO, "FIM", "CONTRARIO" ;
- ENQUANTO = "ENQUANTO", EXPRESSAO, ":", DECLARACAO, "FIM", "ENQUANTO" ;
- EXPRESSAO = EXP1, { (“==” | “<” | ">"), EXP1 } ;
- EXP1 = EXP2, { (“+” | “-” ), EXP2 } ;
- EXP2 = EXP3, { (“*” | “/”), EXP3 } ;
- EXP3 = (“-”, EXP3) | NUMERO | INSERIR | STRING | “(”, EXPRESSAO, “)” | IDENTIFICADOR, ( λ | EXPRESSAO, { ",", EXPRESSAO } ) ;
- ID = LETRA, { LETRA | DIGITO | "_" } ;
- MOVIMENTAR = "movimentar", "(", EXPRESSAO, ")" ;
- ABRIR = "abrir", "(", ")" ;
- FECHAR = "fechar", "(", EXPRESSAO, ")" ;
- NUMERO = DIGITO, { DIGITO } ;
- STRING = ", { LETRA | DIGITO }, " ;
- LETRA = ( a | ... | z | A | ... | Z ) ;
- DIGITO = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

## EXEMPLOS DE ENTRADA

- entrada 1:

```
id_robo = "robo1"
id_objeto = "cilindro"
objeto = inserir()

SE objeto == id_objeto:
abrir()
movimentar(id_robo, 20, 10, -30)
fechar()
movimentar(id_robo, -10, 0, 30)
FIM SE

CONTRARIO:
abrir()
fechar()
FIM CONTRARIO
```

- entrada 2:

```
eixo_y = 5

ENQUANTO eixo_y < 30:
movimentar(id, 0, eixo_y, 0)
eixo_y = eixo_y + 5
FIM ENQUANTO
```