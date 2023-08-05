from importlib.resources import path

import click

from .__version__ import __version__
from .utils import explain_step, run_command


# pylint: disable=no-value-for-parameter
@click.command()
@click.option("-q", "--quiet", help="Only print text if error occured", is_flag=True)
@click.argument("domain")
def genconf(quiet: bool, domain: str) -> None:
    """
    Create HTTPS configuration file with examples for DOMAIN
    """
    explain_step(f"HTTPS configuration file for website {domain}:", quiet=quiet)
    with path(package="webserver", resource="config") as folder:
        click.echo(f"#=== Generated with webserver v{__version__} ===#")
        run_command(
            f'cat {folder}/443-template.conf {folder}/examples/* | sed "s/{{{{SERVER_NAME}}}}/{domain}/g"'
        )
        click.echo("}")


if __name__ == "__main__":
    genconf()
