import flyte

env = flyte.TaskEnvironment(
    name="test_workspace_task_deploy",
    image=flyte.Image.from_base(
        "europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images/flyte:3.14-base"
    ),
)


@env.task(entrypoint=True)
def main() -> str:
    return "Hello from a workspace member"
