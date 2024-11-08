from direct.showbase.ShowBaseGlobal import hidden
from ursina import *

class HUD(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.steering_wheel = Sprite(model='quad', texture='steering_wheel.png', parent=self, y=-.4, scale=.04)
        self.speedometer = Sprite(model='quad', texture='speedometer.png', scale=.06, parent=self, position=(-.5*window.aspect_ratio+.2,-.3))
        self.speed_text = Text(position=(-.5*window.aspect_ratio+.12, -.35), scale=1.5, parent=self)
        self.speedometer_pointer = Sprite(model='quad', texture='speedometer_pointer.png', scale=.03, parent=self, position=(-.5*window.aspect_ratio+.2, -.3))
        self.track = Sprite(model='track_road', parent=self, position=(.5*window.aspect_ratio-.2, -.25, -1), rotation_x=0, rotation_y=90, rotation_z=90, scale=.018, color=color.gray)
        self.car_icon = Sprite(model='circle', color=color.red, parent=self.track, rotation_x = 90)
        self.checkpoint_icon = Sprite(model='circle', color=color.white, parent=self.track, rotation_x=90, visible=False)
        self.open_controls_text = Text(position=(-.5*window.aspect_ratio+.1, .48), scale=1, parent=self, text="Hold 'tab' for controls")
        self.restart_text = Text(position=(-.5*window.aspect_ratio+.1, .45), scale=1.5, parent=self, text="'R' to start race")
        self.lap_text = Text(position=(-.5*window.aspect_ratio+.1, .4), scale=1.5, parent=self)
        self.checkpoint_text = Text(position=(-.5*window.aspect_ratio+.1, .35), scale=1.5, parent=self)
        self.time_text_background = Sprite(model='quad', color=color.dark_gray, parent=self, scale=(.4, .1), unlit=True,
                                           position=(.5*window.aspect_ratio-.5, .42), visible=False)
        self.time_text = Text(position=(.5*window.aspect_ratio-.5, .42), origin=(0,0), scale=3, parent=self)
        self.win_flag_left = Sprite(model='quad', texture='checkerboard.png', parent=self, scale=(4*.25, 5*.25), unlit=True,
                                           position=(.5*window.aspect_ratio-.25, .42), visible=False)
        self.win_flag_right = Sprite(model='quad', texture='checkerboard.png', parent=self, scale=(4*.25, 5*.25), unlit=True,
                                    position=(.5*window.aspect_ratio-.75, .42), visible=False)
        self.controls_background = Sprite(model='quad', parent=self, scale=(1,.6),
                                    position=(0,0), visible=False, color=color.light_gray)
        self.controls_title = Text(position=(0, .2), origin=(0,0), scale=3.5, parent=self, text='Controls:', color=color.dark_gray, visible=False)
        self.controls_text = Text(position=(0, -.05), origin=(0, 0), scale=1.8, parent=self,
                                  text='Forward: W, ↑\nReverse: S, ↓\nTurn Left: A, ←\nTurn Right: D, →\n'
                                        'Brake: S, ↓, Space\nStart Race: R\nPan Camera: Right Click',
                                   color=color.dark_gray, visible=False)


        for key, value in kwargs.items():
            setattr(self, key, value)


    def set_wheel_rotation(self, angle):
        self.steering_wheel.rotation_z = angle

    def set_speedometer_rotation(self, velocity, max_velocity):
        self.speedometer_pointer.rotation_z = -90 + (abs(velocity) / max_velocity) * 240
        self.speed_text.text = '0' if abs(velocity) < 1 else abs(int(velocity))

    def set_controls_visible(self, value):
        self.controls_background.visible_setter(value)
        self.controls_title.visible_setter(value)
        self.controls_text.visible_setter(value)

