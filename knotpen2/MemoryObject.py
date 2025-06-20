import numpy
from . import math_utils
from . import constant_config

class MemoryObject:
    def __init__(self) -> None:
        self.dot_id_max = 0
        self.line_id_max = 0

        self.dot_dict = {}
        self.line_dict = {}
        self.inverse_pairs = {}
        self.degree = {}

        self.base_dot = [] # 记录起始位置
        self.dir_dot = []  # 记录定向位置

    def get_degree(self):
        return self.degree

    def get_inverse_pairs(self):
        return self.inverse_pairs
    
    def shift_position(self, dx, dy): # 所有点一起移动
        for dot_idx in self.dot_dict:
            x, y = self.dot_dict[dot_idx]
            self.dot_dict[dot_idx] = (x + dx, y + dy)

    def set_base_dot(self, dot_idx): # 设置起始位置
        if dot_idx not in self.base_dot:
            self.base_dot.append(dot_idx)

            if dot_idx in self.dir_dot:
                self.dir_dot.remove(dot_idx)
        else:
            self.base_dot.remove(dot_idx)
    
    def set_dir_dot(self, dot_idx): # 设置起始位置的下一个位置，用于确定方向
        if dot_idx not in self.dir_dot:
            self.dir_dot.append(dot_idx)

            if dot_idx in self.base_dot:
                self.base_dot.remove(dot_idx)
        else:
            self.dir_dot.remove(dot_idx)

    def swap_line_order(self, line_idx1, line_idx2):
        assert line_idx1 != line_idx2
        assert self.line_dict.get(line_idx1) is not None
        assert self.line_dict.get(line_idx2) is not None
        
        if int(line_idx1.split("_")[-1]) < int(line_idx2.split("_")[-1]): # 保证 line_idx1 > line_idx2
            line_idx1, line_idx2 = line_idx2, line_idx1

        if self.inverse_pairs.get((line_idx1, line_idx2)) is None: # 如果没有这个逆向对要求，则添加
            self.inverse_pairs[(line_idx1, line_idx2)] = True
        else:                                                      # 如果有这个逆向对要求，则删掉
            del self.inverse_pairs[(line_idx1, line_idx2)]

    def find_nearest_lines(self, x, y, max_dis=constant_config.CIRCLE_RADIUS + constant_config.LINE_WIDTH/2 + 1):
        line_pair_list = []
        for line_id in self.line_dict:
            dot_from, dot_to = self.line_dict[line_id]
            pos_from = self.dot_dict[dot_from]
            pos_to   = self.dot_dict[dot_to]
            dis = math_utils.point_to_line_segment_distance((x, y), pos_from, pos_to)

            if dis <= max_dis:
                line_pair_list.append((line_id, dis))
        return line_pair_list

    def set_dot_position(self, dot_id, x, y): # 设置节点位置
        conflict = False
        for dot_id_now in self.dot_dict:
            if dot_id_now == dot_id:
                continue
            
            xnow, ynow = self.dot_dict[dot_id_now]
            if numpy.linalg.norm(numpy.array([xnow - x, ynow - y])) <= 2*constant_config.CIRCLE_RADIUS + 1:
                conflict =True
                break

        if not conflict: # 不允许点重合
            self.dot_dict[dot_id] = (x, y)

    def get_dot_dict(self) -> dict: # 获得节点表
        return self.dot_dict

    def get_line_dict(self) -> dict: # 获得边表
        return self.line_dict

    def erase_line(self, line_id:str): # 删除一条边
        if self.line_dict.get(line_id) is not None:
            frm, eto = self.line_dict[line_id]
            self.degree[frm] -= 1
            self.degree[eto] -= 1 # 统计度数
            del self.line_dict[line_id]

        inverse_pair_to_erase = []
        for item in self.inverse_pairs:
            line_id_1, line_id_2 = item
            if line_id_1 == line_id or line_id_2 == line_id:
                inverse_pair_to_erase.append(item)

        for item in inverse_pair_to_erase: # 删除所有无效逆序处理
            del self.inverse_pairs[item]

    def new_dot(self, x:int, y:int): # 新增一个节点：不包含共线检查功能
        while self.dot_dict.get("dot_%d" % self.dot_id_max):
            self.dot_id_max += 1
        new_id = "dot_%d" % self.dot_id_max
        self.dot_dict[new_id] = (x, y)
        self.degree[new_id] = 0
        return new_id

    def new_line(self, dot_id_1:str, dot_id_2:str): # 新增一条边：不包含共线检查功能
        assert dot_id_1 != dot_id_2

        if int(dot_id_1.split("_")[-1]) > int(dot_id_2.split("_")[-1]):
            dot_id_1, dot_id_2 = dot_id_2, dot_id_1

        for line_id in self.line_dict:
            frm1, eto1 = self.line_dict[line_id]
            if frm1 == dot_id_1 and eto1 == dot_id_2: # 找到了一个旧的一样的边
                print("old edge found: %s" % line_id)
                return line_id
        
        while self.line_dict.get("line_%d" % self.line_id_max):
            self.line_id_max += 1

        new_id = "line_%d" % self.line_id_max
        self.line_dict[new_id] = (dot_id_1, dot_id_2)
        self.degree[dot_id_1] += 1
        self.degree[dot_id_2] += 1

        print("create new edge: %s" % new_id)
        return new_id

    def erase_dot(self, dot_id:str): # 删除节点的时候，记得删除相应的边，以及边之间的逆序关系
        if self.dot_dict.get(dot_id) is not None:

            if self.base_dot == dot_id: # 删除已经消失的起始点
                self.set_base_dot(None)

            if self.dir_dot == dot_id:
                self.set_dir_dot(None)

            line_list_to_erase = []
            for line_id in self.line_dict:
                dot_id_1, dot_id_2 = self.line_dict[line_id]

                if dot_id in [dot_id_1, dot_id_2]:
                    line_list_to_erase.append(line_id)

            for line_id in line_list_to_erase: # 删除无效线段，以及相应的边关系
                self.erase_line(line_id)

            if dot_id in self.base_dot: # 从两个 list 中删除结点
                self.base_dot.remove(dot_id)

            if dot_id in self.dir_dot:
                self.dir_dot.remove(dot_id)

            del self.dot_dict[dot_id]

            assert self.degree[dot_id] == 0
            del self.degree[dot_id]
            