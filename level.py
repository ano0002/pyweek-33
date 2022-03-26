from ursina import *

class Water(Entity):
    solid = False
    drag = 0.8
    animated = True
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="water.png",color = color.white,**kwargs)
        
    def next_frame(self,elapsed_time,**kwargs):
        self.texture_offset = (0,elapsed_time/5)
  
class Carpet1(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="carpet_1.png",**kwargs)
class Carpet2(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="carpet_2.png",**kwargs)        
class Carpet3(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="carpet_3.png",**kwargs)

class Vines1(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="vines_1.png",**kwargs)
class Vines2(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="vines_2.png",**kwargs)
class Vines3(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="vines_3.png",**kwargs)

  
class Door(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="door",collider="box",**kwargs)
    
    def activate(self,player):
        print("stuff")
        self.activate = None
     
class Air():
    solid = False
    drag = 0
    animated = False
    def __init__(self,**kwargs):
        pass

class Plain(Entity):
    solid = True
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,color=color.black,**kwargs)

class Spike(Entity):
    solid = False
    drag = 0
    animated = False
    deadly=True
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="spike",**kwargs)
        self.collider = BoxCollider(self,center=(0,-0.2,0),size=(1,0.6,1))
        
class HorizontalSawBlade(Animation):
    solid = False
    drag = 0
    animated = False
    deadly=True
    def __init__(self,position,mapdata,**kwargs):
        super().__init__("saw",fps=4,collider="box",position = position,scale=1,**kwargs)
        self.velocity = 1
        self.map = mapdata
    
    def update(self):
        map_y = int(abs(self.position[1]))
        self.x += time.dt*self.velocity
        if self.map.data[map_y][self.X] not in (5,6) and self.velocity == -1:
            self.velocity *= -1
        elif self.map.data[map_y][self.X+1] not in (5,6) and self.velocity == 1:
            self.velocity *= -1
            
class VerticalSawBlade(Animation):
    solid = False
    drag = 0
    animated = False
    deadly=True
    def __init__(self,position,mapdata,**kwargs):
        super().__init__("saw",fps=4,collider="box",position = position,scale=1,**kwargs)
        self.velocity = 1
        self.map = mapdata
        self.last_y_change = self.y
    
    def update(self):
        map_y = int(abs(self.position[1]))+1
        self.y += time.dt*self.velocity
        
        if abs(self.last_y_change-self.y)>0.5 :
            if self.map.data[map_y][self.X] not in (7,6) and self.velocity == -1:
                self.velocity *= -1
                self.last_y_change = self.y
            elif self.map.data[map_y-1][self.X] not in (7,6) and self.velocity == 1:
                self.velocity *= -1
                self.last_y_change = self.y
    
 
BLOCK_IDS = {
    -1 : Air,
    0:Carpet1,
    1:Carpet2,
    2:Carpet3,
    3:Spike,
    4:Vines1,
    5:Vines2,
    6:Vines3,
    7 : Plain,
    8 : Door,
}
"""
    2 : Water,
    3 : Plain,
    4 : Spike,
    5 : HorizontalSawBlade,
    6 : Air,
    7 : VerticalSawBlade,
"""
class Map():
    def __init__(self,file) -> None:
        self.data = []
        self.to_animate = []
        self.load(file)
    
    def load(self,file):
        with open(file,"r") as f:
            for line in f.readlines():
                self.data.append(list(map(lambda x : int(x),line.strip().split(","))))

        self.scale = self.width,self.height = len(self.data[1]),len(self.data)

    def generate(self):

        for i,line in enumerate(self.data):
            i = -i
            for j,block in enumerate(line):
                if block > 0 :
                    block = BLOCK_IDS[block](position=(j,i),above=self.data[abs(i)-1][j],mapdata=self)
                    if block.animated :
                        self.to_animate.append(block)
        for j,(up,down) in enumerate(zip(self.data[0],self.data[-1])):
            if down > 0 :
                block = BLOCK_IDS[down](position=(j,-self.height),above=down)
                if block.animated :
                    self.to_animate.append(block)
            if up > 0 :
                block = BLOCK_IDS[up](position=(j,1),above=self.data[0][j])
                if block.animated :
                    self.to_animate.append(block)

        self.background = Entity(model="cube",scale=self.scale,position=((self.width-1)/2,-(self.height-1)/2,1),color=color.white)#,texture="back.jpg")

    def get_spawns(self):
        spawns = []
        for i in self.data:
            for j in i :
                if j <-1 :
                    spawns.append(None)
                    
        for i,val in enumerate(self.data):
            for j,block in enumerate(val) :
                if block <-1 :
                    spawns[abs(block)-2] = (j,-i)
                    self.data[i][j] = -1
        return spawns
    
    def is_solid(self,pos):
        return BLOCK_IDS[self.data[pos[0]][pos[1]]].solid
    
    def get_drag(self,pos):
        return BLOCK_IDS[self.data[pos[0]][pos[1]]].drag
    
    def setup_camera(self):
        camera.orthographic = True
        camera.position = ((self.width-1)/2,-(self.height-1)/2)
        camera.fov = (self.width-1)/1.72839506