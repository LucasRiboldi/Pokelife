# PokeLife — plano mestre

Revisão de engenharia em 11/11/2026. Este é o ponto de entrada para decidir o que fazer a seguir. O [relatório original](TaskbarHabitat-Relatorio.md) preserva as ideias e os detalhes técnicos. A ordem de execução passa a ser a deste documento.

## 1. O que estamos construindo

PokeLife é um companheiro de desktop para Windows. A pessoa abre uma janela ampla e encontra uma criatura vivendo em um habitat 2D. Ela pode observar ou voltar a outra atividade enquanto o progresso continua. Cuidar da criatura é opcional. Ao reabrir o jogo, o progresso deve ser recuperável e previsível.

- **Primeira entrega:** abrir, minimizar, restaurar, fechar e reabrir com comportamento definido, usando a cena provisória e um save de teste.
- **Primeira versão jogável:** uma Floresta de Viridian, Charmander como personagem de referência, caminhada e descanso, progresso passivo e offline e uma primeira evolução funcional no nível 16. A seleção dos três iniciais já existe. Arte e animação completas dos outros iniciais ficam fora da primeira entrega.
- **Depois:** alimentação, brincadeiras, dia/noite e cenário vivo entram em entregas próprias. Novos habitats, captura, visitantes, shiny e clima dinâmico ficam para depois da primeira versão.

## 2. O que o projeto já tem

| Área | Confirmado na revisão | Lacuna |
|---|---|---|
| Janela | `Program.cs` encaminha novas aberturas à instância existente. `App.xaml.cs` abre a seleção ou o habitat e restaura a janela minimizada. O ícone normal permanece. | A abertura repetida foi testada com o executável. Atalho, Alt+Tab, múltiplos monitores e escalas fracionárias ainda precisam de teste. |
| Tempo | `HabitatWindow.cs` usa um temporizador de 40 ms para a cena. O temporizador para ao minimizar ou fechar. A restauração retoma a animação a partir do tempo visual acumulado. | A simulação persistente e a contagem de tempo ativo fazem parte da etapa 2. |
| Dados | `SaveService` cria o save e lê o inicial. SQLite já armazena campos de XP, nível e tempo. | Carregar e atualizar o estado completo, recuperar tempo offline e evitar crédito duplicado. |
| Visual | O habitat carrega Viridian Ampliada e usa navegação por grade. `ISpriteProvider` carrega a arte anterior. | A animação v2 ficou fora do aplicativo e foi rejeitada pelo usuário. O próximo piloto visual parte da pose-base aprovada e das referências locais. |

Base revisada com SDK .NET 10.0.403, WinUI 3 e Windows App SDK 2.6.5, alvo Windows x64. A compilação Release passou com zero avisos e erros. Os 11 testes existentes passaram. O teste da janela e as medições locais estão no [registro do projeto](../STATE.md).

## 3. Comportamento proposto no Windows

| Quando | Comportamento esperado |
|---|---|
| Abrir pelo atalho | Mostrar uma janela normal, sem ficar por cima dos outros programas. Se já estiver aberto, restaurar a janela existente. |
| Trocar de programa | O jogo permanece aberto. O progresso independe do foco da janela. |
| Minimizar | Suspender a atualização da cena e continuar contando o tempo ativo. Restaurar sem reproduzir todos os quadros perdidos. |
| Fechar pelo X | Gravar o estado, encerrar o processo e contabilizar o intervalo como offline na próxima abertura. |
| Suspender ou desligar o PC | Recuperar o estado salvo e calcular o intervalo na retomada. Proposta: tratar suspensão como offline. |
| Encerrar pelo Gerenciador de Tarefas ou faltar energia | Recuperar o último estado gravado. Uma gravação periódica limita a perda quando não há fechamento normal. |

**Decisão da primeira entrega.** Usar a janela normal do Windows, com acesso pela barra de tarefas e pelo Alt+Tab. O X encerra o aplicativo. A barra de jogo embutida foi removida.

