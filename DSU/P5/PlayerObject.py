from manim import *

class PlayerObject(Group):
    def __init__(self, job, static_spot, *args, **kwargs):
        super().__init__(**kwargs)

        self.job_object = ImageMobject(fr"Resources/{job}.png")
        self.job_object.scale(1.5)
        self.static_spot = static_spot
        self.doom_object = None
        self.has_doom = False

        self.add(self.job_object)

    def move_to_static_spot(self):
        self.move_to(self.static_spot)

    def apply_doom(self):
        self.doom_object = ImageMobject(r"Resources/Doom.png", z_index=1)
        self.doom_object.scale(1.5)
        self.doom_object.move_to(self[0].get_center())
        self.doom_object.shift(.15 * (UP + RIGHT))

        self.add(self.doom_object)
        self.has_doom = True

    def remove_doom(self):
        if self.doom_object:
            self.remove(self.doom_object)
        self.doom_object = None
        self.has_doom = False

    def get_center(self) -> np.ndarray:
        return self.job_object.get_center()
