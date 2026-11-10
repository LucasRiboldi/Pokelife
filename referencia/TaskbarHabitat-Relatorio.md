# Taskbar Habitat — Relatório consolidado

> Referência do projeto, reunindo a mensagem original e o anexo. Os comandos e prompts abaixo fazem parte do relatório. Para o levantamento atual e as escolhas pendentes, veja [Decisões](Decisoes.md).

## 1. Visão do produto

Taskbar Habitat é o nome provisório de um widget para Windows com um habitat 2D em pixel art na barra de tarefas. A criatura vive e ganha experiência sozinha. Alimentar e brincar são cuidados opcionais que aceleram a evolução.

A proposta é criação e evolução por vínculo ou condições, sem combate automático. O plano futuro prevê até seis habitats simultâneos, com ciclo de dia e noite, clima e estações. O protótipo pessoal usa Pokémon e PokéAPI. A interface `ISpriteProvider` permite trocar os sprites por assets originais no futuro.

## 2. Escopo do MVP

- Um habitat, a Floresta de Viridian (`viridian-forest`), e uma criatura ativa.
- Escolha entre Bulbasaur (1), Charmander (4) e Squirtle (7). O banco inicial contém as nove espécies das três famílias.
- Progressão passiva até o nível 100 em cerca de sete dias e primeira evolução no nível 16.
- Alimentar, brincar e consultar status. Ciclo de dia e noite, escala de tempo ajustável em modo de desenvolvimento e clima fixo ensolarado.
- Save local em SQLite e cálculo offline determinístico.
- Ficam para depois outros habitats e regiões, captura, Pokédex completa, conquistas, ovos, clima variável, visitantes, shiny e assets originais.

## 3. Progressão e balanceamento

### 3.1 Meta de XP

| Parâmetro | Valor |
|---|---:|
| Nível 100 passivo | 7 dias (168 horas) |
| XP passivo | 590 XP/h |
| XP total até o nível 100 | 99.000 XP |
| XP passivo por dia | 14.160 XP |
| Meta com jogador ativo | Cerca de 5–5,5 dias |
| Teto diário de XP ativo | 5.000 XP |
| App fechado | 50% do XP passivo, com teto de 24 h |

### 3.2 Curva de XP

XP_next(L) = 900 + 2L



Soma até o level 100:

∑(L=1..99) (900 + 2L) = 99.000 XP



Curva **linear** (não exponencial) é escolha consciente para manter o ritmo passivo previsível e evitar level-ups muito rápidos no começo.

### 3.3 Ações do jogador

| Ação | XP imediato | Bônus | Cooldown |
|---|---:|---|---:|
| Alimentar | +250 | +10% XP passivo por 30 min | 1 h |
| Brincar | +400 | +15% XP passivo por 45 min | 2 h |
| Treinar (pós-MVP) | +700 | +20% XP passivo por 1 h | 4 h |
| Arrumar habitat (pós-MVP) | +300 | Progresso de condição especial | 6 h |

### 3.4 Evolução

- **Nível** sobe sempre com XP, inclusive passivamente.
- **Forma** depende de nível + condições.
- Passivo garante **forma padrão**; jogador desbloqueia **formas especiais**.
- Para os iniciais de Kanto, condições mínimas:
  - Bulbasaur → Ivysaur: nível 16
  - Ivysaur → Venusaur: nível 32
  - Charmander → Charmeleon: nível 16
  - Charmeleon → Charizard: nível 36
  - Squirtle → Wartortle: nível 16
  - Wartortle → Blastoise: nível 36

### 3.5 Simulação offline

- **Widget ativo:** 100% do XP passivo.
- **App fechado/PC desligado:** 50% do XP passivo, com teto de 24 h.
- **Relógio alterado para trás:** ignorar delta.
- **Salto muito grande para frente:** limitar a 24 h.
- **Determinismo:** `seed` baseado em `last_seen_utc` + `save_id`.
- **Tick mínimo:** 15 minutos in-game.

