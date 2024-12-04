from tokenizer import Tokenizer
from nodes import BlockNode, BinOp, UnOp, IntVal, NoOp, Assign, Id, MostrarNode, SeNode, EnquantoNode, VarDec, StrVal, FuncCall, FuncDec, DeclaraRobo
from preprocessor import PrePro
from symbols import RESERVED_WORDS, RESERVED_METHODS
from schemas import FuncTable

class Parser:
    tokenizer = None
    
    @staticmethod
    def parseProgram():
        '''
        Recebe um programa e retorna um nó do tipo BlockNode
        '''
        program = BlockNode("Programa")
        while Parser.tokenizer.next.type != "EOF":
            if Parser.tokenizer.next.type == "COMANDO":
                comando_dec = Parser.parseFunction(is_comando=True)
                program.children.append(comando_dec)
            elif Parser.tokenizer.next.type == "TYPE":
                func_dec = Parser.parseFunction()
                program.children.append(func_dec)
            else:
                raise ValueError("Esperado tipo de retorno da função ou 'COMANDO'")
            
        program.children.append(FuncCall('main'))
        
        return program

    @staticmethod
    def parseFunction(is_comando=False):
        '''
        Parseia a declaração de uma função comum ou 'comando' e retorna um nó FuncDec
        '''
        func_type = "comando" if is_comando else Parser.tokenizer.next.value
        if is_comando:
            Parser.tokenizer.select_next()  # Consome 'COMANDO'
        else:
            Parser.tokenizer.select_next()  # Consome o tipo da função

        if Parser.tokenizer.next.type != "ID":
            raise ValueError("Erro de sintaxe na declaração de função: Esperado nome da função")
        
        func_name = Parser.tokenizer.next.value
        Parser.tokenizer.select_next()
        
        # Verifica se o nome da função é um método reservado
        if func_name in RESERVED_METHODS:
            raise ValueError(f"Erro: Função '{func_name}' é um método reservado e não pode ser redefinida")
        
        if FuncTable.contains(func_name):
            raise ValueError(f"Erro: Função '{func_name}' já declarada")
        
        # Verifica se a próxima parte é '('
        if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()
            parameters = []
            param_types = []
            if not (Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == ")"):
                while True:
                    if Parser.tokenizer.next.type != "TYPE":
                        raise ValueError("Erro de sintaxe na declaração dos parâmetros da função: Esperado tipo")
                    param_type = Parser.tokenizer.next.value
                    Parser.tokenizer.select_next()
                    
                    if Parser.tokenizer.next.type != "ID":
                        raise ValueError("Erro de sintaxe na declaração dos parâmetros da função: Esperado nome do parâmetro")
                    param_name = Parser.tokenizer.next.value
                    Parser.tokenizer.select_next()
                    
                    # Adiciona o parâmetro à lista
                    parameters.append(VarDec(param_type, [Assign(param_name, None)]))
                    param_types.append(param_type)
                    
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                    elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == ")":
                        break
                    else:
                        raise ValueError("Erro de sintaxe na declaração dos parâmetros da função: Esperado ',' ou ')'")
        
            # Fecha o parêntese
            if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == ")":
                Parser.tokenizer.select_next()
            else:
                raise ValueError("Erro de sintaxe na declaração de função: Esperado ')' após parâmetros")
            
            # Verifica se é uma função 'comando' e aplica regras específicas
            if is_comando:
                # A função 'comando' deve ter pelo menos um parâmetro do tipo 'Robo'
                if len(param_types) == 0 or param_types[0] != "Robo":
                    raise ValueError("Erro: Função 'comando' deve receber pelo menos um argumento do tipo 'Robo'")
            else:
                # Para funções comuns, pode adicionar outras verificações se necessário
                pass
            
            # Espera um ':' antes do bloco de código
            if Parser.tokenizer.next.type == "COLON":
                block = Parser.parseBlock()
                # Inclui func_type como primeiro filho do FuncDec
                # Parâmetros já foram adicionados
                parameters_with_block = [StrVal(func_type)] + parameters + [block]
            else:
                raise ValueError("Erro de sintaxe na declaração de função: Esperado ':' após parâmetros")
            
            # Cria o nó de declaração de função
            return FuncDec(func_name, parameters_with_block)
        
        else:
            raise ValueError("Erro de sintaxe na declaração de função: Esperado '(' após nome da função")

    @staticmethod
    def parseBlock():
        '''
        Recebe um bloco de código e retorna um nó do tipo BlockNode
        '''
        if Parser.tokenizer.next.type == "COLON":
            Parser.tokenizer.select_next()
            block = BlockNode(None)
            while Parser.tokenizer.next.type != "FIM":
                block.children.append(Parser.parseStatement())
                if Parser.tokenizer.next.type == "EOF":
                    raise ValueError("Bloco não fechado")
            Parser.tokenizer.select_next() # Pula o 'FIM'
            if Parser.tokenizer.next.type != "EOL":
                raise ValueError("Bloco não fechado")
            Parser.tokenizer.select_next() # Pula o ';'
            return block
        else:
            raise ValueError("Esperado ':' após a declaração de função")

    @staticmethod
    def parseStatement():
        
        if Parser.tokenizer.next.type == "ID":
            assign = Parser.parseAssignment()
            if Parser.tokenizer.next.type == "EOL":
                Parser.tokenizer.select_next()
            else:
                raise ValueError("Esperado ';' no final da linha")
            return assign
        
        elif Parser.tokenizer.next.type == "RETURN":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
                Parser.tokenizer.select_next()
                expression = Parser.parseExpressao()
                if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                    raise ValueError("Parênteses não fechados no return")
                Parser.tokenizer.select_next()
                return expression
        
        elif Parser.tokenizer.next.type == "MOSTRAR":
            print_node = Parser.parseMostrar()
            if Parser.tokenizer.next.type == "EOL":
                Parser.tokenizer.select_next()
            else:
                raise ValueError("Esperado ';' no final da linha")
            return print_node
        

        elif Parser.tokenizer.next.type == "COLON":
            return Parser.parseBlock()

        elif Parser.tokenizer.next.type == "SE":
            return Parser.parseSe()
        
        elif Parser.tokenizer.next.type == "ENQUANTO":
            return Parser.parseEnquanto()
        
        elif Parser.tokenizer.next.type == "EOL":
            Parser.tokenizer.select_next()
            return NoOp(None)
        
        # IRÁ TER QUE TRATAR O TIPO ROBO
        elif Parser.tokenizer.next.type == "TYPE":  # Verifica se há uma declaração de tipo

            if Parser.tokenizer.next.value == "comando":
                raise ValueError("Erro: Comando não pode ser declarado como variável, apenas como função")
            elif Parser.tokenizer.next.value == "void":
                raise ValueError("Erro: Tipo de variável inválido")
            
            var_dec = Parser.parseVarDec()  # Chama o parseVarDec para tratar a declaração de variáveis
            if Parser.tokenizer.next.type == "EOL":
                Parser.tokenizer.select_next()
            else:
                raise ValueError("Esperado ';' no final da linha")
            return var_dec
        
        else:
            raise ValueError("Declaração inválida")
        
    @staticmethod
    def parseAssignment():
        # Verifica se o próximo token é um identificador de variável
        if Parser.tokenizer.next.type == "ID":
            var_name = Parser.tokenizer.next.value  # Captura o nome da variável
            Parser.tokenizer.select_next()

            # Verifica se o token seguinte é o operador de atribuição "="
            if Parser.tokenizer.next.type == "ASSIGN":
                Parser.tokenizer.select_next()

                # Avalia a expressão após o "="
                expression = Parser.parseExpressao()

                # Retorna um nó de atribuição (Assign) com o nome da variável e a expressão
                return Assign(var_name, [expression])
           
            elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
                Parser.tokenizer.select_next()
                args = []
                while Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                    args.append(Parser.parseExpressao())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                    elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == ")":
                        Parser.tokenizer.select_next()
                        break
                    else:
                        raise ValueError("Erro de sintaxe na chamada de função")
                return FuncCall(var_name, args)
            
            else:
                raise ValueError("Esperado '=' após o identificador ou '()' para chamada de função")
        
        else:
            raise ValueError("Esperado identificador de variável")

    @staticmethod
    def parseVarDec():
        variables = []
        var_type = Parser.tokenizer.next.value

        if var_type == "Robo":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "ID":
                var_name = Parser.tokenizer.next.value
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == "ASSIGN":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "TYPE" and Parser.tokenizer.next.value == "Robo":
                        Parser.tokenizer.select_next()
                        if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
                            Parser.tokenizer.select_next()
                            name = Parser.parseExpressao()                        
                            if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                                raise ValueError("Parênteses não fechados")
                            Parser.tokenizer.select_next()
                        else:
                            raise ValueError("Erro de sintaxe: Robô não inicializado ou inicializado incorretamente")

                    else:
                        raise ValueError("Declaração de robo inválida")

                else:
                    raise ValueError("Erro de sintaxe: Robô não inicializado")
                
            return DeclaraRobo(var_name, [name])    
                    


        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type == "ID":
            while Parser.tokenizer.next.type == "ID":
                var_name = Parser.tokenizer.next.value
                Parser.tokenizer.select_next()
                # Verifica se há atribuição durante a declaração
                if Parser.tokenizer.next.type == "ASSIGN":
                    Parser.tokenizer.select_next()
                    expression = Parser.parseExpressao()
                    variables.append(Assign(var_name, [expression]))
                else:
                    variables.append(Assign(var_name, None))  # Inicializa com valor padrão
                if Parser.tokenizer.next.type == "COMMA":
                    Parser.tokenizer.select_next()
                else:
                    break
            else:
                raise ValueError("Erro de sintaxe na declaração de variáveis")
            return VarDec(var_type, variables)
        else:
            raise ValueError("Erro de sintaxe: Tipo de variável esperado")

    @staticmethod
    def parseMostrar():
        if Parser.tokenizer.next.type == "MOSTRAR":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
                Parser.tokenizer.select_next()
                expression = Parser.parseExpressao()
                if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                    raise ValueError("Parênteses não fechados no mostrar")
                Parser.tokenizer.select_next()
                return MostrarNode(None, [expression])
            else:
                raise ValueError("Erro de sintaxe em mostrar")
    
    @staticmethod
    def parseSe():
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()           
            condition = Parser.parseExpressao()
            if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                raise ValueError("Parênteses não fechados no se")
            Parser.tokenizer.select_next()
            if_code = Parser.parseStatement()
            if Parser.tokenizer.next.type == "SENAO":
                Parser.tokenizer.select_next()
                else_code = Parser.parseStatement()
            else:
                else_code = NoOp(None)
            return SeNode(None, [condition, if_code, else_code])
        else:
            raise ValueError("Erro de sintaxe no if")

    @staticmethod
    def parseEnquanto():
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()           
            condition = Parser.parseExpressao()
            if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                raise ValueError("Parênteses não fechados no while")
            Parser.tokenizer.select_next()
            code = Parser.parseStatement()
            return EnquantoNode(None, [condition, code])
        else:
            raise ValueError("Erro de sintaxe no while")

    @staticmethod
    def parseExpressao():
        result = Parser.parseEXP1()
        if Parser.tokenizer.next.type == "RELATIONAL_OPERATOR":
            operator = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            next_expression = Parser.parseEXP1()
            result = BinOp(operator, [result, next_expression])
        return result

    @staticmethod
    def parseEXP1():
        result = Parser.parseEXP2()
        while (Parser.tokenizer.next.type == "MATHEMATICAL_OPERATOR" and Parser.tokenizer.next.value in ("+", "-")) or (Parser.tokenizer.next.type == "LOGICAL_OPERATOR" and Parser.tokenizer.next.value in ("||")):
            operator = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            next_term = Parser.parseEXP2()
            result = BinOp(operator, [result, next_term])
        return result

    @staticmethod
    def parseEXP2():
        result = Parser.parseEXP3()
        while (Parser.tokenizer.next.type == "MATHEMATICAL_OPERATOR" and Parser.tokenizer.next.value in ("*", "/")) or (Parser.tokenizer.next.type == "LOGICAL_OPERATOR" and Parser.tokenizer.next.value == "&&"):
            operator = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            next_factor = Parser.parseEXP3()
            result = BinOp(operator, [result, next_factor])
        return result

    @staticmethod
    def parseEXP3():
        if Parser.tokenizer.next.type == "NUMBER":
            result = IntVal(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            return result
        
        elif Parser.tokenizer.next.type == "MATHEMATICAL_OPERATOR" and Parser.tokenizer.next.value == "-":
            Parser.tokenizer.select_next()
            return UnOp("-", [Parser.parseEXP3()])
        
        elif Parser.tokenizer.next.type == "MATHEMATICAL_OPERATOR" and Parser.tokenizer.next.value == "+":
            Parser.tokenizer.select_next()
            return UnOp("+", [Parser.parseEXP3()])
        
        elif Parser.tokenizer.next.type == "LOGICAL_OPERATOR" and Parser.tokenizer.next.value == "!":
            Parser.tokenizer.select_next()
            return UnOp("!", [Parser.parseEXP3()])
        
        elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()
            result = Parser.parseExpressao()

            if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                raise ValueError("Parênteses não fechados")

            Parser.tokenizer.select_next()
            return result
        
        elif Parser.tokenizer.next.type == "ID":
            name = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            if (Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "("):
                Parser.tokenizer.select_next()
                args = []
                while Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                    args.append(Parser.parseExpressao())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                    elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == ")":
                        Parser.tokenizer.select_next()
                        break
                    else:
                        raise ValueError("Erro de sintaxe na chamada de função")
                return FuncCall(name, args)
            else:
                result = Id(name)
                return result

        elif Parser.tokenizer.next.type == "STRING":
            result = StrVal(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            return result
        
        else:
            raise ValueError("Fator inválido")

    @staticmethod
    def run(source: str):
        preprocessed_source = PrePro.filter(source)
        Parser.tokenizer = Tokenizer(preprocessed_source)
        Parser.tokenizer.select_next()
        result = Parser.parseProgram()        
        if Parser.tokenizer.next.type != "EOF":
            raise ValueError("A expressão está mal formada")
        return result