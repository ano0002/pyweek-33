from ursina import *
import time

class CustomAnimator():
    def __init__(self, animations, start_state):
        self.animations = animations    # dict
        self.set_state(start_state)

    def set_state(self, value):
        for key, anim in self.animations.items():
            anim.enabled = value == key

class Particle(Entity):
    def __init__(self, pos, start, maxi, duration, color=color.red, curve = curve.linear_boomerang,loop=False,velocity = (0,0), **kwargs):
        if not "model" in kwargs :
            kwargs["model"] = "cube"
        super().__init__(color=color, position=pos, scale=start,**kwargs)
        destroy(self,delay=duration)
        self.animate_scale(maxi, duration=duration,
                           curve=curve)
        self.animate_position(self.position+Vec3(velocity[0],velocity[1],0)*duration, duration=duration)


def average(liste):
    return sum(liste)/len(liste)