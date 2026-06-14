import pygame
import numpy
import time
import functools
import os

# 相对导入
import i18n
from i18n import _
import GameObject
import MemoryObject
import MyAlgorithm
import constant_config
import font_utils
import pygame_utils
import math_utils

STATUS_LIST = [
    "free",        # 自由状态
    "select_dot",  # 选中了一个结点
    "quit",        # 退出程序
    "move_dot",    # 移动一个节点
]

class Knotpen2GameObject(GameObject.GameObject):
    def __init__(self, memory_object:MemoryObject.MemoryObject, algo:MyAlgorithm.MyAlgorithm) -> None:
        super().__init__()

        font_path    = font_utils.ensure_font_exists()
        self.font    = pygame.font.Font(font_path, constant_config.MESSAGE_SIZE)
        self.msg_txt = [
            self.font.render("0: %s %s" % (_("欢迎使用"), self.get_window_caption()), True, constant_config.BLACK)
        ]
        self.msg_line_id = 1

        self.node_font = pygame.font.Font(font_path, constant_config.SMALL_TEXT_SIZE)
        self.button_font = pygame.font.Font(font_path, constant_config.BUTTON_FONT_SIZE)
        @functools.cache
        def get_small_text(s:str, color): # 用于避免小文本的重复绘制
            return self.node_font.render(s, True, color)
        self.get_small_text  = get_small_text
        @functools.cache
        def get_button_text(s:str, color): # 用于避免按钮文本的重复绘制
            return self.button_font.render(s, True, color)
        self.get_button_text = get_button_text

        self.memory_object   = memory_object
        self.algo            = algo
        self.status          = "free"
        self.focus_dot       = None
        self.left_mouse_down = False
        self.actually_moved  = False
        self.last_click      = -1          # 上次鼠标左键抬起的时刻
        self.last_backup     = time.time() # 上次自动保存时间
        self.notice_node     = []          # 用红色标出一些节点编号
        self.button_pressed_action = None
        self.button_rects = []
        self.button_panel_rect = None
        self.help_visible = False
    
    def get_window_caption(self) -> str:
        return constant_config.APP_NAME + "_" + constant_config.APP_VERSION

    def handle_quit(self):
        self.leave_message(_("自动保存中，请不要关闭窗口 ..."), constant_config.YELLOW)
        self.memory_object.dump_object(constant_config.AUTOSAVE_FILE) # 自动保存
        self.leave_message(_("自动保存成功"), constant_config.GREEN)

        self.status = "quit"
    
    def handle_mouse_down(self, button, x, y): # 鼠标按下
        super().handle_mouse_down(button, x, y)

        if button == constant_config.LEFT_KEY_ID:
            self.button_pressed_action = self.get_button_action_at(x, y)
            if self.is_mouse_on_control_panel(x, y):
                return

            if self.help_visible:
                return
        
        if button == constant_config.LEFT_KEY_ID:
            self.handle_left_mouse_down(x, y)

    def leave_message(self, s, color=constant_config.BLACK, replace=False): # 在屏幕上绘制信息
        if replace and len(self.msg_txt) >= 1: # 替换最后一条消息
            self.msg_txt = self.msg_txt[:-1]

        text_now = "%d: %s" % (self.msg_line_id, s)
        print(text_now)

        self.msg_txt.append(self.font.render(text_now, True, color))

        if not replace: # 替换最后一条消息的时候，不需要增加 id
            self.msg_line_id += 1

        while len(self.msg_txt) > constant_config.MAX_MESSAGE_CNT:
            self.msg_txt = self.msg_txt[1:]

    def save_answer(self, s:str):
        os.makedirs(constant_config.ANSWER_FOLDER, exist_ok=True)
        foldername  = os.path.basename(constant_config.ANSWER_FOLDER) # 文件夹名称
        outter_name = os.path.basename(os.path.dirname(constant_config.ANSWER_FOLDER))
        filename    = math_utils.get_formatted_datetime() + ".txt"
        filepath    = os.path.join(constant_config.ANSWER_FOLDER, filename)

        with open(filepath, "w") as fp:
            fp.write(s)

        return "%s/%s/%s" % (outter_name, foldername, filename)

    def save_svg_answer(self, svg_filename:str, s):
        os.makedirs(constant_config.ANSWER_FOLDER, exist_ok=True)
        foldername  = os.path.basename(constant_config.ANSWER_FOLDER) # 文件夹名称
        outter_name = os.path.basename(os.path.dirname(constant_config.ANSWER_FOLDER))
        filename    = svg_filename
        filepath    = os.path.join(constant_config.ANSWER_FOLDER, filename)

        with open(filepath, "w") as fp:
            fp.write(s)

        return "%s/%s/%s" % (outter_name, foldername, filename)

    def output_answer(self):
        self.leave_message(_("开始计算 PD_CODE"), constant_config.YELLOW)
        degree_check_list = self.algo.degree_check()
        if len(degree_check_list) > 0: # 发现了有些节点度不为 2
            self.leave_message(_("%d 个节点度数不为 2，请注意灰色标出的节点") % len(degree_check_list), constant_config.RED)
            return
        adj_list, block_list        = self.algo.get_connected_components()           # 计算出所有连通分支
        suc, msg, baseL, dirL, nntc = self.algo.check_base_dir(adj_list, block_list) # 检查每个连通分支是否都有 base 和 dir 节点，检查节点数是否大于等于 3
        self.notice_node            = nntc
        if not suc:
            self.leave_message(msg, constant_config.RED)
            return
        # pd_code_to_show 中记录的是最终计算得到的 pd_code
        # pd_code_final 中记录的是用于在屏幕上显示 pd_code 弧线编号的相关信息
        # parts 记录的是每个连通分量上的交叉点构成的序列，parts 对连通分量的处理顺序与 block_list 一致
        pd_code_to_show, pd_code_final, parts = self.algo.solve_pd_code(adj_list, block_list, baseL, dirL, self.leave_message)
        self.memory_object.set_pd_code_final_info(pd_code_final)

        # 保存文本文件的 PD_CODE
        filename = self.save_answer(str(pd_code_to_show))
        self.leave_message(_("PD_CODE 计算成功"), constant_config.GREEN)
        self.leave_message(_("保存在 %s") % filename, constant_config.GREEN)

        # 生成 svg 文件格式的扭结图片（不带有弧线编号信息）
        svg_filename = filename.split("/")[-1].replace(".txt", ".nonum.svg")
        svg_text = self.algo.calculate_svg(block_list, parts, False, False)
        svg_return_name = self.save_svg_answer(svg_filename, svg_text)
        self.leave_message(_("扭结图像（不带弧线编号信息）生成成功"), constant_config.GREEN)
        self.leave_message(_("保存在 %s") % svg_return_name, constant_config.GREEN)

        # 生成 svg 文件格式的扭结图片（带有弧线编号信息）
        svg_filename = filename.split("/")[-1].replace(".txt", ".num.svg")
        svg_text = self.algo.calculate_svg(block_list, parts, True, False)
        svg_return_name = self.save_svg_answer(svg_filename, svg_text)
        self.leave_message(_("扭结图像（带弧线编号信息）生成成功"), constant_config.GREEN)
        self.leave_message(_("保存在 %s") % svg_return_name, constant_config.GREEN)

        # 生成 svg 文件格式的扭结图片（带有弧线方向信息）
        svg_filename = filename.split("/")[-1].replace(".txt", ".arrow.svg")
        svg_text = self.algo.calculate_svg(block_list, parts, False, True)
        svg_return_name = self.save_svg_answer(svg_filename, svg_text)
        self.leave_message(_("扭结图像（带弧线方向信息）生成成功"), constant_config.GREEN)
        self.leave_message(_("保存在 %s") % svg_return_name, constant_config.GREEN)
    
    def move_view_left(self):
        self.memory_object.shift_position(-constant_config.STRIDE, 0)

    def move_view_right(self):
        self.memory_object.shift_position(+constant_config.STRIDE, 0)

    def move_view_up(self):
        self.memory_object.shift_position(0, -constant_config.STRIDE)

    def move_view_down(self):
        self.memory_object.shift_position(0, +constant_config.STRIDE)

    def set_selected_base_dot(self):
        if self.status == "select_dot" and self.focus_dot is not None:
            self.memory_object.set_base_dot(self.focus_dot)
            self.status = "free"
            self.focus_dot = None # 回退到常规模式

    def set_selected_dir_dot(self):
        if self.status == "select_dot" and self.focus_dot is not None:
            self.memory_object.set_dir_dot(self.focus_dot)
            self.status = "free"
            self.focus_dot = None # 回退到常规模式

    def erase_selected_dot(self):
        if self.status == "select_dot" and self.focus_dot is not None: # 删除节点并回退到正常模式
            self.memory_object.erase_dot(self.focus_dot)
            self.status = "free"
            self.focus_dot = None # 回退到常规模式

    def clear_all_data(self):
        self.memory_object.auto_backup()
        self.memory_object.clear()

    def recover_last_auto_save(self):
        self.memory_object.load_last_auto_save()

    def get_window_size_limits(self):
        desktop_sizes = pygame.display.get_desktop_sizes()
        primary_width, primary_height = desktop_sizes[0]
        max_width = max(constant_config.MIN_WINDOW_WIDTH, primary_width - constant_config.WINDOW_MARGIN)
        max_height = max(constant_config.MIN_WINDOW_HEIGHT, primary_height - constant_config.WINDOW_MARGIN)
        return (
            constant_config.MIN_WINDOW_WIDTH,
            constant_config.MIN_WINDOW_HEIGHT,
            max_width,
            max_height,
        )

    def resize_window(self, delta):
        surface = pygame.display.get_surface()
        if surface is None:
            return

        min_width, min_height, max_width, max_height = self.get_window_size_limits()
        width, height = surface.get_size()
        new_width = min(max(width + delta, min_width), max_width)
        new_height = min(max(height + delta, min_height), max_height)

        if (new_width, new_height) != (width, height):
            pygame.display.set_mode((new_width, new_height))
            self.end_left_mouse_operation()

    def increase_resolution(self):
        self.resize_window(constant_config.WINDOW_RESIZE_STEP)

    def decrease_resolution(self):
        self.resize_window(-constant_config.WINDOW_RESIZE_STEP)

    def switch_language(self):
        i18n.set_next_language(self.leave_message)
        self.get_small_text.cache_clear()
        self.get_button_text.cache_clear()

    def toggle_help_page(self):
        self.help_visible = not self.help_visible
        self.end_left_mouse_operation()

    def get_button_specs(self):
        can_edit = not self.help_visible
        help_label = _("关闭帮助") if self.help_visible else _("帮助")
        return [
            ("move_up", _("上移视图"), self.move_view_up, can_edit),
            ("move_left", _("左移视图"), self.move_view_left, can_edit),
            ("move_down", _("下移视图"), self.move_view_down, can_edit),
            ("move_right", _("右移视图"), self.move_view_right, can_edit),
            ("set_base", _("设为起始点"), self.set_selected_base_dot, can_edit and self.status == "select_dot" and self.focus_dot is not None),
            ("set_dir", _("设为方向点"), self.set_selected_dir_dot, can_edit and self.status == "select_dot" and self.focus_dot is not None),
            ("delete_selected", _("删除选中点"), self.erase_selected_dot, can_edit and self.status == "select_dot" and self.focus_dot is not None),
            ("clear", _("清空全部"), self.clear_all_data, can_edit),
            ("recover", _("恢复存档"), self.recover_last_auto_save, can_edit),
            ("language", _("切换语言"), self.switch_language, True),
            ("help", help_label, self.toggle_help_page, True),
            ("increase_resolution", _("增大窗口"), self.increase_resolution, True),
            ("decrease_resolution", _("减小窗口"), self.decrease_resolution, True),
            ("calculate", _("计算 PD_CODE"), self.output_answer, can_edit),
        ]

    def get_button_layout(self, screen_width, screen_height=None):
        if screen_height is None:
            surface = pygame.display.get_surface()
            if surface is not None:
                screen_height = surface.get_height()
            else:
                screen_height = 720

        button_count = len(self.get_button_specs())
        available_panel_height = max(1, screen_height - 2 * constant_config.BUTTON_MARGIN)
        inner_height = max(1, available_panel_height - 2 * constant_config.BUTTON_PANEL_PADDING)
        button_height = constant_config.BUTTON_HEIGHT
        button_gap = constant_config.BUTTON_GAP

        required_inner_height = button_count * button_height + max(0, button_count - 1) * button_gap
        if required_inner_height > inner_height and button_count > 0:
            button_gap = constant_config.MIN_BUTTON_GAP
            button_height = int((inner_height - max(0, button_count - 1) * button_gap) / button_count)
            button_height = max(constant_config.MIN_BUTTON_HEIGHT, button_height)

        panel_width = constant_config.BUTTON_WIDTH + 2 * constant_config.BUTTON_PANEL_PADDING
        panel_height = (
            button_count * button_height
            + max(0, button_count - 1) * button_gap
            + 2 * constant_config.BUTTON_PANEL_PADDING
        )
        panel_height = min(panel_height, available_panel_height)
        panel_x = screen_width - constant_config.BUTTON_MARGIN - panel_width
        panel_y = constant_config.BUTTON_MARGIN

        return {
            "panel_rect": pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            "button_x": panel_x + constant_config.BUTTON_PANEL_PADDING,
            "button_y": panel_y + constant_config.BUTTON_PANEL_PADDING,
            "button_height": button_height,
            "button_gap": button_gap,
        }

    def compute_button_rects(self, screen_width, screen_height=None):
        layout = self.get_button_layout(screen_width, screen_height)
        x = layout["button_x"]
        y = layout["button_y"]
        button_height = layout["button_height"]
        button_gap = layout["button_gap"]
        rects = []
        for action_id, label, callback, enabled in self.get_button_specs():
            rect = pygame.Rect(x, y, constant_config.BUTTON_WIDTH, button_height)
            rects.append({
                "action_id": action_id,
                "label": label,
                "callback": callback,
                "enabled": enabled,
                "rect": rect,
            })
            y += button_height + button_gap
        return rects

    def compute_button_panel_rect(self, screen_width, screen_height=None):
        return self.get_button_layout(screen_width, screen_height)["panel_rect"]

    def refresh_button_rects_if_needed(self):
        surface = pygame.display.get_surface()
        if surface is not None:
            self.button_rects = self.compute_button_rects(surface.get_width(), surface.get_height())
            self.button_panel_rect = self.compute_button_panel_rect(surface.get_width(), surface.get_height())

    def get_button_info_at(self, x, y):
        self.refresh_button_rects_if_needed()
        for button_info in self.button_rects:
            if button_info["rect"].collidepoint(x, y):
                return button_info
        return None

    def is_mouse_on_button(self, x, y):
        return self.get_button_info_at(x, y) is not None

    def is_mouse_on_control_panel(self, x, y):
        self.refresh_button_rects_if_needed()
        return self.button_panel_rect is not None and self.button_panel_rect.collidepoint(x, y)

    def get_button_action_at(self, x, y):
        button_info = self.get_button_info_at(x, y)
        if button_info is not None and button_info["enabled"]:
            return button_info["action_id"]
        return None

    def run_button_action(self, action_id):
        for button_info in self.button_rects:
            if button_info["action_id"] == action_id and button_info["enabled"]:
                button_info["callback"]()
                return True
        return False

    def handle_key_down(self, key, mod, unicode): # 处理键盘事件
        super().handle_key_down(key, mod, unicode)

    
    def handle_left_mouse_down(self, x, y):
        self.left_mouse_down = True
        mouse_on_dot_id = self.get_mouse_on_dot_id(x, y)
        
        if self.status == "free":
            if mouse_on_dot_id is not None: # 开始移动节点
                self.focus_dot = mouse_on_dot_id
                self.status = "move_dot"
                self.actually_moved = False

    
    def handle_mouse_move(self, x, y, show_log=False):
        super().handle_mouse_move(x, y, show_log)

        if self.help_visible:
            return

        if self.is_mouse_on_control_panel(x, y):
            return

        if self.status == "move_dot" and self.focus_dot is not None:
            self.memory_object.set_dot_position(self.focus_dot, x, y)
            self.actually_moved = True

    def end_left_mouse_operation(self):
        self.left_mouse_down = False
        if self.status == "move_dot":
            self.status = "free"

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
            button_action = self.get_button_action_at(x, y)
            if self.button_pressed_action is not None:
                if button_action == self.button_pressed_action:
                    self.run_button_action(button_action)
                self.button_pressed_action = None
                return

            if button_action is not None or self.is_mouse_on_control_panel(x, y):
                self.end_left_mouse_operation()
                return

            if self.help_visible:
                self.end_left_mouse_operation()
                return

            self.handle_left_mouse_up(x, y)

        elif button == constant_config.RIGHT_KEY_ID: # 右键单击可以删除结点
            if self.help_visible:
                return

            if self.is_mouse_on_control_panel(x, y):
                return

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
            self.leave_message(_("正在自动保存请不要关闭软件 ..."), constant_config.YELLOW)
            self.memory_object.auto_backup()                              # 保存一个时间戳对应的文件
            self.memory_object.dump_object(constant_config.AUTOSAVE_FILE) # 保存一个 auto_save
            self.leave_message(_("自动保存成功"), constant_config.GREEN, replace=True)
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

        # 绘制全局消息
        for i in range(len(self.msg_txt)):
            screen.blit(self.msg_txt[i], constant_config.MESSAGE_POSITION(i))

        # 绘制节点编号
        for dot_id in dot_dict:
            posx, posy = dot_dict[dot_id]
            
            color = constant_config.BLACK
            if dot_id in self.notice_node:
                color = constant_config.RED

            text_now = self.get_small_text(dot_id.split("_")[-1], color)
            screen.blit(text_now, (posx - constant_config.CIRCLE_RADIUS + 1, posy - constant_config.CIRCLE_RADIUS + 1))

        # 绘制 pd_code_final_info
        # 这段代码的用途是对每个交叉点，将数字绘制到交叉点附近
        pd_code_final_info = self.memory_object.get_pd_code_final_info()
        if pd_code_final_info is not None:
            
            # 计算屏幕上需要显示的编号
            number_postion_pairs = self.memory_object.get_number_position_pairs()

            # 将这些编号输出到屏幕上
            for number_str, pos_to_show in number_postion_pairs:
                txt_val = self.get_small_text(number_str, constant_config.RED)
                screen.blit(txt_val, pos_to_show)

        if self.help_visible:
            self.draw_help_page(screen)

        self.draw_buttons(screen)

    def get_help_sections(self):
        return [
            (_("基础编辑"), [
                _("左键空白处创建节点；拖拽节点可以移动。"),
                _("右键节点或边可以删除。"),
                _("双击边的中点可以拆分边。"),
                _("点击交叉点可以切换相交线段的上下关系。"),
            ]),
            (_("连续创建"), [
                _("点击节点进入连续创建模式，红色节点是当前选中点。"),
                _("在空白处继续左键点击会创建新节点并自动连边。"),
                _("点击现有节点可以闭合曲线并退出连续创建模式。"),
            ]),
            (_("右侧按钮"), [
                _("使用视图移动按钮平移画面。"),
                _("选中节点后可以设为起始点或方向点，也可以删除选中点。"),
                _("清空全部会先自动备份；恢复存档会读取上一次自动保存。"),
                _("增大窗口和减小窗口会调整窗口尺寸，并保持窗口不超过屏幕范围。"),
                _("切换语言会影响之后绘制的按钮和帮助文字。"),
            ]),
            (_("计算 PD_CODE"), [
                _("计算前请确保每个节点恰好有两条边。"),
                _("每个连通分支必须有相邻的起始点和方向点。"),
                _("请人工确认没有三线共点。"),
            ]),
        ]

    def wrap_help_text(self, text, font, max_width):
        words = text.split(" ") if " " in text else list(text)
        lines = []
        current = ""
        separator = " " if " " in text else ""

        for word in words:
            candidate = word if current == "" else current + separator + word
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)
        return lines

    def draw_help_page(self, screen):
        screen_width, screen_height = screen.get_size()
        button_area_width = constant_config.BUTTON_WIDTH + 2 * constant_config.BUTTON_MARGIN
        panel_width = max(260, screen_width - button_area_width - 3 * constant_config.BUTTON_MARGIN)
        panel_height = screen_height - 2 * constant_config.BUTTON_MARGIN
        panel_rect = pygame.Rect(
            constant_config.BUTTON_MARGIN,
            constant_config.BUTTON_MARGIN,
            panel_width,
            panel_height,
        )

        overlay = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 242))
        screen.blit(overlay, panel_rect)
        pygame.draw.rect(screen, (60, 60, 60), panel_rect, 1, border_radius=constant_config.BUTTON_BORDER_RADIUS)

        x = panel_rect.x + 18
        y = panel_rect.y + 16
        max_text_width = panel_rect.width - 36

        title = self.font.render(_("帮助"), True, constant_config.BLACK)
        screen.blit(title, (x, y))
        y += constant_config.MESSAGE_SIZE + 10

        hint_lines = self.wrap_help_text(_("再次点击右侧的帮助按钮关闭此页面。"), self.node_font, max_text_width)
        for line in hint_lines:
            screen.blit(self.node_font.render(line, True, (70, 70, 70)), (x, y))
            y += constant_config.SMALL_TEXT_SIZE + 5
        y += 8

        for section_title, lines in self.get_help_sections():
            if y > panel_rect.bottom - 30:
                break

            section_surface = self.button_font.render(section_title, True, constant_config.BLUE)
            screen.blit(section_surface, (x, y))
            y += constant_config.BUTTON_FONT_SIZE + 7

            for line in lines:
                for wrapped_line in self.wrap_help_text("- " + line, self.node_font, max_text_width):
                    if y > panel_rect.bottom - constant_config.SMALL_TEXT_SIZE - 8:
                        return
                    screen.blit(self.node_font.render(wrapped_line, True, constant_config.BLACK), (x, y))
                    y += constant_config.SMALL_TEXT_SIZE + 5
            y += 8

    def draw_buttons(self, screen):
        self.button_rects = self.compute_button_rects(screen.get_width(), screen.get_height())
        self.button_panel_rect = self.compute_button_panel_rect(screen.get_width(), screen.get_height())
        mouse_pos = self.get_mouse_pos()

        pygame.draw.rect(screen, (238, 238, 238), self.button_panel_rect, border_radius=8)
        pygame.draw.rect(screen, (185, 185, 185), self.button_panel_rect, 1, border_radius=8)

        for button_info in self.button_rects:
            rect = button_info["rect"]
            enabled = button_info["enabled"]
            hovering = enabled and rect.collidepoint(mouse_pos)
            pressed = hovering and self.button_pressed_action == button_info["action_id"]

            fill_color = (246, 246, 246)
            border_color = (80, 80, 80)
            text_color = constant_config.BLACK
            if not enabled:
                fill_color = (224, 224, 224)
                border_color = (170, 170, 170)
                text_color = (130, 130, 130)
            elif pressed:
                fill_color = (210, 230, 255)
                border_color = constant_config.BLUE
            elif hovering:
                fill_color = (232, 242, 255)
                border_color = (45, 105, 180)

            pygame.draw.rect(screen, fill_color, rect, border_radius=constant_config.BUTTON_BORDER_RADIUS)
            pygame.draw.rect(screen, border_color, rect, 1, border_radius=constant_config.BUTTON_BORDER_RADIUS)

            text = self.get_button_text(button_info["label"], text_color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    
    def die_check(self):
        return self.status == "quit"
