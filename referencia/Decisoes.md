# Escolhas para começar o Taskbar Habitat

A escolha **A1** foi aplicada. O SDK .NET 10.0.403 foi instalado via WinGet, e a pasta `PokeLife` tem seu próprio repositório Git. A camada de dados já cria o banco e grava o inicial. O plano e os comandos de verificação estão em [Plano-Dados.md](Plano-Dados.md).

## 1. O que você quer ver funcionando primeiro?

- **A. O jogo guarda sua escolha — recomendado.** Começamos pelo banco e testamos se o inicial escolhido fica salvo. O primeiro resultado é um teste automático, sem janela. A tela de escolha e a barra de tarefas vêm na sequência.
- **B. Algo aparece na barra de tarefas.** Começamos por uma amostra visual com conteúdo fixo. Você pode ver se ela encaixa na sua barra do Windows 11. Essa amostra ainda não guarda uma escolha.

As duas etapas fazem parte do projeto. A escolha define qual resultado validamos primeiro. Se escolher A, a recomendação técnica é Dapper, pois permite aproveitar as tabelas SQL já escritas no relatório. EF Core é uma alternativa que automatiza parte do trabalho com alterações de tabelas, com mais configuração inicial.

## 2. Onde prefere instalar o kit para compilar?

- **1. Instalação normal do Windows — recomendado.** O WinGet instala o SDK para usar no terminal em outros projetos também. Pode pedir autorização de administrador.
- **2. Instalação isolada no seu usuário.** Dispensa administrador. Vamos apontar os comandos do projeto para o local escolhido.

Se quiser seguir as duas recomendações, responda **A1**.

## Referências técnicas

- [.NET no Windows — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/install/windows)
- [Dapper](https://github.com/DapperLib/Dapper) e [EF Core com SQLite](https://learn.microsoft.com/ef/core/providers/sqlite/)
- [Deskband11Lib.WinUI no NuGet](https://www.nuget.org/packages/Deskband11Lib.WinUI/1.5.0). A versão 1.5.0 foi usada no [widget testado no Windows 11](Plano-Widget.md).
