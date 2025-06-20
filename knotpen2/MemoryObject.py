class MemoryObject:
    def __init__(self) -> None:
        self.dot_id_max = 0
        self.line_id_max = 0

        self.dot_dict = {}
        self.line_dict = {}

    def debug_output(self): # 输出所有节点信息
        for dot_id in self.dot_dict:
            x, y = self.dot_dict[dot_id]
            print("VERTEX: %10s (%5d, %5d)" % (dot_id, x, y))
        
        for line_id in self.line_dict:
            dot_id_1, dot_id_2 = self.line_dict[line_id]
            print("  LINE: %10s (%10s, %10s)" % (line_id, dot_id_1, dot_id_2))

    def set_dot_position(self, dot_id, x, y): # 设置节点位置
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

    def erase_dot(self, dot_id:str): # 删除节点的时候，记得删除相应的边
        if self.dot_dict.get(dot_id) is not None:
            del self.dot_dict[dot_id]

            line_list_to_erase = []
            for line_id in self.line_dict:
                dot_id_1, dot_id_2 = self.line_dict[line_id]

                if dot_id in [dot_id_1, dot_id_2]:
                    line_list_to_erase.append(line_id)

            for line_id in line_list_to_erase:
                self.erase_line(line_id)
