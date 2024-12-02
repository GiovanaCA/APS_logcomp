from abc import ABC, abstractmethod
from typing import Any, List

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent  # Referência para a tabela de símbolos pai

    def set(self, name: str, value: Any, var_type: str):
        self.symbols[name] = (value, var_type)

    def get(self, name: str) -> Any:
        if name in self.symbols:
            return self.symbols[name][0]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise ValueError(f"Erro: Variável ou função '{name}' não encontrada na tabela de símbolos.")

    def get_type(self, name: str) -> str:
        if name in self.symbols:
            return self.symbols[name][1]
        elif self.parent:
            return self.parent.get_type(name)
        else:
            raise ValueError(f"Erro: Tipo de '{name}' não encontrado na tabela de símbolos.")

    def contains(self, name: str) -> bool:
        if name in self.symbols:
            return True
        elif self.parent:
            return self.parent.contains(name)
        else:
            return False

    def __str__(self):
        return str(self.symbols)

class FuncTable:
    functions = {}

    @staticmethod
    def set(func_name: str, func_node: Any):
        if func_name in FuncTable.functions:
            raise ValueError(f"Erro: Função '{func_name}' já declarada.")
        FuncTable.functions[func_name] = func_node

    @staticmethod
    def get(func_name: str) -> Any:
        if func_name not in FuncTable.functions:
            raise ValueError(f"Erro: Função '{func_name}' não declarada.")
        return FuncTable.functions[func_name]

    @staticmethod
    def contains(func_name: str) -> bool:
        return func_name in FuncTable.functions

    @staticmethod
    def __str__():
        return str(FuncTable.functions)

class Node(ABC):
    def __init__(self, value: Any, children : List['Node'] = None):
        self.value = value
        self.children = children if children is not None else []

    @abstractmethod
    def evaluate(self, table: SymbolTable) -> Any:
        pass

class Token:
    def __init__(self, type: str, value):
        self.value = value
        self.type = type