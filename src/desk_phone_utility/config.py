import shutil
import datetime
import keyring
from keyring.errors import NoKeyringError
import warnings
from importlib.resources import files

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from pathlib import Path

import logging

config_dir = Path("~/.config/desk_phone_utility").expanduser().resolve()
config_dir.mkdir(exist_ok=True, parents=True)
config_path = config_dir / "config.toml"

if not config_path.exists():
    shutil.copy2(files("desk_phone_utility.data") / "example_config.toml", config_path)

_config = tomllib.load(config_path.open("rb"))
log_dir = Path(_config.get("log_dir", "~/.local/share/linux-tools/"))
log_level = _config.get("log_level", "INFO")
if log_level not in ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    warnings.warn(
        f'Got invalid log_level = "{log_level}". Check the '
        f'config at {config_path}. Using "INFO" for now.',
        UserWarning,
    )
    log_level = "INFO"

phone_host = _config.get("phone_host")
phone_user = _config.get("phone_user")

log_dir = log_dir.expanduser().resolve()
log_dir.mkdir(exist_ok=True, parents=True)
logfile_path = log_dir / f"{datetime.datetime.now().strftime('%Y')}.log"

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")

fh = logging.FileHandler(filename=logfile_path, encoding="utf-8", mode="a")
ch = logging.StreamHandler()

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logging.getLogger("").setLevel(log_level)
logging.getLogger("").addHandler(fh)
logging.getLogger("").addHandler(ch)

log = logging.getLogger(__name__)

service_name = f"desk_phone_utility{phone_host}"
try:
    phone_password = keyring.get_password(
        service_name=service_name, username=phone_user
    )
except NoKeyringError:
    phone_password = None
    log.error("No keyring found.")
