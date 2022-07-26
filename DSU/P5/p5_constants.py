from manim import LEFT, RIGHT, UP, DOWN

INNER, OUTER = 4.25, 6.62
NW_X, NW_Y = 4.40, 5.05


class SS:
    NW = NW_X * LEFT + NW_Y * UP
    SW = NW_X * LEFT + NW_Y * DOWN
    NE = NW_X * RIGHT + NW_Y * UP
    SE = NW_X * RIGHT + NW_Y * DOWN
    W_OUTER = OUTER * LEFT
    W_INNER = INNER * LEFT
    E_OUTER = OUTER * RIGHT
    E_INNER = INNER * RIGHT