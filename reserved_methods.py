from schemas import Robo

def reserved_move_frente(robo: Robo, distance: int):
    robo.move_forward(distance)
    return 0

def reserved_move_tras(robo: Robo, distance: int):
    robo.move_backward(distance)
    return 0

def reserved_move_esquerda(robo: Robo, distance: int):
    robo.move_left(distance)
    return 0

def reserved_move_direita(robo: Robo, distance: int):
    robo.move_right(distance)
    return 0

def reserved_gira(robo: Robo, angle: int):
    robo.rotate(angle)
    return 0

def reserved_abre(robo: Robo):
    robo.open()
    return 0

def reserved_fecha(robo: Robo):
    robo.close()
    return 0

def reserved_sobe(robo: Robo):
    robo.raise_arm()
    return 0

def reserved_desce(robo: Robo):
    robo.lower_arm()
    return 0

def reserved_ver_x(robo: Robo):
    return robo.x

def reserved_ver_y(robo: Robo):
    return robo.y

def reserved_ver_angulo(robo: Robo):
    return robo.angle

def reserved_ver_garra(robo: Robo):
    status = "aberta" if robo.claw else "fechada"
    return robo.claw

def reserved_ver_braco(robo: Robo):
    status = "levantado" if robo.arm else "abaixado"
    return robo.arm