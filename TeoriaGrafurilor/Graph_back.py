import copy

class Graph:   

    def solve(self, **problema):
        self.graf = {}
        set_noduri = set()
        
        sursa = problema['sursa']
        destinatie = problema['destinatie']
        
        for id_conexiune, date in problema['date_intrare'].items():
            u, v = date['node']
            capacitate = date['value']
            
            if u not in self.graf:
                self.graf[u] = {}
            if v not in self.graf:
                self.graf[v] = {}
            
            self.graf[u][v] = capacitate
            
            if u not in self.graf[v]:
                self.graf[v][u] = 0
            
            set_noduri.add(u)
            set_noduri.add(v)
            
        self.noduri = list(set_noduri)
        self.graf_original = copy.deepcopy(self.graf)
        
        flux_maxim = 0
        iteratii = []

        while True:
            parinte = {}
            vizitat = {nod: False for nod in self.noduri}
            coada = [sursa]
            vizitat[sursa] = True
            gasit_drum = False

            while coada:
                u = coada.pop(0)
                for v, capacitate in self.graf[u].items():
                    if not vizitat[v] and capacitate > 0:
                        coada.append(v)
                        vizitat[v] = True
                        parinte[v] = u
                        if v == destinatie:
                            gasit_drum = True
                            break
                if gasit_drum:
                    break

            if not gasit_drum:
                iteratii.append({
                    "drum_xt_xs": None,
                    "minim_valori": 0,
                    "flux_maxim_moment": flux_maxim,
                    "test_optimalitate": f"Optim: Nu s-a mai putut găsi un drum de la {sursa} la {destinatie}."
                })
                break

            flux_curent = float("Inf")
            nod_curent = destinatie
            drum_invers = []
            
            while nod_curent != sursa:
                drum_invers.append(nod_curent)
                nod_anterior = parinte[nod_curent]
                flux_curent = min(flux_curent, self.graf[nod_anterior][nod_curent])
                nod_curent = nod_anterior
            
            drum_invers.append(sursa)
            flux_maxim += flux_curent
            
            iteratii.append({
                "drum_xt_xs": drum_invers,
                "minim_valori": flux_curent,
                "flux_maxim_moment": flux_maxim,
                "test_optimalitate": f"Ne-optim: S-a găsit un drum de la {sursa} la {destinatie}."
            })
            
            nod_curent = destinatie
            while nod_curent != sursa:
                nod_anterior = parinte[nod_curent]
                self.graf[nod_anterior][nod_curent] -= flux_curent
                self.graf[nod_curent][nod_anterior] += flux_curent
                nod_curent = nod_anterior

        vizitat_final = {nod: False for nod in self.noduri}
        coada_finala = [sursa]
        vizitat_final[sursa] = True

        while coada_finala:
            u = coada_finala.pop(0)
            for v, capacitate in self.graf[u].items():
                if not vizitat_final[v] and capacitate > 0:
                    vizitat_final[v] = True
                    coada_finala.append(v)

        muchii_taiate = []
        for u in self.noduri:
            for v, capacitate_initiala in self.graf_original[u].items():
                if vizitat_final[u] and not vizitat_final[v] and capacitate_initiala > 0:
                    muchii_taiate.append({
                        "de_la": u,
                        "la": v,
                        "capacitate": capacitate_initiala
                    })

        return flux_maxim, iteratii, muchii_taiate

    def afisare(self):
        rezultat = []
        for u in self.graf:
            for v, capacitate in self.graf[u].items():
                if capacitate > 0:
                    rezultat.append(f"Muchia {u} -> {v} (Capacitate reziduală: {capacitate})")
        
        if not rezultat:
            return "Graful este gol."
        return "\n".join(rezultat)
    

if __name__ == "__main__":
    problema = {
        'date_intrare': {
            'c1': {'node': ('x1', 'x2'), 'value': 20},
            'c2': {'node': ('x1', 'x3'), 'value': 30},
            'c3': {'node': ('x1', 'x4'), 'value': 40},
            'c4': {'node': ('x2', 'x7'), 'value': 21},
            'c5': {'node': ('x2', 'x5'), 'value': 22},
            'c6': {'node': ('x3', 'x5'), 'value': 11},
            'c7': {'node': ('x3', 'x8'), 'value': 23},
            'c8': {'node': ('x3', 'x6'), 'value': 8},
            'c9': {'node': ('x4', 'x6'), 'value': 24},
            'c10': {'node': ('x4', 'x9'), 'value': 25},
            'c11': {'node': ('x5', 'x7'), 'value': 10},
            'c12': {'node': ('x5', 'x8'), 'value': 9},
            'c13': {'node': ('x6', 'x8'), 'value': 12},
            'c14': {'node': ('x6', 'x9'), 'value': 8},
            'c15': {'node': ('x7', 'x10'), 'value': 31},
            'c16': {'node': ('x8', 'x10'), 'value': 26},
            'c17': {'node': ('x9', 'x10'), 'value': 42}
        },
        'sursa': 'x1',
        'destinatie': 'x10'
    }
    
    graf = Graph()
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
    
    print("\nMUCHII TĂIATE (Tăietura minimă):")
    if muchii_taiate:
        for muchie in muchii_taiate:
            print(f"  {muchie['de_la']} -> {muchie['la']} (Capacitate: {muchie['capacitate']})")
    else:
        print("  Nicio muchie tăiată găsită.")