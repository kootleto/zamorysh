import asyncio
import os

import constants

os.environ["KIVY_NO_ARGS"] = "1"

from config import SETTINGS
from engine import controller
from interface import ui


async def main():
    if SETTINGS.gui:
        from interface.gui.main import start
    else:
        from interface.cli.main import start

    while True:

        game_state, definitions, is_save = controller.init_game(
            gs_path=constants.GAME_STATE_PATH, content_dir=constants.CONTENT_DIR
        )
        view_state = ui.init_ui(vs_path=constants.VIEW_STATE_PATH)
        action = await start(game_state, definitions, view_state, is_save)

        if action == "restart":
            if os.path.exists(constants.GAME_STATE_PATH):
                os.remove(constants.GAME_STATE_PATH)
            continue
        elif action == "exit":
            break


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")
