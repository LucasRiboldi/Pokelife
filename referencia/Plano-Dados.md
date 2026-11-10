# Primeira entrega da camada de dados

A escolha A1 aprova começar pelo save local com SQLite e Dapper e instalar o SDK .NET 10 via WinGet.

1. Criar a solução C# com os projetos Core, Data e testes.
2. Testar a criação do banco e do save antes de escrever a implementação.
3. Carregar as tabelas e os dados iniciais da seção 6 do relatório. Rodar a inicialização novamente deve preservar o save.
4. Salvar o inicial escolhido e o estado da criatura em uma única transação. Validar os três iniciais, a reabertura do arquivo, a recusa de uma segunda gravação e a recuperação de falhas.
5. Compilar e rodar os testes. O recorte A1 termina com a escolha persistida e verificada por testes. A janela de seleção e o widget são entregas posteriores.

## Verificação

Abra o terminal na pasta `PokeLife` e rode:

```powershell
dotnet build TaskbarHabitat.sln -c Release
dotnet test TaskbarHabitat.sln -c Release
```

Os sete testes cobrem os dados iniciais, os três iniciais jogáveis, uma escolha inválida, uma falha de gravação e a reabertura do save no disco.

## Próxima escolha

- **A. Tela para escolher o Pokémon — recomendada.** Abra uma janela com os três iniciais. A escolha fica salva e a janela só aparece no primeiro uso. [WinUI 3](https://learn.microsoft.com/en-us/windows/apps/winui/winui3/)
- **B. Amostra na barra de tarefas.** Veja um Pokémon fixo na barra para verificar se o encaixe funciona no seu Windows. [Deskband11Lib.WinUI](https://www.nuget.org/packages/Deskband11Lib.WinUI/1.4.2)
