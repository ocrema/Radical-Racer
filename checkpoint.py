from ursina import *
from ursina.color import rgba



class Checkpoint(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.model = Cylinder(resolution=32, radius=25, height=200)
        self.visible_setter(False)
        self.unlit_setter(True)
        self.color = rgba(1, 1, 1, .3)
        self.collider_setter('mesh')
        self.locations = [(0, 600),
                          (475, 850),
                          (445, 580),
                          (540, 270),
                          (490, -170),
                          (330, -850),
                          (-400, -650),
                          (-400, -200),
                          (-270, 300),
                          (-85, -325),
                          (0,0)]
        self.location_index = -1
        self.lap = 0
        self.race_stage = 0
        self.start_sound = Audio(sound_file_name='square', volume=.4, loop=True, autoplay=False)
        self.win_sound = Audio(sound_file_name='win.mp3', autoplay=False)
        self.woosh_sound = Audio(sound_file_name='woosh.mp3', autoplay=False, volume=.3, pitch=.5)
        self.next_location()
        self.woosh_sound.stop()
        self.timer = 0
        self.num_laps = 3


        for key, value in kwargs.items():
            setattr(self, key, value)

    def start_race(self):
        self.location_index = -1
        self.lap = 0
        self.next_location()
        self.woosh_sound.stop()
        self.visible_setter(True)
        self.race_stage = 1
        self.timer = 0
        invoke(self.start_sound.pitch_setter, 1, delay=.5)
        invoke(self.start_sound.play, delay=.5)
        invoke(self.start_sound.stop, delay=1)
        invoke(self.start_sound.play, delay=1.5)
        invoke(self.start_sound.stop, delay=2)
        invoke(self.start_sound.play, delay=2.5)
        invoke(self.start_sound.stop, delay=3)
        invoke(self.start_sound.pitch_setter, 2, delay=3.5)
        invoke(setattr, self, 'race_stage', 2, delay=3.5)
        invoke(self.start_sound.play, delay=3.5)
        invoke(self.start_sound.stop, delay=4)


    def next_location(self):
        self.location_index = (self.location_index + 1) % len(self.locations)
        if self.location_index == 0:
            if self.lap == 3:
                self.race_stage = 3
                self.visible_setter(False)
                self.win_sound.play()
            else:
                self.lap += 1
        self.x_setter(self.locations[self.location_index][0])
        self.z_setter(self.locations[self.location_index][1])
        self.woosh_sound.play(0)


    def update(self):
        if self.race_stage == 2:
            self.timer += time.dt
