from . import MemoryObject
from . import math_utils

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

    def __dfs(self, vis, adj_list, dot_now, block_now):
        vis[dot_now] = True
        block_now.append(dot_now)

        for dot_next in adj_list[dot_now]:
            if vis.get(dot_next) is not True:
                self.__dfs(vis, adj_list, dot_next, block_now)

    def get_connected_components(self): # 获取每个联通分支的 base 和 dir 点
        vis = {}
        adj_list = self.get_adj_list() # 获取邻接表
        block_list = [] # 记录所有连通分支的信息
        for dot_id in self.memory_object.get_dot_dict():
            if vis.get(dot_id) is True: # 避免重复 bfs 同一个节点
                continue
            block_now = []
            self.__dfs(vis, adj_list, dot_id, block_now)
            block_list.append(block_now)
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
            rep     = block_list[i][0]
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
    def solve_pd_code(self, adj_list, block_list, baseL, dirL, leave_msg):
        
        # 调整 block_list 到正确的顺序：base_node -> dir_node -> ...
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
                block_list[i] = [block_list[i][-1]] + block_list[i][:-1] # 再把最后一个挪到最前面
            
            assert block_list[i][0] == base_val # 调整正确的顺序
            assert block_list[i][1] == dir_val

        # 计算新的编号：Ci_Nj 表示一个节点位于连通分量 i、第 j 个节点
        dot_id_to_new_id = {}
        for i in range(len(block_list)):
            for j in range(len(block_list[i])):
                dot_id_to_new_id[block_list[i][j]] = (i, j)

        # 检查 nid1 是否位于 nid2 的后面的一个
        # 要求 nid1 和 nid2 必须在同一个连通分支上且相邻，否则会报错
        def check_after(nid1, nid2, block_list) -> bool: 
            c1, n1 = nid1
            c2, n2 = nid2

            assert c1 == c2
            length = len(block_list[c1])

            if n1 == 0:
                assert n2 == 1 or n2 == length-1
                return n2 == length-1
            
            else:
                assert abs(n1 - n2) == 1
                return n2 == n1-1

        # 定位所有交叉点的两重身份：(c1, n1, t1), (c2, n2, t2)
        # n1 表示交叉点所在的弧线，位于 c1 连通分支上第 n1 个节点后面的一段弧线
        # t1 表示他在这段弧线上的坐标 \in (0, 1)
        line_dict = self.memory_object.get_line_dict()
        dot_dict = self.memory_object.get_dot_dict()
        crossing_list = []
        for line_id_1 in line_dict:
            for line_id_2 in line_dict:

                if line_id_2 <= line_id_1: # 避免重复计算
                    continue
                d11, d12 = line_dict[line_id_1]
                d21, d22 = line_dict[line_id_2]

                if d21 in [d11, d12] or d22 in [d11, d12]: # 如果有交集，就跑路
                    continue

                p11 = dot_dict[d11] # 找到四个点的空间坐标
                p12 = dot_dict[d12]
                p21 = dot_dict[d21]
                p22 = dot_dict[d22]

                nid11 = dot_id_to_new_id[d11] # 找到四个新编号
                nid12 = dot_id_to_new_id[d12]
                nid21 = dot_id_to_new_id[d21]
                nid22 = dot_id_to_new_id[d22]

                if nid11[1] > nid12[1]: # 先把编号小的 swap 到前面
                    p11, p12 = p12, p11
                    nid11, nid12 = nid12, nid11
                    
                if nid21[1] > nid22[1]: # 先把编号小的 swap 到前面
                    p21, p22 = p22, p21
                    nid21, nid22 = nid22, nid21

                # 注意：n-1 在 0 的前面
                if check_after(nid11, nid12, block_list): # 调整顺序，使得顺序服从原始顺序
                    p11,   p12   =   p12,   p11
                    nid11, nid12 = nid12, nid11

                if check_after(nid21, nid22, block_list): # 调整顺序，使得顺序服从原始顺序
                    p21,   p22   =   p22,   p21
                    nid21, nid22 = nid22, nid21

                # t1 是线段在 p11, p12 上的参数 
                # t2 是线段在 p21, p22 上的参数
                pos, t1, t2 = math_utils.segments_intersect((p11, p12), (p21, p22))
                if pos is None: # 没有找到交叉点，则返回
                    continue

                assert isinstance(t1, float) and isinstance(t2, float)
                assert 0 < float(t1) < 1
                assert 0 < float(t2) < 1 # 这说明有结点位于其他结点上面，可能会导致错误

                crossing_list.append((pos, p11, t1, p21, t2)) # 使用五元组描述所有找到的交叉点
        
        leave_msg("找到了 %d 个交叉点" % len(crossing_list))

        # 考虑交叉点所在的弧线段，并给所有弧线段进行编号