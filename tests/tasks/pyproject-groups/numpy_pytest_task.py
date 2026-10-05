import flyte
import numpy as np

import pytest

PYPI_PROXY_INDEX_URL = "europe-west1-python.pkg.dev/nav-data-images-prod/pypi/simple/"

env = flyte.TaskEnvironment(
    name="test_numpy_pytest_task_deploy",
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
            "UV_DEFAULT_INDEX": f"https://oauth2accesstoken@{PYPI_PROXY_INDEX_URL}",
        }
    )
    .with_uv_project(
        "./pyproject.toml",
        extra_args="--group numpy-task --group pytest-task"
    )
)

@env.task(entrypoint=True)
def main():
    array_1d = np.array([1, 2, 3, 4, 5])
    multiplied_array = array_1d * 2

    print("NumPy Array multiplied by 2:")
    print(multiplied_array)

    assert 0.1 + 0.2 == pytest.approx(0.3)
