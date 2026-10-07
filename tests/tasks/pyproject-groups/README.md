# Deploy med avhengighetsgrupper

## Når passer dette oppsettet?

Bruk dette når prosjektet har avhengigheter i `[dependency-groups]` i `pyproject.toml`, og du vil velge hvilke grupper en deploy og et task-image trenger.

## Slik fungerer eksempelet

- [pyproject.toml](pyproject.toml) har `flyte` i prosjektets vanlige avhengigheter, og gruppene `pytest-task` og `numpy-task`.
- [pytest_task.py](pytest_task.py) importerer `pytest` og velger gruppen `pytest-task` i image-definisjonen. Den viser også `.with_code_bundle("loaded_modules")` for kodepakking.
- [numpy_pytest_task.py](numpy_pytest_task.py) importerer både `numpy` og `pytest` og velger begge gruppene i image-definisjonen.
- CI velger de tilsvarende gruppene med inputen `pyproject-groups`, slik at task-filene kan importeres under deploy.

## Bruk i ditt repository

1. Definer gruppene i `[dependency-groups]`, og behold `flyte` i `[project].dependencies`.
2. Velg gruppene task-imaget trenger med `.with_uv_project("./pyproject.toml", extra_args="--group numpy-task --group pytest-task")` i image-definisjonen.
3. Legg denne jobben under `jobs` i deploy-workflowen din. Her ligger task-filen og prosjektfilen i `tasks/my-project`. Tilpass mappen, filnavnet, gruppene og Union-prosjektet.

```yaml
deploy:
  permissions:
    contents: read
    id-token: write
  uses: navikt/union-deploy/.github/workflows/deploy.yaml@v2
  with:
    working-directory: ./tasks/my-project
    flyte-task-file: numpy_pytest_task.py
    dependency-file: pyproject.toml
    pyproject-groups: "numpy-task,pytest-task"
    union-project: my-union-project
    union-domain: development
```

For varianten med bare `pytest`, bruk `flyte-task-file: pytest_task.py`, `pyproject-groups: pytest-task` og `extra_args="--group pytest-task"` i image-definisjonen.

## Vær oppmerksom på

- Workflow-inputen bruker komma mellom gruppenavn; image-definisjonen bruker ett `--group`-argument per gruppe. Gruppene må finnes i prosjektfilen.
- `pyproject-groups` installerer grupper i CI, ikke i task-imaget. CI trenger pakkene som kreves for å importere task-definisjonen; imaget trenger også pakkene som brukes når tasken kjører.
- `"./pyproject.toml"` i image-definisjonen er relativ til `working-directory`. Ikke gjenta arbeidsmappen i `flyte-task-file` eller `dependency-file`.

## Se også

- [Test-workflowen for dette eksempelet](../../../.github/workflows/deploy-test-pyproject-groups.yaml). Den bruker interne plattformmiljøer; ikke kopier `environment`-inputen til din workflow.
- [Workflow-oppsett og inputreferanse](https://datadoc.ansatt.nav.no/union/deploy/).
- [Flere task-environments](../multiple-environments/README.md) når en task kaller en task med et annet image.
