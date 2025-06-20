from . import GameObject
from . import pygame_interface

def test_main():
    game_object = GameObject.GameObject()
    pygame_interface.pygame_interface(
        mouse_down_recall=game_object.handle_mouse_down,
        mouse_up_recall=game_object.handle_mouse_up,
        handle_key_down=game_object.handle_key_down,
        handle_key_up=game_object.handle_key_up,
        handle_quit=game_object.handle_quit,
        draw_screen=game_object.draw_screen,
        die_check=game_object.die_check,
    )