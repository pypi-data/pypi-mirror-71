from importlib.resources import path

import click

from .utils import docker, explain_step


# pylint: disable=no-value-for-parameter
@click.command()
@click.option("-q", "--quiet", help="Only print text if error occured", is_flag=True)
@click.option("--no-pull", help="Do not pull fresh image", is_flag=True)
def run(quiet: bool, no_pull: bool) -> None:
    """
    Run Highly-Available nginx:mainline-alpine stack
    """
    explain_step('Creating shared "nginx" network (in case not created)', quiet=quiet)
    docker("network create -d overlay --attachable nginx", quiet=quiet)

    explain_step(
        'Creating "nginx-static" and "nginx-conf" volumes (in case not created)',
        quiet=quiet,
    )
    docker(
        "volume create --driver local --opt type=none --opt device=/etc/webserver/static --opt o=bind --name nginx-static",
        quiet=quiet,
    )
    docker(
        "volume create --driver local --opt type=none --opt device=/etc/webserver/conf.d --opt o=bind --name nginx-conf",
        quiet=quiet,
    )

    if not no_pull:
        explain_step("Pulling fresh nginx:mainline-alpine image", quiet=quiet)
        docker(
            "pull nginx:mainline-alpine",
            check=True,
            quiet=quiet,
            error_message="Pulling fresh image failed!",
        )

    explain_step("Deploying to Docker Swarm", quiet=quiet)
    with path(package="webserver", resource="config") as folder:
        docker(
            f"stack deploy -c {folder}/integrated.yml webserver",
            quiet=quiet,
            check=True,
            error_message="Stack deployment failed!",
        )


if __name__ == "__main__":
    run()
