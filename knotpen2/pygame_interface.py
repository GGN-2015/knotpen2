import pygame

# mouse_down_recall(button, x, y): 鼠标按下回调函数
#   button: 1=左键, 2=中键, 3=右键, 4=滚轮上滚, 5=滚轮下滚
# mouse_up_recall(button, x, y): 鼠标抬起回调函数
# key_down_recall(key, mod, unicode): 键盘按键按下回调函数
# key_up_recall(key, mod): 键盘按键释放回调函数
# quit_recall(): 页面关闭回调函数，返回页面是否要继续运行
# draw_screen(screen): 用于绘制屏幕内容
# die_check(): 检测游戏当前是否应该被关闭, True: 是, False: 否
def pygame_interface(mouse_down_recall=None, mouse_up_recall=None, 
                     key_down_recall=None, key_up_recall=None, 
                     quit_recall=None, draw_screen=None,
                     die_check=None):
    pygame.init() # 初始化 Pygame
    
    width, height = 1024, 768 # 设置窗口尺寸
    screen = pygame.display.set_mode((width, height))
    
    # 设置窗口标题
    pygame.display.set_caption("knotpen2")
    
    # 设置字体，用于显示鼠标坐标
    font = pygame.font.SysFont(None, 36)
    
    # 主循环控制变量
    running = True
    
    # 主游戏循环
    while running:
        if die_check is not None:
            running = not die_check()

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 检测退出事件

                if quit_recall is not None:
                    quit_recall()# 调用退出回调函数

            elif event.type == pygame.MOUSEBUTTONDOWN: # 检测鼠标按下
                x, y = event.pos
                button = event.button
                
                if mouse_down_recall is not None:
                    mouse_down_recall(button, x, y)
            
            elif event.type == pygame.MOUSEBUTTONUP: # 检测鼠标抬起
                x, y = event.pos
                button = event.button
                
                if mouse_up_recall is not None:
                    mouse_up_recall(button, x, y)

            elif event.type == pygame.KEYDOWN: # 检测键盘按键按下
                key = event.key
                mod = event.mod    # 按键修饰符（如 Shift、Ctrl 等）
                unicode = event.unicode  # 按键对应的 Unicode 字符
                
                if key_down_recall is not None:
                    key_down_recall(key, mod, unicode)
            
            elif event.type == pygame.KEYUP: # 检测键盘按键释放
                key = event.key
                mod = event.mod    # 按键修饰符（如 Shift、Ctrl 等）
                
                if key_up_recall is not None:
                    key_up_recall(key, mod)
        
        if draw_screen is None:
            screen.fill((255, 255, 255)) # 填充白色背景
        else:
            draw_screen(screen) # 绘制屏幕内容
        pygame.display.flip() # 更新显示

    pygame.quit() # 退出 Pygame

if __name__ == "__main__":
    # 示例：处理键盘事件的回调函数
    def handle_key_down(key, mod, unicode):
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
    
    def handle_key_up(key, mod):
        key_name = pygame.key.name(key)
        print(f"按键释放: {key_name}")
    
    # 鼠标事件处理保持不变
    def handle_mouse_down(button, x, y):
        button_names = {1: "左键", 2: "中键", 3: "右键", 4: "滚轮上滚", 5: "滚轮下滚"}
        button_name = button_names.get(button, f"未知按钮({button})")
        print(f"鼠标按下: {button_name} @ ({x}, {y})")
    
    def handle_mouse_up(button, x, y):
        button_names = {1: "左键", 2: "中键", 3: "右键"}
        if button in button_names:  # 只处理真正的按键抬起事件
            print(f"鼠标抬起: {button_names[button]} @ ({x}, {y})")
    
    quit_cnt = 0
    def quit_recall():
        global quit_cnt
        quit_cnt += 1
        print("尝试关闭窗口（第 %d 次）" % quit_cnt)
    
    def die_check():
        if quit_cnt >= 10:
            print("尝试关闭窗口（第 %d 次），游戏退出" % quit_cnt)
            return True # 窗口已经死了
        else:
            return False # 窗口还没死

    pygame_interface(
        mouse_down_recall=handle_mouse_down,
        mouse_up_recall=handle_mouse_up,
        key_down_recall=handle_key_down,
        key_up_recall=handle_key_up,
        quit_recall=quit_recall,
        die_check=die_check
    )