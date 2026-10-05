# Deploy Union/Flyte tasks with GitHub Actions

Use this reusable workflow to deploy the Flyte tasks defined in a Python file to Union from your repository's CI pipeline.

## Prerequisites

Before deploying:

- Your GitHub repository must be registered with the Union project you want to deploy to. Contact the Dataplattform team if it is not registered or you are unsure.
- Your dependency file must include `flyte`.
- Your task must be defined in a Python (`.py`) file.

## Deploy from CI

Create a workflow such as `.github/workflows/deploy.yaml` in the repository containing your task:

```yaml
name: Deploy Union task

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  deploy:
    permissions:
      contents: read
      id-token: write
    uses: navikt/union-deploy/.github/workflows/deploy.yaml@v1
    with:
      flyte-task-file: ./tasks/my_task.py
      dependency-file: ./pyproject.toml
      union-project: my-union-project
      union-domain: development
```

Adjust the file paths, project, domain, and trigger for your repository. A deploy runs all Flyte entities found in `flyte-task-file`.

The permissions are required so the workflow can check out your repository and authenticate to the platform without long-lived credentials.

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| `flyte-task-file` | Yes | Path to the Python file containing the Flyte task or tasks, relative to `working-directory`, for example `./tasks/my_task.py`. |
| `flyte-task-version` | No | Version identifier for the deployed Flyte tasks, passed to `flyte deploy --version`. If omitted, Flyte uses its default versioning. |
| `dependency-file` | Yes | Path to `pyproject.toml` or a `requirements*.txt` file, relative to `working-directory`, for example `./requirements.txt`. |
| `working-directory` | No | Directory relative to the repository root used for validation, dependency installation, Flyte config creation, and deployment. Defaults to `"."` (the repository root). The directory must already exist in the checked-out repository. |
| `pyproject-groups` | No | Comma-separated dependency groups to install from `pyproject.toml`, for example `numpy-task,pytest-task`. These are installed alongside project dependencies. Only valid with a `pyproject.toml` dependency file. |
| `union-project` | Yes | Union project registered for this GitHub repository. Only letters, numbers, and hyphens are accepted. |
| `union-domain` | Yes | Target domain: `development`, `staging`, or `production`. |
| `python-version` | No | Python version to use with a requirements file, for example `3.12`. With `pyproject.toml`, configure Python in the project instead. |

The workflow reads dependencies from `dependency-file` and installs them into a temporary CI virtual environment, not a project-local `.venv`, so it can import the task definition and run the Flyte deployment command. This also gives uv workspace members an explicit environment location. This does not build the task image in GitHub Actions: Union builds the deployable image using its remote image builder when an image build is needed.

### Working directory and paths

By default, the workflow runs from the repository root. Set `working-directory` when your task expects to run from a subdirectory. Both `flyte-task-file` and `dependency-file` are then relative to that directory, not the repository root. Do not repeat the working-directory prefix in those paths.

For example, with `main.py` and `pyproject.toml` in `tasks/my-project`:

```yaml
    with:
      working-directory: ./tasks/my-project
      flyte-task-file: main.py
      dependency-file: pyproject.toml
      union-project: my-union-project
      union-domain: development
      pyproject-groups: numpy-task,pytest-task
```

Omit `pyproject-groups` if no additional groups are needed. Group names must exist in the supplied project.

Deployment runs in the same working directory where the workflow creates `.flyte/config.yaml`. Relative paths used by your task definition, such as `flyte.Image.with_uv_project("./pyproject.toml")` or paths to requirements files, must also be valid from that directory. Installing groups in CI does not automatically add them to the task image; select the required groups in the image definition too.

For a uv workspace member, you can set `working-directory` to the member directory and `dependency-file` to `pyproject.toml`. The temporary environment is used regardless of uv's usual workspace-root `.venv` location. This controls the CI environment only; the task's image definition must separately handle its build dependencies and workspace sources.

### Python version

To select Python when using a requirements file:

```yaml
    with:
      flyte-task-file: ./tasks/my_task.py
      dependency-file: ./requirements.txt
      union-project: my-union-project
      union-domain: development
      python-version: "3.12"
```

## Troubleshooting

- **Authentication or permission failure:** Verify that the GitHub repository is registered with the value passed to `union-project`, and that both permissions from the example are present.
- **`flyte` is not installed:** Add `flyte` to your `pyproject.toml` or requirements file.
- **Task or dependency file does not exist:** `flyte-task-file` and `dependency-file` are relative to `working-directory`, which defaults to the repository root. Check the spelling and location of both files and avoid repeating the working-directory prefix.
- **Relative path fails during deployment:** Check paths in the task's image definition and other import-time code against `working-directory`, not the task file's directory unless they are the same.
- **Invalid domain:** Use exactly `development`, `staging`, or `production`.
- **Dependencies differ from your local environment:** The workflow currently does not respect `uv.lock`. When using `pyproject.toml`, it resolves dependencies again through our internal PyPI proxy. This can select versions that differ from your local lockfile. This is subject to change in the future when a new PyPI proxy (Artifact Keeper) is ready, at that time we will require `uv.lock` files to be built with that proxy.

## Developing and releasing

The public workflow is `.github/workflows/deploy.yaml`. We use `main` for development and move the `v1` tag manually for stable releases.

### New major versions

Do not release backwards-incompatible changes on `v1`. For breaking changes, create a new tag such as `v2` and have callers reference `navikt/union-deploy/.github/workflows/deploy.yaml@v2` (the current release script only supports `v1`). Add the new version of the reusable workflow to the runner group's selected workflows before callers use `@v2`; otherwise the runner will refuse to pick up their jobs. Keep `v1` available for existing callers.
