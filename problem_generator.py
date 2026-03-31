import numpy as np
from problems import *

def generate_problem(n=15, m=15):

    # 1. Coeficienți de profit (majoritatea pozitivi)
    coef = np.random.uniform(-10, 100, size=n).astype(np.float64)
    
    # 2. Matricea A - IMPORTANT: Folosim valori predominant pozitive
    # pentru a "închide" regiunea fezabilă (resursele se consumă)
    MatriceA = np.random.uniform(0, 10, size=(m, n)).astype(np.float64)
    
    # Adăugăm raritate (doar 20% din celule să fie nenule dacă vrei sparsitate)
    mask = np.random.choice([0, 1], size=(m, n), p=[0.7, 0.3])
    MatriceA *= mask

    # 3. RHS b - Valori strict pozitive mari pentru a asigura un spațiu de start
    b = np.random.uniform(50, 500, size=m).astype(np.float64)
    
    # 4. Inegalități - Predominant <= (mm) pentru a limita creșterea
    inegalitate = np.random.choice([mm, MM, eg], size=m, p=[0.8, 0.1, 0.1])
    
    # 5. Domenii x - Predominant >= 0 (MM) pentru stabilitate
    x_cond = np.random.choice([MM, mm, eg], size=n, p=[0.8, 0.1, 0.1])
    
    return {
        "OPT": np.random.choice([MAX, MIN]),
        "coef": coef,
        "MatriceA": MatriceA,
        "inegalitate": inegalitate,
        "b": b,
        "x": x_cond
    }

if __name__ == "__main__":
    # Generate the complex problem
    p1000_random = generate_problem(1000, 1000)

    print("--- Problem Generated ---")
    print(f"Constraints: {len(p1000_random['inegalitate'])}")
    print(f"Inequality types (count): {np.bincount(p1000_random['inegalitate'])}")
    print(f"Variable domain types (count): {np.bincount(p1000_random['x'])}")
    with open("output.txt", 'w') as file:
        for key, value in p1000_random.items():
            file.write(f"{key}:\n{value}\n\n")