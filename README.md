# Cercetari-Operationale

## Overview

This repository contains an implementation of the **Primal Simplex Algorithm** in Python, used to solve linear programming problems.

## The Simplex Algorithm

The Simplex algorithm is a fundamental method in operations research for solving linear programming problems. It finds the optimal solution (maximum or minimum) to a linear objective function subject to linear constraints.

### Key Features:
- **Optimization Type**: Supports both minimization and maximization problems
- **Constraint Types**: Handles three types of constraints:
  - Less than or equal (≤)
  - Greater than or equal (≥)
  - Equality (=)
- **Method**: Uses the Primal Simplex approach with Gauss-Jordan elimination
- **Big-M Method**: Implements artificial variables for constraint handling

### Algorithm Steps:
1. Convert constraints to standard form with slack/surplus/artificial variables
2. Initialize the basis with artificial variables if needed
3. Calculate reduced costs (Delta values)
4. Check optimality conditions:
   - For maximization: all reduced costs ≤ 0
   - For minimization: all reduced costs ≥ 0
5. If not optimal, select entering and leaving variables
6. Perform pivot operation using Gauss-Jordan elimination
7. Repeat until optimality is reached or unbounded solution is detected

### Method Outputs

#### `solve(data_type, **prob)`
Executes the Primal Simplex Algorithm and returns the result of the optimization. 
* **Optimal Solution:** If a finite optimal solution is found, it returns a 1D `numpy.ndarray` containing the final values of the decision variables.

* **Unbounded Solution:** If the feasible region is open and the objective function can grow infinitely, it returns the string message: 
                                                                              `"Problema are solutie nemarginita (Z tinde la infinit)."`.

* **Incompatible System:** If the problem has no feasible region (artificial variables remain in the basis with a non-zero value), it returns the string message:   
                                                                                                  `"Problema nu are solutie admisibila (sistem incompatibil)."`.

#### `verify()`
Performs three independent mathematical checks to validate the integrity of the computed solution. It returns a `list` of three booleans (`[bool, bool, bool]`).
* **Check 1 (Index 0 - Non-negativity):** `True` if all variables in the final solution satisfy the non-negativity constraint ($x_i \ge 0$).

* **Check 2 (Index 1 - Objective Match):** `True` if the dot product of the original objective coefficients and the computed decision variables matches the algorithm's final $Z$ value (within a `1e-3` tolerance).

* **Check 3 (Index 2 - Matrix Consistency):** `True` if multiplying the initial basis by the final state accurately reconstructs the initial constants, proving the Gauss-Jordan eliminations were applied correctly.

## How to Use the Simplex Class

### Basic Usage

```python
from ASP import Simplex
import numpy as np

# Create a solver instance
solver = Simplex()

# Define your problem parameters
problem = {
    "coef": np.array([3, 2, 0]),            # Objective function coefficients
    "MatriceA": np.array([[1, 1], [2, 1]]), # Constraint coefficients
    "b": np.array([4, 5]),                  # Right-hand side values
    "inegalitate": np.array([1, 1]),        # Constraint types (0 for ≥, 1 for ≤, 2 for =)
    "OPT": 1                                # -1 for MAX, 1 for MIN
}

# Solve the problem
solution = solver.solve(np.float64, **problem)

# Verify the solution
verification_results = solver.verify()

# Print results
print("Solution:", solution)
print("Objective Value (Z):", solver.Z)
print("Verification Results:", verification_results)
```

### It handles:
✅ Minimization & Maximization
✅ All constraint types ($\le, \ge, =$)
✅ Big-M penalties
✅ Identical coefficients (degeneracy)
✅ Equal Delta ties (Bland's Rule)
✅ Incompatible systems (no feasible region)
✅ Unbounded problems
✅ Redundant constraints
✅ Floating-point noise filtering