---

## 4. Decisões de Tempo, Clima, Estações e Visitantes

### 4.1 Relógio in-game

| Parâmetro | Valor |
|---|---:|
| Dia in-game | 24 min reais (padrão) |
| Tick mínimo | 15 min in-game |
| Escalas dev | 1×, 10×, 60×, 360× |
| Base temporal | `game_epoch_utc + elapsed_ticks × tick_duration` |

Modo dev (`#if DEBUG`) permite: forçar estação, forçar clima, avançar N dias/estações manualmente.

### 4.2 Estações (hemisfério sul — Porto Alegre/RS)

| Estação | Início aproximado |
|---|---|
| **Verão** | 21–22 de dezembro |
| **Outono** | 20–21 de março |
| **Inverno** | 20–21 de junho |
| **Primavera** | 22–23 de setembro |

Clima de Porto Alegre: **subtropical úmido (Cfa)**, chuva bem distribuída ao longo do ano. Parâmetros do INMET (normal 1991–2020):

| Estação | Temp. média | Mín. média | Máx. média | Chuva mensal |
|---|---:|---:|---:|---:|
| Verão (Jan–Fev) | 24,7–25,0 °C | 20,7 °C | 30,5–31,0 °C | ~110–121 mm |
| Outono (Abr–Mai) | 17,2–20,7 °C | 13,6–16,8 °C | 22,6–26,4 °C | ~113–114 mm |
| Inverno (Jul–Ago) | 14,1–15,7 °C | 10,4–11,6 °C | 19,7–21,8 °C | ~120–164 mm |
| Primavera (Out–Nov) | 19,7–21,7 °C | 15,7–17,2 °C | 25,2–27,7 °C | ~105–153 mm |

### 4.3 Clima (pós-MVP)

Cadeia de **Markov por estação**, 7 estados:
`Ensolarado`, `ParcialmenteNublado`, `Nublado`, `ChuvaLeve`, `ChuvaForte`, `Tempestade`, `Neblina`.

Efeitos no habitat:
| Clima | Efeito visual | Efeito mecânico |
|---|---|---|
| Ensolarado | Céu claro, sombras fortes | +10% energia; visitantes diurnos mais prováveis |
| Chuva leve | Gotas, poças | +20% aparição Água/Inseto; -5% energia |
| Tempestade | Raios, vento | Visitantes Elétrico/Voador; risco de assustar |
| Neblina | Tela esbranquiçada | Visibilidade reduzida; aparições Fantasma/Gelo |
| Nublado | Céu cinza | Neutro; pequeno bônus de descanso |

### 4.4 Visitantes (pós-MVP)

**Regras de elegibilidade (todas devem ser verdadeiras):**
1. `evolution_stage == 1` (primeira forma)
2. `rarity_tier` ∈ {common, uncommon} (nunca legendary/mythical)
3. Habitat compatível (espécie aparece naquela área na PokéAPI)
4. Horário in-game e clima atual dentro das condições de aparição
5. Cooldown: não apareceu nos últimos N dias in-game

**Janela de visita:** 30–90 min in-game (2–6 min reais na escala padrão).
**Frequência:** 1–3 visitantes por dia in-game.
**Correlação:** habitat de floresta atrai Planta/Inseto; aquático atrai Água. Inverno favorece Gelo; verão favorece Fogo/Elétrico.

### 4.5 Shiny (pós-MVP)

- Taxa base: **1/4096** por visita (âncora clássica da franquia)
- Bônus opcional: +1 reroll a cada 100 h de habitat ativo (máx. 3 rerolls → ~1/1365 no limite)
- **Shiny não despawna** ao fim da janela de visita (permanece até captura ou 24 h in-game)

---

## 5. Arquitetura Técnica

Três camadas separadas, com a simulação determinística como núcleo.

