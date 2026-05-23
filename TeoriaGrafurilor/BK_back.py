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
        
        :param date_intrare: dict în formatul standard cu arce și valori
        :param sursa: nodul de start (ex: 'x8')
        :param destinatie: nodul terminal (ex: 'x3')
        """
        # 1. Identificăm toate nodurile unice și le sortăm numeric după indici
        set_noduri = set()
        for date in date_intrare.values():
            u, v = date['node']
            set_noduri.add(u)
            set_noduri.add(v)
        
        self.noduri = sorted(list(set_noduri), key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else x)
        n = len(self.noduri)
        
        # Mapare rapidă a numelui nodului la indexul din matrice
        nod_to_idx = {nod: idx for idx, nod in enumerate(self.noduri)}
        idx_dest = nod_to_idx[destinatie]
        idx_sursa = nod_to_idx[sursa]

        # 2. Construirea Matricei Ponderilor C (Pasul 1)
        self.matrice_c = [[self.inf for _ in range(n)] for _ in range(n)]
        
        # Completăm arcele existente din datele de intrare
        for date in date_intrare.values():
            u, v = date['node']
            cost = date['value']
            self.matrice_c[nod_to_idx[u]][nod_to_idx[v]] = cost

        # Diagonala principală este întotdeauna 0 (c_ii = 0)
        for i in range(n):
            self.matrice_c[i][i] = 0

        # 3. Inițializarea structurii tabelului de iterații
        tabel_iteratii = []
        
        # --- ITERAȚIA 0 (Pasul 2) ---
        m_curent = [self.matrice_c[i][idx_dest] for i in range(n)]
        m_curent[idx_dest] = 0 # Distanța de la destinație la destinație este 0
        
        tabel_iteratii.append({
            "k": 0,
            "m": list(m_curent),
            "succ": None
        })

        # --- ITERAȚIILE URMATOARE k >= 1 (Pasul 3) ---
        k = 1
        while True:
            m_precedent = list(tabel_iteratii[-1]["m"])
            
            m_nou = [self.inf for _ in range(n)]
            succ_nou = ["-" for _ in range(n)]
            
            # Destinația rămâne permanent pe 0
            m_nou[idx_dest] = 0

            # Calculăm valorile m^(k) și succ^(k) pentru restul nodurilor i
            for i in range(n):
                if i == idx_dest:
                    continue
                
                minim_nod = self.inf
                succesor_nod = None
                
                # Căutăm j-ul care oferă minimul (cu condiția strictă j != i)
                for j in range(n):
                    if j == i: 
                        continue
                        
                    cost_arc = self.matrice_c[i][j]
                    
                    if cost_arc != self.inf and m_precedent[j] != self.inf:
                        valoare_posibila = cost_arc + m_precedent[j]
                        if valoare_posibila < minim_nod:
                            minim_nod = valoare_posibila
                            succesor_nod = self.noduri[j]
                
                m_nou[i] = minim_nod
                if succesor_nod is not None:
                    succ_nou[i] = succesor_nod

            # Salvează rezultatul acestui pas în istoric
            tabel_iteratii.append({
                "k": k,
                "m": list(m_nou),
                "succ": list(succ_nou)
            })

            # TEST DE OPRIRE (Stabilizarea): m^(k) == m^(k-1)
            if m_nou == m_precedent:
                break
                
            k += 1
            if k > 2 * n:
                break

        # 4. Extragerea distanțelor finale d_it de la Iterația Stop
        d_it = tabel_iteratii[-1]["m"]

        # 5. RECONSTRUCȚIA DRUMULUI OPTIM (Pasul 4)
        succesorii_finali = tabel_iteratii[-1]["succ"]
        
        drum_optim = []
        cost_grafic_suma = 0
        nr_arce_drum = 0
        validare_succes = False
        
        if d_it[idx_sursa] != self.inf:
            nod_curent = sursa
            drum_optim.append(nod_curent)
            
            while nod_curent != destinatie:
                idx_curent = nod_to_idx[nod_curent]
                
                if succesorii_finali is not None:
                    urmatorul_nod = succesorii_finali[idx_curent]
                else:
                    break
                
                if urmatorul_nod == "-" or urmatorul_nod is None:
                    break
                    
                idx_urmator = nod_to_idx[urmatorul_nod]
                cost_grafic_suma += self.matrice_c[idx_curent][idx_urmator]
                nr_arce_drum += 1
                
                nod_curent = urmatorul_nod
                drum_optim.append(nod_curent)

            # 6. VALIDAREA MATEMATICĂ INTEGRALĂ (Pasul 5)
            # Validarea de bază și cea mai importantă: Costul adunat de pe graf coincide cu valoarea înscrisă în tabel.
            if cost_grafic_suma == d_it[idx_sursa]:
                validare_succes = True

        return {
            "noduri": self.noduri,
            "matrice_initiala": self.matrice_c,
            "tabel_iteratii": tabel_iteratii,
            "d_it": d_it,
            "drum_optim": drum_optim,
            "cost_total": d_it[idx_sursa] if d_it[idx_sursa] != self.inf else 0,
            "nr_arce": nr_arce_drum,
            "validare_succes": validare_succes
        }

if __name__ == "__main__":
    date_test = {
        'a0': {'node': ('x1', 'x2'), 'value': 10},
        'a1': {'node': ('x1', 'x9'), 'value': 10},
        'a2': {'node': ('x2', 'x3'), 'value': 15},
        'a3': {'node': ('x3', 'x4'), 'value': 12},
        'a4': {'node': ('x4', 'x1'), 'value': 7},
        'a5': {'node': ('x4', 'x9'), 'value': 9},
        'a6': {'node': ('x4', 'x6'), 'value': 8},
        'a7': {'node': ('x5', 'x1'), 'value': 6},
        'a8': {'node': ('x5', 'x6'), 'value': 20},
        'a9': {'node': ('x6', 'x7'), 'value': 17},
        'a10': {'node': ('x6', 'x8'), 'value': 13},
        'a11': {'node': ('x7', 'x1'), 'value': 4},
        'a12': {'node': ('x7', 'x2'), 'value': 6},
        'a13': {'node': ('x8', 'x9'), 'value': 11},
        'a14': {'node': ('x9', 'x5'), 'value': 5},
        'a15': {'node': ('x9', 'x6'), 'value': 3},
    }
    
    nod_start = 'x1'
    nod_scop = 'x3'
    
    bk = BellmanKalaba()
    rez = bk.solve(date_test, sursa=nod_start, destinatie=nod_scop)
    
    print("=== MATRICEA DE COSTURI INITIALA C ===")
    print(f"{'':<4}", " ".join([f"{nod:<4}" for nod in rez["noduri"]]))
    for i, rand in enumerate(rez["matrice_initiala"]):
        rand_formatat = [str(x) if x != float('inf') else '∞' for x in rand]
        print(f"{rez['noduri'][i]:<4}", " ".join([f"{x:<4}" for x in rand_formatat]))
        
    print("\n=== TABEL ITERATII CORECTAT ===")
    print("Noduri: ", rez["noduri"])
    for it in rez["tabel_iteratii"]:
        print(f"k = {it['k']}:")
        print(f"  m   : {[x if x != float('inf') else 'inf' for x in it['m']]}")
        if it['succ'] is not None:
            print(f"  succ: {it['succ']}")
            
    print(f"\n=== REZULTAT RECONSTRUCȚIE DRUM (De la {nod_start} la {nod_scop}) ===")
    print("Drum minim gasit:", " -> ".join(rez["drum_optim"]))
    print("Cost cumulat:    ", rez["cost_total"])
    print("Numar arce drum: ", rez["nr_arce"])
    print("Validare:        ", "SUCCES" if rez["validare_succes"] else "EȘUATĂ")