import asyncio
import time
from copy import deepcopy

from engine import controller
from engine.schema import GameState, Definitions
from interface import ui
from tools.logger import log


async def run(
    gs: GameState,
    definitions: Definitions,
    refresh_ui: bool,
    save_path,
    autosave_interval: int,
    use_sleep: bool = True,
    start_game: bool = True,
):
    if start_game:
        await controller.start_game(gs, definitions)

    next_tick_at = time.perf_counter() + controller.get_tick_interval(gs)

    ticks_before_autosave = autosave_interval
    while controller.is_running(gs):
        ticks_before_autosave -= 1

        if refresh_ui:
            ui.refresh_ui(gs, controller.get_activity_options(gs, definitions))
        # Если не запущена ни одна не-фоновая, игрок должен выбрать активность
        if controller.prompt_required(gs, definitions):
            if ticks_before_autosave <= 0:
                controller.save_game(gs, save_path)
                ui.display_save_notification()
                ticks_before_autosave = autosave_interval

            options = controller.get_activity_options(gs, definitions)
            index = await ui.prompt_activity(options)
            controller.start_selected_activity(gs, definitions, index)
            ui.pop_wait_time()
            next_tick_at = time.perf_counter() + controller.get_tick_interval(gs)
        else:
            next_tick_at += ui.pop_wait_time()

        now = time.perf_counter()
        delay = next_tick_at - now

        if delay < 0:
            log(f"Lag detected: {abs(delay):.4f}s", log_type="warning")

        if use_sleep:
            await asyncio.sleep(max(0.0, delay))

        await controller.update(
            gs, definitions, check_button_pressed=ui.check_button_pressed
        )

        just_finished = controller.get_just_finished(gs)
        if just_finished:
            read_only_gs = deepcopy(gs)
            for entry in just_finished:
                controller.call_on_finish(read_only_gs, definitions, entry)

        next_tick_at += controller.get_tick_interval(gs)

    if refresh_ui:
        ui.refresh_ui(gs, controller.get_activity_options(gs, definitions))

    await ui.on_finish()
