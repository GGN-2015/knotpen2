from . import GameObject
from . import pygame_interface

class ClassBinder:
    def __init__(self, game_object:GameObject.GameObject) -> None:
        assert isinstance(game_object, GameObject.GameObject)
        self.game_object = game_object
    
    def mainloop(self):
        pygame_interface.pygame_interface(
            mouse_down_recall=self.game_object.handle_mouse_down,
            mouse_up_recall=self.game_object.handle_mouse_up,
            handle_key_down=self.game_object.handle_key_down,
            handle_key_up=self.game_object.handle_key_up,
            handle_quit=self.game_object.handle_quit,
            draw_screen=self.game_object.draw_screen,
            die_check=self.game_object.die_check,
        )