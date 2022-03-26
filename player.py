import math
from ursina import *
from custom_stuff import CustomAnimator,average,Particle


class Jump(Animation):
    def __init__(self,pos, **kwargs):
        super().__init__("jump",scale=(2,2/3),origin = (0,-.5),color=color.black,position = pos,loop=False,autoplay=True,**kwargs)

class Turn(Animation):
    def __init__(self,pos,direction=1, **kwargs):
        super().__init__("turn",texture_scale = (direction,1),scale=.2,color=color.black,origin = (0,-.5),position = pos,loop=False,autoplay=True,**kwargs)

class Player(Entity):
    def __init__(self,level,speed = 6,gravity = 1,max_jumps =2,sprite_scale=1,controls = ["q","z","d"],**kwargs):
        super().__init__(model="cube",collider="box",scale = (0.9,0.3), **kwargs)
        self.visible_self = False
        
        self.map = level
        
        self.velocity = Vec2(0,0)
        self.speed = speed
        self.gravity = gravity
        
        self.jumps = 0
        self.max_jumps = max_jumps
        
        self.controls = controls
        
        world_sprite_scale = (sprite_scale[0]/self.scale_x,sprite_scale[1]/self.scale_y)
        sprite_y = self.y-self.scale_y/2
        idle = Animation("idle",parent = self,scale=world_sprite_scale,origin=(0,-.5),color = self.color,world_y=sprite_y)
        right = Animation("walk",parent = self,scale=world_sprite_scale,origin=(0,-.5),color = self.color,world_y=sprite_y)
        left = Animation("walk",parent = self,scale=world_sprite_scale,origin=(0,-.5),color = self.color,texture_scale = (-1,1),world_y=sprite_y)
        self.sprite = CustomAnimator(
            animations = {
                'idle' : idle,
                'right' : right,
                'left' : left
            },
            start_state="idle"
        )
        self.sprite.set_state("idle")
        self.frames = 0
        
    def update(self):
        self.frames +=1
        x = self.x +0.5 +self.velocity[0]*time.dt
        right = int(x+self.scale_x/2)
        left = int(x-self.scale_x/2)
        y = abs(self.y)+0.5
        top = int(y-self.scale_y/2)
        bottom = int(y+self.scale_y/2)
        
        
        if max(left,right) < self.map.width and self.x+0.5 +self.velocity[0]*time.dt-self.scale_x/2 > 0 :
            if not self.map.is_solid((top,left)) and \
               not self.map.is_solid((top,right)) and \
               not self.map.is_solid((bottom,left)) and \
               not self.map.is_solid((bottom,right)) :
                    self.x += self.velocity[0]*time.dt
                
        x = self.x +0.5 
        right = int(x+self.scale_x/2)
        left = int(x-self.scale_x/2)
        y = abs(self.y)+0.5-self.velocity[1]*time.dt
        top = int(y-self.scale_y/2)
        bottom = int(y+self.scale_y/2)
        
        if max(top,bottom) < self.map.height :
            if (top,bottom) != (0,0) :
                if not self.map.is_solid((top,left)) and \
                not self.map.is_solid((top,right)) :
                        if not self.map.is_solid((bottom,left)) and \
                            not self.map.is_solid((bottom,right)) :
                                self.y += self.velocity[1]*time.dt
                                self.velocity[1] -= self.gravity*time.dt*30
                        else :
                            self.jumps = 0
                            self.velocity[1] = 0
                        
                else :
                    self.velocity[1] = 0
            else :
                self.velocity[1] = 0
            drag = 1-average([self.map.get_drag((top,left)), self.map.get_drag((top,right)), self.map.get_drag((bottom,left)), self.map.get_drag((bottom,right))])
        else :
            drag = 1-average([self.map.get_drag((top,left)), self.map.get_drag((top,right))])
            self.die()
            
        self.velocity[0] = (held_keys[self.controls[2]]-held_keys[self.controls[0]])*self.speed
        
        self.velocity[0] *= drag
        self.velocity[1] *= .4+drag*.6
        
        if self.velocity[0] == 0 :
            self.sprite.set_state("idle")
        elif self.velocity[0]< 0 :
            self.sprite.set_state("left")
        elif self.velocity[0]> 0 :
            self.sprite.set_state("right")
            
        self.grounded = abs(self.velocity[1])<self.gravity/2
        touching = self.intersects()
        if touching.hit :
            for entity in touching.entities:
                if hasattr(entity,"deadly") and entity.deadly == True:
                    self.die()
                if hasattr(entity,"activate") and entity.activate != None:
                    entity.activate(self)
        
    def input(self,key):
        if key == self.controls[1]:
            if self.jumps < self.max_jumps :
                jump = Jump(self.position-Vec3(0,self.scale_y/2,0))
                destroy(jump,delay = .35)
                self.velocity[1] = 12
                self.jumps += 1
                
        elif key == self.controls[0]:
            if self.grounded :
                turn = Turn(self.position-Vec3(-self.scale_x/2,self.scale_y/2,0),direction=-1)
                destroy(turn,delay = .35)
                
        elif key == self.controls[2]:
            if self.grounded :
                turn = Turn(self.position-Vec3(self.scale_x/2,self.scale_y/2,0))
                destroy(turn,delay = .35)
    
    def die(self):
        self.disable()
        nb = 10
        for i in range(nb):
                    angle = (360/nb) * i
                    x = math.sin(math.radians(angle))*6
                    y = math.cos(math.radians(angle))*6
                    Particle(pos=self.position,
                             start=(0.01, 0.01),
                             maxi=(0.08, 0.08),
                             curve = curve.linear_boomerang,
                             duration = 0.2,
                             velocity=(x, y),
                             color = color.black)
