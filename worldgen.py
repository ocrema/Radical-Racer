from ursina import *
from random import random

def generate_trees(track1, track2):
    outer_x_distance = 2000
    outer_z_distance = 3000
    num_trees = 60

    for loop in range(0, num_trees):
        tree = Entity(model='tree' + str(int(random() * 5 + 1)), collider='box', texture='treetex.png', scale=random()*3 + 3, rotation_y=random() * 360)

        while True:
            tree.x_setter((random() - .5) * outer_x_distance)
            tree.z_setter((random() - .5) * outer_z_distance)
            if not tree.intersects(track1) and not tree.intersects(track2):
                break
