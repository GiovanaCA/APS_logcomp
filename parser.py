from tokenizer import Tokenizer
from nodes import BlockNode, BinOp, UnOp, IntVal, NoOp, Assign, Id, PrintNode, IfNode, WhileNode, ScanNode, VarDec, StrVal, FuncCall, FuncDec
from preprocessor import PrePro

class Parser:
    tokenizer = None
    
    @staticmethod
    def parseProgram():
        '''
        Recebe um programa e retorna um nó do tipo BlockNode
        '''
        program = BlockNode("Programa")
        while Parser.tokenizer.next.type != "EOF":
            if Parser.tokenizer.next.type != "TYPE":
                raise ValueError("Esperado tipo de retorno da função")
            else:
                func_dec = Parser.parseFunction()
                program.children.append(func_dec)

        program.children.append(FuncCall('main'))

        return program
    
    @staticmethod
    def parseFunction():
        func_type = Parser.tokenizer.next.value
        Parser.tokenizer.select_next()
        parameters = []
        if Parser.tokenizer.next.type == "ID":
            func_name = Parser.tokenizer.next.value
            new_func = Assign(func_name, None)
            parameters.append(VarDec(func_type, [new_func]))
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
                Parser.tokenizer.select_next()
                
                if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == ")":
                    Parser.tokenizer.select_next()
                else:    
                    while Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                        if Parser.tokenizer.next.type == "TYPE":
                            var_type = Parser.tokenizer.next.value
                            Parser.tokenizer.select_next()
                            if Parser.tokenizer.next.type == "ID":
                                var_name = Parser.tokenizer.next.value
                                new_var = Assign(var_name, None)
                                parameters.append(VarDec(var_type, [new_var]))
                                Parser.tokenizer.select_next()
                                
                                if Parser.tokenizer.next.type == "COMMA":
                                    Parser.tokenizer.select_next()
                                elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == ")":
                                    Parser.tokenizer.select_next()
                                    break
                                else:
                                    raise ValueError("Erro de sintaxe na declaração de função")
                            else:
                                raise ValueError("Erro de sintaxe na declaração de função")
                        else:
                            raise ValueError("Erro de sintaxe na declaração de função")
                if Parser.tokenizer.next.type == "BLOCK_OPEN":
                    block = Parser.parseBlock()
                    parameters.append(block)
                else:
                    raise ValueError("Erro de sintaxe na declaração de função")
                

                return FuncDec(func_name, parameters)

            else:
                raise ValueError("Erro de sintaxe na declaração de função")

    @staticmethod
    def parseBlock():
        '''
        Recebe um bloco de código e retorna um nó do tipo BlockNode
        '''
        if Parser.tokenizer.next.type == "BLOCK_OPEN":
            Parser.tokenizer.select_next()
            block = BlockNode(None)
            
            while Parser.tokenizer.next.type != "BLOCK_CLOSE":
                block.children.append(Parser.parseStatement())
                if Parser.tokenizer.next.type == "EOF":
                    raise ValueError("Bloco não fechado")
                
            Parser.tokenizer.select_next() # Pula o '}'
            return block
        else:
            raise ValueError("Esperado '{' no início do bloco")

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
                expression = Parser.parseRelationalExpression()
                if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                    raise ValueError("Parênteses não fechados no return")
                Parser.tokenizer.select_next()
                return expression
        
        elif Parser.tokenizer.next.type == "PRINTF":
            print_node = Parser.parsePrintf()
            if Parser.tokenizer.next.type == "EOL":
                Parser.tokenizer.select_next()
            else:
                raise ValueError("Esperado ';' no final da linha")
            return print_node
        
        elif Parser.tokenizer.next.type == "BLOCK_OPEN":
            return Parser.parseBlock()

        elif Parser.tokenizer.next.type == "IF":
            return Parser.parseIf()
        
        elif Parser.tokenizer.next.type == "WHILE":
            return Parser.parseWhile()
        
        elif Parser.tokenizer.next.type == "EOL":
            Parser.tokenizer.select_next()
            return NoOp(None)
        
        elif Parser.tokenizer.next.type == "TYPE":  # Verifica se há uma declaração de tipo
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
                expression = Parser.parseRelationalExpression()

                # Retorna um nó de atribuição (Assign) com o nome da variável e a expressão
                return Assign(var_name, [expression])
            elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
                Parser.tokenizer.select_next()
                args = []
                while Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                    args.append(Parser.parseRelationalExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                    elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == ")":
                        Parser.tokenizer.select_next()
                        break
                    else:
                        raise ValueError("Erro de sintaxe na chamada de função")
                return FuncCall(var_name, args)
            else:
                raise ValueError("Esperado '=' após o identificador")
        
        else:
            raise ValueError("Esperado identificador de variável")


    @staticmethod
    def parseVarDec():
        variables = []
        var_type = Parser.tokenizer.next.value
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type == "ID":
            

            while Parser.tokenizer.next.type == "ID":
                var_name = Parser.tokenizer.next.value
                Parser.tokenizer.select_next()

                # Verifica se há atribuição durante a declaração
                if Parser.tokenizer.next.type == "ASSIGN":
                    Parser.tokenizer.select_next()
                    expression = Parser.parseRelationalExpression()
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
    def parsePrintf():
        if Parser.tokenizer.next.type == "PRINTF":
            Parser.tokenizer.select_next()
            
            if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
                Parser.tokenizer.select_next()
                expression = Parser.parseRelationalExpression()
                
                if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                    raise ValueError("Parênteses não fechados no printf")
                
                Parser.tokenizer.select_next()
                return PrintNode(None, [expression])
            else:
                raise ValueError("Erro de sintaxe em printf")
    
    @staticmethod
    def parseIf():
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()           
            condition = Parser.parseRelationalExpression()
                
            if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                raise ValueError("Parênteses não fechados no if")
            
            Parser.tokenizer.select_next()
            
            
            if_code = Parser.parseStatement()

            if Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.select_next()
                
                else_code = Parser.parseStatement()
            else:
                else_code = NoOp(None)
                
            return IfNode(None, [condition, if_code, else_code])
        else:
            raise ValueError("Erro de sintaxe no if")

    @staticmethod
    def parseWhile():
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()           
            condition = Parser.parseRelationalExpression()
                
            if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                raise ValueError("Parênteses não fechados no while")
            
            Parser.tokenizer.select_next()
            
           
            code = Parser.parseStatement()
            return WhileNode(None, [condition, code])
        else:
            raise ValueError("Erro de sintaxe no while")

    @staticmethod
    def parseRelationalExpression():
        result = Parser.parseExpression()

        if Parser.tokenizer.next.type == "RELATIONAL_OPERATOR":
            operator = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()

            next_expression = Parser.parseExpression()
            result = BinOp(operator, [result, next_expression])

        return result

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()

        while (Parser.tokenizer.next.type == "MATHEMATICAL_OPERATOR" and Parser.tokenizer.next.value in ("+", "-")) or (Parser.tokenizer.next.type == "LOGICAL_OPERATOR" and Parser.tokenizer.next.value in ("||")):
            operator = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()

            next_term = Parser.parseTerm()

            result = BinOp(operator, [result, next_term])

        return result

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()

        while (Parser.tokenizer.next.type == "MATHEMATICAL_OPERATOR" and Parser.tokenizer.next.value in ("*", "/")) or (Parser.tokenizer.next.type == "LOGICAL_OPERATOR" and Parser.tokenizer.next.value == "&&"):
            operator = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()

            next_factor = Parser.parseFactor()

            result = BinOp(operator, [result, next_factor])

        return result

    @staticmethod
    def parseFactor():
        if Parser.tokenizer.next.type == "NUMBER":
            result = IntVal(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            return result
        
        elif Parser.tokenizer.next.type == "MATHEMATICAL_OPERATOR" and Parser.tokenizer.next.value == "-":
            Parser.tokenizer.select_next()
            return UnOp("-", [Parser.parseFactor()])
        
        elif Parser.tokenizer.next.type == "MATHEMATICAL_OPERATOR" and Parser.tokenizer.next.value == "+":
            Parser.tokenizer.select_next()
            return UnOp("+", [Parser.parseFactor()])
        
        elif Parser.tokenizer.next.type == "LOGICAL_OPERATOR" and Parser.tokenizer.next.value == "!":
            Parser.tokenizer.select_next()
            return UnOp("!", [Parser.parseFactor()])
        
        elif Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()
            result = Parser.parseRelationalExpression()

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
                    args.append(Parser.parseRelationalExpression())
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

        elif Parser.tokenizer.next.type == "SCANF":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "PRIORITY" and Parser.tokenizer.next.value == "(":
                Parser.tokenizer.select_next()            
                if Parser.tokenizer.next.type != "PRIORITY" or Parser.tokenizer.next.value != ")":
                    raise ValueError("Parênteses não fechados no scanf")
                Parser.tokenizer.select_next()
                return ScanNode(None)
            else:
                raise ValueError("Erro de sintaxe no scanf")
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