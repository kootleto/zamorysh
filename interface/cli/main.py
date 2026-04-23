from engine import runner
from engine.schema import GameState, Definitions

async def start(gs: GameState, definitions: Definitions):

    await runner.run(gs, definitions, refresh_ui=True, use_sleep=True)
