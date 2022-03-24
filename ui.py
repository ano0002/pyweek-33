from turtle import position
from ursina import *

class CustomButton(Entity):
    
    def __init__(self,texture, **kwargs):
        super().__init__(model="cube",texture=texture,collider="box",parent=camera.ui)
        self.disabled = False
        self._on_click = None
        self.highlight_scale = 1.1    # multiplier
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.original_scale = self.scale

    def on_mouse_enter(self):
        if not self.disabled and self.model:

            if self.highlight_scale != 1:
                self.scale = self.original_scale*self.highlight_scale



    def on_mouse_exit(self):
        if not self.disabled and self.model:
            if not mouse.left and self.highlight_scale != 1:
                self.scale = self.original_scale


    def on_click(self):
        if self.disabled:
            return
        
class Bubble(Text):
    
    def __init__(self,text,position,next=None, **kwargs):
        super().__init__(text=text[:1],collider="box",current_color =color.black)
        if isinstance(position,Entity):
            self.position = position.position + Vec3(position.scale_x/2,position.scale_y/2,0)
        else :
            self.position = position
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.full_text=text
        self.create_background()
        self.appear()


    def on_click(self):
        if self.appear_sequence:
            self.appear_sequence.finish()
        
    def appear(self,text=None, speed=.025):
        from ursina.ursinastuff import invoke
        self.enabled = True
        if self.appear_sequence:
            self.appear_sequence.finish()

        target_text = text if text != None else self.full_text
        self.full_text = target_text
        self.appear_sequence = Sequence()
        tn = self.text_nodes[0]
        tn.node().setText('')
        new_text = ''

        for char in target_text:
            new_text += char
            self.appear_sequence.append(Wait(speed))
            self.appear_sequence.append(Func(tn.node().setText, new_text))
            self.appear_sequence.append(Func(setattr,self.background,"scale_x",self.scale_x))

        self.appear_sequence.start()
        return self.appear_sequence



if __name__ == "__main__":
    app = Ursina()
    window.color = color.rgb(11,11,11)
    scene.fog_density = 0
    def new_text():
        Bubble("play_button sometimes again",position=(0,.2))
    play = CustomButton("play_button",scale = 0.2,on_click=new_text)
    
    _ed = EditorCamera()
    app.run()