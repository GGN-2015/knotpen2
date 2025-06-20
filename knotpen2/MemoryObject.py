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

        self.base_dot = None # 记录起始位置
        self.dir_dot = None  # 记录定向位置

    def get_inverse_pairs(self):
        return self.inverse_pairs
    
    def shift_position(self, dx, dy): # 所有点一起移动
        for dot_idx in self.dot_dict:
            x, y = self.dot_dict[dot_idx]
            self.dot_dict[dot_idx] = (x + dx, y + dy)

    def set_base_dot(self, dot_idx): # 设置起始位置
        assert self.dot_dict.get(dot_idx) is not None
        self.base_dot = dot_idx
    
    def set_dir_dot(self, dot_idx): # 设置起始位置的下一个位置，用于确定方向
        assert self.dot_dict.get(dot_idx) is not None
        self.dir_dot = dot_idx

    def debug_output(self): # 输出所有节点信息
        for dot_id in self.dot_dict:
            x, y = self.dot_dict[dot_id]
            print("VERTEX: %10s (%5d, %5d)" % (dot_id, x, y))
        
        for line_id in self.line_dict:
            dot_id_1, dot_id_2 = self.line_dict[line_id]
            print("  LINE: %10s (%10s, %10s)" % (line_id, dot_id_1, dot_id_2))

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

    def find_nearest_lines(self, x, y):
        line_pair_list = []
        for line_id in self.line_dict:
            dot_from, dot_to = self.line_dict[line_id]
            pos_from = self.dot_dict[dot_from]
            pos_to   = self.dot_dict[dot_to]
            dis = math_utils.point_to_line_segment_distance((x, y), pos_from, pos_to)

            if dis <= constant_config.LINE_WIDTH / 2 + 1:
                line_pair_list.append((line_id, dis))
        return line_pair_list

    def set_dot_position(self, dot_id, x, y): # 设置节点位置
        conflict = False

        for dot_id_now in self.dot_dict:
            if dot_id_now == dot_id:
                continue
            
            xnow, ynow = self.dot_dict[dot_id_now]
            if numpy.linalg.norm(numpy.array([xnow - x, ynow - y])) <= constant_config.CIRCLE_RADIUS + 1:
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
            del self.line_dict[line_id]

    def new_dot(self, x:int, y:int): # 新增一个节点：不包含共线检查功能
        while self.dot_dict.get("dot_%d" % self.dot_id_max):
            self.dot_id_max += 1
        new_id = "dot_%d" % self.dot_id_max
        self.dot_dict[new_id] = (x, y)
        return new_id

    def new_line(self, dot_id_1:str, dot_id_2:str): # 新增一条边：不包含共线检查功能
        while self.line_dict.get("line_%d" % self.line_id_max):
            self.line_id_max += 1
        new_id = "line_%d" % self.line_id_max
        self.line_dict[new_id] = (dot_id_1, dot_id_2)
        return new_id

    def erase_dot(self, dot_id:str): # 删除节点的时候，记得删除相应的边，以及边之间的逆序关系
        if self.dot_dict.get(dot_id) is not None:
            del self.dot_dict[dot_id]

            line_list_to_erase = []
            for line_id in self.line_dict:
                dot_id_1, dot_id_2 = self.line_dict[line_id]

                if dot_id in [dot_id_1, dot_id_2]:
                    line_list_to_erase.append(line_id)

            for line_id in line_list_to_erase: # 删除无效线段
                self.erase_line(line_id)

            inverse_pair_to_erase = []
            for item in self.inverse_pairs:
                line_id_1, line_id_2 = item
                if line_id_1 in line_list_to_erase or line_id_2 in line_list_to_erase:
                    inverse_pair_to_erase.append(item)

            for item in inverse_pair_to_erase: # 删除所有无效逆序处理
                del self.inverse_pairs[item]