# Deploy med ContainerTask

## Når passer dette oppsettet?

Bruk dette når du vil kjøre en kommando i et eget container-image og kalle den fra en Python-task. Containeren kan ha andre verktøy og avhengigheter enn Python-tasken.

## Slik fungerer eksempelet

- [main.py](main.py) definerer `greeting_task`, en `ContainerTask` som kjører en shell-kommando i et Alpine-image og skriver en hilsen til en output-fil.
- `TaskEnvironment.from_task("container_env", greeting_task)` oppretter environmentet for container-tasken.
- Python-tasken `main` kaller container-tasken med `await greeting_task()`. Dens environment har `depends_on=[container_env]` og et eget Flyte-image.
- [pyproject.toml](pyproject.toml) inneholder `flyte`, slik at CI kan importere task-definisjonen. Verktøyene shell-kommandoen trenger kommer fra Alpine-imaget, ikke fra CI-installasjonen.

## Bruk i ditt repository

1. Tilpass `ContainerTask` i `main.py` med ditt container-image, kommando og eventuelle inputs/outputs. Output-filene må samsvare med `outputs` og `output_data_dir`.
2. Behold koblingen via `TaskEnvironment.from_task(...)` og `depends_on` når Python-tasken kaller container-tasken. Sørg for at prosjektfilen inneholder `flyte` og eventuelle andre Python-avhengigheter.
3. Legg denne jobben under `jobs` i deploy-workflowen din. Eksempelet under forutsetter `main.py` og `pyproject.toml` i repositoryets rot. Bytt ut `my-union-project` med prosjektet ditt.

```yaml
deploy:
  permissions:
    contents: read
    id-token: write
  uses: navikt/union-deploy/.github/workflows/deploy.yaml@v2
  with:
    flyte-task-file: main.py
    dependency-file: pyproject.toml
    union-project: my-union-project
    union-domain: development
```

## Vær oppmerksom på

- Container-tasken og Python-tasken bruker forskjellige images. Pakker installert i CI blir ikke automatisk tilgjengelige i noen av dem.
- Eksempelet refererer til ferdigbygde images med `.from_base(...)`. Workflowen bygger ikke et eget Dockerfile bare fordi det ligger i repositoryet; bygg og publiser container-imaget separat hvis du følger dette oppsettet.
- `depends_on` sørger for deploy-avhengigheten mellom environments, ikke for deling av pakker eller filsystem mellom containerne.

## Se også

- [Test-workflowen for dette eksempelet](../../../.github/workflows/deploy-test-container-task.yaml). Den bruker interne plattformmiljøer; ikke kopier `environment`-inputen til din workflow.
- [Workflow-oppsett og inputreferanse](https://datadoc.ansatt.nav.no/union/deploy/).
- [Flere task-environments](../multiple-environments/README.md) for mer om `depends_on` og ulike kjøremiljøer.
