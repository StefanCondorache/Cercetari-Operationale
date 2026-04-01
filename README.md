# Cercetări Operaționale (Operational Research Solvers)

## Overview

This repository is a comprehensive, Python-based suite of mathematical engines and graphical interfaces designed to solve complex problems in **Operational Research**. 

It focuses on exact mathematical precision (utilizing fraction-based arithmetic to eliminate floating-point errors) and features modern, responsive desktop environments built with **PySide6**.

## Project Structure

The repository is divided into independent modules based on the field of study. Click on the module links below to read their specific documentation, features, and usage instructions.

* 📂 [**ProblemaLineara/**](./ProblemaLineara) 
  * *Linear Programming & The Primal Simplex Algorithm.*
  * Handles maximization/minimization, unrestricted variables, and the Big-M method.
* 📂 [**TeoriaJocurilor/**](./TeoriaJocurilor) 
  * *Game Theory & Zero-Sum Matrix Games.*
  * Automatically calculates saddle points for pure strategies and utilizes the Simplex backend to resolve mixed-strategy probabilities.

---

## Global Requirements

To run any of the modules or graphical interfaces in this repository, you will need Python 3 installed along with the following libraries:

```bash
pip install -r requirements.txt
```
*(Note: Python's built-in `fractions` and `math` libraries are also utilized heavily for mathematical exactness).*

---

## Execution Guide

Because the modules in this repository share underlying utility files (for example, the Game Theory module relies on the Simplex backend), **all scripts must be executed as modules from this root directory.**

### Running a Graphical Interface (GUI)
Activate your virtual environment and run the frontend file using the `-m` flag:
```bash
# To launch the Linear Programming GUI
.venv/bin/python3 -m ProblemaLineara.ASP_front

# To launch the Game Theory GUI
.venv/bin/python3 -m TeoriaJocurilor.JOC_front
```

### Running a Backend / Test Suite
To run the terminal-based solvers or execute the hardcoded test problems:
```bash
# To run the Simplex backend tests
.venv/bin/python3 -m ProblemaLineara.ASP_back

# To run the Game Theory backend tests
.venv/bin/python3 -m TeoriaJocurilor.JOC_back
```

---

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software, as long as the original copyright and license notice are included.
```
