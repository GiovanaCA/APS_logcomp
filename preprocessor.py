class PrePro:
    @staticmethod
    def filter(source: str) -> str:
        new_source = ""
        i = 0
        while i < len(source):
            c = source[i]
            if c.isspace():
                new_source += c
                i += 1
            elif c == "/" and i + 1 < len(source) and source[i + 1] == "/":
                i += 2  # Pula o //
                while i < len(source) - 1 and source[i] != "\n":
                    i += 1
                if i >= len(source) - 1:
                    raise ValueError("Comentário em bloco não fechado")
                i += 1  # Pula o \n
            else:
                new_source += c
                i += 1
        return new_source