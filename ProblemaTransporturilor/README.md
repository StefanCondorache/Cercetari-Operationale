# Problema Transporturilor - Cercetări Operaționale

Acest modul face parte din suita `Cercetari-Operationale` și implementează rezolvarea **Problemei Transporturilor** folosind metode clasice de optimizare, având atât un motor matematic precis (backend), cât și o interfață grafică interactivă (frontend).

## Funcționalități

1. **Echilibrarea Problemei:** Algoritmul detectează automat dacă problema este dezechilibrată ($\sum S \neq \sum D$) și adaugă furnizori sau beneficiari fictivi cu cost $0$.
2. **Soluția Inițială (Metoda Nord-Vest):** Calculează o primă soluție de bază admisibilă. Gestionează automat **degenerarea** forțând introducerea de zero-uri artificiale în bază pentru a respecta mereu condiția $NC = m + n - 1$.
3. **Optimizarea (Metoda MODI / u-v):** - Calculează multiplicatorii $u_i$ și $v_j$ optimizat (pornind de la linia/coloana cu cel mai mare grad).
   - Evaluează celulele non-bază prin matricea $\Delta_{ij}$.
   - Aplică un algoritm **DFS cu Backtracking (Stepping-Stone)** pentru a găsi circuitul de ameliorare a costului.
4. **Jurnal Detaliat (Log-uri):** Afișează pas cu pas (atât în consolă cât și în interfața grafică) evoluția matricilor, vectorilor $u, v$ și a matricii $\Delta$.

## Arhitectura Modulului

* `Transport_back.py` - Core-ul matematic (Clasa `Transport` cu metodele `solve`, `metoda_nord_vest`, `calculeaza_uv`, `gaseste_circuit` și `afisare`).
* `Transport_front.py` - Interfața grafică construită cu **PySide6**. Permite generarea dinamică a tabelului de costuri și afișează rezultatul într-o fereastră formatată similar cu ieșirea din terminal.
* `problems.py` - Un set de probleme standard gata definite (echilibrate, dezechilibrate, degenerate) pentru testarea rapidă a backend-ului.

## Cum se rulează

Deoarece acest modul împarte arhitectura cu restul proiectului, scripturile trebuie rulate din directorul principal (root) al repository-ului, folosind flag-ul `-m`.

### 1. Lansarea Interfeței Grafice (GUI)
Asigurați-vă că aveți mediul virtual activat și dependențele instalate, apoi rulați:
```bash
python -m ProblemaTransporturilor.Transport_front
```

### 2. Rularea testelor în Terminal (CLI)
Pentru a vedea afișarea pas cu pas direct în consolă pe setul de date predefinit:
```bash
python -m ProblemaTransporturilor.problems
```

## Utilizare în propriul cod

Puteți importa backend-ul ușor în alte scripturi din proiect:

```python
import numpy as np
from ProblemaTransporturilor.Transport_back import Transport

solver = Transport()

costuri = [
    [2, 2, 2, 1],
    [10, 8, 5, 4],
    [7, 6, 6, 8]
]
disponibil = [3, 7, 5]
necesitate = [4, 3, 4, 4]

# cu_afisare=True va printa fiecare iterație în consolă
rezultat = solver.solve(costuri, disponibil, necesitate, cu_afisare=True)

print(f"Cost minim: {rezultat['cost_final']}")
```