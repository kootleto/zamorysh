import asyncio
import os

os.environ["KIVY_NO_ARGS"] = "1"

from config import SETTINGS
from engine import controller
from interface import ui


async def main():
    if SETTINGS.gui:
        from interface.gui.main import start
    else:
        from interface.cli.main import start

    game_state, definitions = controller.init_game()
    view_state = ui.init_ui()
    await start(game_state, definitions, view_state)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")
