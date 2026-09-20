"""
Script para geracao da textura da pista do Seguidor de Linha.
Gera uma imagem PNG representando a arena de 2x2 metros com fita preta de 6 cm
sobre fundo branco em circuito fechado suave.
"""

import os
import math
import struct
import zlib

def criar_png_pista(largura=1024, altura=1024, caminho_saida="worlds/textures/pista_circuito.png"):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    # Fundo branco puro (255)
    pixels = bytearray([255] * (largura * altura))
    
    # Circuito perfeitamente arredondado e suave
    pontos_curva = [
        (300, 200),
        (512, 200),
        (720, 210),
        (800, 512),
        (710, 760),
        (540, 670),
        (400, 780),
        (240, 680),
        (200, 480),
        (300, 200)
    ]
    
    def catmull_rom(p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        x = 0.5 * ((2 * p1[0]) +
                   (-p0[0] + p2[0]) * t +
                   (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                   (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
        y = 0.5 * ((2 * p1[1]) +
                   (-p0[1] + p2[1]) * t +
                   (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                   (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
        return x, y

    caminho = []
    n = len(pontos_curva) - 1
    pontos_estendidos = [pontos_curva[-2]] + pontos_curva + [pontos_curva[1], pontos_curva[2]]
    
    passos_por_segmento = 160
    for i in range(1, n + 1):
        p0 = pontos_estendidos[i - 1]
        p1 = pontos_estendidos[i]
        p2 = pontos_estendidos[i + 1]
        p3 = pontos_estendidos[i + 2]
        for s in range(passos_por_segmento):
            t = s / float(passos_por_segmento)
            px, py = catmull_rom(p0, p1, p2, p3, t)
            caminho.append((px, py))
            
    # Raio da fita preta: 16 pixels = ~6.2 cm de largura na arena de 2 metros
    raio_linha = 16
    
    for cx, cy in caminho:
        ix = int(round(cx))
        iy = int(round(cy))
        for dy in range(-raio_linha, raio_linha + 1):
            py = iy + dy
            if 0 <= py < altura:
                row_offset = py * largura
                for dx in range(-raio_linha, raio_linha + 1):
                    px = ix + dx
                    if 0 <= px < largura:
                        if dx * dx + dy * dy <= raio_linha * raio_linha:
                            pixels[row_offset + px] = 0 # Preto

    dados_scanlines = bytearray()
    for y in range(altura):
        dados_scanlines.append(0)
        inicio = y * largura
        dados_scanlines.extend(pixels[inicio:inicio + largura])
        
    dados_comprimidos = zlib.compress(bytes(dados_scanlines), 9)
    
    def chunk(tag, data):
        comprimento = len(data)
        crc = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack(">I", comprimento) + tag + data + struct.pack(">I", crc)
    
    ihdr_data = struct.pack(">IIBBBBB", largura, altura, 8, 0, 0, 0, 0)
    
    with open(caminho_saida, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", ihdr_data))
        f.write(chunk(b"IDAT", dados_comprimidos))
        f.write(chunk(b"IEND", b""))
        
    print(f"[OK] Pista 2x2m com fita de 6cm gerada em: {caminho_saida}")

if __name__ == "__main__":
    criar_png_pista()
