# Deploy fra et uv-workspace

## Når passer dette oppsettet?

Bruk dette når tasken ligger i et medlem av et uv-workspace, og du vil kjøre deploy fra medlemmets mappe. Eksempelet viser installasjon i CI og deploy med et ferdigbygd image, ikke bygging av images med avhengigheter fra flere workspace-medlemmer.

## Slik fungerer eksempelet

- [pyproject.toml](pyproject.toml) i workspace-roten angir `packages/task` som medlem under `[tool.uv.workspace]`.
- [packages/task/pyproject.toml](packages/task/pyproject.toml) oppgir medlemmets avhengigheter, inkludert `flyte`.
- [packages/task/main.py](packages/task/main.py) definerer en task med et ferdigbygd Flyte-image. Den trenger ikke å bygge inn andre workspace-medlemmer.
- CI kjører fra `packages/task` og bruker medlemmets prosjektfil. Avhengighetene installeres i et midlertidig CI-miljø, ikke i uv-workspacets vanlige `.venv`.

## Bruk i ditt repository

1. Sørg for at task-pakken er registrert som workspace-medlem, og at dens `pyproject.toml` inneholder `flyte` og avhengighetene som trengs for å importere task-definisjonen.
2. Tilpass tasken fra `packages/task/main.py`. Bruk et image som har pakkene tasken trenger ved kjøring, og sørg for at nødvendig kildekode blir med.
3. Legg denne jobben under `jobs` i deploy-workflowen din. Her forutsettes workspace-roten å være repositoryets rot. Tilpass medlemsmappen, task-filnavnet og Union-prosjektet.

```yaml
deploy:
  permissions:
    contents: read
    id-token: write
  uses: navikt/union-deploy/.github/workflows/deploy.yaml@v2
  with:
    working-directory: ./packages/task
    flyte-task-file: main.py
    dependency-file: pyproject.toml
    union-project: my-union-project
    union-domain: development
```

## Vær oppmerksom på

- `flyte-task-file` og `dependency-file` er relative til medlemsmappen. Ikke gjenta `packages/task` i disse inputene.
- At workspace-avhengigheter kan installeres i CI betyr ikke at de automatisk følger med i task-imaget. Image-definisjonen og kodepakkingen må også håndtere eventuelle andre workspace-medlemmer tasken bruker.
- Eksempelet bruker ikke `.with_uv_project(...)` til å bygge et workspace-image. Det demonstrerer derfor ikke en generell løsning for slik image-bygging.

## Se også

- [Test-workflowen for dette eksempelet](../../../.github/workflows/deploy-test-pyproject-workspace.yaml). Den bruker interne plattformmiljøer; ikke kopier `environment`-inputen til din workflow.
- [Workflow-oppsett og inputreferanse](https://datadoc.ansatt.nav.no/union/deploy/).
- [Deploy med pyproject.toml](../pyproject-dependency-file/README.md) for et prosjekt uten workspace.
