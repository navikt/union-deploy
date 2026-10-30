import flyte

import pytest

env = flyte.TaskEnvironment(
    name="test_pytest_task_deploy",
    image=flyte.Image.from_base(
        image_uri="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images/flyte:3.14-base"
    )
    .clone(
        registry="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images",
        name="flyte",
        extendable=True,
    )
    .with_uv_project(
        "./pyproject.toml",
        extra_args="--group pytest-task",
        secret_mounts=flyte.Secret(key="ak-pypi-index", as_env_var="UV_DEFAULT_INDEX"),
    )
)

@env.task(entrypoint=True)
def main():
    assert 0.1 + 0.2 == pytest.approx(0.3)
