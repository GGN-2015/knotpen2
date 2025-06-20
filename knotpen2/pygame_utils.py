import pygame
import math
from . import constant_config

def draw_thick_line(screen, start, end, width, color):
    """绘制有宽度的线（使用多边形）"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    
    if length == 0:
        return  # 起点和终点相同，无法绘制线
    
    # 计算垂直于线段的方向
    perp_x = -dy / length
    perp_y = dx / length
    
    # 计算四个顶点
    offset = width / 2
    p1 = (start[0] + perp_x * offset, start[1] + perp_y * offset)
    p2 = (start[0] - perp_x * offset, start[1] - perp_y * offset)
    p3 = (end[0] - perp_x * offset, end[1] - perp_y * offset)
    p4 = (end[0] + perp_x * offset, end[1] + perp_y * offset)
    
    # 绘制填充的多边形（白色长方形）
    pygame.draw.polygon(screen, constant_config.WHITE, [p1, p2, p3, p4])
    
    # 绘制边框（无填充的长方形）
    pygame.draw.polygon(screen, color, [p1, p2, p3, p4], 1)

def draw_empty_circle(screen, border_color, x, y, radius):
    pygame.draw.circle(screen, constant_config.WHITE, (x, y), radius)
    pygame.draw.circle(screen, border_color, (x, y), radius, 1)