O protótipo usa um processo de desktop na sessão do usuário. O `AppInstance` encaminha novas aberturas antes da inicialização do WinUI e do save. A etapa de progressão deve testar execução em segundo plano e suspensão do computador separadamente. [Microsoft Learn — ciclo de vida](https://learn.microsoft.com/en-us/windows/apps/develop/launch/app-lifecycle) · [Microsoft Learn — instância única](https://learn.microsoft.com/en-us/windows/apps/develop/launch/multi-instance-apps)

## 4. Estrutura recomendada

Manter .NET, WinUI e SQLite e ajustar a divisão do código atual. Isso reaproveita a janela, o save e os testes. A alternativa é mover a cena para um motor 2D. Ela traz ferramentas próprias de edição e animação, mas exige revalidar janela, distribuição, leitura de saves e integração no Windows. Só vale comparar um protótipo em outro motor se um teste local revelar um requisito que a base atual não atende com custo razoável.

| Onde | Responsabilidade |
|---|---|
| `src/TaskbarHabitat.Core/` | Regras testáveis sem janela: tempo, XP, nível e evolução. Hoje contém o modelo `SaveState`. |
| `src/TaskbarHabitat.Data/` | Leitura, gravação transacional e migração do SQLite. Preservar saves existentes e o caminho `%LOCALAPPDATA%\TaskbarHabitat\save.db`. |
| `src/TaskbarHabitat.Widget/` | Entrada do aplicativo, janela, eventos do Windows, cena, navegação e reprodução de sprites. A janela mostra o estado calculado pelo jogo. |
| `tests/` | Testes automatizados das regras e dos dados. Eventos de janela, suspensão e escalas do Windows também exigem verificação manual. |
| `referencia/`, `assets/` e `Widget/Assets/` | Referências e decisões, pacotes de arte em produção e recursos consumidos pelo aplicativo, respectivamente. Os assets do aplicativo ficam dentro de `src/TaskbarHabitat.Widget/`. |

O relógio de jogo deve produzir o mesmo resultado com o mesmo save e o mesmo intervalo. Proposta inicial: tempo ativo integral, offline a 50% até 24 horas e intervalo negativo valendo zero. Salvar XP, nível e marco de tempo juntos evita reaplicar o mesmo intervalo quando o app reabre. A meta original de sete dias é aproximada: 99.000 XP a 590 XP/h equivalem a cerca de 167 h e 48 min. Validar essa regra e o tratamento da suspensão antes de implementar. [Relatório de progressão](TaskbarHabitat-Relatorio.md)

## 5. Cronograma por entregas

Estimativa inicial para uma pessoa, em dias úteis de trabalho. A contagem começa após confirmar as decisões de cada etapa. Pausas de aprovação e produção completa de arte ficam fora da estimativa do piloto.

| Etapa | Esforço | Entrega e critério para avançar |
|---|---:|---|
| 1. Estrutura e Windows | 2–3 dias | Registrar o comportamento atual, testar instância única e validar abrir, minimizar, restaurar, fechar e reabrir com a cena provisória. |
| 2. Tempo, save e progressão | 3–5 dias | Atualizar um save existente, validar recuperação e aplicar a primeira evolução com representação provisória. Abrir duas vezes no mesmo instante não duplica XP. |
| 3. Piloto visual no habitat | 2–4 dias | Testar uma pose sentada e um ciclo lateral com a chama independente. Avaliar na escala do jogo, incluindo oclusão e nitidez. Aprovar o piloto antes de encomendar os demais quadros. |
| 4. Completar o visual e preparar entrega | Reestimar após o piloto | Expandir para quatro direções e poses restantes, testar colisão e oclusão no mapa e verificar execução em outro Windows compatível. |

Previsão até o piloto visual: **7–12 dias úteis**. Revisar a estimativa após a primeira etapa. Ao fechar cada entrega, registrar comandos, resultados e decisões em [STATE.md](../STATE.md) e separar as alterações em um checkpoint Git revisável.

## 6. Primeira tarefa — validar a janela atual

- [x] Manter o ícone normal e encerrar pelo X, conforme a decisão da primeira entrega.
- [x] Registrar build, testes e versão do Windows. Validar com save descartável as novas aberturas durante a seleção e no habitat, minimizar, restaurar, fechar e reabrir com o inicial salvo.
- [x] Registrar amostras de CPU, GPU e memória com a janela visível, sem foco e minimizada em [STATE.md](../STATE.md).
- [ ] Verificar atalho, Alt+Tab, suspensão, encerramento forçado, resolução menor, múltiplos monitores e escala de 125% ou 150%.

## 7. Perguntas que orientam a próxima pesquisa

1. **Como a pessoa reencontra o jogo?** Comparar janela padrão e janela oculta pelo efeito real em barra de tarefas, Alt+Tab e reabertura. Decidir antes de pesquisar transparência, janela sempre no topo ou cliques atravessando a janela.
2. **Quanto tempo deve contar?** Testar intervalos visível, minimizado, fechado e suspenso. Incluir relógio voltando, salto longo, duas reaberturas e atualização interrompida. Definir a regra antes de escolher temporizadores.
3. **A arte funciona dentro do habitat?** Usar o [mapa-base](MAPA%20FINAL%201.png) e a pose aprovada no workspace como referências. Comparar desenho manual em editor externo e geração assistida pelo mesmo piloto. Verificar pés alinhados, pixels nítidos, fundo transparente sem vazados e chama conectada. Só ampliar a produção após revisão do usuário.
4. **Outra pessoa consegue continuar?** Validar um checkout e um build limpos, identificar a origem dos assets distribuídos e documentar como executar com um save de teste. Conferir os arquivos antes de publicar uma entrega.
