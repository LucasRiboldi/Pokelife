# Animação do Charmander

Primeiro recorte da [análise dos vídeos](Analise-PokeHabitat.md). Na Floresta de Viridian, o Charmander caminha até os destinos do circuito atual. No gramado, ele senta, deita, respira, acorda e volta a caminhar.

1. Criar poses em pixel art com o mesmo ponto de contato com o chão. Usar quatro quadros de caminhada para cada vista desenhada. Usar o perfil espelhado para o outro lado.
2. Selecionar o quadro de caminhada pelo deslocamento e a pose de descanso pelo tempo decorrido no gramado. Manter a janela e o percurso existentes.
3. Verificar a ordem das poses e a retomada em teste automatizado. Compilar em Release e abrir o habitat no Windows para conferir o encaixe da arte e a transição entre poses.

## Resultado

A folha contém 20 poses em células de 32 × 32 pixels. A caminhada tem três vistas desenhadas e usa o perfil espelhado quando o Pokémon muda de lado. A pausa na região do gramado dura cerca de cinco segundos. O Charmander se abaixa, senta, deita, alterna duas poses de respiração, ergue o corpo e retoma o circuito. [Prévia animada do sprite](Charmander-Animacao.gif)

A compilação Release terminou sem avisos. Os nove testes passaram. No Windows, a escolha do Charmander abriu a floresta. A reabertura carregou o inicial salvo e permitiu observar a caminhada, a pausa com as poses sentada e deitada e o retorno ao percurso. A animação desta etapa cobre o Charmander na janela grande.
