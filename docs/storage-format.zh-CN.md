# 存储文件格式手册

[English version](./storage-format.md)

本文描述 Knotpen2 当前的存档文件格式。

## 稳定性与安全性

当前格式更接近内部实现格式，未来版本可能改变。

当前存档文件不是真正严格的 JSON，而是由 `repr()` 生成、由 `MemoryObject.load_object` 中的 `eval()` 读取的 Python 字面量文本。对不可信文件使用 `eval()` 存在安全风险。请只打开来源可信的存档文件。

## 文件位置

Knotpen2 会把用户作品保存在项目文件夹中。每个项目文件夹包含：

- `project.json`：项目主存档文件。
- `auto_save/`：该项目的自动保存快照。
- `auto_save/auto_save.json`：正常使用和退出时写入的最新自动保存。
- `answer/`：该项目的 PD_CODE 文本和 SVG 输出。

默认项目会创建在可写用户数据目录下的 `projects/default/` 中。崩溃日志位于该目录下的 `error_log/` 文件夹。安装后可以用 `knotpen2 --data-dir` 查看这个目录；从源码运行时可以用 `python knotpen2/test_main.py --data-dir` 查看。

对于 Windows 打包版，可写数据目录就是 `main.exe` 所在文件夹，因此默认项目和崩溃日志仍位于可执行文件旁边。

请通过界面中的 **新建项目**、**打开项目**、**保存项目** 和 **另存为项目** 管理项目文件夹。这些操作会在所选文件夹中创建或读取 `project.json`。

## 编码与扩展名

- 存档文件使用 UTF-8 文本。
- 项目文件名为 `project.json`。
- 自动保存快照使用小写 `.json` 扩展名。
- 文件内容必须能求值为 Python `dict`。

## 顶层对象

存档文件保存一个字典，包含以下键：

```python
{
    "dot_id_max": int,
    "line_id_max": int,
    "dot_dict": dict,
    "line_dict": dict,
    "inverse_pairs": dict,
    "degree": dict,
    "base_dot": list,
    "dir_dot": list,
    "pd_code_final": object | None,
}
```

## 必要字段

### `dot_id_max`

用于分配新节点 ID 的整数计数器。新节点命名为 `dot_0`、`dot_1` 等。如果某个 ID 已被占用，程序会继续向后寻找可用 ID。

### `line_id_max`

用于分配新边 ID 的整数计数器。新边命名为 `line_0`、`line_1` 等。

### `dot_dict`

把节点 ID 映射到二维位置：

```python
{
    "dot_0": (120, 200),
    "dot_1": (260, 200),
}
```

位置以屏幕坐标中的 `(x, y)` 元组保存。

### `line_dict`

把边 ID 映射到端点节点 ID：

```python
{
    "line_0": ("dot_0", "dot_1"),
}
```

一条边必须连接两个不同节点。实现中会按节点编号的数值升序保存端点 ID。

### `inverse_pairs`

保存两条边在交叉点处上下关系的反转记录：

```python
{
    ("line_3", "line_1"): True,
}
```

如果两条交叉边没有出现在 `inverse_pairs` 中，则默认编号较大的边位于编号较小的边上方。如果该边对出现在 `inverse_pairs` 中，则反转默认上下关系。

具体规则见 `MemoryObject.check_line_under`。

### `degree`

把节点 ID 映射到图论意义上的度：

```python
{
    "dot_0": 2,
    "dot_1": 2,
}
```

计算 PD_CODE 前，每个节点的度必须恰好为 2。

### `base_dot`

记录被标记为起始点的节点 ID 列表。计算 PD_CODE 前，每个连通分支都必须恰好有一个起始点。

### `dir_dot`

记录被标记为方向点的节点 ID 列表。计算 PD_CODE 前，每个连通分支都必须恰好有一个方向点，并且方向点必须与起始点相邻。

## 可选/派生字段

### `pd_code_final`

保存计算后用于在屏幕上绘制 PD_CODE 弧线编号的派生信息。

任何影响拓扑结构的编辑都会清空该字段。视图平移不会改变拓扑，因此会同步移动其中保存的位置。

存在时，它通常是类似下面的字典列表：

```python
[
    {
        "X": [1, 2, 3, 4],
        "dir": [(1.0, 0.0), (0.0, 1.0)],
        "pos": (200.0, 160.0),
    }
]
```

## 最小示例

```python
{
    "dot_id_max": 3,
    "line_id_max": 3,
    "dot_dict": {
        "dot_0": (100, 100),
        "dot_1": (200, 100),
        "dot_2": (150, 180),
    },
    "line_dict": {
        "line_0": ("dot_0", "dot_1"),
        "line_1": ("dot_0", "dot_2"),
        "line_2": ("dot_1", "dot_2"),
    },
    "inverse_pairs": {},
    "degree": {
        "dot_0": 2,
        "dot_1": 2,
        "dot_2": 2,
    },
    "base_dot": ["dot_0"],
    "dir_dot": ["dot_1"],
    "pd_code_final": None,
}
```

这个示例描述一个没有交叉点的三角形连通分支。
