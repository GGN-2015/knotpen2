import pygame

# mouse_down_recall(button, x, y): 鼠标按下回调函数
#   button: 1=左键, 2=中键, 3=右键, 4=滚轮上滚, 5=滚轮下滚
# mouse_up_recall(button, x, y): 鼠标抬起回调函数
# handle_key_down(key, mod, unicode): 键盘按键按下回调函数
# handle_key_up(key, mod): 键盘按键释放回调函数
# handle_quit(): 页面关闭回调函数，返回页面是否要继续运行
# draw_screen(screen): 用于绘制屏幕内容
# die_check(): 检测游戏当前是否应该被关闭, True: 是, False: 否

class GameObject:
    def __init__(self) -> None:
        self.quit_cnt = 0

    def draw_screen(self, screen):
        screen.fill((255, 255, 255)) # 填充白色背景

    def handle_mouse_down(self, button, x, y):
        button_names = {1: "左键", 2: "中键", 3: "右键", 4: "滚轮上滚", 5: "滚轮下滚"}
        button_name = button_names.get(button, f"未知按钮({button})")
        print(f"鼠标按下: {button_name} @ ({x}, {y})")

        # 示例：处理键盘事件的回调函数
    def handle_key_down(self, key, mod, unicode):
        key_name = pygame.key.name(key)
        modifiers = []
        if mod & pygame.KMOD_SHIFT:
            modifiers.append("Shift")
        if mod & pygame.KMOD_CTRL:
            modifiers.append("Ctrl")
        if mod & pygame.KMOD_ALT:
            modifiers.append("Alt")
        
        mod_str = "+".join(modifiers) if modifiers else "无"
        print(f"按键按下: {key_name} (Unicode: {unicode}, 修饰键: {mod_str})")
    
    def handle_key_up(self, key, mod):
        key_name = pygame.key.name(key)
        print(f"按键释放: {key_name}")
    
    def handle_mouse_up(self, button, x, y):
        button_names = {1: "左键", 2: "中键", 3: "右键"}
        if button in button_names:  # 只处理真正的按键抬起事件
            print(f"鼠标抬起: {button_names[button]} @ ({x}, {y})")
    
    def handle_quit(self):
        self.quit_cnt += 1
        print("尝试关闭窗口（第 %d 次）" % self.quit_cnt)
    
    def die_check(self):
        if self.quit_cnt >= 3:
            print("尝试关闭窗口（第 %d 次），游戏退出" % self.quit_cnt)
            return True # 窗口已经死了
        else:
            return False # 窗口还没死