```text
┌─────────────────────────────────────────────────────┐
│ Apresentação — WinUI 3 + Deskband11Lib.WinUI │
│ Renderização — MonoGame ou SkiaSharp │
└────────────────────┬────────────────────────────────┘
│
┌────────────────────▼────────────────────────────────┐
│ Simulação — C# .NET 10 Class Library │
│ IdleEngine · GameClock · WeatherSystem │
│ ProgressionSystem · EvolutionSystem │
│ EncounterSystem · VisitorSpawnSystem │
└────────────────────┬────────────────────────────────┘
│
┌────────────────────▼────────────────────────────────┐
│ Dados — SQLite (Pokédex + save) │
│ Populado offline a partir da PokéAPI │
└─────────────────────────────────────────────────────┘
```


### 5.1 Decisões arquiteturais críticas

1. **Simulação determinística:** `IdleEngine` avança em ticks fixos; `seed` baseado em `last_seen_utc` + `save_id`; o mesmo período offline gera os mesmos eventos.
2. **Separação de assets:** `ISpriteProvider` injetável. Protótipo usa sprites da PokéAPI/Showdown; versão pública troca por assets originais sem tocar na lógica.
3. **Camada `Data` isolada:** não referencia `Widget` nem `Rendering`. `IdleEngine` recebe repositórios por injeção de dependência; testes usam SQLite `:memory:`.
4. **Curva linear de XP:** escolha consciente para ritmo passivo previsível.
5. **Modo dev fora do build de produção:** `#if DEBUG`.

### 5.2 Stack e pacotes

| Camada | Tecnologia / Pacote | Observação |
|---|---|---|
| **Widget na taskbar** | **`Deskband11Lib.WinUI`** (NuGet) | Facade WinUI 3 para hospedar conteúdo na barra de tarefas do Windows 11. Lida com `SetParent`, layout, reinício do Explorer e sobreposição com botões do sistema. |
| **UI framework** | **WinUI 3** (Windows App SDK) | Nativo, com suporte a NativeAOT. |
| **Renderização 2D** | **MonoGame** (preferido) ou **SkiaSharp** | MonoGame é maduro para pixel art; SkiaSharp é alternativa mais leve. |
| **Lógica de jogo** | **C# .NET 10**, biblioteca separada | Testável sem UI. |
| **Banco local** | **SQLite** + **Dapper** (ou EF Core) | Leve, embutido. |
| **Aquisição de dados** | **PokéAPI CLI** (`pokeapi-pp-cli`) + skill `pp-pokeapi` | Sincroniza dataset para SQLite local. Alternativa: `PokeApiSharp`. |
| **Testes** | **xUnit** | Para simulação determinística. |
| **Assets de protótipo** | Sprites da PokéAPI/Showdown (uso local) | Substituir via `ISpriteProvider` na versão pública. `hypercutter` (opcional) extrai sprites de ROMs GBA. |

---

## 6. Schema SQLite

