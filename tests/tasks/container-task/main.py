import flyte
from flyte.extras import ContainerTask

greeting_task = ContainerTask(
    name="echo_and_return_greeting",
    image=flyte.Image.from_base(
        "europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-user-images/alpine:3.24.1"
    ),
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    outputs={"greeting": str},
    command=[
        "/bin/sh",
        "-c",
        "echo 'Hello Container Task, my name is foo.' | tee -a /var/outputs/greeting; ",
    ],
)

container_env = flyte.TaskEnvironment.from_task("container_env", greeting_task)

env = flyte.TaskEnvironment(
    name="test_container_deploy",
    depends_on=[container_env],
    image=flyte.Image.from_base(
        image_uri="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images/flyte:3.13-base"
    )
)


@env.task(entrypoint=True)
async def main():
    await greeting_task()
