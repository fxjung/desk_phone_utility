import typer
import keyring
from getpass import getpass

from desk_phone_utility import config
from desk_phone_utility.desk_phone_utility import handle_uri

import logging

log = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def set_password():
    print(f"Enter password for snom phone at {config.phone_host} below:")
    keyring.set_password(
        service_name=config.service_name,
        username=config.phone_user,
        password=getpass(),
    )
    print("Password successfully saved to the system keyring.")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, argument: str = typer.Argument(...)):
    if ctx.invoked_subcommand is not None:
        return
    # Ugly hack. Unfortunately, there seems to be no preferred solution...
    # See also https://github.com/tiangolo/typer/issues/18#issuecomment-833020933
    if ctx.params["argument"] == "set-password":
        app.registered_commands[0].callback()
    else:
        log.info(f"Got {argument}")
        handle_uri(argument)
