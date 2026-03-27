# Cercetari-Operationale - Primal Simplex Solver & GUI

## Overview

This repository contains a robust, production-ready implementation of the **Primal Simplex Algorithm** in Python, used to solve linear programming problems. It includes a highly optimized mathematical backend (`ASP_back.py`), a comprehensive test suite of edge cases (`problems.py`), and a modern Graphical User Interface (`ASP_front.py`) built with PySide6.

## The Simplex Algorithm

The Simplex algorithm is a fundamental method in operations research for solving linear programming problems. It finds the optimal solution (maximum or minimum) to a linear objective function subject to linear constraints.

### Key Features:
- **Optimization Type**: Supports both minimization (`MIN`) and maximization (`MAX`) problems.
- **Constraint Types**: Handles all three types of constraints seamlessly (≤, ≥, =).
- **Method**: Uses the Primal Simplex approach with Gauss-Jordan elimination.
- **Big-M Method**: Automatically implements artificial variables with high penalty ($10^6$) for constraint handling.
- **Cycle Detection**: Prevents infinite loops (degeneracy/cycling) by calculating the theoretical maximum number of iterations (`comb(n_var, n_con)`).

## Mathematical Backend (`ASP_back.py`)

### Method Outputs

#### `solve(data_type, with_table=False, **prob)`
Executes the Primal Simplex Algorithm and returns the result of the optimization. 

* **Optimal Solution (Dictionary):** If a finite optimal solution is found, it returns a detailed dictionary containing metadata for every variable (decision, slack, surplus, and artificial). 
  ```python
  {
    'x1': {'valoare': 20.0, 'tip': 'decizie', 'coef_obiectiv': 15.0},
    'y1': {'valoare': 5.0,  'tip': 'compensare (<=)', 'coef_obiectiv': 0.0},
    # ...
  }
  ```
* **Error / Edge Case Strings:** If the problem cannot be solved, it safely exits and returns one of the following string messages:
  * `"Problema are solutie nemarginita (Z tinde la infinit)."`
  * `"Problema nu are solutie admisibila (sistem incompatibil)."`
  * `"Ciclare detectata: algoritmul nu converge in X iteratii."`

#### `verify()`
Performs three independent mathematical checks to validate the integrity of the computed solution. It returns a `dict` containing the boolean results `[bool, bool, bool]` and detailed mathematical proofs.
* **Check 1 (Non-negativity):** `True` if all variables in the final solution satisfy $x_i \ge 0$.
* **Check 2 (Objective Match):** `True` if the dot product of the original objective coefficients and the computed decision variables matches the algorithm's final $Z$ value (within a `1e-6` tolerance).
* **Check 3 (Matrix Consistency):** `True` if multiplying the initial basis ($S$) by the final state accurately reconstructs the initial constants ($b_0$).

## Graphical User Interface (`ASP_front.py`)

The project includes a fully functional desktop application built with **PySide6**. 

### GUI Features:
- **Dynamic Inputs:** Automatically generates the correct number of input fields based on the specified number of variables and constraints.
- **Easy Constraint Mapping:** Dropdown menus for `< =`, `>`, and `=`.
- **Result Dialog:** Presents the detailed dictionary output and the `verify()` mathematical checks in a clean, readable text window.
- **Visual Mathematical Proofs:** Renders the algebraic consistency checks (e.g., matrix reconstruction $S \times X_b = b$) as beautifully formatted, monospace equations directly in the UI.
- **Error Handling:** Triggers warning pop-ups for unbounded, infeasible, or cycling problems.

**To run the GUI:**
```bash
pip install PySide6 numpy
python ASP_front.py
```

## How to Use the Simplex Class (Backend)

### Basic Usage

```python
from ASP_back import Simplex
import numpy as np

# Create a solver instance
solver = Simplex()

# Define your problem parameters using the required structure
problem = {
    "coef": np.array([3, 2, 0], dtype=np.float64),            
    "MatriceA": np.array([[1, 1], [2, 1]], dtype=np.float64), 
    "b": np.array([4, 5], dtype=np.float64),                  
    "inegalitate": np.array([1, 1], dtype=int), # 0 for ≥, 1 for ≤, 2 for =
    "OPT": -1                                   # -1 for MAX, 1 for MIN
}

# Solve the problem (set with_table=True to print Tableau steps)
solution = solver.solve(np.float64, **problem) # or .solve(np.float64, True, **problem)  -  in order to show the Simplex Table

# Verify the solution
verification_results = solver.verify()

# Print results
if isinstance(solution, dict):
    print("Optimal Solution found!")
    for var, data in solution.items():
        print(f"{var} = {data['valoare']} ({data['tip']})")
    
    print("\nVerification:", verification_results["result"])
else:
    print("Solver Error:", solution)
```

## The Test Suite (`problems.py`)
The repository includes a massive dictionary of over 25 pre-configured linear programming problems designed to stress-test the algorithm. 
It includes:
✅ Standard Minimization & Maximization
✅ 10x10 Enterprise resource planning simulations
✅ **Degeneracy & Ties:** Equal Deltas, identical coefficients, and $b_i = 0$ cases.
✅ **Classic Operations Research Cycles:** Beale's Cycle, Marshall's Cycle, and Bland's rule stress tests.
✅ **Edge Cases:** Unrestricted variables, Big-M swamping, and redundant equality rows.
```