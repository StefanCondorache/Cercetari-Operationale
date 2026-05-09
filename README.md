# Operational Research Algorithms Collection

## Overview

This repository is a comprehensive, Python-based software suite dedicated to modeling, solving, and visualizing fundamental problems in **Operational Research**.

The project emphasizes mathematical exactness (using fraction-based arithmetic to eliminate floating-point errors where applicable) and features interactive, clear, and modern Graphical User Interfaces (GUIs) built with **PySide6**.

The entire suite has been unified under a single **Central Launcher**, providing easy access to all modules.

## Project Structure

The project is modularized by field of study:

* 📈 **ProblemaLineara/**
  * *Linear Programming & The Primal Simplex Algorithm.*
  * Handles maximization/minimization cases, unrestricted variables, and utilizes the penalty method (Big-M).
* 🎮 **TeoriaJocurilor/**
  * *Game Theory & Zero-Sum Strategic Games.*
  * Identifies saddle points for pure strategies and utilizes the internal Simplex engine to resolve probabilities for mixed strategies.
* 🚚 **ProblemaTransporturilor/**
  * *Transportation Problem (North-West Corner & MODI/Potential Method).*
  * Automatically balances the problem (adds dummy rows/columns), handles degeneracy, and finds the absolute minimum cost.
* 🕸️ **TeoriaGrafurilor/**
  * *Network and Graph Optimizations.*
  * Contains step-by-step visual solvers for the maximum flow in a network (Ford-Fulkerson) and the minimum cost perfect matching problem (Hungarian Algorithm).

---

## Global Requirements

To run any module or interface in this repository, you need Python 3 installed (>= 3.8 recommended). All external dependencies have been centralized into a single file located in this root directory.

Installation is done by running the following command:
`pip install -r requirements.txt`

*(Note: Internal Python libraries such as `fractions`, `math`, `re`, and `copy` are also used extensively).*

---

## Execution Guide

Because the modules in this project share functionalities and are structured as packages, **the application must be launched from this main root directory**.

### Running the Main Menu (GUI)

The simplest way to interact with the project is by launching the central menu, which allows you to visually navigate to any desired algorithm.

Activate your virtual environment (if you are using one) and run the `main` module:
`.venv/bin/python3 -m main`

*(In case you do not use an environment use plain python3 instead of .venv/bin/python3)*
*(From the menu that opens, you can select any of the 4 problems, configure input data in graphical tables, and run the visualizations).*

### Running the Mathematical Engines (Backend / Test Suite)

If you wish to run the calculation engines directly from the terminal to test hardcoded problems (without opening the GUI), execute the specific `_back` modules:

# For Simplex
`.venv/bin/python3 -m ProblemaLineara.ASP_back`

# For Transportation Problem
`.venv/bin/python3 -m ProblemaTransporturilor.Transport_back`

# For Ford-Fulkerson (Max Flow)
`.venv/bin/python3 -m TeoriaGrafurilor.AFF_back`

# For Hungarian Algorithm (Assignment)
`.venv/bin/python3 -m TeoriaGrafurilor.AU_back`

# For Game Theory
`.venv/bin/python3 -m TeoriaJocurilor.JOC_back`

---

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software, provided that the original copyright and license notices are preserved.