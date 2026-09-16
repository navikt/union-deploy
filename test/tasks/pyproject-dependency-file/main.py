import flyte
from kubernetes import client as k8s


env = flyte.TaskEnvironment(
    name="hello_ci_deploy",
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
    .with_pip_packages(
        "kubernetes",
        index_url=(
            "https://oauth2accesstoken@"
            "europe-west1-python.pkg.dev/nav-data-images-prod/pypi/simple/"
        ),
    ),
)

@env.task
def foo() -> str:
    return "ci"

@env.task(entrypoint=True)
def main() -> str:
    return "Hello, " + foo()
