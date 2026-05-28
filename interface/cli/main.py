import constants
from engine import runner
from engine.schema import GameState, Definitions
from interface import ui


async def start(gs: GameState, definitions: Definitions, _vs, is_save):

    if is_save:
        ui.display_load_notification()

    await runner.run(
        gs,
        definitions,
        refresh_ui=True,
        save_path=constants.GAME_STATE_PATH,
        autosave_interval=constants.AUTOSAVE_INTERVAL,
        use_sleep=True,
        start_game=not is_save,
    )
    return "exit"
