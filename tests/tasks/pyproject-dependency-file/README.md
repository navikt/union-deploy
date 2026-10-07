# Deploy med pyproject.toml

## Når passer dette oppsettet?

Bruk dette når prosjektet har én felles liste med Python-avhengigheter i `pyproject.toml`, uten behov for avhengighetsgrupper.

## Slik fungerer eksempelet

- [main.py](main.py) definerer en task og importerer `flyte` og `kubernetes` på modulnivå. Begge pakkene må derfor finnes under deploy, selv om task-kroppen bare returnerer en hilsen.
- [pyproject.toml](pyproject.toml) oppgir pakkene i `[project].dependencies` og Python-versjonen i `requires-python`.
- Image-definisjonen bruker `.with_uv_project(...)` til å legge prosjektets avhengigheter i task-imaget. CI installerer fra samme fil, men i et separat miljø.

## Bruk i ditt repository

1. Legg `flyte` og taskens øvrige avhengigheter i `[project].dependencies`.
2. Tilpass tasken og image-definisjonen fra `main.py`. Hvis `pyproject.toml` ligger i roten av ditt repository, endrer du `pyproject_file` i `.with_uv_project(...)` til `"./pyproject.toml"`.
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

- Du trenger ikke `pyproject-groups` for dette oppsettet.
- Filstier i image-definisjonen er relative til workflowens arbeidsmappe, ikke til task-filen. Testen her kjører fra repositoryets rot og bruker derfor prefikset `tests/tasks/pyproject-dependency-file/`.
- CI-installasjonen legger ikke automatisk pakker eller kildekode i task-imaget. Behold en image-definisjon som dekker det tasken trenger ved kjøring.

## Se også

- [Test-workflowen for dette eksempelet](../../../.github/workflows/deploy-test-pyproject-dependency-file.yaml). Den bruker interne plattformmiljøer; ikke kopier `environment`-inputen til din workflow.
- [Workflow-oppsett og inputreferanse](https://datadoc.ansatt.nav.no/union/deploy/).
- [Velge avhengighetsgrupper](../pyproject-groups/README.md) hvis ulike tasks trenger ulike pakker.
