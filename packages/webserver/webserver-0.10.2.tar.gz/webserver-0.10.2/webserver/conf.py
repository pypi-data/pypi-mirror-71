from os import path
from sys import exit

import click

from .utils import docker, explain_error, explain_step, run_command


@click.group()
def conf() -> None:
    """
    Commands that deal with configurations
    """


@click.command()
@click.argument("domain")
def create(domain: str) -> None:
    """
    Create configuration for DOMAIN using webserver genconf command
    """
    explain_step(f"Creating default configuration file for website {domain}")
    run_command(
        f"webserver genconf -q {domain} | sudo tee /etc/webserver/conf.d/{domain}.conf > /dev/null"
    )


@click.command()
@click.argument("domain")
@click.argument("config_file")
def add(domain: str, config_file: str) -> None:
    """
    Add CONFIG_FILE for DOMAIN
    """
    explain_step(f"Adding configuration file for website {domain}")
    run_command(f"sudo cp {config_file} /etc/webserver/conf.d/{domain}.conf")


@click.command()
@click.argument("domain")
@click.argument("editor", required=False)
def edit(domain: str, editor: str) -> None:
    """
    Edit configuration for DOMAIN with EDITOR if configuration exist

    If no EDITOR provided - nano is used
    """
    if not path.exists(f"/etc/webserver/conf.d/{domain}.conf"):
        explain_error(f"No configuration exist for {domain}!")
        explain_step("Use `webserver add` to add it")
        exit(1)

    run_command(
        f"sudo {editor if editor else 'nano'} /etc/webserver/conf.d/{domain}.conf"
    )


@click.command()
def reload() -> None:
    """
    Reload configurations without downtime
    """
    ps_output = str(
        docker("ps -qf 'name=webserver_nginx'", capture_output=True).stdout,
        encoding="utf8",
    )
    containers = ps_output.rsplit("\n")[:-1]
    for container in containers:
        explain_step(f"Reloading container {container}:")
        docker(f"exec {container} sh -c 'nginx -t && nginx -s reload'")


conf.add_command(create)
conf.add_command(add)
conf.add_command(edit)
conf.add_command(reload)

if __name__ == "__main__":
    conf()
