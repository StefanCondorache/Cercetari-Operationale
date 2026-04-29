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

        return flux_maxim, iteratii

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
            'conexiune1': {'node': ('A', 'B'), 'value': 10},
            'conexiune2': {'node': ('B', 'C'), 'value': 5},
            'conexiune3': {'node': ('A', 'C'), 'value': 15},
        },
        'sursa': 'A',
        'destinatie': 'C'
    }
    
    graf = Graph()
    flux_maxim, iteratii = graf.solve(**problema)
    
    print("=== ISTORIC ITERAȚII ===")
    for i, it in enumerate(iteratii):
        print(f"\nIterația {i + 1}:")
        print(f"  Test optimalitate: {it['test_optimalitate']}")
        
        if it['drum_xt_xs']:
            drum_str = " -> ".join(it['drum_xt_xs'])
            print(f"  Drum xt -> xs:     {drum_str}")
            print(f"  Minim valori:      {it['minim_valori']}")
            print(f"  Flux maxim curent: {it['flux_maxim_moment']}")
            
    print(f"\nFLUX MAXIM FINAL: {flux_maxim}\n")
    
    print("=== STAREA FINALĂ A GRAFULUI (Rețeaua Reziduală) ===")
    print(graf.afisare())