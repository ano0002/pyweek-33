from ursina import *

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

class Dialogue():
    def __init__(self,file,main,evil,after) -> None:
        self.users = {
            "main" : main,
            "evil" : evil,
            "mom" : (0,-2,0),
            "action" : (0,-2,0)
            }
        self.lines = []
        with open(file,"r") as f:
            for line in f.readlines():
                self.lines.append(line.strip().split(":"))
        self.after = after
    
    def next(self):
        from ui import Bubble   
        if len(self.lines) > 0 :
            user,text = self.lines.pop(0)
            if user == "mom":
                text = "mom : "+text
            elif user =="action" :
                text = "*"+text+"*"
            self.current = Bubble(text,self.users[user],next=self.next)
            self.current.appear()
            
        else :
            if self.after != None :
                self.after()

def average(liste):
    return sum(liste)/len(liste)

if __name__ =="__main__":
    app = Ursina()
    
    def input(key):
        if key == "space" or key == "left mouse down":
            entities = scene.entities.copy()
            for entity in  entities:
                if isinstance(entity,Bubble):
                    entity.skip()
                    
    Dialogue("lore/start.dialogue",(5,0,0),(-5,0,0),Func(print,"test"))
    
    _ed = EditorCamera()
    app.run()