from typing import List, Any
from schemas import SymbolTable, Node, FuncTable, RobotTable, Robo
from symbols import RESERVED_METHODS

class DeclaraRobo(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        var_name = self.value  # Nome da variável, por exemplo, 'robo1'
        
        # Avalia o nome do robô, que deve ser uma string
        robo_name, robo_type = self.children[0].evaluate(table)  # Ex: ('RoboAlpha', 'str')
        
        # Verifica se o tipo do nome do robô é 'str'
        if robo_type != "str":
            raise ValueError("Erro: Nome do robô deve ser uma string")
        
        # Verifica se o nome do robô já está na RobotTable
        if RobotTable.contains(robo_name):
            raise ValueError(f"Erro: Robô '{robo_name}' já declarado")
        
        # Verifica se o nome da variável já está na SymbolTable
        if table.contains(var_name):
            raise ValueError(f"Erro: Variável '{var_name}' já declarada")
        
        # Cria uma nova instância de Robo
        novo_robo = Robo(robo_name)
        
        # Registra o robô na RobotTable
        RobotTable.set(robo_name, novo_robo)
        
        # Registra a variável na SymbolTable
        table.set(var_name, novo_robo, "Robo")
        return 0, "int"


# nodes.py

class FuncDec(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        func_name = self.value
        
        # Extrai func_type do primeiro filho (StrVal)
        func_type_node = self.children[0]
        func_type = func_type_node.value  # 'int', 'comando', etc.
        
        # Verifica se o nome da função é um método reservado
        if func_name in RESERVED_METHODS:
            raise ValueError(f"Erro: Função '{func_name}' é um método reservado e não pode ser redefinida")
        
        # Verifica se a função já foi declarada
        if FuncTable.contains(func_name):
            raise ValueError(f"Erro: Função '{func_name}' já declarada")
        
        # Coleta os parâmetros da função
        params = []
        for child in self.children[1:-1]:  # Exclui func_type e bloco
            if isinstance(child, VarDec):
                for var in child.children:
                    var_name = var.value  # Nome da variável
                    var_type = child.value  # Tipo da variável
                    params.append((var_name, var_type))
        
        # Obtém o bloco de código da função
        block = self.children[-1]
        
        # Registra a função na FuncTable
        FuncTable.set(func_name, {
            'type': func_type,
            'params': params,
            'block': block
        })
        return 0, "int"


class FuncCall(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        func_name = self.value
        if not FuncTable.contains(func_name):
            raise ValueError(f"Erro: Função '{func_name}' não declarada")
        
        func_entry = FuncTable.get(func_name)
        
        # Verifica se é um método reservado
        if func_name in RESERVED_METHODS:
            method_info = RESERVED_METHODS[func_name]
            expected_arg_types = method_info["arg_types"]
            
            # Verifica se a quantidade de argumentos é compatível
            if len(self.children) < len(expected_arg_types):
                raise ValueError(f"Erro: Função '{func_name}' requer pelo menos {len(expected_arg_types)} argumentos")
            
            # Avalia os argumentos
            args = []
            for i, expected_type in enumerate(expected_arg_types):
                if i >= len(self.children):
                    break
                arg_node = self.children[i]
                arg_value, arg_type = arg_node.evaluate(table)
                if arg_type != expected_type:
                    raise TypeError(f"Erro: Argumento {i+1} da função '{func_name}' deve ser do tipo '{expected_type}', mas foi '{arg_type}'")
                args.append(arg_value)
            
            # Chama a implementação reservada com os argumentos
            result = method_info["implementation"](*args)
            return result, "int"  # Retorna o valor retornado pela implementação reservada e o tipo
        
        else:
            # Função definida pelo usuário
            func_node = func_entry
            params = func_node['params']
            block = func_node['block']
            func_type = func_node['type']
            
            # Verifica se a quantidade de argumentos é compatível
            if len(self.children) != len(params):
                raise ValueError(f"Erro: Número de argumentos inválido para a função '{func_name}'")
            
            # Avalia os argumentos e os atribui à tabela de símbolos local
            local_table = SymbolTable()
            for arg_node, (param_name, param_type) in zip(self.children, params):
                arg_value, arg_type = arg_node.evaluate(table)
                if arg_type != param_type:
                    raise TypeError(f"Erro: Tipo de argumento inválido para a função '{func_name}' no parâmetro '{param_name}'")
                local_table.set(param_name, arg_value, param_type)
            
            # Avalia o bloco de código da função
            return block.evaluate(local_table)


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

        if op1_type == "Robo" or op2_type == "Robo":
            raise TypeError(f"Operação inválida para o tipo {op1_type} e {op2_type}")

        if op1_type == "bool":
            op1_value = 1 if bool(op1_value) else 0
        if op2_type == "bool":
            op2_value = 1 if bool(op2_value) else 0

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
        elif self.value == "<=":
            if op1_type != op2_type:
                raise TypeError(f"Erro: Tipos incompatíveis: {op1_type} e {op2_type}")
            return int(op1_value <= op2_value), "int"
        elif self.value == ">=":
            if op1_type != op2_type:
                raise TypeError(f"Erro: Tipos incompatíveis: {op1_type} e {op2_type}")
            return int(op1_value >= op2_value), "int"
        elif self.value == "!=":
            if op1_type != op2_type:
                raise TypeError(f"Erro: Tipos incompatíveis: {op1_type} e {op2_type}")
            return int(op1_value != op2_value), "int"
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


class MostrarNode(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        value, value_type = self.children[0].evaluate(table)
        print(value)
        return 0, "int"


class SeNode(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        condition_value, condition_type = self.children[0].evaluate(table)
        if condition_type != "int":
            raise TypeError("Erro: Condição do 'if' deve ser do tipo int")
        if condition_value:
            return self.children[1].evaluate(table)
        else:
            return self.children[2].evaluate(table)


class EnquantoNode(Node):
    def evaluate(self, table: SymbolTable) -> Any:
        result = 0
        while self.children[0].evaluate(table)[0]:
            result += self.children[1].evaluate(table)[0]
        return result, "int"


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