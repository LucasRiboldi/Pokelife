# Redesenho da Floresta de Viridian

A clareira ganha uma montanha com caverna, um riacho alto que cai em cascata e um rio que cruza o vale. A vista em três quartos separa a vegetação do fundo, o gramado e as árvores em primeiro plano. [Referência visual](Analise-PokeHabitat.md)

1. Desenhar o cenário em 384 × 216 pixels, com arte de fundo, quadros de água e árvores em primeiro plano. Manter a caverna, a margem e o gramado conectados pelo caminho.
2. Sobrepor os quadros de água ao fundo e avançar a corrente pelo relógio da janela, inclusive durante as pausas do Pokémon. Ajustar o circuito aos pontos do cenário.
3. Conferir o ciclo da água nos testes e verificar no Windows a escala, o percurso e as sobreposições.

## Resultado

O riacho corre pelo platô e cai ao lado da caverna. Oito quadros animam a corrente, a queda e a espuma. As árvores próximas são desenhadas sobre o Pokémon para dar profundidade à clareira. O circuito liga a entrada da caverna, a margem do rio e a parada de descanso no gramado. [Prévia das camadas do cenário](Viridian-Cachoeira.gif)

Os três arquivos de arte são incluídos na compilação. Para regerá-los, use `python referencia/gerar-viridian.py` com Pillow disponível. O jogo usa os PNGs prontos.

A compilação Release terminou sem avisos e os dez testes passaram. A checagem das imagens confirmou oito quadros distintos de água e os 19 trechos do circuito em terra. A janela abriu com o Charmander no Windows. A ferramenta de captura retornou erro do dispositivo gráfico, portanto a prévia foi composta com as próprias camadas do jogo.
