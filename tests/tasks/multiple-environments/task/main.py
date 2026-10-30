import flyte

from modules.numpy_task.numpy_task import numpy_env, numpy_task

env = flyte.TaskEnvironment(
    name="test_multiple_environments",
    image=flyte.Image.from_base(
        image_uri="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images/flyte:3.13-base"
    )
    .clone(
        registry="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images",
        name="flyte",
        extendable=True,
    )
    .with_uv_project(
        "./pyproject.toml",
        extra_args="--group pytest-task --group numpy-task",
        secret_mounts=flyte.Secret(key="ak-pypi-index", as_env_var="UV_DEFAULT_INDEX"),
    ),
    depends_on=[numpy_env],
    )


@env.task(entrypoint=True)
def main() -> str:
    numpy_task()
    return "Hello, ci"
