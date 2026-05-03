import asyncio

from engine import runner, controller
from engine.schema import Definitions, GameState
from interface.gui.app import GameApp


async def start(gs: GameState, definitions: Definitions):
    app = GameApp(gs, lambda: controller.get_activity_options(gs, definitions))

    kivy_task = asyncio.create_task(app.async_run())

    await app.ready

    engine_task = asyncio.create_task(
        runner.run(gs, definitions, refresh_ui=False, use_sleep=True)
    )

    done, pending = await asyncio.wait(
        [kivy_task, engine_task], return_when=asyncio.FIRST_COMPLETED
    )

    if kivy_task in done:
        engine_task.cancel()

    elif engine_task in done:
        await kivy_task
