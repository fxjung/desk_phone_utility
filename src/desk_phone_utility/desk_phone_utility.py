import re
import requests
import urllib.parse

from requests.auth import HTTPDigestAuth
from desk_phone_utility import config
from desk_phone_utility.gui import show_qt_questionbox

import logging

log = logging.getLogger(__name__)


def construct_snom_url(*, phone_number: str, phone_host: str) -> str:
    """
    Return a command URL for `phone_host` that calls `phone_number`.

    Parameters
    ----------
    phone_number
        Phone number to call
    phone_host
        snom phone host to use

    Returns
    -------
    command url
    """
    return f"http://{phone_host}/command.htm?number={phone_number}"


def initiate_call(phone_number: str) -> None:
    """
    Initiate a phone call to `phone_number`.

    Parameters
    ----------
    phone_number
        Number to call
    """
    url = construct_snom_url(phone_number=phone_number, phone_host=config.phone_host)
    r = requests.get(url, auth=HTTPDigestAuth(config.phone_user, config.phone_password))


def handle_uri(uri: str) -> None:
    """
    Handle tel URI. This incorporates parsing and sanitizing, displaying a GUI dialog
    box to check whether we actually want to initiate the call and doing just that
    if the user if the user clicks "Yes".

    Parameters
    ----------
    uri
        tel URI
    """
    o = urllib.parse.urlparse(uri)
    if o.scheme != "tel":
        raise ValueError("Not a tel URI")

    phone_number = urllib.parse.unquote(o.path)
    phone_number = re.sub(r"[\., ]", "", phone_number)

    if not re.fullmatch(r"\+?[0-9]{1,15}", phone_number):
        raise ValueError(
            "Must only contain '+' as an optional first character, "
            f"and digit characters. Max length is 15 digits. "
            f"Offending number: '{phone_number}'"
        )

    hphone_number = phone_number
    hphone_number = re.sub(r"(^(?:\+|00)[0-9]{2})", r"\1 ", hphone_number)

    do_initiate_call = show_qt_questionbox(
        title="Initiate call?",
        message=f"Initiate a call to '{hphone_number}'?",
    )

    phone_number = phone_number.replace("+", "00")

    if do_initiate_call:
        log.info(f"Initiating call for '{phone_number}'")
        initiate_call(phone_number)
    else:
        log.info(f"Call for '{phone_number}' aborted.")
