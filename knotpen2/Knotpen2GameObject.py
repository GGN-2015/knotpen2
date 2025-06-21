import pygame
import numpy
import time

from . import GameObject
from . import MemoryObject
from . import constant_config
from . import pygame_utils

STATUS_LIST = [
    "free",        # 自由状态
    "select_dot",  # 选中了一个结点
    "quit",        # 退出程序
    "move_dot",    # 移动一个节点
]

class Knotpen2GameObject(GameObject.GameObject):
    def __init__(self, memory_object:MemoryObject.MemoryObject) -> None:
        super().__init__()

        self.memory_object   = memory_object
        self.status          = "free"
        self.focus_dot       = None
        self.left_mouse_down = False
        self.actually_moved  = False
        self.last_click      = -1          # 上次鼠标左键抬起的时刻
        self.last_backup     = time.time() # 上次自动保存时间

    def handle_quit(self):
        print("自动保存中，请不要关闭窗口 ...")
        self.memory_object.dump_object(constant_config.AUTOSAVE_FILE) # 自动保存
        print("自动保存成功")

        self.status = "quit"

    def handle_mouse_down(self, button, x, y): # 鼠标按下
        super().handle_mouse_down(button, x, y)
        
        if button == constant_config.LEFT_KEY_ID:
            self.handle_left_mouse_down(x, y)

    def handle_key_down(self, key, mod, unicode): # 处理键盘事件
        super().handle_key_down(key, mod, unicode)

        key_name = pygame.key.name(key)
        if key_name == 'a':
            self.memory_object.shift_position(-constant_config.STRIDE, 0)

        elif key_name == 'd':
            self.memory_object.shift_position(+constant_config.STRIDE, 0)

        elif key_name == 'w':
            self.memory_object.shift_position(0, -constant_config.STRIDE)

        elif key_name == 's':
            self.memory_object.shift_position(0, +constant_config.STRIDE)

        elif key_name == 'b': # set base point

            if self.status == "select_dot" and self.focus_dot is not None:
                self.memory_object.set_base_dot(self.focus_dot)
                self.status = "free"
                self.focus_dot = None # 回退到常规模式

            else:
                self.memory_object.set_base_dot(self.focus_dot) # 再添加一次变成取消

        elif key_name == 't': # set dir point
            if self.status == "select_dot" and self.focus_dot is not None:
                self.memory_object.set_dir_dot(self.focus_dot)
                self.status = "free"
                self.focus_dot = None # 回退到常规模式

            else:
                self.memory_object.set_dir_dot(self.focus_dot)
        
        elif key_name == 'delete' or key_name == 'backspace':
            if self.status == "select_dot" and self.focus_dot is not None: # 删除节点并回退到正常模式
                self.memory_object.erase_dot(self.focus_dot)
                self.status = "free"
                self.focus_dot = None # 回退到常规模式

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
        
        if self.status == "free":
            if mouse_on_dot_id is None:
                line_pair_list = self.memory_object.find_nearest_lines(x, y)

                if len(line_pair_list) == 2: # 左键交换上下关系
                    self.memory_object.swap_line_order(line_pair_list[0][0], line_pair_list[1][0])

                elif len(line_pair_list) == 0: # 自由状态创建点
                    self.memory_object.new_dot(x, y)

                elif len(line_pair_list) == 1 and time.time() - self.last_click < constant_config.DOUBLE_CLICK_TIME:
                    self.memory_object.split_line_at(line_pair_list[0][0], x, y)
            
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
        
        self.last_click = time.time() # 设置上次鼠标左键抬起的时刻

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

            else: # 右键点击可以删除线
                line_pair_list = self.memory_object.find_nearest_lines(x, y)

                if len(line_pair_list) == 1: # 删除一个边
                    self.memory_object.erase_line(line_pair_list[0][0])
        
        elif self.status == "select_dot": # 退出节点选择模式
            self.status = "free"

    def draw_screen(self, screen): # 绘制屏幕内容
        super().draw_screen(screen)

        time_now = time.time()
        if time_now - self.last_backup > constant_config.BACKUP_TIME:     # 自动保存
            self.memory_object.auto_backup()                              # 保存一个时间戳对应的文件
            self.memory_object.dump_object(constant_config.AUTOSAVE_FILE) # 保存一个 auto_save
            self.last_backup = time_now

        if self.memory_object.base_dot is not None: # 绘制起始点
            for base_dot_id in self.memory_object.base_dot:
                x, y = self.memory_object.dot_dict[base_dot_id]
                pygame_utils.draw_empty_circle(screen, constant_config.BLUE, x, y, constant_config.CIRCLE_RADIUS + 3)

        if self.memory_object.dir_dot is not None: # 绘制方向点
            for dir_dot_id in self.memory_object.dir_dot:
                x, y = self.memory_object.dot_dict[dir_dot_id]
                pygame_utils.draw_empty_circle(screen, constant_config.GREEN, x, y, constant_config.CIRCLE_RADIUS + 3)

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

            if self.memory_object.get_degree()[dot_id] != 2:
                pygame_utils.draw_full_circle(screen, constant_config.GREY, x, y, constant_config.CIRCLE_RADIUS - 3)

        # 重新绘制所有逆向边遮挡
        for item in self.memory_object.get_inverse_pairs():
            line_id1, line_id2 = item
            dot_11, dot_12 = self.memory_object.get_line_dict()[line_id1]
            dot_21, dot_22 = self.memory_object.get_line_dict()[line_id2]
            pos_11 = dot_dict[dot_11]
            pos_12 = dot_dict[dot_12]
            pos_21 = dot_dict[dot_21]
            pos_22 = dot_dict[dot_22]
            pygame_utils.draw_line_on_line(screen, pos_11, pos_12, pos_21, pos_22, constant_config.BLACK)

    def die_check(self):
        return self.status == "quit"