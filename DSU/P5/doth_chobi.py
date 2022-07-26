import random
from dataclasses import dataclass

from manim import *

from PlayerObject import PlayerObject
from p5_constants import SS

FLEX_OFFSET = 2 ** .5
STATIC_OFFSET = 2 ** .5 / 2


class MeteorSpots:
    NE_FLEX = FLEX_OFFSET * (RIGHT + UP)
    NE_STATIC = NE_FLEX + STATIC_OFFSET * RIGHT
    SE_FLEX = FLEX_OFFSET * (RIGHT + DOWN)
    SE_STATIC = SE_FLEX + STATIC_OFFSET * RIGHT
    SW_FLEX = FLEX_OFFSET * (LEFT + DOWN)
    SW_STATIC = SW_FLEX + STATIC_OFFSET * LEFT
    NW_FLEX = FLEX_OFFSET * (LEFT + UP)
    NW_STATIC = NW_FLEX + STATIC_OFFSET * LEFT

@dataclass
class Pair:
    flex: PlayerObject
    static: PlayerObject

    def members(self) -> list[PlayerObject]:
        return [self.flex, self.static]

    def dooms(self) -> list[PlayerObject]:
        return [player for player in self.members() if player.has_doom]

    def cleanses(self) -> list[PlayerObject]:
        return [player for player in self.members() if not player.has_doom]


class Party:
    def __init__(self, party_members):
        self.ne = Pair(
            flex=PlayerObject(party_members[0], MeteorSpots.NE_FLEX, z_index=1),
            static=PlayerObject(party_members[1], MeteorSpots.NE_STATIC, z_index=1))
        self.se = Pair(
            flex=PlayerObject(party_members[2], MeteorSpots.SE_FLEX, z_index=1),
            static=PlayerObject(party_members[3], MeteorSpots.SE_STATIC, z_index=1))
        self.sw = Pair(
            flex=PlayerObject(party_members[4], MeteorSpots.SW_FLEX, z_index=1),
            static=PlayerObject(party_members[5], MeteorSpots.SW_STATIC, z_index=1))
        self.nw = Pair(
            flex=PlayerObject(party_members[6], MeteorSpots.NW_FLEX, z_index=1),
            static=PlayerObject(party_members[7], MeteorSpots.NW_STATIC, z_index=1))

    def members(self) -> list[PlayerObject]:
        return self.ne.members() + self.se.members() + self.sw.members() + self.nw.members()

    def pairs(self) -> list[Pair]:
        return [self.ne, self.se, self.sw, self.nw]

# manim -pqh DSU/P5/doth_chobi.py -r 1080,1080 Chobi
# manim -o test --format=gif -r 1080,1080 DSU/P5/doth_chobi.py Chobi


