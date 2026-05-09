import copy

class HungarianAlgorithm:
    def solve(self, cost_matrix):
        # Inițializare și copiere
        n = len(cost_matrix)
        matrice_initiala = copy.deepcopy(cost_matrix)
        matrice = copy.deepcopy(cost_matrix)
        
        iteratii = []
        
        # --- ITERAȚIA 0: REDUCEREA MATRICEI ---
        # 1. Minime pe linii
        minime_linii = [min(rand) for rand in matrice]
        for i in range(n):
            for j in range(n):
                matrice[i][j] -= minime_linii[i]
                
        # 2. Minime pe coloane (doar dacă nu există deja 0 pe coloana respectivă)
        minime_coloane = [0] * n
        for j in range(n):
            coloana = [matrice[i][j] for i in range(n)]
            if 0 not in coloana:
                min_col = min(coloana)
                minime_coloane[j] = min_col
                for i in range(n):
                    matrice[i][j] -= min_col

        suma_minime_0 = sum(minime_linii) + sum(minime_coloane)
        
        iteratia_curenta = 0
        
        # --- BUCLA PRINCIPALĂ ---
        while True:
            # === TESTUL DE OPTIMALITATE (Încadrarea Zerourilor) ===
            zerouri_disponibile = set()
            for i in range(n):
                for j in range(n):
                    if matrice[i][j] == 0:
                        zerouri_disponibile.add((i, j))
                        
            zerouri_incadrate = set()
            zerouri_taiate = set()
            
            while zerouri_disponibile:
                # Numărăm zerourile disponibile pe fiecare linie
                nr_zerouri_linie = {}
                for r, c in zerouri_disponibile:
                    nr_zerouri_linie[r] = nr_zerouri_linie.get(r, 0) + 1
                
                # Căutăm linia cu numărul minim de zerouri
                min_zerouri = min(nr_zerouri_linie.values())
                
                # De sus în jos (luăm indexul minim de linie care are min_zerouri)
                linii_candidate = [r for r, count in nr_zerouri_linie.items() if count == min_zerouri]
                linie_aleasa = min(linii_candidate)
                
                # Primul zero de la stânga (indexul minim de coloană pe linia aleasă)
                coloane_pe_linie = [c for r, c in zerouri_disponibile if r == linie_aleasa]
                coloana_aleasa = min(coloane_pe_linie)
                
                # Încadrăm zeroul ales
                zerouri_incadrate.add((linie_aleasa, coloana_aleasa))
                zerouri_disponibile.remove((linie_aleasa, coloana_aleasa))
                
                # Tăiem cu 'x' restul zerourilor de pe linie și coloană
                de_taiat = [(r, c) for r, c in zerouri_disponibile if r == linie_aleasa or c == coloana_aleasa]
                for z in de_taiat:
                    zerouri_taiate.add(z)
                    zerouri_disponibile.remove(z)
            
            n0 = len(zerouri_incadrate)
            
            # Condiția de Stop
            if n0 == n:
                iteratii.append({
                    "iteratie": iteratia_curenta,
                    "matrice": copy.deepcopy(matrice),
                    "incadrate": list(zerouri_incadrate),
                    "taiate": list(zerouri_taiate),
                    "optimal": True
                })
                break
                
            # === PROCEDURA DE MARCAJ (Cu steluță) ===
            linii_cu_incadrate = {r for r, c in zerouri_incadrate}
            
            # Pas 1: Marcăm liniile fără 0 încadrat
            linii_marcate = set(range(n)) - linii_cu_incadrate
            coloane_marcate = set()
            
            schimbare = True
            while schimbare:
                schimbare = False
                
                # Alternanța 1: de la linie marcată (cu 0 tăiat cu x) -> marcăm coloana
                for r, c in zerouri_taiate:
                    if r in linii_marcate and c not in coloane_marcate:
                        coloane_marcate.add(c)
                        schimbare = True
                
                # Alternanța 2: de la coloană marcată (cu 0 încadrat) -> marcăm linia
                for r, c in zerouri_incadrate:
                    if c in coloane_marcate and r not in linii_marcate:
                        linii_marcate.add(r)
                        schimbare = True

            # === SUPORTUL MINIMAL ===
            # Linii FĂRĂ steluță și Coloane CU steluță
            linii_suport = set(range(n)) - linii_marcate
            coloane_suport = coloane_marcate
            
            # === CALCUL EPSILON ===
            # Epsilon = minimul elementelor care nu sunt în suportul minimal
            # (Adică rândul ARE steluță, coloana NU are steluță)
            elemente_neacoperite = []
            for i in range(n):
                for j in range(n):
                    if i in linii_marcate and j not in coloane_marcate:
                        elemente_neacoperite.append(matrice[i][j])
                        
            epsilon = min(elemente_neacoperite)
            
            # Salvăm starea înainte de a modifica matricea
            iteratii.append({
                "iteratie": iteratia_curenta,
                "matrice": copy.deepcopy(matrice),
                "incadrate": list(zerouri_incadrate),
                "taiate": list(zerouri_taiate),
                "linii_marcate": list(linii_marcate),
                "coloane_marcate": list(coloane_marcate),
                "epsilon": epsilon,
                "n0": n0,
                "optimal": False
            })
            
            # === ACTUALIZAREA MATRICEI ===
            for i in range(n):
                for j in range(n):
                    # Neacoperite (nici rând, nici coloană în suport)
                    if i in linii_marcate and j not in coloane_marcate:
                        matrice[i][j] -= epsilon
                    # Dublu acoperite (intersecția suportului: rând fără stea, coloană cu stea)
                    elif i not in linii_marcate and j in coloane_marcate:
                        matrice[i][j] += epsilon
                    # Restul (acoperite o singură dată) rămân neschimbate
            
            iteratia_curenta += 1

        # === REZULTAT FINAL ===
        # Valoarea cuplajului se calculează adunând valorile originale din celulele încadrate
        w_max_arce = list(zerouri_incadrate)
        cost_minim = sum(matrice_initiala[i][j] for i, j in w_max_arce)
        
        # === VERIFICARE ===
        suma_epsiloane_verificare = sum(it["epsilon"] * (n - it["n0"]) for it in iteratii if not it["optimal"])
        verificare_cost = suma_minime_0 + suma_epsiloane_verificare
        
        return {
            "iteratii": iteratii,
            "cost_minim": cost_minim,
            "verificare": verificare_cost,
            "w_max": w_max_arce
        }

