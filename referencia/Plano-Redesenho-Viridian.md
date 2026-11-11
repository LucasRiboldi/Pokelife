# Redesenho da Floresta de Viridian

Este documento registra o cenário anterior. A janela atual usa o [mapa ampliado com navegação](Plano-Navegacao-Habitat.md), que reaproveita peças desse trabalho.

O vale mede 512 × 288 pixels. A câmera fixa enquadra 342 × 192 pixels, o que aproxima a cena em cerca de 50%. A vista de cima com fachadas frontais segue a perspectiva de Pokémon Gold. As copas irregulares e as raízes aparentes seguem o estudo visual do PokeHabitat. O Charmander atravessa a clareira de grama e flores para visitar a casa, a caverna, o rio e a frutífera central, onde descansa. [Estudo visual](Analise-PokeHabitat.md)

O terreno mantém o relevo e as margens. A água usa oito quadros para animar a corrente, a queda e a espuma. Casa, pedras, troncos caídos, troncos de árvores, copas, frutas, grama, flores e arbustos usam PNGs separados. A vegetação tem quatro quadros de vento, com ritmos e fases diferentes para distribuir o movimento. Pedras e madeira ficam firmes.

O catálogo [layout.json](../src/TaskbarHabitat.Widget/Assets/Habitats/Viridian/layout.json) define o enquadramento e a posição de cada objeto. As copas e os frutos se sobrepõem ao Charmander quando ele passa atrás da árvore. Para regerar a arte, rode `python referencia/gerar-viridian.py` com Pillow. A compilação usa os PNGs e o catálogo prontos.
