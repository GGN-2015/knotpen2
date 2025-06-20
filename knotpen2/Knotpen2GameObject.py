import pygame
import numpy

from . import GameObject
from . import MemoryObject
from . import constant_config

STATUS_LIST = [
    "free",        # 自由状态
    "select_dot",  # 选中了一个结点
    "select_line", # 选中了一条边
]

class Knotpen2GameObject(GameObject.GameObject):
    def __init__(self, memory_object:MemoryObject.MemoryObject) -> None:
        super().__init__()

        self.memory_object = memory_object
        self.status        = "free"

    def handle_mouse_up(self, button, x, y):
        super().handle_mouse_up(button, x, y)
        mouse_on_dot_id = None

        dot_dict = self.memory_object.get_dot_dict() # 绘制所有节点
        for dot_id in dot_dict:
            x_dot, y_dot = dot_dict[dot_id]
            if numpy.linalg.norm(numpy.array([x_dot - x, y_dot - y])) <= constant_config.CIRCLE_RADIUS + 1:
                mouse_on_dot_id = dot_id
                break
        
        if self.status == "free": # 自由状态创建点
            if mouse_on_dot_id is None:
                self.memory_object.new_dot(x, y)
            
            assert False

    def draw_screen(self, screen): # 绘制屏幕内容
        super().draw_screen(screen)

        dot_dict = self.memory_object.get_dot_dict() # 绘制所有节点
        for dot_id in dot_dict:
            x, y = dot_dict[dot_id]

            pygame.draw.circle(screen, constant_config.WHITE, (x, y), constant_config.CIRCLE_RADIUS)
            pygame.draw.circle(screen, constant_config.BLACK, (x, y), constant_config.CIRCLE_RADIUS, 1)