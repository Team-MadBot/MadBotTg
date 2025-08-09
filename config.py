import os
from typing import TypedDict

from dotenv import load_dotenv

load_dotenv()


class TypedSettings(TypedDict):
    token: str
    apiToken: str
    owners: tuple[int, ...]
    bot_domain: str
    mxdcxt_thoughts_id: int
    mxdcxt_tarahtelka_id: int  # don't blame me pls
    plugins_ignore: tuple[str, ...]


settings: TypedSettings = {
    "token": os.environ["BOT_TOKEN"],
    "apiToken": os.environ["API_TOKEN"],
    "owners": tuple(map(int, os.environ["BOT_OWNERS"].split())),
    "bot_domain": os.environ["BOT_DOMAIN"],
    "mxdcxt_thoughts_id": int(os.environ["MXDCXT_THOUGHTS_ID"]),
    "mxdcxt_tarahtelka_id": int(os.environ["MXDCXT_TARAHTELKA_ID"]),
    "plugins_ignore": tuple(os.environ.get("PLUGINS_IGNORE", "").split())
    + ("plugins.__template__",),
}
