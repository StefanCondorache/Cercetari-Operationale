# Ford-Fulkerson Algorithm Visualizer

This project is a Python-based interactive application that calculates and visualizes the maximum flow in a flow network using the **Ford-Fulkerson Algorithm** (implemented via Breadth-First Search, also known as the Edmonds-Karp algorithm).

## Features

The application provides an interactive Graphical User Interface (GUI) designed to help users dissect and understand the underlying mathematics of the algorithm:
* **Step-by-Step Visualization:** Advance through the algorithm iteration by iteration to see exactly how the flow is formed.
* **Accurate Node Labeling:** Displays standard algorithmic labels, using `(+x)` for forward edge traversal and `(-x)` for backward residual edge traversal.
* **Detailed Flow History:** Edges display a cumulative history of flow additions/subtractions (e.g., `21 = 20 + 1 ●`). Saturated edges are clearly marked with a `●`, while unsaturated ones are marked with a `+`.
* **Bidirectional Navigation:** A "Step Back" feature allows you to undo the last iteration and reconstruct the previous mathematical state, making it easier to analyze complex paths and residual flows.
* **Min-Cut Visualization:** Upon completion, the "bottleneck" edges that restrict the flow (the minimum cut) are graphically highlighted with dashed orange lines, practically demonstrating the Max-Flow Min-Cut Theorem.

## Project Structure

* `Graph_back.py` - The backend engine. The `Graph` class processes the input data, solves the mathematical problem, and generates the iteration history, the maximum flow, and the minimum cut edges.
* `Graph_front.py` - The frontend GUI built with **PySide6**. It handles rendering the nodes, directional arrows, labels, and the logic for the navigation buttons.
* `requirements.txt` - The list of dependencies required to run the project.

## Installation

1. Ensure you have [Python](https://www.python.org/downloads/) installed (version 3.8 or newer).
2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To launch the graphical visualizer, run the main frontend script:

```bash
python Graph_front.py
```

## Customizing the Input Data
At the bottom of the `Graph_front.py` file, there is a dictionary named `problema_test`. You can modify this dictionary to build and solve your own custom flow networks. Ensure you maintain the following structure:

```python
problema_test = {
    'date_intrare': {
        'c1': {'node': ('start_node', 'target_node'), 'value': capacity},
        # ... add as many edges as needed
    },
    'sursa': 'name_of_source_node',
    'destinatie': 'name_of_sink_node'
}
```