```sql
CREATE TABLE species (
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    display_name    TEXT NOT NULL,
    region          TEXT NOT NULL DEFAULT 'kanto',
    type1           TEXT NOT NULL,
    type2           TEXT,
    evolution_stage INTEGER NOT NULL DEFAULT 1,
    evolves_from    INTEGER REFERENCES species(id),
    is_legendary    INTEGER NOT NULL DEFAULT 0,
    is_mythical     INTEGER NOT NULL DEFAULT 0,
    rarity_tier     TEXT NOT NULL DEFAULT 'common'
);

CREATE TABLE evolutions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    from_species_id INTEGER NOT NULL REFERENCES species(id),
    to_species_id   INTEGER NOT NULL REFERENCES species(id),
    trigger         TEXT NOT NULL DEFAULT 'level-up',
    min_level       INTEGER,
    condition_note  TEXT,
    UNIQUE(from_species_id, to_species_id)
);

CREATE TABLE habitats (
    id              TEXT PRIMARY KEY,
    display_name    TEXT NOT NULL,
    region          TEXT NOT NULL DEFAULT 'kanto',
    description     TEXT
);

CREATE TABLE encounters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    habitat_id      TEXT NOT NULL REFERENCES habitats(id),
    species_id      INTEGER NOT NULL REFERENCES species(id),
    method          TEXT NOT NULL DEFAULT 'walk',
    chance          INTEGER NOT NULL CHECK (chance BETWEEN 0 AND 100),
    time_window     TEXT,
    weather         TEXT,
    UNIQUE(habitat_id, species_id, method)
);

CREATE TABLE save_state (
    id              INTEGER PRIMARY KEY CHECK (id = 1),
    starter_id      INTEGER NOT NULL REFERENCES species(id),
    xp              INTEGER NOT NULL DEFAULT 0,
    level           INTEGER NOT NULL DEFAULT 1,
    last_seen_utc   TEXT NOT NULL,
    game_epoch_utc  TEXT NOT NULL,
    total_ticks     INTEGER NOT NULL DEFAULT 0,
    save_id         TEXT NOT NULL,
    created_at_utc  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE creature_state (
    save_id         INTEGER PRIMARY KEY REFERENCES save_state(id),
    hunger          REAL NOT NULL DEFAULT 0.0,
    energy          REAL NOT NULL DEFAULT 100.0,
    happiness       REAL NOT NULL DEFAULT 50.0,
    last_updated_utc TEXT NOT NULL
);

```

### 6.1 Seed dos iniciais de Kanto
```sql

INSERT INTO species (id, name, display_name, type1, type2, evolution_stage, evolves_from, rarity_tier) VALUES
(1, 'bulbasaur', 'Bulbasaur', 'grass', 'poison', 1, NULL, 'common'),
(2, 'ivysaur', 'Ivysaur', 'grass', 'poison', 2, 1, 'common'),
(3, 'venusaur', 'Venusaur', 'grass', 'poison', 3, 2, 'common'),
(4, 'charmander', 'Charmander', 'fire', NULL, 1, NULL, 'common'),
(5, 'charmeleon', 'Charmeleon', 'fire', NULL, 2, 4, 'common'),
(6, 'charizard', 'Charizard', 'fire', 'flying', 3, 5, 'common'),
(7, 'squirtle', 'Squirtle', 'water', NULL, 1, NULL, 'common'),
(8, 'wartortle', 'Wartortle', 'water', NULL, 2, 7, 'common'),
(9, 'blastoise', 'Blastoise', 'water', NULL, 3, 8, 'common');

INSERT INTO evolutions (from_species_id, to_species_id, trigger, min_level) VALUES
(1, 2, 'level-up', 16), (2, 3, 'level-up', 32),
(4, 5, 'level-up', 16), (5, 6, 'level-up', 36),
(7, 8, 'level-up', 16), (8, 9, 'level-up', 36);

INSERT INTO habitats (id, display_name, region, description) VALUES
('viridian-forest', 'Floresta de Viridian', 'kanto', 'Uma floresta densa e úmida ao oeste de Viridian City.');

INSERT INTO encounters (habitat_id, species_id, method, chance) VALUES
('viridian-forest', 1, 'walk', 15),
('viridian-forest', 4, 'walk', 15),
('viridian-forest', 7, 'walk', 15);

```

