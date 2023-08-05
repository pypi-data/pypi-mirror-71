import click

from .utils import docker, explain_step


# pylint: disable=no-value-for-parameter
@click.command()
@click.option("-q", "--quiet", help="Only print text if error occured", is_flag=True)
@click.option("--no-pull", help="Do not pull fresh image", is_flag=True)
def update(quiet: bool, no_pull: bool) -> None:
    """
    Update nginx:mainline-alpine image of webserver stack
    """
    if not no_pull:
        explain_step("Pulling fresh nginx:mainline-alpine image", quiet=quiet)
        docker(
            "pull nginx:mainline-alpine",
            check=True,
            quiet=quiet,
            error_message="Pulling fresh image failed!",
        )

    explain_step("Updating image of webserver Docker Swarm stack", quiet=quiet)
    docker(
        "service update --image nginx:mainline-alpine webserver_nginx",
        quiet=quiet,
        check=True,
        error_message="Update failed!",
    )


if __name__ == "__main__":
    update()
