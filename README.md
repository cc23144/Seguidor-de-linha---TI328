# 🤖 Robô Seguidor de Linha no Webots

Trabalho prático de simulação de um robô móvel seguidor de linha autônomo desenvolvido no simulador **Webots**, utilizando controle diferencial e sensores ópticos de refletância infravermelha sobre uma placa de teste de 2x2 metros.

---

## 👨‍🎓 Identificação do Aluno
* **Nome:** [SEU NOME COMPLETO AQUI]
* **RA:** [SEU RA AQUI]
* **Disciplina:** Robótica / Sistemas Embarcados
* **Simulador:** Webots
* **Linguagem:** Python 3

---

## 📁 Estrutura do Projeto

```text
├── worlds/
│   ├── pista_seguidor.wbt          # Mundo 3D no Webots com o tabuleiro 2x2m e o robô
│   └── textures/
│       └── pista_circuito.png      # Imagem do circuito da pista
├── controllers/
│   └── seguidor_linha/
│       └── seguidor_linha.py       # Controlador em Python do seguidor de linha
├── cliente_controle.py             # Script para teste de envio do comando via socket
├── gerar_pista.py                  # Script que desenha o circuito
└── README.md                       # Documentação do projeto
```

---

## ⚙️ Características do Projeto

* **Arena / Tabuleiro:** Placa de 2x2 metros (tamanho real padrão de bancada de laboratório de robótica) com acabamento lateral em moldura de madeira e piso claro.
* **Circuito:** Linha contínua preta (estilo fita isolante) de alto contraste sobre fundo branco, contendo retas e curvas suaves.
* **Robô Móvel:** Chassi em azul metálico com 4 rodas normais (duas traseiras tracionadas por motores independentes `motorE` e `motorD`, e duas dianteiras de apoio com rotação livre e direcionamento suave) e dois sensores ópticos infravermelhos frontais (`DSE` e `DSD`).
* **Lógica de Controle:**
  * Ambos os sensores na linha $\rightarrow$ Segue em frente em linha reta com velocidade estável.
  * Sensor esquerdo na linha $\rightarrow$ Curva para a esquerda (reduz roda interna, acelera externa).
  * Sensor direito na linha $\rightarrow$ Curva para a direita (acelera roda esquerda, reduz interna).
  * Perda momentânea de linha $\rightarrow$ Mecanismo de busca e autocentralização baseado na última direção vista (`ultima_direcao`).

---

## 🚀 Como Executar no Webots

1. Abra o **Webots**.
2. Clique em **File -> Open World...** e abra o arquivo `worlds/pista_seguidor.wbt`.
3. Clique no botão de **Play** no topo da janela.
4. O robô começará a seguir a linha pelo circuito da placa.

---

## 🎥 Como Gravar o Vídeo de Entrega

1. No Webots, clique no menu superior: **File -> Make Movie...** (ou `Ctrl + F10`).
2. Salve o arquivo com o nome `video_funcionamento.mp4`.
3. Deixe o robô dar uma volta completa na pista.
4. Clique no botão vermelho de parar no topo para finalizar o vídeo.