## 7. Estrutura da Solução
```text

TaskbarHabitat.sln
├── src/
│   ├── TaskbarHabitat.Core/              # Modelos de domínio (Species, SaveState, GameClock)
│   ├── TaskbarHabitat.Data/              # SQLite: DbContext, repositórios, migrações
│   │   ├── Migrations/
│   │   ├── Repositories/
│   │   └── Seed/
│   │       └── KantoSeedData.cs
│   ├── TaskbarHabitat.Simulation/        # IdleEngine, ProgressionSystem, EvolutionSystem
│   ├── TaskbarHabitat.Widget/            # WinUI 3 + Deskband11Lib
│   │   ├── Views/
│   │   │   ├── StarterSelectionWindow.xaml
│   │   │   └── HabitatView.xaml
│   │   └── App.xaml.cs
│   └── TaskbarHabitat.Rendering/         # MonoGame/SkiaSharp
└── tests/
    └── TaskbarHabitat.Simulation.Tests/

Regra de dependência: Data não referencia Widget nem Rendering. Simulation referencia apenas Core e interfaces de repositório. Widget referencia Simulation, Data, Rendering.
```

## 8. Ambiente do Codex — Instalação de Ferramentas

Execute estes comandos antes de iniciar o desenvolvimento.
### 8.1 Marketplace oficial .NET (dotnet/skills)
```powershell

```
codex plugin marketplace add dotnet/skills

Depois, dentro do Codex, use /plugins para instalar:

    dotnet-ai — workflows de MCP server em C# com SDK oficial

    dotnet-data — Entity Framework e acesso a dados

    dotnet-test — execução de testes e workflows MSTest/xUnit

### 8.2 GliderMCP — navegação e refatoração C#
```powershell

codex plugin marketplace add glidermcp/glidermcp
```
codex plugin add glidermcp@glidermcp

Requer .NET 10 SDK e acesso ao NuGet. Fornece análise semântica com Roslyn, navegação, refatoração e GliderTrace para execução e evidências de runtime.
### 8.3 PokéAPI CLI + skill pp-pokeapi
```powershell

```
npx -y @mvanhorn/printing-press-library install pokeapi --agent codex

Sincroniza todo o dataset da PokéAPI para um SQLite local com busca full-text, type math e SQL passthrough. A skill é instalada automaticamente para o Codex.
### 8.4 Ferramentas opcionais

    NugetMcpServer — inspeção de metadados de pacotes NuGet (Deskband11Lib, MonoGame, Dapper) antes de gerar código dependente.

    hypercutter — extração de sprites de ROMs GBA em PNG (incluindo shiny) para protótipo local.

## 9. Estado Atual do Desenvolvimento
### 9.1 Concluído (planejamento)

    ✅ Visão do produto e escopo do MVP

    ✅ Decisões de progressão (curva de XP, teto diário, offline)

    ✅ Especificação de tempo, estações, clima, visitantes e shiny

    ✅ Arquitetura em três camadas

    ✅ Stack tecnológica

    ✅ Schema SQLite completo

    ✅ Seed dos 9 primeiros registros de Kanto

    ✅ Estrutura da solução

    ✅ Ferramentas do Codex verificadas

    ✅ Fluxo de seleção do inicial (design)

### 9.2 Não iniciado (implementação)

    ❌ Solução .NET criada e compilando

    ❌ Camada Data implementada

    ❌ GameClock implementado

    ❌ IdleEngine implementado

    ❌ ProgressionSystem implementado

    ❌ Janela de seleção do inicial implementada

    ❌ Widget anexado à taskbar

    ❌ Teste de 7 dias passando

### 9.3 Próximo passo imediato

Implementar a camada de dados (schema + seed + SaveService) e a tela de seleção do inicial, conforme o prompt de continuação na seção 11.
## 10. Cronograma de Fases
Fase	Duração	Entregável
Fase 0 — PoC do widget	1–2 semanas	Janela WinUI 3 na taskbar com sprite estático
Fase 1 — Camada de dados	1 semana	SQLite com schema + seed + SaveService
Fase 2 — Motor de simulação	2–3 semanas	IdleEngine, GameClock, ProgressionSystem testados
Fase 3 — Loop de jogo no widget	3–4 semanas	Habitat com sprite animado, menu de contexto, diário offline
Fase 4 — Evolução e primeiro marco	1–2 semanas	Evolução no nível 16; teste de 7 dias passando
Fase 5 — Captura, Pokédex, achievements	2–3 semanas	Loop completo de captura e progressão regional
Fase 6 — Clima, estações, visitantes, shiny	2–3 semanas	Cadeia de Markov, spawns, raridade
Fase 7 — Expansão regional	contínuo	Johto, Hoenn etc. como pacotes de conteúdo

