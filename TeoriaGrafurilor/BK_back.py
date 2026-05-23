# Copyright (c) 2026. All rights reserved.
import copy

class BellmanKalaba:
    def __init__(self):
        self.graf = {}
        self.noduri = []
        self.matrice_c = []
        self.inf = float('inf')

    def solve(self, date_intrare, sursa, destinatie):
        """
        Rezolvă problema drumului minim folosind algoritmul Bellman-Kalaba.
        
        :param date_intrare: dict în formatul tău standard cu arce și valori
        :param sursa: nodul de start (ex: 'x1')
        :param destinatie: nodul terminal (ex: 'x6')
        """
        # 1. Identificăm toate nodurile unice și le sortăm alfabetic/numeric
        set_noduri = set()
        for date in date_intrare.values():
            u, v = date['node']
            set_noduri.add(u)
            set_noduri.add(v)
        
        # Sortare alfabetică simplă (funcționează excelent pentru x1, x2, x3...)
        self.noduri = sorted(list(set_noduri), key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else x)
        n = len(self.noduri)
        
        # Mapare rapidă a numelui nodului la indexul din matrice
        nod_to_idx = {nod: idx for idx, nod in enumerate(self.noduri)}
        idx_dest = nod_to_idx[destinatie]
        idx_sursa = nod_to_idx[sursa]

        # 2. Construirea Matricei Ponderilor C (Pasul 1)
        # Inițializăm totul cu INF, iar diagonala cu '-' (reprezentat prin None sau INF în calcule)
        self.matrice_c = [[self.inf for _ in range(n)] for _ in range(n)]
        
        for date in date_intrare.values():
            u, v = date['node']
            cost = date['value']
            self.matrice_c[nod_to_idx[u]][nod_to_idx[v]] = cost

        # Diagonala principală este blocată pentru succesori (c_ii = -)
        for i in range(n):
            self.matrice_c[i][i] = self.inf

        # 3. Inițializarea structurii tabelului de iterații
        # Fiecare iterație va fi un dicționar salvat în istoric pentru frontend
        tabel_iteratii = []
        
        # --- ITERAȚIA 0 (Pasul 2) ---
        # m^(0) coincide cu coloana nodului terminal
        m_curent = [self.matrice_c[i][idx_dest] for i in range(n)]
        m_curent[idx_dest] = 0 # Costul de la destinație la destinație este 0
        
        # Adăugăm iterația 0 în tabel (fără rând de succesori)
        tabel_iteratii.append({
            "k": 0,
            "m": copy.deepcopy(m_curent),
            "succ": None # Iterația 0 nu are succesori
        })

        # --- ITERAȚIILE URMATOARE k >= 1 (Pasul 3) ---
        k = 1
        while True:
            m_precedent = tabel_iteratii[-1]["m"]
            m_nou = [self.inf for _ in range(n)]
            succ_nou = [None for _ in range(n)]
            
            # Destinația rămâne mereu pe 0 și nu are succesor
            m_nou[idx_dest] = 0
            succ_nou[idx_dest] = "-"

            # Calculăm pentru restul nodurilor i
            for i in range(n):
                if i == idx_dest:
                    continue
                
                minim_nod = self.inf
                succesor_nod = None
                
                # Căutăm j-ul care oferă minimul (cu condiția j != i)
                for j in range(n):
                    if j == i: 
                        continue # Regula: excludem auto-legătura
                        
                    cost_arc = self.matrice_c[i][j]
                    if cost_arc != self.inf and m_precedent[j] != self.inf:
                        valoare_posibila = cost_arc + m_precedent[j]
                        if valoare_posibila < minim_nod:
                            minim_nod = valoare_posibila
                            succesor_nod = self.noduri[j] # Salvăm numele nodului
                
                m_nou[i] = minim_nod
                succ_nou[i] = succesor_nod if succesor_nod is not None else "-"

            # Salvează rezultatul acestui pas în istoric
            tabel_iteratii.append({
                "k": k,
                "m": copy.deepcopy(m_nou),
                "succ": copy.deepcopy(succ_nou)
            })

            # TEST DE OPRIRE (Stabilizarea): m^(k) == m^(k-1)
            if m_nou == m_precedent:
                break
                
            k += 1
            # Siguranță împotriva buclelor infinite în grafuri cu circuite negative
            if k > n + 2:
                break

        # 4. Extragerea valorilor finale d_it (de la Iterația Stop)
        d_it = tabel_iteratii[-1]["m"]

        # 5. RECONSTRUCȚIA DRUMULUI OPTIM (Pasul 4)
        # Folosim exclusiv rândul de succesori de la Iterația Stop
        succesorii_finali = tabel_iteratii[-1]["succ"]
        
        drum_optim = []
        cost_grafic_suma = 0
        nr_arce_drum = 0
        validare_succes = False
        
        # Reconstruim doar dacă nodul de start poate ajunge la destinație
        if d_it[idx_sursa] != self.inf:
            nod_curent = sursa
            drum_optim.append(nod_curent)
            
            while nod_curent != destinatie:
                idx_curent = nod_to_idx[nod_curent]
                urmatorul_nod = succesorii_finali[idx_curent]
                
                if urmatorul_nod == "-" or urmatorul_nod is None:
                    break # Drum întrerupt/imposibil
                    
                # Calculăm costul arcului din graf pentru validare
                idx_urmator = nod_to_idx[urmatorul_nod]
                cost_grafic_suma += self.matrice_c[idx_curent][idx_urmator]
                nr_arce_drum += 1
                
                nod_curent = urmatorul_nod
                drum_optim.append(nod_curent)

            # 6. VALIDAREA MATEMATICĂ (Pasul 5)
            # Nr. arce trebuie să fie egal cu numărul de iterații active (k de oprire - 1)
            nr_iteratii_active = tabel_iteratii[-1]["k"]
            
            conditie_cost = (cost_grafic_suma == d_it[idx_sursa])
            conditie_arce = (nr_arce_drum == nr_iteratii_active)
            
            if conditie_cost and conditie_arce:
                validare_succes = True

        return {
            "noduri": self.noduri,
            "matrice_initiala": self.matrice_c,
            "tabel_iteratii": tabel_iteratii,
            "d_it": d_it,
            "drum_optim": drum_optim,
            "cost_total": d_it[idx_sursa],
            "validare_arce": {
                "arce_drum": nr_arce_drum,
                "iteratii_active": tabel_iteratii[-1]["k"]
            },
            "validare_succes": validare_succes
        }

