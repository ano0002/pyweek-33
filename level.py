from numpy import isin
from ursina import *
     
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
        super().__init__(model="plane",rotation_x=-90,position = position,color=color.black,**kwargs)

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


class Button(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,map,to_activate,**kwargs):
        super().__init__(model="cube",position = position,texture="button_ontop.png",**kwargs)
        self.collider = BoxCollider(self,center=(0,-0.2,0),size=(0.9,0.6,1))
        self.is_touched = False
        self.map = map
        self.to_activate = to_activate
        self.frames = 0

    def update(self):
        self.frames += 1
        if self.frames % 10 == 0 :
            self.is_touched= self.intersects().hit
            if self.is_touched :
                for indices in self.to_activate:
                    if self.map.disappearings_block[indices].solid :
                        self.map.disappearings_block[indices].disappear()
                self.texture = "pushed_button_ontop.png"
            else :
                for indices in self.to_activate:
                    if not self.map.disappearings_block[indices].solid :
                        self.map.disappearings_block[indices].appear()
                self.texture="button_ontop.png"
            
class Lever(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,to_activate,map,**kwargs):
        super().__init__(model="cube",position = position,texture="lever.png",**kwargs)
        self.collider = BoxCollider(self,center=(0,-0.2,0),size=(0.9,0.6,1))
        self.was_touched = False
        self.activated = False
        self.map = map
        self.to_activate = to_activate
        self.frames = 0

    def update(self):
        self.frames += 1
        if self.frames % 10 == 0 :
            if self.intersects().hit :
                if not self.was_touched :
                    self.activated = not self.activated
                    self.texture_scale = (1-2*self.activated,1)
                    for indices in self.to_activate:
                        self.map.disappearings_block[indices].toggle()
                self.was_touched = True
            else :
                self.was_touched = False
                

class DisappearingWall(Entity):
    drag = 0
    animated = False
    solid = True
    def __init__(self,position,mapdata,**kwargs):
        self.solid = True
        self.mapdata = mapdata.data
        super().__init__(model="cube",position = position,color=color.rgb(0,255,0),**kwargs)

    def disappear(self):
        self.mapdata[abs(self.Y)][abs(self.X)] = -1
        self.solid = False
        self.animate_color(color.clear)
        
    def appear(self):
        self.mapdata[abs(self.Y)][abs(self.X)] = 0
        self.animate_color(color.rgb(0,255,0))
        self.solid = True
    
    def toggle(self):
        if self.color == color.clear :
            self.appear()
        else :
            self.disappear()
    
    def on_click(self):
        self.toggle()
        
class Door(Entity):
    solid = False
    drag = 0
    animated = False
    def __init__(self,position,**kwargs):
        super().__init__(model="cube",position = position,texture="door",collider="box",**kwargs)
    
    def activate(self,player):
        player.freeze()
        self.activate = None


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
        if self.map.data[map_y][self.X] not in (17,18) and self.velocity == -1:
            self.velocity *= -1
        elif self.map.data[map_y][self.X+1] not in (17,18) and self.velocity == 1:
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
        self.last_y_change = -50
    
    def update(self):
        map_y = int(abs(self.position[1]))+1
        self.y += time.dt*self.velocity
        
        if abs(self.last_y_change-self.y)>0.7 :
            if self.map.data[map_y][self.X] not in (4,17) and self.velocity == -1:
                self.velocity *= -1
                self.last_y_change = self.y
            elif self.map.data[map_y-1][self.X] not in (4,17) and self.velocity == 1:
                self.velocity *= -1
                self.last_y_change = self.y
    
 
BLOCK_IDS = {
    -1 : Air,
    0:Plain,
    1:Vines1,
    2:Carpet1,
    3:Air,#lever
    4:VerticalSawBlade,
    5:Vines2,
    6:Vines3,
    7:Carpet2,
    8:Spike,
    9:DisappearingWall,
    10:Carpet3,
    11:Air,#button
    13:Door,
    15:Water,
    16:DisappearingWall,
    17:Air,#SawBlade Paths
    18:HorizontalSawBlade,
    20:Lever,
    25:Button,
}

class Map():
    def __init__(self,file) -> None:
        self.data = []
        self.to_animate = []
        self.load(file)
        self.disappearings_block = []
    
    def load(self,file):
        with open(file,"r") as f:
            lines = f.readlines()
            for line in lines[:-2]:
                self.data.append(list(map(lambda x : int(x),line.strip().split(","))))
                
            if lines[-2].strip() != "_":
                self.activator_buttons = [list(map(lambda x : int(x),line.strip().split(","))) for line in lines[-2].strip().split(";")]
            else : 
                self.activator_buttons = []
            if lines[-1].strip() != "_":
                self.activator_lever = [list(map(lambda x : int(x),line.strip().split(","))) for line in lines[-1].strip().split(";")]
            else : 
                self.activator_lever = []
                
        self.scale = self.width,self.height = len(self.data[1]),len(self.data)

    def generate(self):

        for i,line in enumerate(self.data):
            i = -i
            for j,block in enumerate(line):
                if block > -1 :
                    if block < 20 :
                        block = BLOCK_IDS[block](position=(j,i),above=self.data[abs(i)-1][j],mapdata=self)
                        if block.animated :
                            self.to_animate.append(block)
                        if isinstance(block,DisappearingWall):
                            self.disappearings_block.append(block)
                    elif block<25:
                        self.data[-i][j] = -1
                        block = BLOCK_IDS[20](position=(j,i),to_activate=self.activator_lever[block-20],map = self)
                        
                    elif block<30:
                        self.data[-i][j] = -1
                        block = BLOCK_IDS[25](position=(j,i),to_activate=self.activator_buttons[block-25],map = self)
                        
        for j,(up,down) in enumerate(zip(self.data[0],self.data[-1])):
            if down > -1 :
                block = BLOCK_IDS[down](position=(j,-self.height),above=down)
                if block.animated :
                    self.to_animate.append(block)
            if up > -1 :
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
        return spawns
    
    def is_solid(self,pos):
        if self.data[pos[0]][pos[1]]<0:
            return False
        return BLOCK_IDS[self.data[pos[0]][pos[1]]].solid
    
    def get_drag(self,pos):
        if self.data[pos[0]][pos[1]]<0:
            return 0
        return BLOCK_IDS[self.data[pos[0]][pos[1]]].drag
    
    def setup_camera(self):
        camera.orthographic = True
        camera.position = ((self.width-1)/2,-(self.height-1)/2)
        
        camera.fov = (max(self.width,self.height+40)-1)/1.72839506