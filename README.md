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

## Developing and releasing

The public workflow is `.github/workflows/deploy.yaml`. We use `main` for development and move the `v2` tag manually for stable releases.

### New major versions

Do not release backwards-incompatible changes on `v2`. For breaking changes, create a new tag such as `v3` and have callers reference `navikt/union-deploy/.github/workflows/deploy.yaml@v3` (the current release script only supports `v2`). Add the new version of the reusable workflow to the runner group's selected workflows before callers use `@v3`; otherwise the runner will refuse to pick up their jobs. Keep `v2` available for existing callers.
