# Animação do Charmander

## Atualização de 11/11/2026

O experimento v2 do workspace contém 50 quadros de corpo e 12 de chama independente. A revisão corrigiu vazados, mudanças bruscas na caminhada lateral e o encaixe do fogo. O protótipo público usa a folha anterior. Consulte o [estado atual](../STATE.md) e o [plano mestre](Plano-Mestre-PokeLife.md).

## Histórico da animação anterior

Este documento registra a folha usada na janela do habitat. O [plano mestre](Plano-Mestre-PokeLife.md) descreve a próxima etapa de animação.

Primeiro recorte da [análise dos vídeos](Analise-PokeHabitat.md). Na Floresta de Viridian, o Charmander caminha pelo circuito da casa, da caverna e do rio. Sob a frutífera central, ele senta, deita, respira, acorda e volta a caminhar.

1. Criar poses em pixel art com o mesmo ponto de contato com o chão. Usar quatro quadros de caminhada para cada vista desenhada. Usar o perfil espelhado para o outro lado.
2. Selecionar o quadro de caminhada pelo deslocamento e a pose de descanso pelo tempo decorrido sob a frutífera.
3. Verificar a ordem das poses e a retomada em teste automatizado. Compilar em Release e abrir o habitat no Windows para conferir o encaixe da arte e a transição entre poses.

## Resultado

A folha contém 20 poses desenhadas em células de 32 × 32 pixels e exportadas com escala inteira de 3×. A caminhada tem três vistas e usa o perfil espelhado quando o Pokémon muda de lado. A pausa dura cerca de cinco segundos. O Charmander se abaixa, senta, deita, alterna duas poses de respiração, ergue o corpo e retoma o circuito. [Atlas do protótipo](../src/TaskbarHabitat.Widget/Assets/Sprites/charmander-habitat.png)
