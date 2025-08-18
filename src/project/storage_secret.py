from __future__ import annotations

import datetime
import json
import pathlib
import uuid

# The code for migrating data from old token to new token is not added yet
ENABLE_ROTATION = False
"Whether to replace tokens after certain amount of time"

LIFE_SPAN = datetime.timedelta(days=1)
"The duration after which the token is considered outdated"

_file = pathlib.Path("secret_token.json")
"""The file path in which the token is stored

This file is ignored by git. The file contains the following keys:

    token (str):    the storage secret required by nicegui
    created (str):  the time at which the token was created
"""


def _new_token() -> str:
    return str(uuid.uuid4())


def _store_token(token: str) -> None:
    creation_time = datetime.datetime.now()  # noqa: DTZ005

    with _file.open("w") as fp:
        data = {
            "token": token,
            "created": creation_time.isoformat(),
        }
        json.dump(data, fp)


def _read_token() -> tuple[str, bool]:
    with _file.open("r") as fp:
        data = json.load(fp)

    if not ENABLE_ROTATION:
        return data["token"], False

    creation_time = datetime.datetime.fromisoformat(data["created"])
    current_time = datetime.datetime.now()  # noqa: DTZ005
    expired = current_time - creation_time > LIFE_SPAN

    return data["token"], expired


def get_secret_token() -> str:
    """Return the secret token to enable user storage.

    Returns:
        str: the secret token

    """
    if not _file.exists():
        new_token = _new_token()
        _store_token(new_token)
        return new_token

    token, expired = _read_token()

    if expired:
        token = _new_token()

    return token
