from ursina import *
from ursina.color import black


class Car(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.model = 'car2'
        self.flipped_faces_setter(False)
        self.double_sided_setter(True)
        self.y = .25
        self.texture = 'Palette_Red.png'
        self.collider = 'box'
        self.scale = 1

        self.acceleration = 40
        self.drag_mult = .87
        self.drag_sub = 3
        self.max_wheel_angle = 1
        self.wheel_turn_rate = 5
        self.brake_mult = .2
        self.brake_sub = 3
        self.wheel_center_rate = 2
        self.reverse_acceleration = 15
        self.crash_deactivate_time = .85
        self.deactivate_timer = 0
        self.shake_timer = 0

        self.wheel_angle = 0
        self.velocity = 0

        self.min_engine_pitch = .9
        self.active_engine_pitch_function = lambda x : 1 + abs(x) / 300
        self.engine_pitch_drop_rate = .4
        self.engine_pitch = self.min_engine_pitch

        self.engine_sounds = [Audio(sound_file_name='car_engine.mp3', volume=.5, pitch=self.engine_pitch, autoplay=True, loop=True) for i in range(7)]
        for i in range(len(self.engine_sounds)):
            self.engine_sounds[i].play(start=(i / len(self.engine_sounds) * self.engine_sounds[0].length_getter()))

        self.crash_sound = Audio(sound_file_name='crash.mp3', autoplay=False, pitch=.9)
        self.brake_sounds = [Audio(sound_file_name='brake.mp3', autoplay=False, pitch=.5) for i in range(2)]
        self.wind_sound = Audio(sound_file_name='wind.mp3', volume=0, loop=True, autoplay=True)

        self.wheels = [Entity(model='wheel', parent=self, x=.9, z=1.37, y=.1, texture='Palette_Red.png') for i in range(4)]
        self.wheels[1].x *= -1
        self.wheels[2].z *= -1
        self.wheels[1].rotation_z = 180
        self.wheels[3].x *= -1
        self.wheels[3].z *= -1
        self.wheels[3].rotation_z = 180

        for key, value in kwargs.items():
            setattr(self, key, value)


    def turn_wheel_right(self):
        self.wheel_angle += self.wheel_turn_rate * time.dt
        if self.wheel_angle > self.max_wheel_angle:
            self.wheel_angle = self.max_wheel_angle

    def turn_wheel_left(self):
        self.wheel_angle -= self.wheel_turn_rate * time.dt
        if self.wheel_angle < -self.max_wheel_angle:
            self.wheel_angle = -self.max_wheel_angle

    def accelerate(self):
        self.velocity += self.acceleration * time.dt

    def reverse(self):
        self.velocity -= self.reverse_acceleration * time.dt

    def brake(self):
        self.velocity *= self.brake_mult ** time.dt
        if self.velocity > 0:
            self.velocity -= self.brake_sub * time.dt
            if self.velocity < 0:
                self.velocity = 0
        elif self.velocity < 0:
            self.velocity += self.brake_sub * time.dt
            if self.velocity > 0:
                self.velocity = 0


    def move(self):
        if self.wheel_angle != 0 and self.velocity != 0:
            self.rotation_y += time.dt * math.sin(self.wheel_angle) * 100 * (1 if self.velocity > 0 else -1)
        self.position += self.forward * self.velocity * time.dt
        self.velocity *= self.drag_mult ** time.dt
        if self.velocity > 0:
            self.velocity -= self.drag_sub * time.dt
            if self.velocity < 0:
                self.velocity = 0
        elif self.velocity < 0:
            self.velocity += self.drag_sub * time.dt
            if self.velocity > 0:
                self.velocity = 0


    def center_wheel(self):
        if self.wheel_angle > 0:
            self.wheel_angle -= self.wheel_center_rate * time.dt
            if self.wheel_angle < 0:
                self.wheel_angle = 0
        elif self.wheel_angle < 0:
            self.wheel_angle += self.wheel_center_rate * time.dt
            if self.wheel_angle > 0:
                self.wheel_angle = 0

    def update(self):

        # prevent jolts during lag spikes
        if time.dt >= 1/20:
            return

        self.previous_position = self.position
        self.previous_rotation = self.rotation

        self.center_wheel()
        if held_keys['a'] or held_keys['left arrow']:
            self.turn_wheel_left()
        if held_keys['d'] or held_keys['right arrow']:
            self.turn_wheel_right()

        self.wheels[0].rotation_y = math.degrees(self.wheel_angle) / 2
        self.wheels[1].rotation_y = math.degrees(self.wheel_angle) / 2

        for wheel in self.wheels:
            wheel.rotation_x_setter((wheel.rotation_x + (self.velocity * time.dt * 360) / (math.pi * .5)) % 360)

        if (held_keys['w'] or held_keys['up arrow']) and not (held_keys['space'] or held_keys['s'] or held_keys['down arrow']) and self.deactivate_timer <= 0:
            self.accelerate()
            self.engine_pitch = self.active_engine_pitch_function(self.velocity)
        elif (held_keys['s'] or held_keys['down arrow']) and not held_keys['space'] and self.velocity <= 0 and self.deactivate_timer <= 0:
            self.reverse()
            self.engine_pitch = self.active_engine_pitch_function(self.velocity)
        else:
            self.engine_pitch -= self.engine_pitch_drop_rate * time.dt
            if self.engine_pitch < self.min_engine_pitch:
                self.engine_pitch = self.min_engine_pitch
            if held_keys['space'] or held_keys['s'] or held_keys['down arrow']:
                self.brake()
                if self.velocity > 70 and not self.brake_sounds[0].playing_getter():
                    self.brake_sounds[0].play(0)
                    self.brake_sounds[1].play(.3)

        self.wind_sound.volume_setter(abs(self.velocity) / 50)


        for sound in self.engine_sounds:
            sound.pitch_setter(self.engine_pitch)


        self.move()

        if self.intersects(self.track):
            self.position = self.previous_position
            self.rotation = self.previous_rotation
            self.velocity = 0
            self.crash_sound.play(0)
            self.deactivate_timer = self.crash_deactivate_time
            self.shake_timer = .5


        if self.deactivate_timer > 0:
            self.deactivate_timer -= time.dt
        if self.shake_timer > 0:
            self.shake_timer -= time.dt


    def get_wheel_angle(self):
        return (self.wheel_angle / self.max_wheel_angle) * 90