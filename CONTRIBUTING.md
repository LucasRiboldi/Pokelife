# Desenvolver o PokeLife

Use os passos do [README](README.md) para clonar e compilar. O [estado do projeto](STATE.md) registra o que já passou por validação. Antes de começar uma mudança de comportamento, confira a etapa em andamento no [plano mestre](referencia/Plano-Mestre-PokeLife.md).

## Onde fazer mudanças

- [TaskbarHabitat.Core](src/TaskbarHabitat.Core/) guarda o modelo do save e é o lugar previsto para as regras de tempo e XP.
- [TaskbarHabitat.Data](src/TaskbarHabitat.Data/) cuida do SQLite, das migrações e da leitura e gravação do inicial.
- [TaskbarHabitat.Widget](src/TaskbarHabitat.Widget/) cuida do ciclo da janela, da navegação e da apresentação do habitat.
- [Testes](tests/) cobrem SQLite, rotas, água e animação. Valide mudanças de janela também em uma sessão interativa do Windows.

## Testar

```powershell
dotnet build TaskbarHabitat.sln -c Release
dotnet test tests/TaskbarHabitat.Simulation.Tests/TaskbarHabitat.Simulation.Tests.csproj -c Release --no-build
pwsh -NoProfile -File tests/Test-WindowsLifecycle.ps1
```

O último comando usa PowerShell 7, exige que o PokeLife esteja fechado e abre janelas de teste. Ele cria um save em `%TEMP%` por meio de `POKELIFE_SAVE_DIRECTORY`. O GitHub Actions executa a compilação e os testes sem interface.

## Publicar uma versão

Quando houver um pedido de deploy, execute o workflow [Release PokeLife](https://github.com/LucasRiboldi/Pokelife/actions/workflows/release.yml) com **Run workflow** na `main`, ou rode `gh workflow run release.yml --ref main`. O workflow compila, roda os testes e publica o ZIP para Windows 11 x64 na página de Releases. A primeira versão é `v0.1.0`. Cada deploy seguinte incrementa o último número, como de `v0.1.0` para `v0.1.1`.

## Editar o habitat

O [guia de navegação](referencia/Plano-Navegacao-Habitat.md) explica o mapa do Tiled, as colisões e os destinos. Python com Pillow é necessário para regerar as imagens e a grade. Inclua os arquivos de origem e as saídas usadas pelo jogo quando mudar o terreno ou as rotas.

Para relatar um erro, abra uma [issue](https://github.com/LucasRiboldi/Pokelife/issues/new) com os passos, o resultado esperado e a versão do Windows. Para uma mudança de arte, inclua a origem do material e uma prévia.