MVP jogável: Fases 0–4 (8–12 semanas).
## 11. Prompt de Inicialização para o Codex

Execute o bloco abaixo como primeira mensagem no Codex, após instalar as ferramentas da seção 8.


Você é o engenheiro responsável pelo projeto “Taskbar Habitat”, um widget de Windows na barra de tarefas onde uma criatura estilo Pokémon vive em um habitat 2D em pixel art, progride passivamente até o level 100 em ~7 dias, e o jogador pode acelerar o desenvolvimento com ações opcionais de cuidado.

Leia o relatório consolidado (TaskbarHabitat-Relatorio.md) que segue com esta mensagem. Ele contém todas as decisões de produto, arquitetura, stack, schema SQLite e ferramentas que você deve usar.

## Objetivo desta sessão
Criar o esqueleto funcional do projeto com escopo mínimo, mas com arquitetura que permita crescer sem refatoração. O foco é validar o loop central: uma criatura inicial de Kanto (Bulbasaur, Charmander ou Squirtle) escolhida pelo jogador, vivendo em um único habitat, ganhando XP passivo, com relógio in-game e clima básico.

## Stack obrigatória
- Solução .NET 10 em C#.
- Projeto de UI: WinUI 3 com `Deskband11Lib.WinUI` para hospedar a janela na barra de tarefas.
- Projeto de simulação: biblioteca de classes separada, sem dependência de UI.
- Projeto de dados: SQLite local, populado com os dados mínimos de Kanto (9 espécies dos 3 iniciais).
- Renderização: MonoGame (preferido) ou SkiaSharp, dentro da janela WinUI.
- Testes: xUnit para a camada de simulação.

## Estrutura de solução esperada
TaskbarHabitat.sln
├── src/
│   ├── TaskbarHabitat.Core/
│   ├── TaskbarHabitat.Data/
│   ├── TaskbarHabitat.Simulation/
│   ├── TaskbarHabitat.Widget/
│   └── TaskbarHabitat.Rendering/
└── tests/
    └── TaskbarHabitat.Simulation.Tests/

## O que implementar agora (Fase 1)
1. **Schema SQLite** conforme seção 6 do relatório, usando EF Core ou Dapper.
2. **Seed dos 9 registros** de Kanto (Bulbasaur até Blastoise) e das 6 evoluções, conforme seção 6.1.
3. **`SaveService.CreateNewSave(int starterId)`** que gera `save_id` (GUID), define `game_epoch_utc` e `last_seen_utc` como `DateTime.UtcNow`, insere em `save_state` e `creature_state`, e retorna o save.
4. **Tela de seleção do inicial** em WinUI 3 (`StarterSelectionWindow.xaml`) com três botões (Bulbasaur, Charmander, Squirtle). No `App.xaml.cs`, verificar se existe save; se não, abrir a janela; ao clicar, chamar `SaveService.CreateNewSave` e fechar.
5. **Integração com `Deskband11Lib.WinUI`**: após o save ser criado, criar `MainWindow`, criar `TaskbarContentHost` com `PreferredWidth = 360`, `PreferredHeight = 48`, e chamar `AttachWhenLayoutReadyAsync`.
6. **Testes xUnit**:
   - Banco é criado e populado com 9 espécies e 6 evoluções.
   - `CreateNewSave(1)` insere `save_state` com `starter_id = 1` e `creature_state` com valores iniciais.

## O que NÃO implementar agora
- `GameClock`, `IdleEngine`, `ProgressionSystem` (Fase 2).
- Captura de outros Pokémon, múltiplos habitats.
- Pokédex regional completa, achievements.
- Cadeia de Markov climática, visitantes, shiny.
- Assets originais.

