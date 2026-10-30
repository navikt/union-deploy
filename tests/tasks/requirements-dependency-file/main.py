import flyte
from kubernetes import client as k8s

env = flyte.TaskEnvironment(
    name="test_requirements_deploy",
    image=flyte.Image.from_base(
        image_uri="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images/flyte:3.13-base"
    )
    .clone(
        registry="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images",
        name="flyte",
        extendable=True,
    )
    .with_requirements(
        file="tests/tasks/requirements-dependency-file/requirements.txt",
        secret_mounts=flyte.Secret(key="ak-pypi-index", as_env_var="UV_DEFAULT_INDEX"),
    ),
)

@env.task(entrypoint=True)
def main() -> str:
    return "Hello, ci"
