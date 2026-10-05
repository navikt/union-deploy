import flyte
from kubernetes import client as k8s


env = flyte.TaskEnvironment(
    name="test_pyproject_deploy",
    image=flyte.Image.from_base(
        image_uri="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images/flyte:3.14-base"
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
        pyproject_file="pyproject.toml",
        index_url=(
            "https://oauth2accesstoken@"
            "europe-west1-python.pkg.dev/nav-data-images-prod/pypi/simple/"
        ),
    ),
)

@env.task(entrypoint=True)
def main() -> str:
    return "Hello, ci"
