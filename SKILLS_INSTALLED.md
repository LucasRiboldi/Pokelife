# Skills de desenvolvimento de jogos no PokeLife

Em 10/11/2026, **8 dos 10 pacotes solicitados estão instalados**. O Codex reconheceu **91 skills locais**. Meowa e o pacote oficial da Unity ficaram pendentes. A skill de pixel art do Summer foi adaptada para uso manual local. O Summer Engine MCP não foi instalado.

## Ambiente

- Windows 11 Pro, build 26200, com PowerShell 7.6.9.
- Codex Desktop 26.1103.7773.0 e CLI 0.167.0-alpha.3.2.
- Git 2.56.0.windows.4, Python 3.13.15, pip 26.2.1, Node.js 26.12.1, npm 11.20.0, WinGet 1.29.380 e FFmpeg 9.0.2.
- Skills nativas em `.agents/skills`. Executáveis e ambiente Python em `bin/skill-tools`, sob a regra de exclusão do Git já existente. [Diretórios de skills do Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
- O Go 1.27.3 portátil foi usado para compilar a CLI do sprite-gen. Blender e Unity ficaram fora do ambiente validado.

## Inventário

| Pacote | Status | Invocação e uso no PokeLife | Fonte primária |
| --- | --- | --- | --- |
| Agent Sprite Forge | **Instalada** | `$generate2dsprite`, `$codeart2d`, `$video2dsprite`, `$generate2dmap`, `$generate2dmedia`. Cinco guias com instruções locais para arte por código e processamento de arquivos existentes. | [Forge no commit verificado](https://github.com/0x0funky/agent-sprite-forge/tree/6b3da5c444363378e20f3fce130ebecc22f343dd) |
| Character Animation Creator | **Instalada** | `$game-character-sprites` na versão 0.2.0. O README também menciona o alias antigo `game-character-64`. Validação de folhas 32×32, 64×64 e 128×128 com Python e Pillow. A geração via ImageGen ficou pendente. O snapshot consultado não traz licença explícita de redistribuição. | [Character Animation Creator no commit verificado](https://github.com/tachikomared/character-animation-creator-skill/tree/9ce98dffb98c84488fe7b99b62c49fabee20abd6) |
| pixling | **Instalada** | `$pixling` e CLI `bin/skill-tools/python/Scripts/pixling.exe`. Fluxos por código e arquivos locais. Scenario fica pendente. | [Código da skill](https://github.com/trinity-works/pixling/tree/a52d6eae912f13c03dc2e3b87ab84a008bc4a219), [pacote 0.3.1](https://pypi.org/project/pixling/0.3.1/) |
| sprite-gen | **Instalada** | `$sprite-gen` e CLI `bin/skill-tools/sprite-gen.exe`. Inspeção de PNGs e exportação de atlas. A CLI usa a versão 0.1.1. | [Skill no commit verificado](https://github.com/kkjang/sprite-gen/tree/b2d38ad57e9463783db5537061a0f138512f0870), [CLI v0.1.1](https://github.com/kkjang/sprite-gen/tree/v0.1.1) |
| Meowa Game Assets Skill | **Pendente** | `$game-assets` requer conta Meowa e `MEOWART_API_KEY`. | [Instalação do Meowa](https://github.com/Meowa-AI/meowa-skills#install) |
| Pixel Art Skill do Summer Engine | **Instalada como adaptação local** | `$pixel-art`. Guia manual de grade, paleta, transparência, escala e alinhamento de quadros. Inclui licença MIT e referência ao original. A geração oficial requer o serviço Summer e ficou pendente. | [Skill original](https://github.com/SummerEngine/summer/blob/2b58eef8f63b763a8e15d3e3354fa1fb5e83b56e/library/skills/pixel-art/SKILL.md) |
| Game Superpowers | **Instalada** | `$game-superpowers`. A versão atual usa esse alias. O alias anterior `$using-game-superpowers` foi retirado da fonte. | [Game Superpowers no commit verificado](https://github.com/mike007jd/game-superpowers/tree/a1796f6fd79554ee85e6f382011cb601dfcb1808) |
| Unity Skills oficiais | **Pendente** | A licença exige um projeto dependente da Unity. O PokeLife usa .NET. Testes de Editor requerem ambiente Unity compatível. | [Pacote oficial](https://github.com/Unity-Technologies/skills/tree/60f95e6d4beaeacf4dfdff7829ec9b35008a0be0), [Unity Companion License](https://unity.com/legal/licenses/unity-companion-license) |
| Game Development Studio Skills | **Instalada** | `$game-development-studio`, `$game-asset-production`, `$game-asset-vendoring`, `$game-visual-debugging`, `$game-performance-optimization`. CLI `bin/skill-tools/studio/node_modules/.bin/game-dev.cmd`, versão 1.4.0. Captura local funciona. Fluxos com Blender e provedores externos ficaram pendentes. | [Release v1.4.0](https://github.com/theisegoria/game-development-studio-skills/releases/tag/v1.4.0) |
| awesome-gamedev-agent-skills | **Instalada** | `$router` e 75 guias especializados. O roteador ganhou instruções para o projeto .NET. Os guias comunitários de Unity incluídos pertencem a esta coleção. `$steam-publish` e `$itch-publish` ficaram pendentes por exigirem contas. | [Coleção no commit verificado](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/tree/4cce500ce1a779b12fdd824be581c7d2ab4e7ba2) |

## Instalação e testes executados

Os comandos abaixo omitem o caminho temporário dos arquivos baixados. Os testes de imagem e captura gravaram seus resultados em pastas temporárias.

| Pacote ou etapa | Comandos e operações | Resultado |
| --- | --- | --- |
| Inventário | `Get-CimInstance Win32_OperatingSystem`, `Get-AppxPackage -Name OpenAI.Codex`, consultas `Get-Command` e `--version`, `git rev-parse --show-toplevel`, `git status --short`. | Ambiente e raiz confirmados. |
| Fontes | `Invoke-RestMethod` e `Invoke-WebRequest` para metadados, arquivos e arquivos ZIP oficiais. `Expand-Archive`, `Copy-Item` e `Set-Content` para instalar os diretórios e registrar as adaptações locais. | Revisões fixadas nas fontes da tabela. Licenças incluídas quando fornecidas. |
| Python | `python -m venv bin/skill-tools/python`, seguido de `python -m pip install --only-binary=:all: pixling==0.3.1 "numpy>=1.26" "Pillow>=10.1" "scipy>=1.11"` e `python -m pip check` com o Python do projeto. | pixling 0.3.1, NumPy 2.5.4, Pillow 13.0.0 e SciPy 1.18.1. Dependências consistentes. |
| Forge | `python tools/install_skills.py --apply --dest <staging>` e `--check --dest <staging>`. Após a cópia, nova checagem no projeto. `python render_pixelspec.py --spec <slime.pixelspec.json> --output-dir <temp> --preview-scale 4 --strict-qc`. | Instalação upstream íntegra antes da adaptação. A checagem no projeto aponta apenas os cinco `SKILL.md` com as instruções locais. O teste gerou três variantes com três quadros cada e passou na checagem estrita. |
| Character Animation Creator | `python validate_sheet.py --help` e `python validate_sheet.py --input <png> --rows 1 --columns 3 --cell 64 --json-out <json> --fail-on-warnings`. | Folha de três quadros validada sem erros ou avisos. |
| pixling | Cópia do diretório da skill. `pixling --help`, `pixling doctor` e `pixling build <shade_wolf.json> --clips idle --dirs S,E --out <temp>`. | Núcleo funcional. Dois PNGs produzidos. O instalador `pixling agent install .` foi dispensado porque também edita `AGENTS.md`. |
| sprite-gen | Download do Go portátil para área temporária, SHA-256 conferido com o catálogo de go.dev. `go install github.com/kkjang/sprite-gen/cmd/sprite-gen@v0.1.1` com `GOBIN` no projeto. `sprite-gen version`, `sprite-gen --json spec`, `sprite-gen inspect frame <png> --json`, `sprite-gen export --list-formats` e `sprite-gen export <frames> --format sheet --out <temp> --cols 3`. | Inspeção de um quadro 32×32 sem pixels com alfa parcial. Exportação de atlas 96×32 com três quadros e manifesto JSON. A entrada de exportação usa nomes `frame_*.png`. |
| Summer Pixel Art, Game Superpowers e awesome-gamedev | Instalação dos manifestos e recursos locais. Revisão do guia manual, da referência `presentation.md` e das instruções do roteador. | Descoberta dos aliases confirmada. São guias sem CLI própria. |
| Game Development Studio | Conferência do SHA-256 `c1909ebeff19bfc423fea312a22acbe0cef8ae8c1d3bb725c228387a8ba0620f` com a release oficial. `npm install --prefix bin/skill-tools/studio --ignore-scripts --no-fund --no-audit <tarball>`. `game-dev --help`, `game-dev doctor --workflow generic-capture --expected-version 1.4.0`, `game-dev adapter sample --project <nova-pasta> --confirm`, `game-dev scenario plan capture --project <pasta>`, `game-dev scenario run capture --project <pasta> --confirm` e `game-dev capture verify <run>`. | Captura de exemplo executada em CPU. Hashes e lista de artefatos verificados. A checagem opcional do `doctor` consulta o diretório de usuário. A descoberta no projeto foi confirmada pelo Codex. |
| Descoberta no Codex | `codex app-server` com JSON-RPC `initialize`, `initialized` e `skills/list` com `forceReload: true` e a raiz do PokeLife. | 91 de 91 manifestos descobertos e habilitados, sem erros locais. O teste confirma descoberta. Os fluxos de execução testados estão listados acima. |
| Exclusão do MCP | `codex mcp list` e inspeção dos diretórios instalados. | Nenhuma entrada Summer. Nenhum MCP registrado ou iniciado durante a instalação. |

Os limites de execução local estão nos guias instalados. Preserve essas instruções ao atualizar os pacotes. Os testes cobrem as ferramentas e a descoberta das skills. Fluxos de geração por provedores, Blender, Unity e publicação ficaram fora dos testes.

## Aliases da coleção awesome-gamedev-agent-skills

Use `$router` para selecionar o guia. Os demais aliases também podem ser invocados diretamente.

- **disciplines** — `$ai-behavior-trees-utility-ai`, `$audio-design`, `$camera-systems`, `$create-game-assets`, `$dialogue-systems`, `$game-ai`, `$game-feel`, `$game-ui-ux`, `$input-systems`, `$level-design`, `$performance-optimization`, `$physics-tuning`, `$procedural-gen`, `$save-systems`, `$shader-programming`.
- **ebitengine** — `$ebitengine-game`.
- **genres** — `$card-game`, `$fps-shooter`, `$platformer`, `$puzzle`, `$roguelike`, `$rpg`, `$survival-crafting`, `$tower-defense`, `$visual-novel`.
- **godot** — `$godot-2d-movement`, `$godot-3d-essentials`, `$godot-animation`, `$godot-audio`, `$godot-csharp`, `$godot-export`, `$godot-gdscript`, `$godot-gdscript-headless-testing`, `$godot-multiplayer`, `$godot-nodes-scenes`, `$godot-physics`, `$godot-resources`, `$godot-shaders`, `$godot-signals-groups`, `$godot-tilemap`, `$godot-ui-control`.
- **other-engines** — `$bevy-ecs`, `$defold-core`, `$love2d-core`, `$pygame-core`, `$roblox-characters`, `$roblox-datastores`, `$roblox-luau`, `$roblox-networking`, `$roblox-physics`, `$roblox-simulator-economy`, `$roblox-studio-workflow`, `$roblox-ui`.
- **unity** — `$unity-animation`, `$unity-build-pipeline`, `$unity-csharp-scripting`, `$unity-input-system`, `$unity-navmesh`, `$unity-physics`, `$unity-scriptableobjects`, `$unity-tilemap-2d`.
- **unreal** — `$unreal-behavior-trees`, `$unreal-blueprints`, `$unreal-cpp-gameplay`, `$unreal-enhanced-input`, `$unreal-niagara`, `$unreal-packaging`.
- **web-engines** — `$phaser-arcade-physics`, `$phaser-core`, `$pixijs-rendering`, `$threejs-gltf-loading`, `$threejs-materials-lighting`, `$threejs-scene-setup`.
- **workflows** — `$game-jam`, `$prototype-fast`.
