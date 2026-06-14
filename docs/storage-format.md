# Storage File Format Manual

[中文版本](./storage-format.zh-CN.md)

This manual describes the current Knotpen2 save file format.

## Stability And Safety

The format is implementation-oriented and may change in future versions.

Current save files are not strict JSON. They are Python literal text generated with `repr()` and loaded with `eval()` in `MemoryObject.load_object`. This is unsafe for untrusted files. Only open save files that you trust.

## File Locations

Knotpen2 stores user work in project folders. Each project folder contains:

- `project.json`: the main project save file.
- `auto_save/`: automatic save snapshots for that project.
- `auto_save/auto_save.json`: the latest automatic save written during normal use and on exit.
- `answer/`: PD_CODE text and SVG outputs for that project.

The default project is created under `projects/default/` next to the executed program. Crash logs remain under the executed program's `error_log/` folder.

Use **New project**, **Open project**, **Save project**, and **Save as project** in the interface to manage project folders. These actions create or read `project.json` inside the selected folder.

## Encoding And Extension

- Save files use UTF-8 text.
- The project file name is `project.json`.
- Automatic save snapshots use the lowercase `.json` extension.
- The file content must evaluate to a Python `dict`.

## Top-Level Object

A save file stores one dictionary with these keys:

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

## Required Fields

### `dot_id_max`

An integer counter used when allocating new node IDs. New nodes use names like `dot_0`, `dot_1`, and so on. The implementation skips already-used IDs if needed.

### `line_id_max`

An integer counter used when allocating new edge IDs. New edges use names like `line_0`, `line_1`, and so on.

### `dot_dict`

Maps node IDs to 2D positions:

```python
{
    "dot_0": (120, 200),
    "dot_1": (260, 200),
}
```

Positions are stored as `(x, y)` tuples in screen coordinates.

### `line_dict`

Maps edge IDs to endpoint node IDs:

```python
{
    "line_0": ("dot_0", "dot_1"),
}
```

An edge must connect two different nodes. The implementation stores endpoint IDs in ascending numeric node order.

### `inverse_pairs`

Stores crossing order overrides between pairs of edges:

```python
{
    ("line_3", "line_1"): True,
}
```

If two crossing edges do not appear in `inverse_pairs`, the edge with the larger numeric ID is treated as above the edge with the smaller numeric ID. If the pair appears in `inverse_pairs`, that default order is inverted.

The exact rule is implemented by `MemoryObject.check_line_under`.

### `degree`

Maps node IDs to their graph degree:

```python
{
    "dot_0": 2,
    "dot_1": 2,
}
```

PD_CODE calculation requires every node degree to be exactly 2.

### `base_dot`

A list of node IDs marked as base nodes. Each connected component must have exactly one base node before PD_CODE calculation.

### `dir_dot`

A list of node IDs marked as direction nodes. Each connected component must have exactly one direction node before PD_CODE calculation. The direction node must be adjacent to the base node.

## Optional/Derived Field

### `pd_code_final`

Stores derived information used to render PD_CODE arc numbers on the screen after calculation.

This value is cleared whenever topology-affecting edits occur. View panning updates the stored positions because panning does not change topology.

When present, it is a list of dictionaries similar to:

```python
[
    {
        "X": [1, 2, 3, 4],
        "dir": [(1.0, 0.0), (0.0, 1.0)],
        "pos": (200.0, 160.0),
    }
]
```

## Minimal Example

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

This example describes one triangular component without crossings.
