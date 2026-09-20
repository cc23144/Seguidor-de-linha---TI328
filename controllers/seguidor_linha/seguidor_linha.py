"""
=============================================================================
PROJETO: ROBO SEGUIDOR DE LINHA - WEBOTS
DISCIPLINA: ROBÓTICA
Nome: Lorrayne Argenton dos Santos
RA: 23144
=============================================================================
Controlador do robo seguidor de linha em arena 2x2 metros.
Carrinho estavel de 4 rodas normais (tracao traseira diferencial).
Sensores infravermelhos frontais (DSE e DSD):
  - Fundo BRANCO: leitura alta (~550 a 900)
  - Linha PRETA:  leitura baixa (~300)
  - Limiar: 440 (abaixo de 440 = PRETO, acima de 440 = BRANCO)
=============================================================================
"""

import socket
import _thread
import os
import sys
from controller import Robot

MAX_STEPS = int(os.environ.get("WEBOTS_TEST_STEPS", "0"))
passos_executados = 0

# False = Inicia a correr direto ao dar Play
AGUARDAR_SOCKET = False
robo_ativo = not AGUARDAR_SOCKET

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def servidor_socket(host, porta):
    global robo_ativo
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((host, porta))
    except Exception:
        s.bind(('', porta))
    s.listen(1)
    while True:
        try:
            conn, addr = s.accept()
            msg = conn.recv(1024).decode('utf-8').strip().lower()
            if 'anda' in msg:
                robo_ativo = True
                print("[SOCKET] Comando 'anda' recebido! Robô liberado.")
            elif 'para' in msg:
                robo_ativo = False
                print("[SOCKET] Comando 'para' recebido! Robô parado.")
            conn.close()
        except Exception:
            break

try:
    _thread.start_new_thread(servidor_socket, (get_ip(), 9001))
except Exception:
    pass

# =============================================================================
# INICIALIZAÇÃO DO ROBÔ
# =============================================================================
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Motores traseiros (esquerdo e direito)
motorE = robot.getDevice('motorE')
motorD = robot.getDevice('motorD')
motorE.setPosition(float('inf'))
motorD.setPosition(float('inf'))
motorE.setVelocity(0.0)
motorD.setVelocity(0.0)

# Sensores ópticos
dse = robot.getDevice('DSE')
dsd = robot.getDevice('DSD')
dse.enable(timestep)
dsd.enable(timestep)

# =============================================================================
# VELOCIDADES E CALIBRAÇÃO ÓPTICA
# =============================================================================
VEL_RETA = 2.0          # Velocidade constante na reta (suave e estavel)
VEL_CURVA_LENTA = -0.2  # Roda interna com contra-esterco para virar no raio certo
VEL_CURVA_RAPIDA = 2.2  # Roda externa com tracao firme
VEL_BUSCA = 1.6         # Velocidade de recuperacao se perder o centro

LIMIAR = 440            # Limiar optico (preto < 440, branco >= 440)
ultima_direcao = 0
contador_print = 0

print("=" * 60)
print("SEGUIDOR DE LINHA 4 RODAS INICIADO COM SUCESSO")
print("=" * 60)

# =============================================================================
# LOOP PRINCIPAL
# =============================================================================
while robot.step(timestep) != -1:
    passos_executados += 1
    if MAX_STEPS > 0 and passos_executados >= MAX_STEPS:
        print(f"[TESTE] Finalizando teste automatizado apos {passos_executados} passos.")
        sys.exit(0)
    
    if not robo_ativo:
        motorE.setVelocity(0.0)
        motorD.setVelocity(0.0)
        continue

    # Leitura dos sensores ópticos infravermelhos
    ve = dse.getValue()
    vd = dsd.getValue()

    # Preto absorve luz infravermelha -> leitura baixa (< 440)
    esq_preto = ve < LIMIAR
    dir_preto = vd < LIMIAR

    acao = ""

    # 1. Ambos na fita preta -> Segue reto em frente
    if esq_preto and dir_preto:
        motorE.setVelocity(VEL_RETA)
        motorD.setVelocity(VEL_RETA)
        ultima_direcao = 0
        acao = "RETA"

    # 2. Só o esquerdo no preto -> Curva para esquerda
    elif esq_preto and not dir_preto:
        motorE.setVelocity(VEL_CURVA_LENTA)
        motorD.setVelocity(VEL_CURVA_RAPIDA)
        ultima_direcao = -1
        acao = "CURVA ESQUERDA"

    # 3. Só o direito no preto -> Curva para direita
    elif dir_preto and not esq_preto:
        motorE.setVelocity(VEL_CURVA_RAPIDA)
        motorD.setVelocity(VEL_CURVA_LENTA)
        ultima_direcao = 1
        acao = "CURVA DIREITA"

    # 4. Ambos fora da fita -> Recuperação imediata
    else:
        if ultima_direcao == -1:
            motorE.setVelocity(-VEL_BUSCA)
            motorD.setVelocity(VEL_BUSCA)
            acao = "RECUPERANDO PELA ESQUERDA"
        elif ultima_direcao == 1:
            motorE.setVelocity(VEL_BUSCA)
            motorD.setVelocity(-VEL_BUSCA)
            acao = "RECUPERANDO PELA DIREITA"
        else:
            motorE.setVelocity(1.2)
            motorD.setVelocity(1.2)
            acao = "AVANÇANDO"

    # Log de acompanhamento no console do Webots
    contador_print += 1
    if contador_print % 25 == 0:
        s_e = "PRETO " if esq_preto else "BRANCO"
        s_d = "PRETO " if dir_preto else "BRANCO"
        print(f"E: {ve:4.0f} [{s_e}] | D: {vd:4.0f} [{s_d}] | {acao}")
