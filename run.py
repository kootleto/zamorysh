import asyncio
import os

from config import SETTINGS
from engine import controller

os.environ["KIVY_NO_ARGS"] = "1"


async def main():
    if SETTINGS.gui:
        from interface.gui.main import start
    else:
        from interface.cli.main import start

    game_state, definitions = await controller.init_game()
    await start(game_state, definitions)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")
