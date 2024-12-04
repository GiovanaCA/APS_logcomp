# Definições de Símbolos
from reserved_methods import reserved_move_frente, reserved_move_tras, reserved_move_esquerda, reserved_move_direita, reserved_gira, reserved_abre, reserved_fecha, reserved_sobe, reserved_desce, reserved_ver_x, reserved_ver_y, reserved_ver_angulo, reserved_ver_garra, reserved_ver_braco

NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
MATHEMATICAL_OPERATORS = ['+', '-', '*', '/']
LOGICAL_OPERATORS = ['&&', '||', '!']
RELATIONAL_OPERATORS = ['<', '>', '==', '<=', '>=', '!=']
SYMBOLS = ['=', ';', ':']
PRIORITIES = ['(', ')']
RESERVED_WORDS = {
    'mostrar': 'MOSTRAR',
    'SE': 'SE',
    'SENAO': 'SENAO',
    'ENQUANTO': 'ENQUANTO',
    'FIM': 'FIM',
    'return': 'RETURN',
    'comando': 'COMANDO',
}
TYPES = ['str', 'bool', 'int', 'void', 'Robo']
BOOLEAN_VALUES = ['true', 'false']
RESERVED_METHODS = {
    'move_frente': {
        'arg_types': ['Robo', 'int'],
        'implementation': reserved_move_frente
    },
    'move_tras': {
        'arg_types': ['Robo', 'int'],
        'implementation': reserved_move_tras
    },
    'move_esquerda': {
        'arg_types': ['Robo', 'int'],
        'implementation': reserved_move_esquerda
    },
    'move_direita': {
        'arg_types': ['Robo', 'int'],
        'implementation': reserved_move_direita
    },
    'gira': {
        'arg_types': ['Robo', 'int'],
        'implementation': reserved_gira
    },
    'abre': {
        'arg_types': ['Robo'],
        'implementation': reserved_abre
    },
    'fecha': {
        'arg_types': ['Robo'],
        'implementation': reserved_fecha
    },
    'sobe': {
        'arg_types': ['Robo'],
        'implementation': reserved_sobe
    },
    'desce': {
        'arg_types': ['Robo'],
        'implementation': reserved_desce
    },
    'ver_x': {
        'arg_types': ['Robo'],
        'implementation': reserved_ver_x
    },
    'ver_y': {
        'arg_types': ['Robo'],
        'implementation': reserved_ver_y
    },
    'ver_angulo': {
        'arg_types': ['Robo'],
        'implementation': reserved_ver_angulo
    },
    'ver_garra': {
        'arg_types': ['Robo'],
        'implementation': reserved_ver_garra
    },
    'ver_braco': {
        'arg_types': ['Robo'],
        'implementation': reserved_ver_braco
    },
}