## Ferramentas que você deve usar
- `pp-pokeapi` para validar nomes e IDs das espécies se necessário.
- `GliderMCP` para navegar pela solução e verificar referências.
- `dotnet-test` para rodar os testes.
- `NugetMcpServer` (se disponível) para inspecionar a API de `Deskband11Lib.WinUI` antes de gerar código.

## Critérios de aceite
- `dotnet build` passa sem erros.
- O banco SQLite é criado na primeira execução e contém 9 espécies e 6 evoluções.
- A janela de seleção aparece apenas quando não há save.
- Após escolher um inicial, o widget aparece na barra de tarefas com o `starter_id` correto persistido.
- Os dois testes xUnit passam.

## Fluxo de trabalho
Comece criando a solução e a camada de dados. Depois de cada etapa, rode `dotnet build` e `dotnet test`, e me mostre o resultado antes de avançar para a UI. Se encontrar um erro de API na `Deskband11Lib`, consulte via `NugetMcpServer` em vez de assumir assinaturas.

## 12. Prompt de Continuação (após Fase 1 concluída)

Quando a Fase 1 estiver validada, use este prompt para a Fase 2.


Fase 1 concluída: schema, seed, SaveService e tela de seleção do inicial funcionando, com testes passando.

Agora implemente o motor de simulação (Fase 2), respeitando as decisões do relatório:

1. **`GameClock`** com ticks de 15 min in-game, dia de 24 min reais, e modo dev (`#if DEBUG`) com aceleração 1×–360× e seleção de estação.
2. **`IdleEngine`** com cálculo offline determinístico: dado `last_seen_utc` e `save_id`, simular N ticks de 15 min, aplicar 590 XP/h passivo, com 50% e teto de 24 h para período offline.
3. **`ProgressionSystem`** com curva `XP_next = 900 + 2L`.
4. **`EvolutionSystem`** mínimo: verificar `min_level` da tabela `evolutions` e disparar evolução.
5. **Teste xUnit** que simula 7 dias de ticks a partir de um save inicial e verifica que o level 100 é atingido em ~168 h.

Critérios de aceite:
- `dotnet test` passa com os três testes novos.
- O cálculo offline é determinístico: dois runs com o mesmo `last_seen_utc` e `save_id` produzem o mesmo XP.
- O código da simulação não referencia `Widget` nem `Rendering`.

## 13. Resumo Executivo

O que é: Widget de Windows na barra de tarefas com criatura estilo Pokémon vivendo em habitat pixel art, progressão idle de 7 dias até level 100, e ações opcionais de cuidado que aceleram o desenvolvimento.

Como está construído: Três camadas (.NET 10 + WinUI 3 + SQLite), simulação determinística com ticks fixos, curva linear de XP, offline com limite de 24 h e 50%.

Estado atual: Planejamento completo; implementação não iniciada. Fase 1 (camada de dados + seleção do inicial) é o próximo passo imediato.

Ferramentas do Codex: dotnet/skills, GliderMCP, pp-pokeapi, dotnet-test, NugetMcpServer — todas com comandos de instalação verificados.

Riscos principais: Estabilidade da taskbar no Windows 11, consistência do cálculo offline, escopo excessivo (1025 espécies). Mitigações: Deskband11Lib, ticks determinísticos, lançamento em ondas (Kanto primeiro).

Meta do MVP: Fases 0–4 em 8–12 semanas, com um habitat, três iniciais, progressão passiva, evolução no nível 16 e teste de 7 dias passando.



Este relatório está pronto para ser salvo como `TaskbarHabitat-Relatorio.md` e usado como contexto inicial no Codex. Se quiser, o próximo passo é executar os comandos da seção 8 no seu ambiente e colar o prompt da seção 11 para iniciar a implementação.
