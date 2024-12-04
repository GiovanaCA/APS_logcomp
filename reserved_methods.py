from schemas import Robo

def reserved_move_frente(robo: Robo, distance: int):
    robo.move_forward(distance)
    print(f"{robo.name} moveu-se para frente {distance} unidades.")
    return 0

def reserved_move_tras(robo: Robo, distance: int):
    robo.move_backward(distance)
    print(f"{robo.name} moveu-se para trás {distance} unidades.")
    return 0

def reserved_move_esquerda(robo: Robo, distance: int):
    robo.move_left(distance)
    print(f"{robo.name} moveu-se para a esquerda {distance} unidades.")
    return 0

def reserved_move_direita(robo: Robo, distance: int):
    robo.move_right(distance)
    print(f"{robo.name} moveu-se para a direita {distance} unidades.")
    return 0

def reserved_gira(robo: Robo, angle: int):
    robo.rotate(angle)
    print(f"{robo.name} girou {angle} graus.")
    return 0

def reserved_abre(robo: Robo):
    robo.open()
    print(f"Garra de {robo.name} aberta.")
    return 0

def reserved_fecha(robo: Robo):
    robo.close()
    print(f"Garra de {robo.name} fechada.")
    return 0

def reserved_sobe(robo: Robo):
    robo.raise_arm()
    print(f"Braço de {robo.name} levantado.")
    return 0

def reserved_desce(robo: Robo):
    robo.lower_arm()
    print(f"Braço de {robo.name} abaixado.")
    return 0

def reserved_ver_x(robo: Robo):
    print(f"Posição X de {robo.name}: {robo.x}")
    return robo.x

def reserved_ver_y(robo: Robo):
    print(f"Posição Y de {robo.name}: {robo.y}")
    return robo.y

def reserved_ver_angulo(robo: Robo):
    print(f"Ângulo de {robo.name}: {robo.angle}°")
    return robo.angle

def reserved_ver_garra(robo: Robo):
    status = "aberta" if robo.claw else "fechada"
    print(f"Garra de {robo.name} está {status}.")
    return robo.claw

def reserved_ver_braco(robo: Robo):
    status = "levantado" if robo.arm else "abaixado"
    print(f"Braço de {robo.name} está {status}.")
    return robo.arm