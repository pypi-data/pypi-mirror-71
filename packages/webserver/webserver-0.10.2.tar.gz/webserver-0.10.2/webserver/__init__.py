from os import path
from subprocess import run as run_command

import click

from .conf import conf
from .genconf import genconf
from .gendh import gendh
from .gentls import gentls
from .run import run
from .static import static
from .update import update

if not path.exists("/etc/webserver"):
    click.echo("Initializing /etc/webserver directory")
    for folder in ("dhparams", "letsencrypt", "logs", "static", "conf.d"):
        run_command(["sudo", "mkdir", "-p", f"/etc/webserver/{folder}"])


@click.group()
def cli() -> None:
    pass


cli.add_command(run)
cli.add_command(update)
cli.add_command(genconf)
cli.add_command(gentls)
cli.add_command(gendh)
cli.add_command(conf)
cli.add_command(static)

if __name__ == "__main__":
    cli()
