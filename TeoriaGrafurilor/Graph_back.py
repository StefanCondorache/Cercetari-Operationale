import copy

class Graph:   

    def solve(self, **problema):
        """Execută salvarea/resetarea și algoritmul Ford-Fulkerson.
            problema : {
                'date_intrare': {
                    'conexiune1': {'node': ('A', 'B'), 'value': 10},
                    'conexiune2': {'node': ('B', 'C'), 'value': 5},
                    ...
                },
                'sursa': 'A',
                'destinatie': 'C'
            }
        """
        self.graf = {}
        set_noduri = set()
        
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
        drumuri_gasite = []

        while True:
            parinte = {}
            vizitat = {nod: False for nod in self.noduri}
            coada = [problema['sursa']]
            vizitat[problema['sursa']] = True
            gasit_drum = False

            while coada:
                u = coada.pop(0)
                for v, capacitate in self.graf[u].items():
                    if not vizitat[v] and capacitate > 0:
                        coada.append(v)
                        vizitat[v] = True
                        parinte[v] = u
                        if v == problema['destinatie']:
                            gasit_drum = True
                            break
                if gasit_drum:
                    break

            if not gasit_drum:
                break

            flux_curent = float("Inf")
            nod_curent = problema['destinatie']
            drum = []
            
            while nod_curent != problema['sursa']:
                drum.insert(0, nod_curent)
                nod_anterior = parinte[nod_curent]
                flux_curent = min(flux_curent, self.graf[nod_anterior][nod_curent])
                nod_curent = nod_anterior
            
            drum.insert(0, problema['sursa'])
            drumuri_gasite.append({"drum": drum, "flux_adaugat": flux_curent})
            flux_maxim += flux_curent
            
            nod_curent = problema['destinatie']
            while nod_curent != problema['sursa']:
                nod_anterior = parinte[nod_curent]
                self.graf[nod_anterior][nod_curent] -= flux_curent
                self.graf[nod_curent][nod_anterior] += flux_curent
                nod_curent = nod_anterior

        return flux_maxim, drumuri_gasite

    def afisare(self):
        """Afișează muchiile cu capacitate nenulă din graful curent."""
        rezultat = []
        for u in self.graf:
            for v, capacitate in self.graf[u].items():
                if capacitate > 0:
                    rezultat.append(f"Muchia {u} -> {v} (Capacitate: {capacitate})")
        
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
    flux_maxim, drumuri_gasite = graf.solve(**problema)
    
    print(f"Flux maxim: {flux_maxim}")
    print("Drumuri găsite:")
    for drum in drumuri_gasite:
        print(f"Drum: {' -> '.join(drum['drum'])}, Flux adăugat: {drum['flux_adaugat']}")
    
    print("\nStarea finală a grafului:")
    print(graf.afisare())