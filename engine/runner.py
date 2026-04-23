import asyncio
import time

from engine import controller
from engine.schema import GameState, Definitions
from interface import ui
from tools.logger import log


async def run(
    gs: GameState,
    definitions: Definitions,
    refresh_ui: bool,
    use_sleep: bool = True,
):
    next_tick_at = time.perf_counter() + controller.get_tick_interval(gs)

    while controller.is_running(gs):
        if refresh_ui:
            ui.refresh_stats(gs)
        # Если не запущена ни одна не-фоновая, игрок должен выбрать активность
        if controller.prompt_required(gs, definitions):
            options = controller.get_activity_options(gs, definitions)
            index = await ui.prompt_activity(options)
            controller.start_selected_activity(gs, definitions, index)

        next_tick_at += ui.pop_wait_time()

        now = time.perf_counter()
        delay = next_tick_at - now

        if delay < 0:
            log(f"Lag detected: {abs(delay):.4f}s", log_type="warning")

        if use_sleep:
            start = time.perf_counter()
            await asyncio.sleep(max(0.0, delay))
            end = time.perf_counter()

        await controller.update(
            gs, definitions, check_button_pressed=ui.check_button_pressed
        )

        next_tick_at += controller.get_tick_interval(gs)
        print("NOW", round(time.perf_counter(), 4))

    if refresh_ui:
        ui.refresh_stats(gs)

    await ui.on_finish()
