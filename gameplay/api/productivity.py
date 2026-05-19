from gameplay.api import vitals


def get(gs):
    return (
        1 - (vitals.get(gs, vitals.SLEEPINESS) + vitals.get(gs, vitals.FATIGUE)) / 200
    )
