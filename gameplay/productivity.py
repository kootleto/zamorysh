from engine import gs_api
from random import randint


def get_productivity(gs):
    return (
        1 - (gs_api.get_vital(gs, "fatigue") + gs_api.get_vital(gs, "sleepiness")) / 200
    )
