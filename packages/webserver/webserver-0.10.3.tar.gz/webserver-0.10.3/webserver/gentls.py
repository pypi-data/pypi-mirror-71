import click

from .utils import explain_step, run_command


# pylint: disable=no-value-for-parameter
@click.command()
@click.argument("domain")
def gentls(domain: str) -> None:
    """
    Get LetsEncrypt TLS certificate for DOMAIN
    """
    explain_step(f"Getting TLS certificate for website {domain}:")
    run_command(
        f"sudo certbot certonly --webroot -w /etc/webserver/letsencrypt/ -d {domain}"
    )


if __name__ == "__main__":
    gentls()