# --- TEST CENTRALIZAT ÎN TERMINAL ---
if __name__ == "__main__":
    # Graf de test simplu
    date_test = {
        'a0': {'node': ('x1', 'x2'), 'value': 10},
        'a1': {'node': ('x1', 'x9'), 'value': 10},
        'a2': {'node': ('x2', 'x3'), 'value': 15},
        'a3': {'node': ('x3', 'x4'), 'value': 12},
        'a4': {'node': ('x4', 'x1'), 'value': 7},
        'a5': {'node': ('x4', 'x9'), 'value': 9},
        'a6': {'node': ('x4', 'x6'), 'value': 8},
        'a7': {'node': ('x5', 'x1'), 'value': 26},
        'a8': {'node': ('x5', 'x6'), 'value': 20},
        'a9': {'node': ('x6', 'x7'), 'value': 17},
        'a10': {'node': ('x6', 'x8'), 'value': 13},
        'a11': {'node': ('x7', 'x1'), 'value': 4},
        'a12': {'node': ('x7', 'x2'), 'value': 6},
        'a13': {'node': ('x8', 'x9'), 'value': 11},
        'a14': {'node': ('x9', 'x5'), 'value': 5},
        'a15': {'node': ('x9', 'x6'), 'value': 3},
    }
    
    bk = BellmanKalaba()
    rez = bk.solve(date_test, sursa='x1', destinatie='x3')
    
    print("=== MATRICEA INITIALA C ===")
    for rand in rez["matrice_initiala"]:
        print([x if x != float('inf') else '∞' for x in rand])
        
    print("\n=== TABEL ITERATII ===")
    print("Noduri: ", rez["noduri"])
    for it in rez["tabel_iteratii"]:
        print(f"k = {it['k']}:")
        print(f"  m   : {it['m']}")
        print(f"  succ: {it['succ']}")
        
    print("\n=== REZULTATE FINALE ===")
    print("Distanțe d_it :", rez["d_it"])
    print("Drum Optim    :", " -> ".join(rez["drum_optim"]))
    print("Cost Total    :", rez["cost_total"])
    print("Validare Succes:", rez["validare_succes"])