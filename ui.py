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



if __name__ == "__main__":
    app = Ursina()
    window.color = color.rgb(11,11,11)
    scene.fog_density = 0
    CustomButton("play_button",scale = 0.2,on_click=Func(print,"hey"))
    app.run()