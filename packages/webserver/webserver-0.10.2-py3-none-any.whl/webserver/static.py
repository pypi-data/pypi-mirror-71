import click

from .utils import docker, explain_error, explain_step, run_command


@click.group()
def static() -> None:
    """
    Commands that deal with static files
    """


@click.command()
@click.argument("domain")
@click.argument("files_dir")
def add(domain: str, files_dir: str) -> None:
    """
    Add static FILES_DIR for DOMAIN to use
    """
    explain_step(f"Rsync'ing static files from {files_dir} for {domain}")
    run_command(f"sudo mkdir -p {files_dir}/")
    run_command(f"sudo rsync -ah {files_dir}/ /etc/webserver/static/{domain}/ --delete")


static.add_command(add)

if __name__ == "__main__":
    static()
