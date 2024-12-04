import sys
from preprocessor import PrePro
from tokenizer import Tokenizer

def main(source: str):
    preprocessor = PrePro()
    source = preprocessor.filter(source)
    tokenizer = Tokenizer(source)
    tokenizer.select_next()
    print(tokenizer.next.type)
    while tokenizer.next.value is not None:
        tokenizer.select_next()
        print(tokenizer.next.type)
    return 0

if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            source = file.read()
    else:
        sys.stderr.write('Número de argumentos inválido: apenas 1 argumento é permitido\n')
    if not source:
        sys.stderr.write('Arquivo vazio\n')
    result = main(source)