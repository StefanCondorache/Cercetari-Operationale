# Copyright (c) 2026 Condorache Ștefan-Eugen. All rights reserved.
# Licensed under the MIT License.

import numpy as np

class Transport:
    def afisare(self, titlu_iteratie, u, v, Delta=None):
        """
        Desenează tabelul de transport în consolă la fiecare iterație.
        """
        print(f"\n" + "="*70)
        print(f" {titlu_iteratie.upper()} ")
        print("="*70)
        
        m, n = self.C.shape
        
        header = f"{'':<8} | "
        for j in range(n):
            header += f"{'B'+str(j+1):<5} x(c) | "
        header += f"{'Disp(D)':<8} | {'u_i':<8}"
        print(header)
        print("-" * len(header))

        for i in range(m):
            row_str = f"{'A'+str(i+1):<8} | "
            for j in range(n):
                alloc = f"{self.X[i,j]:g}" if (i, j) in self.baza else "-"
                cell = f"{alloc} ({self.C[i,j]:g})"
                row_str += f"{cell:<10} | "
            
            row_str += f"{self.D[i]:<8g} | "
            row_str += f"{u[i]:<8g}" if u is not None and not np.isnan(u[i]) else f"{'-':<8}"
            print(row_str)
            
        print("-" * len(header))

        nec_str = f"{'Nec(N)':<8} | "
        for j in range(n):
            nec_str += f"{self.N[j]:<10g} | "
        nec_str += f"{'':<8} | {'':<8}"
        print(nec_str)
        
        if v is not None:
            v_str = f"{'v_j':<8} | "
            for j in range(n):
                v_str += f"{v[j]:<10g}" if not np.isnan(v[j]) else f"{'-':<10}"
                v_str += " | "
            print(v_str)
            print("-" * len(header))
            
        if Delta is not None:
            print("\nMatricea Delta (c_ij - u_i - v_j) pentru celulele non-bază:")
            for i in range(m):
                d_row = "         "
                for j in range(n):
                    val = Delta[i,j]
                    d_row += f"{val:<10g}   " if not np.isnan(val) else f"{'-':<10}   "
                print(d_row)
        print()

    def solve(self, costuri, disponibil, necesitate, cu_afisare=True):
        """
        Rezolvă problema de transport folosind Metoda Nord-Vest 
        și optimizarea MODI (Distribuției Modificate / u-v).
        """
        self.C_initial = np.array(costuri, dtype=np.float64)
        self.D_initial = np.array(disponibil, dtype=np.float64)
        self.N_initial = np.array(necesitate, dtype=np.float64)

        # Echilibrarea problemei
        suma_disp = np.sum(self.D_initial)
        suma_nec = np.sum(self.N_initial)

        self.C = np.copy(self.C_initial)
        self.D = np.copy(self.D_initial)
        self.N = np.copy(self.N_initial)

        if suma_disp > suma_nec:
            # Adăugăm un beneficiar fictiv (coloană) cu cost 0
            diferenta = suma_disp - suma_nec
            self.N = np.append(self.N, diferenta)
            col_fictiva = np.zeros((self.C.shape[0], 1))
            self.C = np.hstack((self.C, col_fictiva))
            if cu_afisare: print(f"-> Echilibrare: S-a adăugat Beneficiar Fictiv (Nec: {diferenta})")
            
        elif suma_nec > suma_disp:
            # Adăugăm un furnizor fictiv (linie) cu cost 0
            diferenta = suma_nec - suma_disp
            self.D = np.append(self.D, diferenta)
            lin_fictiva = np.zeros((1, self.C.shape[1]))
            self.C = np.vstack((self.C, lin_fictiva))
            if cu_afisare: print(f"-> Echilibrare: S-a adăugat Furnizor Fictiv (Disp: {diferenta})")

        self.m, self.n = self.C.shape

        # Metoda Tabelului Nord-Vest (Atenție la degenerare!)
        self.X, self.baza = self.metoda_nord_vest(self.D, self.N)

        if cu_afisare:
            self.afisare("Soluția Inițială (Metoda Nord-Vest)", np.full(self.m, np.nan), np.full(self.n, np.nan))

        # Verificare degenerare
        V = self.m + self.n - 1
        NC = len(self.baza)
        tip_degenerare = "Nedegenerată"
        if NC < V:
            tip_degenerare = "Degenerată (rezolvată prin zero-uri artificiale)"

        self.istoric_iteratii = []
        optim = False
        iteratie = 0

        # Iterații de optimizare
        while not optim and iteratie < 100:
            iteratie += 1
            f_k = np.sum(self.X * self.C)

            u, v = self.calculeaza_uv(self.C, self.baza)

            Delta = np.full((self.m, self.n), np.nan)
            for i in range(self.m):
                for j in range(self.n):
                    if (i, j) not in self.baza:
                        Delta[i, j] = self.C[i, j] - (u[i] + v[j])

            min_delta = np.nanmin(Delta)
            
            self.istoric_iteratii.append({
                "iteratie": iteratie,
                "X": np.copy(self.X),
                "u": np.copy(u),
                "v": np.copy(v),
                "Delta": np.copy(Delta),
                "cost": f_k,
                "baza": list(self.baza)
            })
            
            if cu_afisare:
                self.afisare(f"Iterația {iteratie}", u, v, Delta)
                print(f"Cost curent (Z): {f_k}")

            if min_delta >= -1e-9:
                optim = True
                if cu_afisare: print("\n>>> OPTIM ATINS: Toate valorile Delta sunt pozitive (>= 0). <<<")
                break

            # Condiția de intrare (cel mai mic Delta negativ)
            intra_i, intra_j = np.unravel_index(np.nanargmin(Delta), Delta.shape)
            
            if cu_afisare:
                print(f"-> Variabila X[{intra_i+1}, {intra_j+1}] intră în bază (Delta = {min_delta:g}).")
            
            # Condiția de ieșire (Căutarea poligonului cu Backtracking)
            circuit = self.gaseste_circuit(intra_i, intra_j, self.baza)
            
            if not circuit:
                return {"status": "error", "msg": f"Ciclare fatală la iterația {iteratie}. Baza este deconectată."}

            celule_scadere = [self.X[x, y] for idx, (x, y) in enumerate(circuit) if idx % 2 == 1]
            theta = min(celule_scadere)
            
            if cu_afisare:
                circuit_str = " -> ".join([f"X[{r+1},{c+1}]" for r, c in circuit])
                print(f"-> Circuit detectat: {circuit_str}")
                print(f"-> Valoare Theta minimă: {theta:g}")

            celula_iese = (0,0)
            for idx, (x, y) in enumerate(circuit):
                if idx % 2 == 0:
                    self.X[x, y] += theta
                else:
                    self.X[x, y] -= theta
                    if abs(self.X[x, y]) < 1e-9:
                        celula_iese = (x, y)

            self.baza.append((intra_i, intra_j))
            if celula_iese in self.baza:
                self.baza.remove(celula_iese)
                
            if cu_afisare:
                print(f"-> Variabila X[{celula_iese[0]+1}, {celula_iese[1]+1}] iese din bază.")

        cost_final = np.sum(self.X * self.C)

        if cu_afisare:
            print(f" >> COST FINAL MINIM (f_MIN): {cost_final:g}")

        return {
            "status": "success",
            "echilibrare": "Necesara" if suma_disp != suma_nec else "Nu a fost necesara",
            "degenerare": f"NC={NC}, V={V} ({tip_degenerare})",
            "iteratii": iteratie,
            "cost_final": cost_final,
            "solutie_X": self.X,
            "istoric": self.istoric_iteratii
        }

    def metoda_nord_vest(self, D, N):
        """Metoda Nord-Vest robustă. Forcează mereu m+n-1 elemente în bază."""
        m, n = len(D), len(N)
        X = np.zeros((m, n))
        baza = []
        disp = np.copy(D)
        nec = np.copy(N)
        
        i, j = 0, 0
        while i < m and j < n:
            cantitate = min(disp[i], nec[j])
            X[i, j] = cantitate
            baza.append((i, j))
            
            disp[i] -= cantitate
            nec[j] -= cantitate
            
            if abs(disp[i]) < 1e-9 and abs(nec[j]) < 1e-9:
                if i != m - 1 or j != n - 1:
                    i += 1
                else:
                    break
            elif abs(disp[i]) < 1e-9:
                i += 1
            else:
                j += 1
                
        return X, baza

    def calculeaza_uv(self, C, baza):
        """Rezolvarea sistemului u+v=c folosind BFS pe graful bipartit creat de bază.
           Optimizare: Începe cu linia sau coloana cu cele mai multe alocări."""
        m, n = C.shape
        u = np.full(m, np.nan)
        v = np.full(n, np.nan)
        
        grad_linii = {i: 0 for i in range(m)}
        grad_coloane = {j: 0 for j in range(n)}
        
        for i, j in baza:
            grad_linii[i] += 1
            grad_coloane[j] += 1
            
        max_linie = max(grad_linii, key=grad_linii.get)         #type:ignore
        max_coloana = max(grad_coloane, key=grad_coloane.get)   #type:ignore
        
        if grad_linii[max_linie] >= grad_coloane[max_coloana]:
            u[max_linie] = 0
            start_node = f"r_{max_linie}"
        else:
            v[max_coloana] = 0
            start_node = f"c_{max_coloana}"

        adj = {f"r_{i}": [] for i in range(m)}
        for j in range(n):
            adj[f"c_{j}"] = []
            
        for i, j in baza:
            adj[f"r_{i}"].append((f"c_{j}", C[i, j]))
            adj[f"c_{j}"].append((f"r_{i}", C[i, j]))
            
        coada = [start_node]
        while coada:
            curent = coada.pop(0)
            e_linie = curent.startswith("r_")
            idx = int(curent.split("_")[1])
            
            for vecin, cost in adj[curent]:
                v_idx = int(vecin.split("_")[1])
                
                if e_linie and np.isnan(v[v_idx]):
                    v[v_idx] = cost - u[idx]
                    coada.append(vecin)
                elif not e_linie and np.isnan(u[v_idx]):
                    u[v_idx] = cost - v[idx]
                    coada.append(vecin)
                    
        return u, v

    def gaseste_circuit(self, start_i, start_j, baza):
        """
        Algoritm Backtracking pentru a găsi circuitul problemei transporturilor.
        Alterneaza Orizontal -> Vertical și se întoarce la (start_i, start_j).
        """
        def dfs(nod_curent, traseu, mergi_orizontal):
            if len(traseu) > 3 and nod_curent == (start_i, start_j):
                return traseu[:-1]

            r_cur, c_cur = nod_curent
            noduri_posibile = baza + [(start_i, start_j)]
            
            for (r, c) in noduri_posibile:
                if (r, c) != nod_curent:
                    if mergi_orizontal and r == r_cur:
                        if (r, c) not in traseu or ((r, c) == (start_i, start_j) and len(traseu) > 3):
                            rez = dfs((r, c), traseu + [(r, c)], not mergi_orizontal)
                            if rez: return rez
                            
                    elif not mergi_orizontal and c == c_cur:
                        if (r, c) not in traseu or ((r, c) == (start_i, start_j) and len(traseu) > 3):
                            rez = dfs((r, c), traseu + [(r, c)], not mergi_orizontal)
                            if rez: return rez
            return None

        circuit = dfs((start_i, start_j), [(start_i, start_j)], True)
        if not circuit:
            circuit = dfs((start_i, start_j), [(start_i, start_j)], False)
            
        return circuit

if __name__ == "__main__":
    costuri = [
        [4, 5, 2, 3],
        [1, 2, 1, 3],
        [4, 4, 5, 1]
    ]
    disponibil = [30, 27, 43]
    necesitate = [25, 35, 18, 22]
    
    solver = Transport()
    print("\nLANSAM REZOLVAREA CU AFISARE IN CONSOLA:\n")
    rezultat = solver.solve(costuri, disponibil, necesitate, cu_afisare=True)
    print("\nREZULTAT FINAL:", rezultat)