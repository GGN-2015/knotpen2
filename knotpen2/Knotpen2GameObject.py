import pygame
import numpy

from . import GameObject
from . import MemoryObject
from . import constant_config
from . import pygame_utils

STATUS_LIST = [
    "free",        # 自由状态
    "select_dot",  # 选中了一个结点
    "select_line", # 选中了一条边
    "move_dot",    # 移动一个节点
]

class Knotpen2GameObject(GameObject.GameObject):
    def __init__(self, memory_object:MemoryObject.MemoryObject) -> None:
        super().__init__()

        self.memory_object   = memory_object
        self.status          = "free"
        self.focus_dot      = None
        self.focuse_line     = None
        self.left_mouse_down = False
        self.actually_moved  = False

    def handle_mouse_down(self, button, x, y): # 鼠标按下
        super().handle_mouse_down(button, x, y)
        
        if button == constant_config.LEFT_KEY_ID:
            self.handle_left_mouse_down(x, y)

    def handle_left_mouse_down(self, x, y):
        self.left_mouse_down = True
        mouse_on_dot_id = self.get_mouse_on_dot_id(x, y)
        
        if self.status == "free":
            if mouse_on_dot_id is not None: # 开始移动节点
                self.focus_dot = mouse_on_dot_id
                self.status = "move_dot"
                self.actually_moved = False

    def handle_mouse_move(self, x, y):
        super().handle_mouse_move(x, y)

        if self.status == "move_dot" and self.focus_dot is not None:
            self.memory_object.set_dot_position(self.focus_dot, x, y)
            self.actually_moved = True

    def get_mouse_on_dot_id(self, x, y):
        mouse_on_dot_id = None
        dot_dict = self.memory_object.get_dot_dict() # 绘制所有节点
        for dot_id in dot_dict:
            x_dot, y_dot = dot_dict[dot_id]
            if numpy.linalg.norm(numpy.array([x_dot - x, y_dot - y])) <= constant_config.CIRCLE_RADIUS + 1:
                mouse_on_dot_id = dot_id
                break
        return mouse_on_dot_id

    def handle_left_mouse_up(self, x, y):
        self.left_mouse_down = False
        mouse_on_dot_id = self.get_mouse_on_dot_id(x, y)

        if self.status == "move_dot": # 移动节点结束
            self.status = "free"
        
        if self.status == "free": # 自由状态创建点
            if mouse_on_dot_id is None:
                self.memory_object.new_dot(x, y)
            
            elif not self.actually_moved: # 刚刚结束拖动的时候不可以选中
                self.focus_dot = mouse_on_dot_id
                self.status = "select_dot"

        elif self.status == "select_dot":
            if mouse_on_dot_id is not None: # 选中点的前提下点击空地
                if self.focus_dot is not None and mouse_on_dot_id != self.focus_dot:
                    self.memory_object.new_line(mouse_on_dot_id, self.focus_dot)
                self.status = "free"
                self.focus_dot = None
            else:
                if mouse_on_dot_id is None and self.focus_dot is not None: # 传递一个新的 focus
                    dot_id = self.memory_object.new_dot(x, y)
                    self.memory_object.new_line(dot_id, self.focus_dot)
                    self.status    = "select_dot"
                    self.focus_dot = dot_id # 焦点传递

    def handle_mouse_up(self, button, x, y):
        super().handle_mouse_up(button, x, y)
        if button == constant_config.LEFT_KEY_ID: # 点击左键可以添加结点
            self.handle_left_mouse_up(x, y)

        elif button == constant_config.RIGHT_KEY_ID: # 右键单击可以删除结点
            self.handle_right_mouse_up(x, y)

    def handle_right_mouse_up(self, x, y):
        if self.status == "free":
            mouse_on_dot_id = self.get_mouse_on_dot_id(x, y)

            if mouse_on_dot_id is not None: # 右键删除节点
                self.memory_object.erase_dot(mouse_on_dot_id)

            else: # 右键点击交叉点可以调整交叉点的重叠次序
                line_pair_list = self.memory_object.find_nearest_lines(x, y)

                if len(line_pair_list) == 2:
                    self.memory_object.swap_line_order(line_pair_list[0][0], line_pair_list[1][0])

    def draw_screen(self, screen): # 绘制屏幕内容
        super().draw_screen(screen)

        dot_dict  = self.memory_object.get_dot_dict()
        line_dict = self.memory_object.get_line_dict()
        for line_id in line_dict:
            dot_from, dot_to = line_dict[line_id]
            pos_from = dot_dict[dot_from]
            pos_to   = dot_dict[dot_to]
            pygame_utils.draw_thick_line(screen, pos_from, pos_to, constant_config.LINE_WIDTH, constant_config.BLACK)

        for dot_id in dot_dict: # 绘制所有节点
            x, y = dot_dict[dot_id]

            color = constant_config.BLACK
            if self.status == "select_dot" and dot_id == self.focus_dot:
                color = constant_config.RED
            pygame_utils.draw_empty_circle(screen, color, x, y, constant_config.CIRCLE_RADIUS)

        # 重新绘制所有逆向点
        for item in self.memory_object.get_inverse_pairs():
            line_id1, line_id2 = item
            dot_11, dot_12 = self.memory_object.get_line_dict()[line_id1]
            dot_21, dot_22 = self.memory_object.get_line_dict()[line_id2]
            pos_11 = dot_dict[dot_11]
            pos_12 = dot_dict[dot_12]
            pos_21 = dot_dict[dot_21]
            pos_22 = dot_dict[dot_22]
            pygame_utils.draw_line_on_line(screen, pos_11, pos_12, pos_21, pos_22, constant_config.BLACK)