if __name__ == "__main__":
    # Test cu o matrice de costuri 4x4
    matrice_test = [
        [58, 29, 88, 77, 68, 68],
        [38, 92, 16, 66, 26, 19],
        [33, 16, 95, 91, 14, 31],
        [64, 88, 13, 98, 57, 27],
        [94, 93, 88, 61, 59, 27],
        [68, 77, 46, 21, 88, 31]
    ]
    
    algoritm = HungarianAlgorithm()
    rezultat = algoritm.solve(matrice_test)
    n = len(matrice_test)
    
    print("=== ISTORIC ALGORITMUL UNGAR ===")
    for it in rezultat['iteratii']:
        print(f"\n[ Iterația {it['iteratie']} ]")
        
        # Printare Matrice cu Zerouri Încadrate '[0]' și Tăiate ' x'
        for i in range(n):
            rand_str = []
            stea_linie = "*" if "linii_marcate" in it and i in it["linii_marcate"] else " "
            for j in range(n):
                val = it['matrice'][i][j]
                if (i, j) in it['incadrate']:
                    rand_str.append(f"[{val:2}]")
                elif (i, j) in it['taiate']:
                    rand_str.append(f" {val:2}x")
                else:
                    rand_str.append(f" {val:2} ")
            print(f"{stea_linie}  " + "  ".join(rand_str))
            
        if "coloane_marcate" in it:
            stele_col = ["   * " if j in it["coloane_marcate"] else "     " for j in range(n)]
            print("   " + "".join(stele_col))
            
        if it['optimal']:
            print("=> Test Optimalitate: SUCCES (n0 == n). Stop algoritm.")
        else:
            print(f"=> Test Optimalitate: EȘUAT (n0={it['n0']} < n={n}).")
            print(f"   Epsilon calculat: {it['epsilon']}")
            
    print("\n=== SOLUȚIA FINALĂ ===")
    print(f"Cuplaj Maxim Wmax (Arce): {rezultat['w_max']}")
    print(f"Cost Minim Afectare: {rezultat['cost_minim']}")
    print(f"Verificare (Formula): {rezultat['verificare']}")
    print("Status Verificare:", "CORECT" if rezultat['cost_minim'] == rezultat['verificare'] else "GREȘIT")