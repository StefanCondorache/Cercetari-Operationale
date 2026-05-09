# Graph Theory & Network Optimizations

This module contains interactive Python-based applications that solve and visually demonstrate two of the most well-known graph optimization problems.

The module is integrated into the main suite and features graphical configuration screens (tables) for dynamic data input.

## 1. Ford-Fulkerson Algorithm Visualizer (Max Flow)

Calculates and displays the maximum flow that can traverse a network from a source node to a sink node (implemented via Breadth-First Search, also known as the Edmonds-Karp algorithm).

### Features
* **Step-by-Step Visualization:** Advance through the algorithm iteration by iteration to observe the flow's path through the network.
* **Accurate Labeling:** Displays standard algorithmic labels (e.g., `(+x)` for forward edges and `(-x)` for backward edges).
* **Detailed Flow History:** A cumulative history of the flow is displayed on the edges (e.g., `20 = 10 + 10 ●`). Saturated edges are clearly marked with a `●`, and unsaturated ones with a `+`.
* **Bidirectional Navigation:** The "Step Back" button allows you to undo the last iteration for a deeper analysis of residual graphs.
* **Min-Cut Theorem:** Upon completion of the algorithm, the "bottleneck" edges that restrict the network (the minimum cut) are highlighted with dashed orange lines.

## 2. Hungarian Algorithm Visualizer (Assignment Problem)

Finds the minimum cost perfect matching in a bipartite graph (e.g., the optimal allocation of `N` workers to `N` tasks).

### Features
* **Bipartite Representation:** Visualizes the solution as two independent sets of nodes (Left - `L` and Right - `R`), drawing the matching connections between them.
* **Matrix Reductions Console:** While the visualization focuses on the graph, the side console clearly shows the matrix transformations (framed zeros `[0]`, crossed-out zeros `0x`, and row/column coverage with asterisks `*`).
* **Dynamic Matching Update:** At each failed step, the algorithm calculates `epsilon` and modifies the matrix, reflecting the newly found partial matching in the interface.
* **Mathematical Validation:** The final solution displayed in the console includes the minimum assignment cost and the cross-verification test of sums (minimums + epsilons).

## How to Run

This module can be ran in isolation using the following command:

`.venv/bin/python3 -m TeoriaGrafurilor.main`

Once the menu opens, choose between the Max Flow and Assignment problems, and then input your data into the configuration tables.