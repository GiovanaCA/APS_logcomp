import sys
from typing import List, Any
from schemas import SymbolTable, Node, Token, FuncTable
from nodes import BlockNode, BinOp, UnOp, IntVal, NoOp, Assign, Id, MostrarNode
from tokenizer import Tokenizer

from parser import Parser

from symbols import RESERVED_METHODS

# Registro das funções reservadas no FuncTable
for method_name, method_info in RESERVED_METHODS.items():
    FuncTable.set(method_name, method_info)

def main(args):
    parser = Parser()
    ast = parser.run(args)
    table = SymbolTable()
    a = int(ast.evaluate(table)[0])
    return a

if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            source = file.read()
    else:
        sys.stderr.write('Número de argumentos inválido: apenas 1 argumento é permitido\n')
    if not source:
        sys.stderr.write('Arquivo vazio\n')
    result = main(source)