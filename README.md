# Deploy Union/Flyte tasks with GitHub Actions

See [dataplattform documentation](https://datadoc.ansatt.nav.no/union/deploy/)

## Developing and releasing

The public workflow is `.github/workflows/deploy.yaml`. We use `main` for development and move the `v1` tag manually for stable releases.

### New major versions

Do not release backwards-incompatible changes on `v1`. For breaking changes, create a new tag such as `v2` and have callers reference `navikt/union-deploy/.github/workflows/deploy.yaml@v2` (the current release script only supports `v1`). Add the new version of the reusable workflow to the runner group's selected workflows before callers use `@v2`; otherwise the runner will refuse to pick up their jobs. Keep `v1` available for existing callers.
