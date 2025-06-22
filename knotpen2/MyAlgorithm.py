from . import MemoryObject
import collections

class MyAlgorithm:
    def __init__(self, memory_object:MemoryObject.MemoryObject) -> None:
        self.memory_object = memory_object

    def degree_check(self): # 检查是不是所有节点的度都等于 2
        dot_dict = self.memory_object.get_dot_dict()
        degree   = self.memory_object.get_degree()

        degree_fault_arr = [] # 返回度数不对的节点
        for dot_id in dot_dict:
            if degree[dot_id] != 2:
                degree_fault_arr.append(dot_id)
        return degree_fault_arr
    
    def get_adj_list(self) -> dict: # 获得节点邻接表
        dot_dict  = self.memory_object.get_dot_dict()
        line_dict = self.memory_object.get_line_dict()

        adj_list = {}
        for dot in dot_dict:
            adj_list[dot] = [] # 记录所有后继节点

            for line in line_dict:
                dot_id_1, dot_id_2 = line_dict[line] # 枚举边表
                if dot_id_1 == dot:
                    adj_list[dot].append(dot_id_2)
                elif dot_id_2 == dot:
                    adj_list[dot].append(dot_id_1)
        return adj_list

    def get_connected_components(self): # 获取每个联通分支的 base 和 dir 点
        vis = {}
        queue = collections.deque()
        adj_list = self.get_adj_list() # 获取邻接表
        block_list = [] # 记录所有连通分支的信息
        for dot_id in self.memory_object.get_dot_dict():
            if vis.get(dot_id) is True: # 避免重复 bfs 同一个节点
                continue
            block_now = [dot_id]
            vis[dot_id] = True
            queue.append(dot_id)

            while len(queue) > 0: # BFS
                node_now = queue.popleft()
                for next_dot in adj_list[node_now]:
                    if vis.get(next_dot) is not True:
                        block_now.append(next_dot)
                        vis[next_dot] = True
                        queue.append(next_dot)
            
            block_list.append(block_now) # 记录当前连通分支
        return adj_list, block_list
    
    def check_base_dir(self, adj_list, block_list): # 检查每个连通分支是否有 base 和 dir 以及他们是否相邻
        block_id_to_base_dot = {}
        block_id_to_dir_dot = {}

        for i in range(len(block_list)):
            block_id_to_base_dot[i] = []
            block_id_to_dir_dot[i] = []
            block_now = block_list[i]

            for j in range(len(block_now)):
                node_now = block_now[j]

                if node_now in self.memory_object.base_dot: # 记录所有 base_dot
                    block_id_to_base_dot[i].append(node_now)

                if node_now in self.memory_object.dir_dot: # 记录所有 dir_dot
                    block_id_to_dir_dot[i].append(node_now)
        
        for i in range(len(block_list)): # 返回检查到的错误信息
            rep    = block_list[i][0]
            rep_num = int(rep.split("_")[-1]) # 代表元

            if len(block_id_to_base_dot[i]) == 0:
                return False, "节点 %d 所在的连通分支没有定义起始点" % rep_num, None, None, [rep]
            
            if len(block_id_to_base_dot[i]) >= 2:
                return False, "节点 %d 所在的连通分支没有定义了太多起始点" % rep_num, None, None, [rep]
            
            if len(block_id_to_dir_dot[i]) == 0:
                return False, "节点 %d 所在的连通分支没有定义方向点" % rep_num, None, None, [rep]
            
            if len(block_id_to_dir_dot[i]) >= 2:
                return False, "节点 %d 所在的连通分支没有定义了太多方向点" % rep_num, None, None, [rep]
            
            base = block_id_to_base_dot[i][0]
            dirx  = block_id_to_dir_dot[i][0]

            if dirx not in adj_list[base]:
                base_num = int(base.split("_")[-1])
                dirx_num = int(dirx.split("_")[-1])
                return False, "起始点 %d 与方向点 %d 在同一连通分支但并不相邻" % (base_num, dirx_num), None, None, [base, dirx]
        
        return True, "", block_id_to_base_dot, block_id_to_dir_dot, [] # 没有检查到错误

    # 计算 pd_code
    # 这个程序可能很慢将来再考虑优化问题
    def solve_pd_code(self, adj_list, block_list, baseL, dirL):
        
        for i in range(len(block_list)):
            base_val = baseL[i][0]
            dir_val  = dirL[i][0]

            find = None
            for j in range(len(block_list[i])): # 找到 base 所在的位置
                if block_list[i][j] == base_val:
                    find = j
                    break
            assert find is not None

            block_list[i] = block_list[i][find:] + block_list[i][:find]

            if block_list[i][1] != dir_val: # 这说明 dir_val 在最后
                block_list[i] = block_list[i][::-1] # 先反转
                block_list[i] = block_list[i][-1] + block_list[i][:-1] # 再把最后一个挪到最前面

            assert block_list[i][0] == base_val # 调整正确的顺序
            assert block_list[i][0] == dir_val