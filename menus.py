from ursina import *
from ui import CustomButton


class StartMenu():
    
    def __init__(self,on_start) -> None:
        self.button = CustomButton("play_button",scale = 0.2,on_click=self.start)
        self.on_start = on_start
    
    def start(self):
        camera.overlay.color = color.black
        destroy(self.button)
        self.on_start()
        camera.overlay.color = color.clear

class EndMenu():
    
    def __init__(self) -> None:
        scene.clear()
        Text(text="Good job for finishing the game\n\nI hope you enjoyed it",size=.05,position=(-.4,.1),current_color=color.white,font="assets\\fonts\\Retro Gaming.ttf")