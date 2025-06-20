import pygame
import numpy

from . import GameObject
from . import MemoryObject
from . import constant_config

STATUS_LIST = [
    "free",        # 自由状态
    "select_dot",  # 选中了一个结点
    "select_line", # 选中了一条边
    "move_dot",    # 移动一个节点
]

class Knotpen2GameObject(GameObject.GameObject):
    def __init__(self, memory_object:MemoryObject.MemoryObject) -> None:
        super().__init__()

        self.memory_object = memory_object
        self.status         = "free"
        self.focuse_dot     = None
        self.focuse_line    = None
        self.mouse_down     = False
        self.actually_moved = False

    def handle_mouse_down(self, button, x, y): # 鼠标按下
        super().handle_mouse_down(button, x, y)
        self.mouse_down = True

        mouse_on_dot_id = None

        dot_dict = self.memory_object.get_dot_dict() # 绘制所有节点
        for dot_id in dot_dict:
            x_dot, y_dot = dot_dict[dot_id]
            if numpy.linalg.norm(numpy.array([x_dot - x, y_dot - y])) <= constant_config.CIRCLE_RADIUS + 1:
                mouse_on_dot_id = dot_id
                break
        
        if self.status == "free":
            if mouse_on_dot_id is not None: # 开始移动节点
                self.focuse_dot = mouse_on_dot_id
                self.status = "move_dot"
                self.actually_moved = False

    def handle_mouse_move(self, x, y):
        super().handle_mouse_move(x, y)

        if self.status == "move_dot" and self.focuse_dot is not None:
            self.memory_object.set_dot_position(self.focuse_dot, x, y)
            self.actually_moved = True

    def handle_left_mouse_up(self, x, y):
        self.mouse_down = False
        mouse_on_dot_id = None

        if self.status == "move_dot": # 移动节点结束
            self.status = "free"

        dot_dict = self.memory_object.get_dot_dict() # 绘制所有节点
        for dot_id in dot_dict:
            x_dot, y_dot = dot_dict[dot_id]
            if numpy.linalg.norm(numpy.array([x_dot - x, y_dot - y])) <= constant_config.CIRCLE_RADIUS + 1:
                mouse_on_dot_id = dot_id
                break
        
        if self.status == "free": # 自由状态创建点
            if mouse_on_dot_id is None:
                self.memory_object.new_dot(x, y)
            
            elif not self.actually_moved: # 刚刚结束拖动的时候不可以选中
                self.focuse_dot = mouse_on_dot_id
                self.status = "select_dot"

        elif self.status == "select_dot":
            if mouse_on_dot_id is not None and mouse_on_dot_id != self.focuse_dot: # 选中点的前提下点击空地
                
                if self.focuse_dot is not None:
                    self.memory_object.new_line(mouse_on_dot_id, self.focuse_dot)
            self.status = "free"
            self.focuse_dot = None

    def handle_mouse_up(self, button, x, y):
        super().handle_mouse_up(button, x, y)
        if button == constant_config.LEFT_KEY_ID:
            self.handle_left_mouse_up(x, y)

    def draw_screen(self, screen): # 绘制屏幕内容
        super().draw_screen(screen)

        dot_dict = self.memory_object.get_dot_dict()
        line_dict = self.memory_object.get_line_dict()
        for line_id in line_dict:
            dot_from, dot_to = line_dict[line_id]
            pos_from = dot_dict[dot_from]
            pos_to   = dot_dict[dot_to]
            pygame.draw.line(screen, constant_config.BLACK, pos_from, pos_to, 1)

        for dot_id in dot_dict: # 绘制所有节点
            x, y = dot_dict[dot_id]

            color = constant_config.BLACK
            if self.status == "select_dot" and dot_id == self.focuse_dot:
                color = constant_config.RED

            pygame.draw.circle(screen, constant_config.WHITE, (x, y), constant_config.CIRCLE_RADIUS)
            pygame.draw.circle(screen, color, (x, y), constant_config.CIRCLE_RADIUS, 1)