class Chobi(Scene):
    party_members = [
        "DarkKnight", "Summoner",
        "Scholar", "Ninja",
        "Gunbreaker", "Dancer",
        "Astrologian", "Monk",
    ]

    loops = 3

    def construct(self):
        self.swaps = []
        self.loop_count = 0
        self.add(ImageMobject(r"Resources/dsu-p4-cropped.png", z_index=-1).scale_to_fit_height(14))

        boss = ImageMobject(r"Resources/Boss.png", z_index=0).scale(2).shift(.1 * UP)
        target = SVGMobject(r"Resources/Target.svg", z_index=0)
        self.boss_group = Group(boss, target).shift(UP * 3)

        self.party = Party(self.party_members)

        self.players = self.party.members()

        self.starting_screen()

        for i in range(self.loops):
            self.loop()

    def starting_screen(self):
        text = Text("Chobi DotH", font="Calibri", font_size=128)
        self.add(text)

        sig = VGroup(Text("🤍", font_size=24, color=BLUE), Text("tae", color=LIGHT_PINK)).arrange(RIGHT, buff=.1)
        sig.shift(6 * RIGHT + 6.2 * DOWN).set_opacity(.4)
        self.add(sig)

        self.add(self.boss_group)

        for i in [1, 2, 3, 6]:
            self.players[i].apply_doom()

        for player in self.players:
            player.move_to_static_spot()
            self.add(player)

        self.wait(.5)
        self.fade_out_all(text)
        self.reset()


    def fade_in_players(self):
        for player in self.players:
            player.move_to(random.uniform(-1, 1) * RIGHT + random.uniform(-1, 1) * UP)
        self.play(*[FadeIn(player) for player in self.players])

    dooms_to_apply = [
        [1, 2, 3, 6],
        [2, 3, 4, 5],
        [0, 1, 5, 7],
    ]

    def apply_doom(self):
        if self.loop_count < len(self.dooms_to_apply):
            for n in self.dooms_to_apply[self.loop_count]:
                self.players[n].apply_doom()
        else:
            for player in random.sample(self.players, 4):
                player.apply_doom()

    def doom_shift(self):
        two_doom_pairs: list[Pair] = []
        no_doom_pairs: list[Pair] = []

        for pair in self.party.pairs():
            doom_count = len(pair.dooms())
            if doom_count == 2:
                two_doom_pairs.append(pair)
            elif doom_count == 0:
                no_doom_pairs.append(pair)

        animations = []

        def swap(pair1, pair2):
            pair1_spot = pair1.flex.get_center()
            pair2_spot = pair2.flex.get_center()

            pair1.flex, pair2.flex = pair2.flex, pair1.flex

            self.swaps.append([pair1, pair2])

            return [pair1.flex.animate.move_to(pair1_spot), pair2.flex.animate.move_to(pair2_spot)]

        if len(two_doom_pairs) == 1:
            animations.extend(swap(two_doom_pairs[0], no_doom_pairs[0]))
        elif len(two_doom_pairs) == 2:
            if len(self.party.nw.dooms()) == len(self.party.sw.dooms()):
                animations.extend(swap(self.party.nw, self.party.ne))
                animations.extend(swap(self.party.sw, self.party.se))
            else:
                animations.extend(swap(self.party.nw, self.party.sw))
                animations.extend(swap(self.party.ne, self.party.se))

        if animations:
            self.play(*animations)

    def move_to_safe_spot(self):
        animations = [
            self.party.ne.dooms()[0].animate.move_to(SS.NE),
            self.party.se.dooms()[0].animate.move_to(SS.E_INNER),
            self.party.sw.dooms()[0].animate.move_to(SS.W_INNER),
            self.party.nw.dooms()[0].animate.move_to(SS.NW),

            self.party.ne.cleanses()[0].animate.move_to(SS.E_OUTER),
            self.party.se.cleanses()[0].animate.move_to(SS.SE),
            self.party.sw.cleanses()[0].animate.move_to(SS.SW),
            self.party.nw.cleanses()[0].animate.move_to(SS.W_OUTER),
        ]

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

    def fade_out_all(self, extras=[]):
        animations = [FadeOut(self.boss_group)]
        animations.extend([FadeOut(player) for player in self.players])
        if extras:
            animations.extend([FadeOut(extra) for extra in extras])
        self.play(*animations)

    def reset(self):
        for player in self.players:
            player.remove_doom()

        for swap in self.swaps:
            swap[0].flex, swap[1].flex = swap[1].flex, swap[0].flex
        self.swaps = []

    def loop(self):
        self.fade_in_players()
        self.wait(.5)
        self.play(FadeIn(self.boss_group))
        self.wait(.5)
        self.play(*[player.animate.move_to_static_spot() for player in self.players])
        self.wait(.5)
        self.apply_doom()
        self.wait(1)
        self.doom_shift()
        self.wait(1)
        self.move_to_safe_spot()
        self.wait(1)
        cleanse_puddles = self.show_cleanse_puddles()
        self.wait(.5)
        self.fade_out_all(cleanse_puddles)
        self.wait(.5)
        self.reset()

        self.loop_count += 1