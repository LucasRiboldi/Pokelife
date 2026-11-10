# Tela de escolha do inicial

A opção A aprova a janela com Bulbasaur, Charmander e Squirtle. A implementação usa WinUI 3 e reaproveita a gravação em SQLite.

1. Ler o nome do Pokémon escolhido no save existente.
2. Na primeira abertura, mostrar os três botões. Depois da gravação, mostrar o nome do inicial em uma janela de confirmação.
3. Ao reabrir, mostrar a confirmação diretamente. Se houver erro de gravação, manter a janela de escolha aberta.
4. Compilar, rodar os testes e verificar a primeira abertura e a reabertura no Windows.

O banco fica na pasta de dados locais do usuário. A janela de confirmação serve para esta etapa. A integração com a barra de tarefas terá uma etapa própria.

## Abrir no Windows

Na pasta `PokeLife`, rode:

```powershell
dotnet build TaskbarHabitat.sln -c Release
& './src/TaskbarHabitat.Widget/bin/Release/net10.0-windows10.0.26100.0/win-x64/TaskbarHabitat.Widget.exe'
```

A versão local é WinUI 3 x64, sem instalador, com o runtime do Windows App SDK incluído na saída da compilação. O save fica em `%LOCALAPPDATA%\TaskbarHabitat\save.db`. A versão atual abre o [widget na barra](Plano-Widget.md) após a escolha.

## Resultado da verificação

A compilação Release passou sem avisos e os sete testes de dados passaram. No Windows 11, a automação encontrou os três botões, escolheu Squirtle e confirmou que a segunda abertura mostra o mesmo inicial diretamente. A pasta com o save da verificação foi movida para uma pasta temporária, deixando a primeira abertura livre para a escolha do jogador.

## Próxima escolha

- **A. Ver o Pokémon na barra de tarefas — recomendada.** Verificar o encaixe no Windows 11 com o inicial salvo. [Deskband11Lib.WinUI](https://www.nuget.org/packages/Deskband11Lib.WinUI/1.4.2)
- **B. Fazer o Pokémon ganhar XP com o tempo.** Testar a progressão passiva e o cálculo do tempo com o jogo fechado. [Relatório do projeto](TaskbarHabitat-Relatorio.md#12-prompt-de-continuação-após-fase-1-concluída)
