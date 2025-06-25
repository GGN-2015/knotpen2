from . import MemoryObject
from . import math_utils
import numpy as np

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
        # 这里的 nid 能够反应前进方向，但是并不是最终的弧线编号，而只是一个节点编号
        # debug 中：block_list 的计算为检测到异常
        dot_id_to_new_id = {}
        new_id_to_dot_id = {}
        for i in range(len(block_list)):
            for j in range(len(block_list[i])):
                dot_id_to_new_id[block_list[i][j]] = (i, j)
                new_id_to_dot_id[(i, j)] = block_list[i][j] # 这个过程必须是可逆的

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
                if n2 == 0:
                    assert n1 == 1 or n1 == length-1
                    return n1 == 1

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

                p11 = dot_dict[d11] # 找到四个点的空间坐标，现在的顺序还是 line_dict 中的顺序，这里面的顺序一般来说都不对
                p12 = dot_dict[d12]
                p21 = dot_dict[d21]
                p22 = dot_dict[d22]

                nid11 = dot_id_to_new_id[d11] # 找到四个新编号，新编号是 bid 和 bdid 的二元组
                nid12 = dot_id_to_new_id[d12]
                nid21 = dot_id_to_new_id[d21]
                nid22 = dot_id_to_new_id[d22]

                # 注意：n-1 在 0 的前面
                if check_after(nid11, nid12, block_list): # 调整顺序，使得顺序服从原始顺序
                    d11, d12 = d12, d11
                    p11,   p12   =   p12,   p11
                    nid11, nid12 = nid12, nid11

                if check_after(nid21, nid22, block_list): # 调整顺序，使得顺序服从原始顺序
                    d21, d22 = d22, d21
                    p21,   p22   =   p22,   p21
                    nid21, nid22 = nid22, nid21

                # 保证 nid11 在 nid12 前面， 保证 nid21 在 nid22 前面
                assert check_after(nid12, nid11, block_list)
                assert check_after(nid22, nid21, block_list)

                # t1 是线段在 p11, p12 上的参数 
                # t2 是线段在 p21, p22 上的参数
                pos, t1, t2 = math_utils.segments_intersect((p11, p12), (p21, p22))
                if pos is None: # 没有找到交叉点，则返回
                    continue

                assert isinstance(t1, float) and isinstance(t2, float)
                assert 0 < float(t1) < 1
                assert 0 < float(t2) < 1 # 这说明有结点位于其他结点上面，可能会导致错误

                crossing_list.append((pos, nid11, t1, nid21, t2, line_id_1, line_id_2)) # 使用七元组描述所有找到的交叉点
        
        leave_msg("总计找到了 %d 个交叉点" % len(crossing_list))

        # 考虑交叉点所在的弧线段，并给所有弧线段进行编号
        parts = [[] for _ in range(len(block_list))] # 为每一个连通分支，记录它上面有哪些交点
        for crossing_index, crossing in enumerate(crossing_list):
            pos, nid11, t1, nid21, t2, _, _ = crossing             # 拿出一个交叉点来
            parts[nid11[0]].append((nid11[1], t1, crossing_index, 0)) # 这样可以确定出两个半交点
            parts[nid21[0]].append((nid21[1], t2, crossing_index, 1)) # 我们可以为每个半交点计算出，它所在的连通分支以及它是第几个

        cid_half_id_to_bid_arc_id = {}
        for bid in range(len(block_list)): # 对所有分界点进行排序
            parts[bid] = sorted(parts[bid])
            leave_msg("连通分支 %d 被分割成了 %d 段" % (bid, len(parts[bid])))

            for arc_id, half_crossing in enumerate(parts[bid]):
                _, _, cid, half_id = half_crossing
                cid_half_id_to_bid_arc_id[(cid, half_id)] = (bid, arc_id)

        def check_left_turn(vec1, vec2): # 检查 vec1 到 vec2 是否是左转
            x1, y1 = vec1
            x2, y2 = vec2
            return x1 * y2 - x2 * y1 > 0

        def np_point_to_tuple(np_point:np.ndarray):
            assert np_point.shape == (2, )
            return (float(np_point[0]), float(np_point[1]))

        # 为每一个交叉点生成字符串形式的 pd_code_raw
        pd_code_raw = []
        for cid in range(len(crossing_list)):
            pos, nid11, t1, nid21, t2, line_id_1, line_id_2  = crossing_list[cid]

            bid1, aid1 = cid_half_id_to_bid_arc_id[(cid, 0)]
            bid2, aid2 = cid_half_id_to_bid_arc_id[(cid, 1)]

            line_1_under_line_2 = self.memory_object.check_line_under(line_id_1, line_id_2)

            if not line_1_under_line_2: # 交换，使得 line_1 总是在 line_2 下面
                nid11, nid21 = nid21, nid11
                t1, t2 = t2, t1
                line_id_1, line_id_2 = line_id_2, line_id_1
                bid1, bid2 = bid2, bid1
                aid1, aid2 = aid2, aid1
                line_1_under_line_2 = True

            # 于是我们知道 line_1 总是在 line_2 下面
            dot_id_11 = new_id_to_dot_id[nid11]
            dot_id_21 = new_id_to_dot_id[nid21]

            # 获得原始位置向量
            pos11 = self.memory_object.get_dot_dict()[dot_id_11]
            pos21 = self.memory_object.get_dot_dict()[dot_id_21]

            # 条件成立，说明 pos21 在 pos11 的左侧
            if check_left_turn(np.array(pos11) - np.array(pos), np.array(pos21) - np.array(pos)):
                pd_code_raw.append({"X":[
                    (bid1, aid1),
                    (bid2, aid2),
                    (bid1, (aid1 + 1) % len(parts[bid1])),
                    (bid2, (aid2 + 1) % len(parts[bid2])), # 需要考虑最后一条 arc
                ], "dir":[
                    np_point_to_tuple(np.array(pos11) - np.array(pos)), # 记录第一个 index 对应的方向和第二个 index 对应的方向，用于未来显示
                    np_point_to_tuple(np.array(pos21) - np.array(pos))
                ], "pos": pos})
            else:
                pd_code_raw.append({"X":[
                    (bid1, aid1),
                    (bid2, (aid2 + 1) % len(parts[bid2])),
                    (bid1, (aid1 + 1) % len(parts[bid1])), # 需要考虑最后一条 arc
                    (bid2, aid2),
                ], "dir":[
                    np_point_to_tuple(np.array(pos11) - np.array(pos)), # 记录第一个 index 对应的方向和第二个 index 对应的方向，用于未来显示
                    np_point_to_tuple(-(np.array(pos21) - np.array(pos)))
                ], "pos": pos})
        
        # 程序运行到这里已经获得了可用的 pd_code_raw 了
        # 我们需要借助排序进一步计算得到具有统一编号的 pd_code
        item_list = []
        for crossing in pd_code_raw: # 拿出所有编号来
            for term in crossing["X"]:
                if term not in item_list:
                    item_list.append(term)

        item_list = sorted(item_list)
        tup_to_real_id = {}
        for idx, val in enumerate(item_list): # 为每一个弧线段赋予一个最终的有效整数 id
            tup_to_real_id[val] = idx + 1

        # 经过这一次处理后得到的 pd_code 将是最终的 pd_code
        # 我们首先对 pd_code_raw 进行一次深拷贝
        pd_code_final = eval(repr(pd_code_raw))
        pd_code_to_show = []
        for pd_code_term in pd_code_final:
            for i in range(4):
                pd_code_term["X"][i] = tup_to_real_id[pd_code_term["X"][i]]

            clock_wise = pd_code_term["X"]
            anti_clock_wise = [clock_wise[0]] + clock_wise[1:][::-1]
            pd_code_to_show.append(anti_clock_wise)
        
        # 返回最终 pd_code
        return sorted(pd_code_to_show), pd_code_final
