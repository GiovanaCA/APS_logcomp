# tokenizer.py
from schemas import Token
from symbols import (
    RELATIONAL_OPERATORS,
    MATHEMATICAL_OPERATORS,
    LOGICAL_OPERATORS,
    PRIORITIES,
    RESERVED_WORDS,
    TYPES,
    BOOLEAN_VALUES,
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

        # Pula espaços em branco e comentários
        while current_char.isspace() or current_char == '#':
            if current_char == '#':
                # Pula até o final da linha para ignorar comentários
                while self.position < len(self.source) and self.source[self.position] != '\n':
                    self.position += 1
                if self.position >= len(self.source):
                    self.next = Token("EOF", None)
                    return
                current_char = self.source[self.position]
            else:
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

        # Operadores Lógicos
        elif any(self.source.startswith(op, self.position) for op in LOGICAL_OPERATORS):
            if self.source.startswith('&&', self.position):
                self.next = Token("LOGICAL_OPERATOR", '&&')
                self.position += 2
            elif self.source.startswith('||', self.position):
                self.next = Token("LOGICAL_OPERATOR", '||')
                self.position += 2
            elif self.source.startswith('!', self.position):
                self.next = Token("LOGICAL_OPERATOR", '!')
                self.position += 1
            else:
                raise ValueError(f"Operador lógico inválido em posição {self.position}: '{current_char}'")

        # Operadores Matemáticos
        elif current_char in MATHEMATICAL_OPERATORS:
            token = Token("MATHEMATICAL_OPERATOR", current_char)
            self.position += 1
            self.next = token

        # Operadores Relacionais
        elif any(self.source.startswith(op, self.position) for op in RELATIONAL_OPERATORS):
            matched = False
            for op in sorted(RELATIONAL_OPERATORS, key=lambda x: -len(x)):  # Ordena por comprimento decrescente
                if self.source.startswith(op, self.position):
                    self.next = Token("RELATIONAL_OPERATOR", op)
                    self.position += len(op)
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Operador relacional inválido em posição {self.position}: '{current_char}'")

        # Prioridades
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

            # Verifica se é uma palavra reservada
            if value in RESERVED_WORDS:
                token_type = RESERVED_WORDS[value]
                self.next = Token(token_type, value)
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
                if self.source[self.position] == '\\':  # Tratamento de caracteres de escape
                    self.position += 1
                    if self.position < len(self.source):
                        esc_char = self.source[self.position]
                        if esc_char == 'n':
                            value += '\n'
                        elif esc_char == 't':
                            value += '\t'
                        elif esc_char == '"':
                            value += '"'
                        elif esc_char == '\\':
                            value += '\\'
                        else:
                            value += esc_char
                        self.position += 1
                    else:
                        raise ValueError("String não fechada corretamente após escape.")
                else:
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
            self.next = Token("EOL", ";")
            self.position += 1

        elif current_char == ':':
            self.next = Token("COLON", ":")
            self.position += 1

        elif current_char == ',':
            self.next = Token("COMMA", ",")
            self.position += 1

        elif current_char == '(':
            self.next = Token("PRIORITY", "(")
            self.position += 1

        elif current_char == ')':
            self.next = Token("PRIORITY", ")")
            self.position += 1

        else:
            raise ValueError(f"Caractere inválido: '{current_char}'")