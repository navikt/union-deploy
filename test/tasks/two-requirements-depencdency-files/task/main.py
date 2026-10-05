import sys
from pathlib import Path

import flyte
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.numpy_task.numpy_task import numpy_env, numpy_task
from kubernetes import client as k8s


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
    .with_requirements(
        file="requirements/requirements_pytest.txt",
        index_url=(
            "https://oauth2accesstoken@"
            "europe-west1-python.pkg.dev/nav-data-images-prod/pypi/simple/"
            ),
        ),
    depends_on=[numpy_env],
    )


@env.task(entrypoint=True)
def main() -> str:
    numpy_task()
    return "Hello, ci"
