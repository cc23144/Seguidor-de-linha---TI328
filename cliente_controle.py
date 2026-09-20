"""
=============================================================================
SCRIPT CLIENTE SOCKET TCP PARA ENVIO DE COMANDOS AO ROBÔ WEBOTS
=============================================================================
Permite enviar comandos via rede para o robô seguidor de linha no Webots.
Comandos suportados:
  - 'anda' : autoriza o início da corrida do robô
  - 'para' : pausa o robô na pista
=============================================================================
"""

import socket
import sys

PORTA_PADRAO = 9001

def get_ip_local():
    """Descobre o IP local da máquina."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def enviar_comando(comando, ip=None, porta=None):
    """Envia uma mensagem de comando via socket TCP para o robô."""
    ip_alvo = ip or get_ip_local()
    porta_alvo = porta or PORTA_PADRAO

    print(f"[CLIENTE] Conectando a {ip_alvo}:{porta_alvo}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    
    try:
        sock.connect((ip_alvo, porta_alvo))
        sock.sendall(comando.strip().encode('utf-8'))
        print(f"[SUCESSO] Comando '{comando}' enviado com sucesso!")
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar! Verifique se a simulação no Webots está RODANDO (Play).")
    except Exception as e:
        print(f"[ERRO] Ocorreu uma falha: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    print("=" * 60)
    print("PAINEL DE CONTROLE REMOTO SOCKET - SEGUIDOR DE LINHA WEBOTS")
    print("=" * 60)
    print("Comandos disponíveis: 'anda', 'para' ou 'sair'")
    
    while True:
        try:
            cmd = input("\nDigite o comando para o robô: ").strip()
            if not cmd:
                continue
            if cmd.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando cliente.")
                break
            enviar_comando(cmd)
        except KeyboardInterrupt:
            print("\nEncerrado pelo usuário.")
            break
