# Algorithm Manual

[中文版本](./algorithm-manual.zh-CN.md)

This manual describes the main algorithms used by Knotpen2.

## Scope

Knotpen2 works with a user-drawn planar projection of a knot or link. Nodes represent control points on the projected curve, and edges connect adjacent control points. Crossings are not stored as nodes; they are detected from geometric intersections of edges.

The core implementation is in:

- `knotpen2/MyAlgorithm.py`
- `knotpen2/MemoryObject.py`
- `knotpen2/math_utils.py`

## Preconditions For PD_CODE

Before PD_CODE calculation, the program checks:

1. There are at least three nodes.
2. Every node has degree exactly 2.
3. Every connected component has exactly one base node.
4. Every connected component has exactly one direction node.
5. The base node and direction node in each component are adjacent.

The program does not currently detect every invalid geometric situation. Users must manually ensure that no point has three segments meeting there.

## Graph Model

The diagram is represented as an undirected graph:

- `dot_dict` stores node positions.
- `line_dict` stores edges between nodes.
- `degree` stores the graph degree of each node.

Because every valid node has degree 2, each connected component is treated as a closed polygonal cycle.

## Connected Components

`MyAlgorithm.get_adj_list()` builds an adjacency list from `line_dict`.

`MyAlgorithm.get_connected_components()` performs DFS over that adjacency list and returns:

- `adj_list`: node adjacency information.
- `block_list`: a list of connected components, each represented as a list of node IDs.

## Orientation

Each connected component must have:

- A base node.
- A direction node adjacent to the base node.

`solve_pd_code()` rotates and possibly reverses each component so that:

```text
component[0] == base node
component[1] == direction node
```

This gives each component a deterministic traversal direction.

## Crossing Detection

Crossings are detected by checking every unordered pair of edges.

Two edges are skipped if they share an endpoint. Otherwise, `math_utils.segments_intersect()` computes the intersection point and parameters `t1`, `t2` on the two segments.

Only strict interior crossings are accepted:

```text
0 < t1 < 1
0 < t2 < 1
```

For each crossing, Knotpen2 records:

- The intersection position.
- The component/node segment identity for both intersecting edges.
- The local segment parameters.
- The two edge IDs.

## Crossing Order

Crossing over/under information is stored in `MemoryObject.inverse_pairs`.

`MemoryObject.check_line_under(line_id_1, line_id_2)` determines whether one edge passes under the other. The default order is derived from numeric edge IDs, and `inverse_pairs` toggles that default.

Users can click a crossing in the UI to toggle this relation.

## Arc Splitting

After crossings are detected, each connected component is split into arc segments.

For every crossing, the algorithm creates two half-crossing records, one on each involved component. It then sorts those records by:

```text
(node index on component, local segment parameter)
```

The sorted half-crossings partition the component into arcs. Each arc later receives a global integer label used in the final PD_CODE.

## PD_CODE Construction

For each crossing, the algorithm:

1. Determines which strand is below and which is above.
2. Locates the incoming and outgoing arc IDs around the crossing.
3. Uses a 2D left-turn test to choose the correct local ordering.
4. Produces a raw crossing record with four arc identifiers.

Raw arc identifiers are component-local tuples. The algorithm sorts all unique arc identifiers and maps them to final integer labels starting from 1.

The final displayed PD_CODE is a sorted list of quadruples.

## SVG Generation

`MyAlgorithm.calculate_svg()` uses the component traversal and crossing split data to produce SVG paths.

Important details:

- Curves are emitted as quadratic Bezier paths.
- Under-strands are shortened near crossings so the over/under relationship is visible.
- `.num.svg` includes arc number text.
- `.nonum.svg` omits arc numbers.
- `.arrow.svg` includes direction arrows.

The SVG view box is computed from the diagram's node bounding box.

## Known Limitations

- The program does not automatically reject triple intersections.
- The save format trusts internal consistency between `line_dict` and `degree`.
- Very dense diagrams may become slow because crossings are found by checking edge pairs.
- The over/under state is tied to edge pairs, so moving nodes can change which crossings exist. Users should recheck crossing order after moving nodes.
