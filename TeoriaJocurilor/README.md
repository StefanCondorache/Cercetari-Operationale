# TeoriaJocurilor - Game Theory Solver & GUI

## Overview

This repository contains a robust implementation for solving finite, two-player, zero-sum games. It features a highly precise mathematical backend (`JOC_back.py`) that leverages Linear Programming, exact fraction arithmetic, and a dynamic Graphical User Interface (`JOC_front.py`) built with PySide6.

## The Game Theory Algorithm

The solver automatically determines the optimal strategies for both players by analyzing the payoff matrix.

### Key Features:
* **Pure Strategies (Saddle Point):** Automatically detects if a game has a saddle point using the maximin ($v_1$) and minimax ($v_2$) principles. If $v_1 = v_2$, it assigns pure optimal strategies.
* **Mixed Strategies (Linear Programming):** If no saddle point exists, the game is automatically translated into a Linear Programming problem and solved using the Primal Simplex backend (`ASP_back.py`).
* **Exact Mathematics:** Uses Python's `Fraction` module to prevent floating-point rounding errors, ensuring the value of the game and probability distributions are absolutely mathematically exact.
* **Console Visualization:** Includes an `afisare_tabel()` utility to draw a perfectly aligned, Unicode-supported representation of the game matrix directly in the terminal.

---

## How to Run (Command Line Execution)

Because the project relies on absolute imports between different modules (e.g., importing the Simplex solver from `ProblemaLineara`), you must run the scripts as modules from the root directory of the project.

**To launch the Graphical Interface:**
```bash
.venv/bin/python3 -m TeoriaJocurilor.JOC_front
```

**To run the Backend script (test cases/console output):**
```bash
.venv/bin/python3 -m TeoriaJocurilor.JOC_back
```

---

## Mathematical Backend (`JOC_back.py`)

### Method Outputs

#### `solve(data_type, Matrice, with_table=False)`

Analyzes the payoff matrix and returns a comprehensive dictionary containing the optimal strategies and the value of the game.

* **Solution Output (Dictionary):**
  ```python
  {
      "status": "success",
      "tip_strategie": "mixta", # sau "pura"
      "sol": {
          "v": Fraction(13, 5), 
          "X_optim": array([Fraction(0, 1), Fraction(3, 5), Fraction(2, 5)]), 
          "Y_optim": array([Fraction(4, 5), Fraction(0, 1), Fraction(1, 5)])
      },
      "msg": {
          "A": "Valoarea jocului este 13/5 unități.",
          "B": "Ambele părți folosesc strategii mixte."
      }
  }
  ```

#### `verify()`

Performs three independent mathematical checks to validate the integrity of the computed strategy. It returns a `dict` containing the boolean results `[bool, bool, bool]` and detailed mathematical proofs.

* **Check 1 (Probability Positivity):** `True` if all calculated probabilities for both players are $\ge 0$.
* **Check 2 (Probability Sum):** `True` if the sum of probabilities for Player A equals $1$ and the sum for Player B equals $1$.
* **Check 3 (Game Value Consistency):** `True` if the dot product of the strategies and the payoff matrix ($X_{opt} \cdot Q \cdot Y_{opt}^T$) perfectly equals the computed value of the game ($v$).

---

## Graphical User Interface (`JOC_front.py`)

The project includes a fully functional desktop application built with **PySide6**.

### GUI Features:
* **Dynamic Grid Generation:** Input the number of strategies for Player A and Player B, and the UI automatically generates a perfectly centered, shrink-wrapped input grid.
* **Fraction Support:** Cells accept both standard numbers (`3`, `-1.5`) and string fractions (`"1/2"`), translating them perfectly into the backend.
* **Smart Resizing:** The window calculates the required pixel space and elegantly expands to fit the generated matrix.
* **Result Dialog:** Presents the optimal strategies as cleanly formatted arrays and displays the mathematical verification proofs in a monospace font for perfect alignment.

---

## How to Use the Game Class (Backend)

### Basic Usage

```python
import numpy as np
from TeoriaJocurilor.JOC_back import Joc

# Create a solver instance
joc = Joc()

# Define your payoff matrix (Player A rows, Player B columns)
Matrice_Payoff = np.array([
    [1, 1, 2],
    [3, 2, 1],
    [2, 4, 5]
], dtype=np.float64)

# Solve the game (set with_table=True to print the matrix in the console)
# Note: You must pass the required data_type parameter (e.g., np.float64)
solution = joc.solve(np.float64, Matrice=Matrice_Payoff, with_table=True)

# Verify the mathematical integrity of the solution
verification_results = joc.verify()

# Print results
if solution["status"] == "success":
    print(f"Strategy Type: {solution['tip_strategie']}")
    print(f"Value (V) = {solution['sol']['v']}")
    print(f"Player A Strategy = {solution['sol']['X_optim']}")
    print(f"Player B Strategy = {solution['sol']['Y_optim']}")
    
    print("\nVerification Passed:", verification_results["result"])
else:
    print("Solver Error:", solution["msg"])
```

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software, as long as the original copyright and license notice are included.
```