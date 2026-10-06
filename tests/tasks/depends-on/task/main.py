import flyte

from modules.numpy_task.numpy_task import numpy_env, numpy_task


env = flyte.TaskEnvironment(
    name="test_requirements_deploy_pytest",
    image=flyte.Image.from_base(
        image_uri="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images/flyte:3.13-base"
    )
    .clone(
        registry="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images",
        name="flyte",
        extendable=True,
    )
    .with_env_vars(
        {
            "UV_KEYRING_PROVIDER": "subprocess",
        }
    )
    .with_uv_project(
        "./pyproject.toml",
        extra_args="--group pytest-task --group numpy-task"
    )
    .with_code_bundle('all'),
    depends_on=[numpy_env],
    )


@env.task(entrypoint=True)
def main() -> str:
    numpy_task()
    return "Hello, ci"
