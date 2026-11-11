# Habitat em janela grande

A opção B abre a Floresta de Viridian em uma janela grande após escolher o inicial ou carregar um save. Para reabrir a janela, clique no Pokémon da barra de tarefas e escolha **Abrir habitat**. O cenário mantém as proporções ao redimensionar ou maximizar a janela. [Como abrir o jogo](Plano-Tela-Inicial.md#abrir-no-windows) · [Janelas no Windows App SDK](https://learn.microsoft.com/en-us/windows/apps/develop/ui/windowing-overview)

A paisagem é original, em pixel art com vista de três quartos inspirada em Stardew Valley. O Pokémon percorre uma trilha fixa e pausa na entrada da caverna, perto do rio e no gramado.

## Verificação

A compilação Release passou sem avisos. Os sete testes automatizados passaram. No Windows 11 build 26200, conferi com Squirtle a abertura após a escolha, a maximização, a caminhada, as três pausas, a reabertura pelo widget e o carregamento do save.

## Próxima escolha

- **A. Ganhar XP com o tempo.** Fazer o Pokémon progredir sozinho e recuperar parte do XP ao reabrir o jogo. [Relógio testável do .NET](https://learn.microsoft.com/en-us/dotnet/standard/datetime/timeprovider-overview)
- **B. Dar mais vida à floresta.** Animar a água e dar ao Pokémon ações próprias na margem, na caverna e no gramado. [Temporizador do Windows App SDK](https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.ui.dispatching.dispatcherqueuetimer)
