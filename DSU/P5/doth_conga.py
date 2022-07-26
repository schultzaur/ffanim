import random

from manim import *
from dataclasses import dataclass
from PlayerObject import PlayerObject
from p5_constants import SS

# manim -pqh DSU/P5/doth_conga.py -r 1080,1080 Maxwell
# manim -o test --format=gif -r 1080,1080 DSU/P5/doth_conga.py Maxwell

@dataclass
class CongaConfig:
    name: str
    conga_direction: np.array
    doom_direction: np.array
    doom_safe_spots: list[int]
    cleanse_safe_spots: list[int]

class DotH(Scene):
    config = CongaConfig(
        name="maxwell",
        conga_direction=RIGHT * (2 ** .5),
        doom_direction=DOWN * (2 ** .5),
        doom_safe_spots=[SS.W_INNER, SS.SW, SS.SE, SS.E_INNER],
        cleanse_safe_spots=[SS.W_OUTER, SS.NW, SS.NE, SS.E_OUTER])
    party_members = ["Astrologian", "BlackMage", "Monk", "Ninja", "DarkKnight", "Dancer", "Gunbreaker", "Scholar"]
    loops = 10

    def construct(self):
        map = ImageMobject(r"Resources/dsu-p4-cropped.png", z_index=-1)
        map.scale_to_fit_height(14)
        self.add(map)

        boss = ImageMobject(r"Resources/Boss.png", z_index=0)
        boss.scale(2)
        boss.shift(UP * .1)
        target = SVGMobject(r"Resources/Target.svg", z_index=0)
        self.boss_group = Group(boss, target)
        self.boss_group.shift(UP * 3)

        self.players = []
        for i, party_member in enumerate(self.party_members):
            player = PlayerObject(party_member, (-3.5+i)/2 * self.config.conga_direction, z_index=1)
            self.players.append(player)

        for i in range(self.loops):
            self.loop()

    def fade_in_players(self):
        for player in self.players:
            player.move_to(random.uniform(-1, 1) * RIGHT + random.uniform(-1, 1) * UP)
        self.play(*[FadeIn(player) for player in self.players])

    def apply_doom(self):
        for player in random.sample(self.players, 4):
            player.apply_doom()

    def doom_shift(self):
        animations = []
        for player in self.players:
            if player.has_doom:
                animations.append(player.animate.shift(.5 * self.config.doom_direction))
            else:
                animations.append(player.animate.shift(-.5 * self.config.doom_direction))
        self.play(*animations)

    def move_to_safe_spot(self):
        animations = []
        for count, player in enumerate(player for player in self.players if player.has_doom):
            animations.append(player.animate.move_to(self.config.doom_safe_spots[count]))
        for count, player in enumerate(player for player in self.players if not player.has_doom):
            animations.append(player.animate.move_to(self.config.cleanse_safe_spots[count]))

        self.play(*animations, run_time=1.5)

    def show_cleanse_puddles(self):
        circles = []

        for player in self.players:
            if player.has_doom:
                continue

            circles.append(Circle(
                radius=1.5,
                color=WHITE,
                stroke_opacity=.25,
                fill_opacity=.25,
                z_index=0).move_to(player.get_center()))

        self.play(*[FadeIn(circle) for circle in circles])

        return circles

    def fade_out_all(self, cleanse_puddles):
        animations = [FadeOut(self.boss_group)]
        animations.extend([FadeOut(player) for player in self.players])
        animations.extend([FadeOut(puddle) for puddle in cleanse_puddles])
        self.play(*animations)

    def reset_dooms(self):
        for player in self.players:
            player.remove_doom()

    def loop(self):
        self.fade_in_players()
        self.wait(.5)
        self.play(FadeIn(self.boss_group))
        self.wait(.5)
        self.play(*[player.animate.move_to_static_spot() for player in self.players])
        self.wait(.5)
        self.apply_doom()
        self.wait(.5)
        self.doom_shift()
        self.wait(1)
        self.move_to_safe_spot()
        self.wait(1)
        cleanse_puddles = self.show_cleanse_puddles()
        self.wait(.5)
        self.fade_out_all(cleanse_puddles)
        self.wait(.5)
        self.reset_dooms()


class Week1NS(DotH):
    config = CongaConfig(
        name="week 1 strat n/s",
        conga_direction=RIGHT + DOWN,
        doom_direction=(LEFT + DOWN),
        doom_safe_spots=[SS.NW, SS. W_INNER, SS.SW, SS.E_INNER],
        cleanse_safe_spots=[SS.W_OUTER, SS.NE, SS.E_OUTER, SS.SE])


class NSAlternative(DotH):
    config = CongaConfig(
        name="n/s alternative",
        conga_direction=DOWN * (2 ** .5),
        doom_direction=LEFT * (2 ** .5),
        doom_safe_spots=[SS.NW, SS.W_INNER, SS.SW, SS.E_INNER],
        cleanse_safe_spots=[SS.NE, SS.E_OUTER, SS.SE, SS.W_OUTER])


class MaxwellFllipped(DotH):
    config = CongaConfig(
        name="Maxwell (flipped)",
        conga_direction=RIGHT * (2 ** .5),
        doom_direction=UP * (2 ** .5),
        doom_safe_spots=[SS.W_INNER, SS.NW, SS.NE, SS.E_INNER],
        cleanse_safe_spots=[SS.W_OUTER, SS.SW, SS.SE, SS.E_OUTER])


class Bien(DotH):
    config = CongaConfig(
        name="bien",
        conga_direction=RIGHT * (2 ** .5),
        doom_direction=UP * (2 ** .5),
        doom_safe_spots=[SS.NW, SS.W_INNER, SS.SW, SS.E_INNER],
        cleanse_safe_spots=[SS.NE, SS.E_OUTER, SS.SE, SS.W_OUTER])

class Victalis(DotH):
    party_members = ["Scholar", "Astrologian", "Gunbreaker", "Warrior", "Monk", "Ninja", "Dancer", "Summoner"]
    loops = 1
