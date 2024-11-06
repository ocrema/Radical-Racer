
from ursina import *
from ursina.shaders import lit_with_shadows_shader
from car import Car
from checkpoint import Checkpoint
from hud import HUD
from worldgen import generate_trees
from random import random

app = Ursina(title=None)
window.cog_button.visible_setter(False)
window.entity_counter.visible_setter(False)
window.collider_counter.visible_setter(False)
#window.fps_counter.visible_setter(False)
Text.default_font = 'resources\ZeroCool.ttf'
Entity.default_shader = lit_with_shadows_shader
window.fullscreen = True
Audio.volume_multiplier = .3
ground = Entity(model='plane', scale=10000, texture='grass', texture_scale=(400, 400))

track = Entity(model='track_edge', scale=(100, 20, 100), collider='mesh',
               texture_scale=(100, 1), texture='concrete.jpg', rotation_y=90, flipped_faces= False)
track_road = Entity(model='track_road', scale=(100, 20, 100), color=color.light_gray, y=-.25, collider='mesh',
               texture_scale=(200, 2), texture='concrete.jpg', rotation_y=90, flipped_faces= False)

car = Car(track=track)

checkpoint = Checkpoint(visible=False)

camera.parent = car
camera.car_xz_distance = 10
camera.position = (0, 6, camera.car_xz_distance)
camera.rotation_x += 20
camera.rotate_speed = 20
camera.previous_steer_rotation = 0

hud = HUD(parent=camera.ui)

mouse.traverse_target = None

sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
Sky()
generate_trees(track, track_road)


def set_camera():
    camera.fov_setter(80 + car.velocity / 10 if car.velocity > 0 else 80)
    camera.rotation_y += camera.previous_steer_rotation

    if held_keys['right mouse']:
        camera.rotation_y_setter((camera.rotation_y + mouse.velocity[0] * 100) % 360)
    else:
        if camera.rotation_y <= camera.rotate_speed * time.dt or camera.rotation_y >= 360 - camera.rotate_speed * time.dt:
            camera.rotation_y_setter(0)
        else:
            camera.rotation_y += camera.rotate_speed * time.dt if camera.rotation_y > 180 else -1 * camera.rotate_speed * time.dt

    camera.previous_steer_rotation = car.wheel_angle * 4.5
    camera.rotation_y -= camera.previous_steer_rotation

    camera.x_setter(math.sin(math.radians(camera.rotation_y)) * camera.car_xz_distance * -1)
    camera.z_setter(math.cos(math.radians(camera.rotation_y)) * camera.car_xz_distance * -1)
    camera.y_setter(6)

def set_hud():
    hud.set_wheel_rotation(car.get_wheel_angle())
    hud.set_speedometer_rotation(car.velocity, 250)
    hud.car_icon.z = car.x / track.scale[0]
    hud.car_icon.x = -car.z / track.scale[2]
    hud.checkpoint_icon.z = checkpoint.x / track.scale[0]
    hud.checkpoint_icon.x = -checkpoint.z / track.scale[2]

    hud.x_setter(0)
    hud.y_setter(0)
    hud.z_setter(0)

    hud.set_controls_visible(held_keys['tab'])

def shake_logic():
    if car.velocity > 130:
        camera.x_setter(camera.x + (random() - .5) * (car.velocity - 130) * .001)
        camera.y_setter(camera.y + (random() - .5) * (car.velocity - 130) * .001)
        camera.z_setter(camera.z + (random() - .5) * (car.velocity - 130) * .001)
        hud.x_setter(hud.x + (random() - .5) * (car.velocity - 130) * .0002)
        hud.y_setter(hud.y + (random() - .5) * (car.velocity - 130) * .0002)
        hud.z_setter(hud.z + (random() - .5) * (car.velocity - 130) * .0002)
    if car.shake_timer > 0:
        camera.x_setter(camera.x + (random() - .5) * .5)
        camera.y_setter(camera.y + (random() - .5) * .5)
        camera.z_setter(camera.z + (random() - .5) * .5)
        hud.x_setter(hud.x + (random() - .5) * .05)
        hud.y_setter(hud.y + (random() - .5) * .05)

def race_logic():

    if checkpoint.race_stage != 1 and held_keys['r']:
        checkpoint.start_race()
        hud.restart_text.text = "'R' to restart race"
        hud.lap_text.text = 'Lap 1/' + str(checkpoint.num_laps)
        hud.checkpoint_text.text = 'Checkpoint 1/' + str(len(checkpoint.locations))
        hud.time_text.text = '0:00:00'
        hud.time_text_background.visible_setter(True)
        car.x_setter(0)
        car.z_setter(0)
        car.rotation_y_setter(0)
        car.deactivate_timer = 3.5
        car.velocity = 0
        hud.checkpoint_icon.visible_setter(True)
        hud.win_flag_left.visible_setter(False)
        hud.win_flag_right.visible_setter(False)

    elif checkpoint.race_stage == 3:
        hud.lap_text.text = ''
        hud.checkpoint_text.text = ''
        hud.checkpoint_icon.visible_setter(False)
        hud.win_flag_left.visible_setter(True)
        hud.win_flag_right.visible_setter(True)

    elif checkpoint.race_stage == 2:
        hud.lap_text.text = 'Lap ' + str(checkpoint.lap) + '/' + str(checkpoint.num_laps)
        hud.checkpoint_text.text = 'Checkpoint ' + str(checkpoint.location_index + 1) + '/' + str(len(checkpoint.locations))
        hud.time_text.text = (str(int(checkpoint.timer) // 60) + ':' + ('0' if int(checkpoint.timer) % 60 < 10 else '') + str(int(checkpoint.timer) % 60)
                              + ':' + str(int(checkpoint.timer * 10) % 10) + str(int(checkpoint.timer * 100) % 10))
        if car.intersects(checkpoint):
            checkpoint.next_location()



def update():

    set_camera()
    set_hud()
    shake_logic()
    race_logic()

    #if held_keys['l']:
    #    car.y += time.dt * 20

app.run()