# PokeLife — ponto de retomada

Atualizado em 11/11/2026. Este arquivo registra o estado do protótipo e a ordem de continuidade.

## Produto e decisões preservadas

- Jogo de habitat em segundo plano no Windows, com uma janela de cenário no desktop.
- A barra de jogo embutida na barra de tarefas foi removida. O ícone normal da janela permanece.
- Escopo visual atual: um mapa e um Charmander. Manter a composição do mapa aprovado, as referências locais e a identidade da pose aprovada.
- O Pokémon deve caminhar respeitando água, árvores e obstáculos, com oclusão coerente ao passar atrás de objetos.
- Corpo e chama têm animações independentes. A chama fica acesa e conectada à ponta da cauda em todas as poses.

## Desenvolvimento salvo

- Seleção do inicial, persistência SQLite e janela de habitat existentes.
- Uma nova abertura restaura a janela existente. Minimizar pausa as animações. O X encerra o processo e a próxima abertura recupera o inicial salvo.
- Removidos o host embutido `MainWindow.cs`, sua recriação automática e a dependência `Deskband11Lib.WinUI`.
- O experimento local em `assets/charmander-v2/` contém 50 quadros de corpo, 12 de chama, atlas PNG, frames individuais, manifesto JSON e prévias WebP.
- Corpo: caminhada em quatro direções com oito quadros por direção; sentar com seis; deitar, respirar e levantar com quatro cada.
- Revisão mais recente: caminhada lateral usa uma base consistente; reparo de pequenos vazados internos; remoção de resíduos de fundo; encaixe calculado na cauda transformada; base do fogo fixa e ponta animada.
- O gerador do experimento permanece no workspace em `referencia/gerar-charmander-v2.py`.

**O pacote v2 não foi integrado ao aplicativo.** A execução atual continua usando a animação anterior. A pose-base foi aprovada. O usuário rejeitou os sprites e a animação da revisão v2, que ficam como referência de experimento.

## Evidências e limites

- A validação do experimento, em `assets/charmander-v2/validation.json`, registrou 50 corpos, 12 chamas, alpha binário e oito quadros distintos por caminhada.
- Todas as 600 combinações corpo/chama têm sobreposição, com mínimo de 17 pixels. Base da chama fixa, 12 formas de chama distintas e regressão de pequenos furos aprovada.
- Prévias locais do experimento em `assets/charmander-v2/walk-east-revisado.webp` e `assets/charmander-v2/qa-contrast.png`.
- Build Release com zero erros e avisos, 11 testes automatizados e [teste do ciclo da janela](tests/Test-WindowsLifecycle.ps1) em Windows 11 build 26200. O teste usa um save em `%TEMP%`, definido por `POKELIFE_SAVE_DIRECTORY` apenas nos processos que ele inicia.
- Frente e costas precisam de revisão de consistência com o perfil aprovado. A pose deitada usa reconstrução local. Não houve geração image-to-video.
- Medição local em 3840 × 2160, escala de 100%, com uma Radeon RX 7700 XT. Em amostras curtas, a CPU do processo registrou 171,5 ms/s visível, 125,0 ms/s sem foco, 0,0 ms/s minimizado e 101,9 ms/s após restaurar. O maior motor de GPU do processo, em média por amostra, registrou 0,77%, 0,67%, 0,00% e 0,52%. O conjunto de trabalho variou entre 176,0 e 219,7 MiB. Antes da correção, a abertura duplicava o processo e a CPU minimizada registrou 6,2 ms/s em uma amostra de cinco segundos.
- Pendentes os testes com Alt+Tab, suspensão, encerramento forçado, resolução menor, múltiplos monitores e escala fracionária.

## Retomar daqui

1. Ler o [plano mestre](referencia/Plano-Mestre-PokeLife.md), que reúne a revisão técnica e o cronograma.
2. Conferir `git status --short` antes de criar um checkpoint. Selecionar os arquivos da entrega e verificar a origem de novos recursos.
3. Repetir o teste da janela com `pwsh -File tests/Test-WindowsLifecycle.ps1` após compilar em Release. Completar a verificação manual nas condições pendentes.
4. Definir as regras de tempo ativo e offline. Implementar XP e persistência antes de retomar a produção de sprites. Na etapa visual, validar uma amostra pequena com o usuário.

O [guia de desenvolvimento](CONTRIBUTING.md) reúne os comandos e o [README](README.md) descreve o conteúdo da versão pública.
