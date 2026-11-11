# Pokémon na barra de tarefas

A opção A aprova testar o encaixe do inicial salvo na barra do Windows 11. O protótipo usa Deskband11Lib.WinUI e um sprite estático para cada inicial.

- Após escolher ou reabrir com um save existente, mostrar o sprite e o nome na barra.
- Usar arquivos da PokéAPI incluídos no aplicativo. O provedor de sprites fica na apresentação.
- Disponibilizar a ação **Fechar widget** ao clicar no Pokémon. Se o encaixe falhar, mostrar uma janela com o nome salvo.
- Compilar e verificar no Windows se o widget entra na barra, exibe a escolha persistida e sai ao fechar.

[Deskband11Lib](https://github.com/airtaxi/Deskband11Lib) · [Sprites da PokéAPI](https://github.com/PokeAPI/sprites/tree/master/sprites/pokemon/versions/generation-iii/emerald)

## Resultado

No Windows 11 build 26200, o widget apareceu dentro da barra após escolher Squirtle. O menu **Fechar widget** encerrou o processo. Ao reabrir, Squirtle apareceu na barra sem passar pela tela de escolha. A compilação Release passou sem avisos e os sete testes de dados passaram.

A versão atual usa Deskband11Lib.WinUI 1.5.0 e compila para Windows build 26100. A captura mostra o sprite estático. A recuperação após reiniciar o Explorer ainda precisa de validação.

[Como abrir o jogo](Plano-Tela-Inicial.md#abrir-no-windows)

## Próxima escolha

- **A. Ganhar XP com o tempo — recomendada.** Validar a evolução de nível e o cálculo do XP com o jogo fechado. [Relógio testável do .NET](https://learn.microsoft.com/en-us/dotnet/standard/datetime/timeprovider-overview)
- **B. Mostrar um habitat na barra.** Montar o cenário da Floresta de Viridian em volta do Pokémon. [Relatório do projeto](TaskbarHabitat-Relatorio.md)
