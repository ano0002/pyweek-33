from ursina import *
from player import Player
from level import Map
from menus import StartMenu,EndMenu
from custom_stuff import Dialogue
from ui import Bubble

app = Ursina()

musics = [Audio("OST - dist 0",autoplay=False)]

sfx = {
    "clack" : Audio("SFX 1",autoplay=False),
    "door" : Audio("Door",autoplay=False)
}

window.color = color.black
scene.fog_density = 0

def next_level():
    if gamemap :
        scene.clear()
        start()
    else :
        freeze()
        restart()
        Dialogue("lore/lore3.dialogue",player1,player2,EndMenu).next()
    
gamemap = [(Map("levels/1.1.csv",end=next_level),"lore/lore0.dialogue"),(Map("levels/1.2.csv",end=next_level),"lore/lore1.dialogue"),(Map("levels/1.3.csv",end=next_level),"lore/lore2.dialogue")]

level,dialogue_file = (None,None)

    
def start():
    global level,dialogue_file,player1,player2
    sfx["door"].play()
    level,dialogue_file = gamemap.pop(0)
    level.generate()
    level.setup_camera()
    player1 = Player(level)
    player2 = Player(level,evil=True)
    level.add_player(player1)
    level.add_player(player2)
    restart()
    dialogue = Dialogue(dialogue_file,player1,player2,unfreeze)
    dialogue.next()

    
def restart():
    spawn_pos = level.get_spawns()
    for block in level.disappearings_block:
        if not block.solid :
            block.appear()
    player1.set_position((*spawn_pos[0],0))
    player1.revive()
    player2.set_position((*spawn_pos[1],0))
    player2.revive()

def unfreeze():
    player1.unfreeze()
    player2.unfreeze()
def freeze():
    player1.freeze()
    player2.freeze()

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
    if level != None :
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
    if key == "r" :
        restart()
        



app.run()