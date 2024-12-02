from typing import List, Any
from schemas import SymbolTable, Node, FuncTable


class FuncDec(Node):
    def evaluate(self, table: FuncTable = FuncTable) -> Any:
        func_name = self.value
        if FuncTable.contains(func_name):
            raise ValueError(f"Erro: Função '{func_name}' já declarada")
        
        FuncTable.set(func_name, self)
        return 0, "int"
    
class FuncCall(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        func_name = self.value
        if not FuncTable.contains(func_name):
            raise ValueError(f"Erro: Função '{func_name}' não declarada")
        
        func_node = FuncTable.get(func_name)
        params = func_node.children

        local_table = SymbolTable()
        
        # Verifica se a quantidade de argumentos é compatível
        if len(self.children) != len(params)-2:
            raise ValueError(f"Erro: Número de argumentos inválido para a função '{func_name}'")
        
        # Avalia os argumentos e os atribui à tabela de símbolos local
        for arg_node, param_node in zip(self.children, params[1:-1]):
            arg_value, arg_type = arg_node.evaluate(table)
            param_name = param_node.children[0].value
            param_type = param_node.value
            
            if arg_type != param_type:
                raise TypeError(f"Erro: Tipo de argumento inválido para a função '{func_name}'")
            
            local_table.set(param_name, arg_value, arg_type)
        
        # Avalia o bloco de código da função
        return func_node.children[-1].evaluate(local_table)

class BlockNode(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        result = 0
        for child in self.children:
            a, b = child.evaluate(table)
            result += a
        return result, "int"

class BinOp(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        op1_value, op1_type = self.children[0].evaluate(table)
        op2_value, op2_type = self.children[1].evaluate(table)

        if op1_type == "bool":
            op1_value = 1 if bool(op1_value) else 0
        if op2_type == "bool":
            op2_value = 1 if bool(op2_value) else 0
        
        # Verifica tipos
        if self.value == "+" and op1_type != "str" and op2_type != "str":
            return int(op1_value + op2_value), "int"
        
        elif self.value == "+" and (op1_type == "str" or op2_type == "str"):
            return str(op1_value) + str(op2_value), "str"
        
        elif self.value == "-" and op1_type != "str" and op2_type != "str":
            return int(op1_value - op2_value), "int"
        
        elif self.value == "*" and op1_type != "str" and op2_type != "str":
            return int(op1_value * op2_value), "int"
        
        elif self.value == "/" and op1_type != "str" and op2_type != "str":
            return int(op1_value / op2_value), "int"
        
        elif self.value == "<":
            if op1_type != op2_type:
                raise TypeError(f"Erro: Tipos incompatíveis: {op1_type} e {op2_type}")
            return int(op1_value < op2_value), "int"
        
        elif self.value == ">":
            if op1_type != op2_type:
                raise TypeError(f"Erro: Tipos incompatíveis: {op1_type} e {op2_type}")
            return int(op1_value > op2_value), "int"
        
        elif self.value == "==":
            if op1_type != op2_type:
                raise TypeError(f"Erro: Tipos incompatíveis: {op1_type} e {op2_type}")
            return int(op1_value == op2_value), "int"
        
        elif self.value == "&&" and op1_type != "str" and op2_type != "str":
            return op1_value and op2_value, "int"
        
        elif self.value == "||" and op1_type != "str" and op2_type != "str":
            return op1_value or op2_value, "int"
        
        else:
            raise TypeError(f"Operação inválida para o tipo {op1_type}")

        

class UnOp(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        value, value_type = self.children[0].evaluate(table)

        # Mapeia booleanos para inteiros
        if value_type == "bool":
            value = 1 if value else 0
            value_type = "int"

        # Operador Unário de Negação (-)
        if self.value == "-":
            return -value, "int"
        
        # Operador Unário Lógico NOT (!)
        elif self.value == "!":
            if value_type == "str":
                raise TypeError("Erro: Operador '!' não pode ser aplicado a strings")
            return (0 if value != 0 else 1), "int"  # Mapeia para 0 ou 1

        else:
            raise ValueError(f"Operador unário desconhecido: {self.value}")
        
class IntVal(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        return self.value, "int"  # Retorna o valor e o tipo

class StrVal(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        return self.value, "str"  # Retorna o valor e o tipo
class NoOp(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        return 0, "int"

class Assign(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        var_name = self.value  # Nome da variável
        if len(self.children) == 0:
            return 0, "int"
        var_value, value_type = self.children[0].evaluate(table)  # Avalia a expressão
        # Verifica se a variável foi declarada
        if not table.contains(var_name):
            raise ValueError(f"Erro: Variável '{var_name}' não foi declarada")

        # Verifica se o tipo do valor é compatível com o tipo da variável
        var_type = table.get_type(var_name)
        if var_type != value_type:
            raise TypeError(f"Erro: Tentativa de atribuir tipo '{value_type}' à variável '{var_name}' de tipo '{var_type}'")

        # Atualiza o valor da variável na tabela de símbolos
        table.set(var_name, var_value, var_type)
        return 0, "int"
    

class Id(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        if table.contains(self.value):
            return table.get(self.value), table.get_type(self.value)
        else:
            raise ValueError(f"Erro: Variável '{self.value}' não declarada")
        
class PrintNode(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        value, value_type = self.children[0].evaluate(table)
        print(value)
        return 0, "int"
        
class IfNode(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        condition_value, condition_type = self.children[0].evaluate(table)

        if condition_type != "int":
            raise TypeError("Erro: Condição do 'if' deve ser do tipo int")

        if condition_value:
            return self.children[1].evaluate(table)
        else:
            return self.children[2].evaluate(table)

class WhileNode(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        result = 0
        while self.children[0].evaluate(table)[0]:
            result += self.children[1].evaluate(table)[0]
        return result, "int"
    
class ScanNode(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        value = int(input())
        return value, "int"
    
class VarDec(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        var_type = self.value
        for child in self.children:
            
            var_name = child.value
            if table.contains(var_name):
                raise ValueError(f"Erro: Variável '{var_name}' já declarada")
            
            table.set(var_name, None, var_type)
        
        # Avalia as atribuições associadas às declarações
        for child in self.children:
            child.evaluate(table)
        
        return 0, "int"
