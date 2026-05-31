import asyncio

from kivy.config import Config
from kivy.core.text import LabelBase, Label

import constants
from engine import runner, controller
from engine.schema import Definitions, GameState
from interface import ui
from interface.gui.app import GameApp
from interface.gui.gui import KivyState

LabelBase.register(
    name="UMTypewriter",
    fn_regular="assets/fonts/UMTypewriter-Regular.ttf",
)
LabelBase.register(
    name="UMTypewriter_bold",
    fn_regular="assets/fonts/UMTypewriter-Bold.ttf",
)
LabelBase.register(
    name="UMTypewriter_bold_italic",
    fn_regular="assets/fonts/UMTypewriter-BoldItalic.ttf",
)
LabelBase.register(
    name="UMTypewriter_italic",
    fn_regular="assets/fonts/UMTypewriter-Italic.ttf",
)
LabelBase.register(
    name="UMTypewriter_oblique",
    fn_regular="assets/fonts/UMTypewriter-Oblique.ttf",
)
Label.font_name = "UMTypewriter"

Config.set("input", "wm_pen", "")
Config.set("input", "wm_touch", "")
Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set("graphics", "show_cursor", "1")
Config.write()


async def start(gs: GameState, definitions: Definitions, vs: KivyState, is_save: bool):
    app = GameApp(
        gs, vs, lambda: controller.get_activity_options(gs, definitions), is_save
    )

    app.session_result = asyncio.get_running_loop().create_future()

    kivy_task = asyncio.create_task(app.async_run())

    await app.ready

    if is_save:
        ui.display_load_notification()

    engine_task = asyncio.create_task(
        runner.run(
            gs,
            definitions,
            refresh_ui=False,
            use_sleep=True,
            save_path=constants.GAME_STATE_PATH,
            autosave_interval=constants.AUTOSAVE_INTERVAL,
            start_game=not is_save,
        )
    )

    done, pending = await asyncio.wait(
        [kivy_task, engine_task], return_when=asyncio.FIRST_COMPLETED
    )

    if kivy_task in done:
        engine_task.cancel()
        return "exit"

    else:
        result = await app.session_result
        app.stop()
        await kivy_task
        return result
