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

class Robo:
    def __init__(self, name: str):
        self.name = name
        self.x = 0
        self.y = 0
        self.angle = 0
        self.claw = False
        self.arm = False

    def __str__(self):
        return f"Robô {self.name} em ({self.x}, {self.y}) com ângulo {self.angle}°"

    def __repr__(self):
        return str(self)
    
    def move_forward(self, distance: int):
        self.x += distance
    
    def move_backward(self, distance: int):
        self.x -= distance
    
    def move_left(self, distance: int):
        self.y -= distance

    def move_right(self, distance: int):
        self.y += distance

    def rotate(self, angle: int):
        self.angle += angle

    def open(self):
        self.claw = True
    
    def close(self):
        self.claw = False
    
    def raise_arm(self):
        self.arm = True
    
    def lower_arm(self):
        self.arm = False


class RobotTable:

    robots = {}

    @staticmethod
    def set(robot_name: str, robot: Robo):
        if robot_name in RobotTable.robots:
            raise ValueError(f"Erro: Robô '{robot_name}' já declarado.")
        RobotTable.robots[robot_name] = robot

    @staticmethod
    def get(robot_name: str) -> Robo:
        if robot_name not in RobotTable.robots:
            raise ValueError(f"Erro: Robô '{robot_name}' não declarado.")
        return RobotTable.robots[robot_name]

    @staticmethod
    def contains(robot_name: str) -> bool:
        return robot_name in RobotTable.robots

    @staticmethod
    def __str__():
        return str(RobotTable.robots)

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
    
class RobotTable:
    robots = {}

    @staticmethod
    def set(robot_name: str, robot_node: Any):
        if robot_name in RobotTable.robots:
            raise ValueError(f"Erro: Robô '{robot_name}' já declarado.")
        RobotTable.robots[robot_name] = robot_node

    @staticmethod
    def get(robot_name: str) -> Any:
        if robot_name not in RobotTable.robots:
            raise ValueError(f"Erro: Robô '{robot_name}' não declarado.")
        return RobotTable.robots[robot_name]

    @staticmethod
    def contains(robot_name: str) -> bool:
        return robot_name in RobotTable.robots
    

    @staticmethod
    def __str__():
        return str(RobotTable.robots)

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