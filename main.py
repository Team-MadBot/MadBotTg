import asyncio
import importlib
import logging
import os
import sys

from aiogram import Bot, Dispatcher

from config import settings

dp = Dispatcher()


async def load_plugins(dp: Dispatcher):  # MadBot™️ Original©️ + youmibot source code
    for path, _, files in os.walk("plugins"):  # FIXME: unsafe shit
        for file in files:
            if not file.endswith(".py"):
                continue

            egg = os.path.join(path, file).removesuffix(".py").replace("/", ".")
            if egg in settings["plugins_ignore"]:
                continue

            if egg in sys.modules:
                importlib.reload(sys.modules[egg])
                module = sys.modules[egg]
            else:
                module = importlib.import_module(egg)

            if hasattr(module, "setup"):
                await getattr(module, "setup")(dp)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings["token"])
    await load_plugins(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
