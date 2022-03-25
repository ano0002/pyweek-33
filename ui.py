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
        self.next = next


    def on_click(self):
        self.skip()
    
    def skip(self):
        if self.appear_sequence and not self.appear_sequence.finished:
            self.appear_sequence.finish()
        else :
            if isinstance(self.next,Bubble):
                self.next.appear()
            elif self.next != None:
                self.next()
            self.next = None
            self.visible = False
            self.disable()
            
    
    def appear(self,text=None, speed=.025):
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

        self.appear_sequence.start()
        return self.appear_sequence



if __name__ == "__main__":
    import random,string
    
    #Create a function that generate random word
    def random_word(length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))
    
    #Create a function that generate random sentences using random word
    def random_sentence(length):
        return " ".join(random_word(random.randint(2,6)) for i in range(length))
    
    app = Ursina()
    window.color = color.rgb(11,11,11)
    scene.fog_density = 0
    def new_text():
        bubble = Bubble(random_sentence(5),position=(0,(random.random()-0.5)*0.5),next=new_text)
        bubble.appear()
    
    new_text()
    
    _ed = EditorCamera()
    app.run()