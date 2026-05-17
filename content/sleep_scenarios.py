from gameplay.api import vitals
from interface import ui


def falling_asleep():
    def check_sleepy(gs):
        return vitals.get(gs, vitals.SLEEPINESS) >= 80

    def go_to_sleep():
        ui.display("Вам пора бы лечь спать...")

    def check_very_sleepy(gs):
        return vitals.get(gs, vitals.SLEEPINESS) == 100

    # def sleep(gs):

