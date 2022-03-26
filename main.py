from ursina import *
from player import Player
from level import Map
from start_menu import StartMenu
from ui import Bubble

app = Ursina(vsync = True)

musics = [Audio("OST - dist 0",autoplay=False)]

sfx = {
    "clack" : Audio("SFX 1",autoplay=False),
    "door" : Audio("Door",autoplay=False)
}

window.color = color.rgb(11,11,11)
scene.fog_density = 0

level = Map("levels/map.csv")


def start():
    global player1,player2
    sfx["door"].play()
    level.generate()
    level.setup_camera()
    spawn_pos = level.get_spawns()
    player1 = Player(level,position = spawn_pos[0],sprite_scale = (1,1))
    player2 = Player(level,position = spawn_pos[1],sprite_scale = (1,1),controls=['left arrow','up arrow','right arrow'])


StartMenu(on_start=start)

def next_music(current):
    musics[current%len(musics)].stop(destroy=False)
    nexti = (current+1)%len(musics)
    musics[nexti].play()
    invoke(next_music,nexti,delay=musics[nexti].length)

next_music(-1)

elapsed_time = 0
iteration = 0

def update():
    global elapsed_time,iteration
    for elem in level.to_animate :
        elem.next_frame(elapsed_time=elapsed_time,iteration = iteration)
    elapsed_time+=time.dt
    iteration+=1

def input(key):
    if key == "space" or key == "left mouse down":
        entities = scene.entities.copy()
        for entity in  entities:
            if isinstance(entity,Bubble):
                entity.skip()
    if key == "a" :
        bubble = Bubble("random text placeholder",position=player1)
        bubble.appear()
        


_ed = EditorCamera( )

app.run()