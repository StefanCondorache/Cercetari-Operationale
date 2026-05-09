import re

def extrage_index(nume_nod):
    """Extrage numărul din șirul nodului pentru sortarea strictă pe indici (ex: 'x10' -> 10)."""
    match = re.search(r'\d+', nume_nod)
    return int(match.group()) if match else float('inf')

class AFF:   

    def solve(self, **problema):
        self.graf = {}
        self.date_intrare = problema['date_intrare']
        
        sursa = problema['sursa']
        destinatie = problema['destinatie']
        set_noduri = set()
        
        for id_conexiune, date in self.date_intrare.items():
            u, v = date['node']
            capacitate = date['value']
            
            if u not in self.graf: self.graf[u] = {}
            if v not in self.graf: self.graf[v] = {}
            
            self.graf[u][v] = {'cap': capacitate, 'flux': 0}
            
            set_noduri.add(u)
            set_noduri.add(v)
            
        self.noduri = sorted(list(set_noduri), key=extrage_index)
        
        flux_maxim = 0
        iteratii = []

        # ======================================================================
        # FAZA 1: DRUMURI INIȚIALE (Căutare BFS pentru cele mai directe rute)
        # ======================================================================
        vecini_sursa = sorted(list(self.graf.get(sursa, {}).keys()), key=extrage_index)
        
        for vecin in vecini_sursa:
            parinte = {vecin: sursa}
            vizitat = {nod: False for nod in self.noduri}
            vizitat[sursa] = True
            vizitat[vecin] = True
            coada = [vecin] 
            gasit = False
            
            while coada and not gasit:
                u = coada.pop(0) 
                vecini_u = sorted(list(self.graf.get(u, {}).keys()), key=extrage_index)
                for v in vecini_u:
                    if not vizitat[v]:
                        cap = self.graf[u][v]['cap']
                        flux = self.graf[u][v]['flux']
                        if flux < cap:
                            parinte[v] = u
                            vizitat[v] = True
                            coada.append(v)
                            if v == destinatie:
                                gasit = True
                                break
            
            if gasit:
                nod_curent = destinatie
                drum_invers = []
                flux_curent = float('inf')
                
                while nod_curent != sursa:
                    drum_invers.append(nod_curent)
                    p = parinte[nod_curent]
                    cap_disp = self.graf[p][nod_curent]['cap'] - self.graf[p][nod_curent]['flux']
                    flux_curent = min(flux_curent, cap_disp)
                    nod_curent = p
                
                drum_invers.append(sursa)
                
                nod_curent = destinatie
                while nod_curent != sursa:
                    p = parinte[nod_curent]
                    self.graf[p][nod_curent]['flux'] += flux_curent
                    nod_curent = p
                    
                flux_maxim += flux_curent
                
                iteratii.append({
                    "drum_xt_xs": drum_invers,
                    "minim_valori": flux_curent,
                    "flux_maxim_moment": flux_maxim,
                    "test_optimalitate": "Faza inițială (Drum obișnuit)",
                    "etichete_ui": {}
                })

        # ======================================================================
        # FAZA 2: ETICHETARE (CĂUTARE ÎN LĂȚIME / BFS STRICT PE INDICI)
        # Permite utilizarea capacității pe oricare sens, adunând pozitiv.
        # ======================================================================
        while True:
            etichete = {sursa: ('+', None, float('inf'))}
            coada = [sursa] # Folosim COADĂ pentru explorare pe niveluri (BFS)
            gasit_drum = False

            while coada and not gasit_drum:
                u = coada.pop(0) 
                vecini_posibili = []
                
                for v in self.noduri:
                    if v in etichete:
                        continue 
                        
                    # 1. ARC DIRECT NESATURAT
                    if v in self.graf.get(u, {}):
                        flux = self.graf[u][v]['flux']
                        cap = self.graf[u][v]['cap']
                        if flux < cap:
                            vecini_posibili.append((v, '+', cap - flux))
                            
                    # 2. ARC INVERS NESATURAT (Gândit ca o conductă bidirecțională)
                    elif u in self.graf.get(v, {}):
                        flux = self.graf[v][u]['flux']
                        cap = self.graf[v][u]['cap']
                        if flux < cap:
                            vecini_posibili.append((v, '-', cap - flux))
                            
                # Sortăm vecinii posibili după index
                vecini_posibili.sort(key=lambda x: extrage_index(x[0]))
                
                # Etichetăm toți vecinii valizi ai nodului curent
                for v, semn, cap_disp in vecini_posibili:
                    if v not in etichete:
                        minim_curent = min(etichete[u][2], cap_disp)
                        etichete[v] = (semn, u, minim_curent)
                        coada.append(v)
                        
                        if v == destinatie:
                            gasit_drum = True
                            break
            
            # Construim etichetele pentru UI
            etichete_ui = {"x1": "(+)"}
            for nod, data in etichete.items():
                if nod != sursa:
                    etichete_ui[nod] = f"({data[0]}{data[1]})"

            if not gasit_drum:
                iteratii.append({
                    "drum_xt_xs": None,
                    "minim_valori": 0,
                    "flux_maxim_moment": flux_maxim,
                    "test_optimalitate": f"Test Optim: STOP. Nu s-a mai putut eticheta {destinatie}.",
                    "etichete_ui": etichete_ui
                })
                break

            nod_curent = destinatie
            drum_gasit = [destinatie]
            flux_adaugat = etichete[destinatie][2]
            
            while nod_curent != sursa:
                semn, parinte, _ = etichete[nod_curent]
                
                # ADUNĂM MEREU POZITIV, indiferent de direcție
                if semn == '+':
                    self.graf[parinte][nod_curent]['flux'] += flux_adaugat
                elif semn == '-':
                    self.graf[nod_curent][parinte]['flux'] += flux_adaugat
                
                nod_curent = parinte
                drum_gasit.append(nod_curent)
                
            flux_maxim += flux_adaugat
            
            iteratii.append({
                "drum_xt_xs": drum_gasit,
                "minim_valori": flux_adaugat,
                "flux_maxim_moment": flux_maxim,
                "test_optimalitate": "Test Ne-Optim: Destinația a primit etichetă.",
                "etichete_ui": etichete_ui
            })

        # ======================================================================
        # DETERMINAREA TĂIETURII
        # ======================================================================
        noduri_etichetate = set(etichete.keys())
        muchii_taiate = []
        for u in self.noduri:
            for v in self.graf.get(u, {}):
                cap = self.graf[u][v]['cap']
                flux = self.graf[u][v]['flux']
                if u in noduri_etichetate and v not in noduri_etichetate and flux >= cap:
                    muchii_taiate.append({
                        "de_la": u,
                        "la": v,
                        "capacitate": cap
                    })

        return flux_maxim, iteratii, muchii_taiate

