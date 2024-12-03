import sys
from typing import List, Any
from schemas import SymbolTable, Node, Token, FuncTable
from nodes import BlockNode, BinOp, UnOp, IntVal, NoOp, Assign, Id, MostrarNode

from parser import Parser
class SemanticAnalyzer:
    @staticmethod
    def run(node: Node) -> Any:
        if isinstance(node, BinOp):
            for child in node.children:
                SemanticAnalyzer.run(child)
        elif isinstance(node, UnOp):
            SemanticAnalyzer.run(node.children[0])
        elif isinstance(node, IntVal):
            pass
        elif isinstance(node, NoOp):
            pass
        else:
            raise ValueError(f"Tipo de nó inválido: {type(node)}")

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