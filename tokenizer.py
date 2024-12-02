# tokenizer.py
from schemas import Token
from symbols import (
    RELATIONAL_OPERATORS,
    MATHEMATICAL_OPERATORS,
    LOGICAL_OPERATORS,
    PRIORITIES,
    RESERVED_WORDS,
    TYPES,
    BOOLEAN_VALUES
)

class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        current_char = self.source[self.position]

        # Pula espaços em branco
        while current_char.isspace():
            self.position += 1
            if self.position >= len(self.source):
                self.next = Token("EOF", None)
                return
            current_char = self.source[self.position]

        # Número
        if current_char.isdigit():
            value = 0
            while self.position < len(self.source) and self.source[self.position].isdigit():
                value = value * 10 + int(self.source[self.position])
                self.position += 1
            self.next = Token("NUMBER", value)

        # Operadores Lógicos (incluindo '&&' e '||')
        elif any(current_char == op[0] for op in LOGICAL_OPERATORS):
            # Verifica operadores de múltiplos caracteres como '&&' e '||'
            if self.source.startswith('&&', self.position):
                self.next = Token("LOGICAL_OPERATOR", '&&')
                self.position += 2
            elif self.source.startswith('||', self.position):
                self.next = Token("LOGICAL_OPERATOR", '||')
                self.position += 2
            elif current_char == '!':
                self.next = Token("LOGICAL_OPERATOR", '!')
                self.position += 1
            else:
                raise ValueError(f"Operador lógico inválido em posição {self.position}: '{current_char}'")

        # Operadores Matemáticos
        elif current_char in MATHEMATICAL_OPERATORS:
            token = Token("MATHEMATICAL_OPERATOR", current_char)
            self.position += 1
            self.next = token

        # Operadores Relacionais (incluindo '<=', '>=', '==', '!=')
        elif current_char in RELATIONAL_OPERATORS:
            # Verifica operadores de múltiplos caracteres como '<=', '>=', '==', '!='
            if self.source.startswith('<=', self.position):
                self.next = Token("RELATIONAL_OPERATOR", '<=')
                self.position += 2
            elif self.source.startswith('>=', self.position):
                self.next = Token("RELATIONAL_OPERATOR", '>=')
                self.position += 2
            elif self.source.startswith('==', self.position):
                self.next = Token("RELATIONAL_OPERATOR", '==')
                self.position += 2
            elif self.source.startswith('!=', self.position):
                self.next = Token("RELATIONAL_OPERATOR", '!=')
                self.position += 2
            elif current_char in ['<', '>']:
                self.next = Token("RELATIONAL_OPERATOR", current_char)
                self.position += 1
            else:
                raise ValueError(f"Operador relacional inválido em posição {self.position}: '{current_char}'")

        # Prioridades (parênteses e chaves)
        elif current_char in PRIORITIES:
            token = Token("PRIORITY", current_char)
            self.position += 1
            self.next = token

        # Identificadores e Palavras Reservadas
        elif current_char.isalpha() or current_char == '_':
            value = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                value += self.source[self.position]
                self.position += 1
            if value in RESERVED_WORDS:
                self.next = Token(RESERVED_WORDS[value], value)
            elif value in TYPES:
                self.next = Token("TYPE", value)
            elif value in BOOLEAN_VALUES:
                self.next = Token("BOOLEAN", value)
            else:
                self.next = Token("ID", value)

        # Strings
        elif current_char == '"':
            value = ""
            self.position += 1  # Pula a aspa inicial
            while self.position < len(self.source) and self.source[self.position] != '"':
                value += self.source[self.position]
                self.position += 1
            if self.position >= len(self.source):
                raise ValueError("String não fechada.")
            self.position += 1  # Pula a aspa final
            self.next = Token("STRING", value)

        # Operadores de Atribuição e Múltiplos Caracteres
        elif current_char == '=':
            if self.source.startswith('==', self.position):
                self.next = Token("RELATIONAL_OPERATOR", '==')
                self.position += 2
            else:
                self.next = Token("ASSIGN", '=')
                self.position += 1

        elif current_char == ';':
            self.position += 1
            self.next = Token("EOL", ";")

        elif current_char == ',':
            self.position += 1
            self.next = Token("COMMA", ",")

        elif current_char == '{':
            self.position += 1
            self.next = Token("BLOCK_OPEN", "{")

        elif current_char == '}':
            self.position += 1
            self.next = Token("BLOCK_CLOSE", "}")

        elif current_char == '(':
            self.position += 1
            self.next = Token("PRIORITY", "(")

        elif current_char == ')':
            self.position += 1
            self.next = Token("PRIORITY", ")")

        else:
            raise ValueError(f"Caractere inválido: '{current_char}'")

        # Debug: Exibir o token atual (opcional)
        # print(f"Token: {self.next.type}, Valor: {self.next.value}")