if __name__ == "__main__":
    problema = {
        'date_intrare': {
            'c1': {'node': ('x1', 'x2'), 'value': 20},
            'c2': {'node': ('x1', 'x3'), 'value': 30},
            'c3': {'node': ('x1', 'x4'), 'value': 40},
            'c4': {'node': ('x2', 'x7'), 'value': 10},
            'c5': {'node': ('x2', 'x5'), 'value': 28},
            'c6': {'node': ('x3', 'x5'), 'value': 17},
            'c7': {'node': ('x3', 'x8'), 'value': 4},
            'c8': {'node': ('x3', 'x6'), 'value': 18},
            'c9': {'node': ('x4', 'x6'), 'value': 19},
            'c10': {'node': ('x4', 'x9'), 'value': 23},
            'c11': {'node': ('x5', 'x7'), 'value': 10},
            'c12': {'node': ('x5', 'x8'), 'value': 9},
            'c13': {'node': ('x6', 'x8'), 'value': 12},
            'c14': {'node': ('x6', 'x9'), 'value': 8},
            'c15': {'node': ('x7', 'x10'), 'value': 31},
            'c16': {'node': ('x8', 'x10'), 'value': 19},
            'c17': {'node': ('x9', 'x10'), 'value': 42}
        },
        'sursa': 'x1',
        'destinatie': 'x10'
    }
    
    graf = AFF()
    flux_maxim, iteratii, muchii_taiate = graf.solve(**problema)
    
    print("=== ISTORIC ITERAȚII ===")
    for i, it in enumerate(iteratii):
        print(f"\nIterația {i + 1}:")
        print(f"  Test optimalitate: {it['test_optimalitate']}")
        
        if it['drum_xt_xs']:
            drum_str = " -> ".join(it['drum_xt_xs'])
            print(f"  Drum xt -> xs:     {drum_str}")
            print(f"  Minim valori:      {it['minim_valori']}")
            print(f"  Flux maxim curent: {it['flux_maxim_moment']}")
            
    print(f"\n=== REZULTATE FINALE ===")
    print(f"FLUX MAXIM: {flux_maxim}")
    print("\nMUCHII TĂIATE (Tăietura trece strict prin arcele saturate):")
    for muchie in muchii_taiate:
        print(f"  {muchie['de_la']} -> {muchie['la']} (Capacitate: {muchie['capacitate']})")