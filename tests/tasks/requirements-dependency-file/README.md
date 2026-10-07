# Deploy med requirements.txt

## Når passer dette oppsettet?

Bruk dette når prosjektet oppgir Python-avhengigheter i en requirements-fil, og du ikke trenger `pyproject.toml` for deploy.

## Slik fungerer eksempelet

- [main.py](main.py) definerer en task og importerer `flyte` og `kubernetes` på modulnivå.
- [requirements.txt](requirements.txt) inneholder begge pakkene, slik at CI kan importere task-definisjonen.
- Image-definisjonen bruker `.with_requirements(...)` til å installere pakkene i task-imaget. CI installerer fra samme fil, men i et separat miljø.

## Bruk i ditt repository

1. Legg `flyte` og taskens øvrige avhengigheter i `requirements.txt`.
2. Tilpass tasken og image-definisjonen fra `main.py`. Hvis requirements-filen ligger i roten av ditt repository, endrer du `file` i `.with_requirements(...)` til `"./requirements.txt"`.
3. Legg denne jobben under `jobs` i deploy-workflowen din. Eksempelet under forutsetter `main.py` og `requirements.txt` i repositoryets rot. Bytt ut prosjektet og velg en Python-versjon som passer tasken.

```yaml
deploy:
  permissions:
    contents: read
    id-token: write
  uses: navikt/union-deploy/.github/workflows/deploy.yaml@v2
  with:
    flyte-task-file: main.py
    dependency-file: requirements.txt
    python-version: "3.13"
    union-project: my-union-project
    union-domain: development
```

## Vær oppmerksom på

- `python-version` velger Python i CI, ikke i task-imaget. Velg også et passende base-image i task-definisjonen.
- Filstier i image-definisjonen er relative til workflowens arbeidsmappe. Testen her kjører fra repositoryets rot og bruker derfor prefikset `tests/tasks/requirements-dependency-file/`.
- `pyproject-groups` kan ikke brukes med requirements-filer. Pakker som tasken trenger ved kjøring må være med i image-definisjonen, også hvis de ikke importeres under deploy.

## Se også

- [Test-workflowen for dette eksempelet](../../../.github/workflows/deploy-test-requirements-dependency-file.yaml). Den bruker interne plattformmiljøer; ikke kopier `environment`-inputen til din workflow.
- [Workflow-oppsett og inputreferanse](https://datadoc.ansatt.nav.no/union/deploy/).
- [Deploy med pyproject.toml](../pyproject-dependency-file/README.md) som alternativ.
