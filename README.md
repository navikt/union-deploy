# Deploy Union/Flyte tasks with GitHub Actions

See [dataplattform documentation](https://datadoc.ansatt.nav.no/union/deploy/)

## Examples

Choose the example closest to your project. Each README is a short recipe for adapting the setup to your own repository, with links to the task code and its test workflow. Deployment registers tasks in Union; it does not execute them.

- [Deploy with pyproject.toml](tests/tasks/pyproject-dependency-file/README.md): One dependency list, without groups.
- [Deploy with requirements.txt](tests/tasks/requirements-dependency-file/README.md): Dependencies in a requirements file.
- [Deploy with dependency groups](tests/tasks/pyproject-groups/README.md): Select one or several groups from `pyproject.toml`.
- [Multiple task environments](tests/tasks/multiple-environments/README.md): A task calls tasks in other environments, with alternatives using a combined dependency file for CI and the parent image, or function-local imports.
- [Deploy from a workspace member](tests/tasks/pyproject-workspace/README.md): A task package in a uv workspace, using a prebuilt image.
- [Deploy with ContainerTask](tests/tasks/container-task/README.md): A Python task invokes a command in a separate container.

## Running a deployed task

The reusable `.github/workflows/run.yaml` workflow submits an already-deployed task
using `flyte run deployed-task`. Specify both its environment and fully qualified
entrypoint name; no deployment-output parsing or task source file is needed.
This initial workflow supports tasks without arguments and does not pin a task
version or explicitly wait for remote execution to finish.

For example, in a calling workflow in this repository:

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/deploy.yaml
    with:
      working-directory: tests/tasks/pyproject-dependency-file
      flyte-task-file: main.py
      dependency-file: pyproject.toml
      union-project: my-project
      union-domain: development

  run:
    needs: deploy
    uses: ./.github/workflows/run.yaml
    with:
      union-project: my-project
      union-domain: development
      task-environment: test_pyproject_deploy
      task-name: test_pyproject_deploy.main
```

The run workflow installs the latest Flyte CLI in a dedicated environment using
uv's default Python selection, independent of the caller's project. It does not
install the caller's project or task dependencies.
It follows deployment's authentication pattern, but fetches the API key directly
with the Secret Manager action instead of installing Cloud SDK. The key is only
supplied to the execution step.
It can also be called independently, without the deploy job. Before use, add
`run.yaml` to the runner group's selected workflows where that restriction applies.

## Developing and releasing

The public workflow is `.github/workflows/deploy.yaml`. We use `main` for development and move the `v2` tag manually for stable releases.

### New major versions

Do not release backwards-incompatible changes on `v2`. For breaking changes, create a new tag such as `v3` and have callers reference `navikt/union-deploy/.github/workflows/deploy.yaml@v3` (the current release script only supports `v2`). Add the new version of the reusable workflow to the runner group's selected workflows before callers use `@v3`; otherwise the runner will refuse to pick up their jobs. Keep `v2` available for existing callers.
