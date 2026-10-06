import flyte
import numpy

numpy_env = flyte.TaskEnvironment(
    name="test_requirements_deploy_numpy",
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
        extra_args="--group numpy-task"
    )
    .with_code_bundle('loaded_modules'),
)

@numpy_env.task(entrypoint=True)
def numpy_task() -> str:
    return "Hello, numpy"