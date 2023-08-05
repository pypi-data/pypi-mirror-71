import click

from .utils import explain_step, run_command


# pylint: disable=no-value-for-parameter
@click.command()
@click.argument("domain")
def gendh(domain: str) -> None:
    """
    Generate DH params for DOMAIN
    """
    explain_step(f"Generating 3072 bit DH params for website {domain}:")
    run_command(f"sudo openssl dhparam -out /etc/webserver/dhparams/{domain}.pem 3072")


if __name__ == "__main__":
    gendh()
