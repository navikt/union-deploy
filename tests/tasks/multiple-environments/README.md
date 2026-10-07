# Deploy med flere task-environments

## Når passer dette oppsettet?

Bruk dette når en task kaller andre tasks som trenger egne images, ressurser eller annen konfigurasjon. En `TaskEnvironment` beskriver hvor og hvordan en task kjører; dette er ikke det samme som Union-domenet `development`, `staging` eller `production`.

## Slik fungerer eksempelet

- [task/main.py](task/main.py) definerer parent-tasken `main`, som importerer og kaller `numpy_task`.
- [modules/numpy_task/numpy_task.py](modules/numpy_task/numpy_task.py) definerer child-tasken og dens `numpy_env`. Modulen importerer `numpy` på modulnivå.
- Parent-environmentet har `depends_on=[numpy_env]`. Det forteller Flyte at child-environmentet må klargjøres ved deploy, inkludert bygging av imaget ved behov.
- [pyproject.toml](pyproject.toml) definerer gruppene `pytest-task` og `numpy-task`. Parent-imaget velger begge; child-imaget velger bare `numpy-task`. `pytest-task` illustrerer en ekstra gruppe, men brukes ikke i task-kroppen her.
- CI installerer begge gruppene. `numpy` må finnes både i CI og i parent-imaget fordi import av child-modulen kjører dens modulnivå-importer. Child-tasken kjører likevel i sitt eget image.

## Bruk i ditt repository

1. Definer én `TaskEnvironment` per ønsket kjøremiljø, og la parent-tasken importere child-tasken og dens environment. Legg child-environmentet i parentens `depends_on`.
2. Velg grupper i hvert image med `.with_uv_project("./pyproject.toml", extra_args="--group ...")`. Parent-imaget må dekke egne avhengigheter og det som trengs for å importere child-modulene; child-imaget må dekke child-taskens kjøring.
3. Legg denne jobben under `jobs` i deploy-workflowen din. Eksempelet forutsetter samme mappestruktur som her, lagt i `tasks/my-project`. Tilpass mappen, gruppene og Union-prosjektet.

```yaml
deploy:
  permissions:
    contents: read
    id-token: write
  uses: navikt/union-deploy/.github/workflows/deploy.yaml@v2
  with:
    working-directory: ./tasks/my-project
    flyte-task-file: task/main.py
    dependency-file: pyproject.toml
    pyproject-groups: "pytest-task,numpy-task"
    union-project: my-union-project
    union-domain: development
```

## Vær oppmerksom på

- `depends_on` etablerer deploy-avhengigheten mellom environments. Det installerer ikke child-taskens pakker i parent-imaget.
- CI må kunne importere task-filen og modulene den importerer. Det betyr ikke nødvendigvis at alle pakker som brukes inne i alle task-kropper må installeres i CI.
- Task-signaturer, dekoratorer og image-/environment-definisjoner behandles også ved import. Pakker brukt der kan ikke uten videre flyttes til lokale importer.
- Image-definisjonenes `"./pyproject.toml"` er relativ til arbeidsmappen, ikke til `task/` eller `modules/numpy_task/`.

### Alternativ: Samlet avhengighetsfil for deploy og parent-tasken

Du kan beholde en egen requirements-fil per child-task og lage én samlet `requirements.txt` som inneholder unionen av alle taskenes avhengigheter, inkludert `flyte` og parent-taskens egne pakker. Det gir et alternativ til avhengighetsgrupper uten at alle child-images trenger alle pakkene.

- Bruk den samlede filen som `dependency-file` i CI, og utelat `pyproject-groups`.
- Bruk `.with_requirements(file="./requirements.txt")` i parent-imaget. Da får det også pakkene som trengs for å importere child-modulene.
- Bruk hver child-tasks egen fil i dens image-definisjon, for eksempel `.with_requirements(file="./requirements-numpy.txt")`. Stiene er relative til workflowens arbeidsmappe.

Hold den samlede filen oppdatert når child-taskenes avhengigheter endres. Parent-imaget får alle pakkene, men child-images kan fortsatt være små og task-spesifikke. Behold separate environments og `depends_on` som i gruppe-eksempelet.

Pakkene og versjonskravene i den samlede filen må kunne installeres sammen. Separate child-images løser ikke motstridende krav i CI eller parent-imaget. Hvis en child-pakke bare trengs i task-kroppen, kan lokale importer som beskrevet under gjøre at den ikke trenger å være med i den samlede filen eller parent-imaget.

Du kan også samle avhengighetene i `[project].dependencies` i en `pyproject.toml` og bruke den med `.with_uv_project(...)` i parent-imaget, mens child-images fortsatt bruker egne avhengighetsfiler. Uten grupper kan du utelate både `pyproject-groups` og `--group`-argumentene.

### Alternativ: Importer inne i task-funksjonen

Hvis en pakke bare brukes i child-taskens kropp, kan du importere den der i stedet for på modulnivå. En variant av child-tasken kan for eksempel se slik ut:

```python
@numpy_env.task(entrypoint=True)
def numpy_task() -> str:
    import numpy

    return str(numpy.sum([1, 2, 3]))
```

Fjern da også `import numpy` fra modulnivå. Parent-modulen kan fortsatt importere `numpy_task` uten at `numpy` er installert. I dette eksempelet kan du da fjerne `numpy-task` fra CI-inputen og parent-imagets gruppevalg, men **beholde gruppen i child-imaget**. Behold også `depends_on=[numpy_env]`.

Dette fungerer fordi signaturen bruker den innebygde typen `str`, og modulens øvrige definisjoner ikke krever `numpy` ved import. Hvis en pakke brukes i taskens parameter- eller returtyper, eller i kode som kjører på modulnivå, må den fortsatt være tilgjengelig ved import.

De to alternativene over er tilpasninger du kan gjøre i eget prosjekt, ikke egne testede varianter i dette repositoryet. Se Union-dokumentasjonen for en grundigere forklaring og alternativet med remote tasks.

## Se også

- [Test-workflowen for dette eksempelet](../../../.github/workflows/deploy-test-multiple-environments.yaml). Den bruker interne plattformmiljøer; ikke kopier `environment`-inputen til din workflow.
- [Workflow-oppsett og inputreferanse](https://datadoc.ansatt.nav.no/union/deploy/).
- [Union: Multiple environments](https://www.union.ai/docs/v2/union/user-guide/tasks/task-configuration/multiple-environments/).
- [Deploy med pyproject.toml uten grupper](../pyproject-dependency-file/README.md), [requirements.txt](../requirements-dependency-file/README.md) eller [avhengighetsgrupper](../pyproject-groups/README.md).
