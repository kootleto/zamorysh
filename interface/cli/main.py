from engine import runner
from engine.schema import GameState, Definitions


async def start(gs: GameState, definitions: Definitions, vs):

    await runner.run(gs, vs, definitions, refresh_ui=True, use_sleep=True)
