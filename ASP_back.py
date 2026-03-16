import numpy as np
from problems import *
from math import comb

class Simplex:

    def afisare(self):
        print("Coef: ", self.coef, end='\n')
        print("C_b: ", self.C_b, end='\n')
        print("Baza: ", self.iBaza, end='\n')
        print("X_b: ",self.X_b, end='\n')
        print("Z: ", self.Z, end='\n')
        print("Delta: ", self.Delta, end='\n')
        print("A: \n", self.MatriceA, end='\n')

    def solve(self, data_type, **prob):

        self.coef           = prob["coef"].astype(data_type)
        self.MatriceA       = prob["MatriceA"].astype(data_type)
        self.b              = prob["b"].astype(data_type)
        self.M = max(np.max(np.abs(self.coef)), 
                     np.max(np.abs(self.MatriceA)),
                     np.max(np.abs(self.b))) * 10**6
        self.inegalitate    = prob["inegalitate"]
        self.OPT            = prob["OPT"]
        self.nr_variabile   = prob["coef"].shape[0]

        self.Baza_I0        = np.array([])
        self.S_I_stop       = np.array([])
        self.Baza_I_stop    = np.array([])

        self.istoric_variabile = []
        for i in range(self.nr_variabile):
            self.istoric_variabile.append({
                "nume": f"x{i+1}", 
                "tip": "decizie", 
                "coeficient": self.coef[i]
            })

        assert self.MatriceA.shape[0] == self.b.shape[0],             'numarul de ecuatii trebuie sa coincida cu numarul de elemnte din b'
        assert self.MatriceA.shape[1] == self.coef.shape[0],          'dimensiunea lui x trebuie sa fie egala cu dimensiunea lui c'
        assert self.MatriceA.shape[0] == self.inegalitate.shape[0],   'trebuie sa fiu acelasi numar de inegalitati ca si numarul de ecuatii '
        assert self.OPT in (-1, 1),                                   'Optimul poate fi doar 1 (MIN) sau -1 (MAX)'

        print("Algoritmul Simplex Primal presupune ca in conditia-3: x >= 0; (default)", end='\n')

        # Verificarea b_i >= 0, pentru toate i >= 0
        for i, b_i in enumerate(self.b):
            if b_i < 0:
                self.b[i] = np.abs(self.b[i])
                self.MatriceA[i] = -self.MatriceA[i]
                print(f"ecuatia {i} a fost inmultita cu -1", end="\n")
                if self.inegalitate[i] in (MM, mm):
                    self.inegalitate[i] = mm if self.inegalitate[i] == MM else MM

        # Regulla 1: skip deoarece se considera implicit x >= 0
        # Regula 2

        for i, semn in enumerate(self.inegalitate):
            if semn == mm:
                self.coef = np.append(self.coef, 0)
                col = np.zeros((len(self.inegalitate)), dtype=data_type);  col[i] = 1
                self.MatriceA = np.column_stack([self.MatriceA, col])
                self.istoric_variabile.append({"nume": f"y{i+1}", "tip": "compensare (<=)", "coeficient": 0})
            elif semn == MM:
                self.coef = np.append(self.coef, np.array([0, self.OPT*self.M], dtype=data_type))
                col1 = np.zeros((len(self.inegalitate),), dtype=data_type); col1[i] = -1
                col2 = np.zeros((len(self.inegalitate),), dtype=data_type); col2[i] = 1
                self.MatriceA = np.column_stack([self.MatriceA, col1])
                self.MatriceA = np.column_stack([self.MatriceA, col2])
                self.istoric_variabile.append({"nume": f"y{i+1}", "tip": "surplus (>=)", "coeficient": 0})
                self.istoric_variabile.append({"nume": f"z{i+1}", "tip": "artificial", "coeficient": self.OPT*self.M})
            else: 
                self.coef = np.append(self.coef, self.OPT*self.M)
                col = np.zeros((len(self.inegalitate),), dtype=data_type); col[i] = 1
                self.MatriceA = np.column_stack([self.MatriceA, col])
                self.istoric_variabile.append({"nume": f"z{i+1}", "tip": "artificial", "coeficient": self.OPT*self.M})

        self.C_b             = np.zeros(self.MatriceA.shape[0])
        self.X_b             = np.copy(self.b)
        self.Z               = None

        optim                = False
        victor_unique        = np.zeros(self.MatriceA.shape[0])
        victor_unique        [self.MatriceA.shape[0]-1] = 1
        self.iBaza           = np.zeros(self.MatriceA.shape[0])
        Identitate           = np.eye(self.MatriceA.shape[0])
        self.Delta           = np.zeros(self.coef.shape[0])
        
        self.Baza_I0        = np.copy(self.X_b)
        self.Matrix_initial = np.copy(self.MatriceA)

        for j, victor in enumerate(self.MatriceA.T):
            if np.all(np.sort(victor) == victor_unique):
                filtru              = np.all(Identitate == victor, axis=1)
                index               = np.where(filtru)[0]
                self.iBaza[index]   = j
                self.C_b[index]     = self.coef[j]

        n_var = self.coef.shape[0]
        n_con = self.MatriceA.shape[0]
        max_iteratii = comb(n_var, n_con)
        iteratie_curenta = 0

        while not optim:

            iteratie_curenta += 1
            if iteratie_curenta > max_iteratii:
                return f"Ciclare detectata: algoritmul nu converge in {max_iteratii} iteratii."
            
            temp                    = self.Z
            self.Z                  = np.dot(self.C_b, self.X_b.T)
            
            if temp is not None:
                if self.OPT == MAX and self.Z >= temp: print("z creste - corect")
                elif self.OPT == MIN and self.Z <= temp: print("z descreste - corect")
                else: 
                    return "z nu evolueaza corect"


            produs      = np.dot(self.C_b, self.MatriceA)
            self.Delta  = self.coef - produs

            if self.OPT == MAX:
                optim = all(d <= 0 for d in self.Delta)
            elif self.OPT == MIN:
                optim = all(d >= 0 for d in self.Delta)
            
            #self.afisare()
            if optim : break

            # Conditia de intrare in baza
            MaxMin                          = max(self.Delta) if self.OPT == MAX else min(self.Delta)
            intra_in_baza                   = np.where(self.Delta == MaxMin)[0][0]

            # Conditia de iesire din baza
            pivot_col                       = self.MatriceA[:, intra_in_baza]
            list1                           = [ (self.X_b[i] / pivot_col[i]) if pivot_col[i] > 0 else np.inf for i in range(self.X_b.shape[0]) ]

            if all(ratio == np.inf for ratio in list1):
                return "Problema are solutie nemarginita (Z tinde la infinit)."

            Min                             = min(list1)
            iese_din_baza                   = list1.index(Min)
            
            Pivot                            = self.MatriceA[iese_din_baza, intra_in_baza]
            self.X_b[iese_din_baza]         /= Pivot; 
            self.MatriceA[iese_din_baza]    /= Pivot
            
            # Gauss-Jordan
            for i in range(self.MatriceA.shape[0]):
                if i != iese_din_baza:
                    factor = self.MatriceA[i, intra_in_baza]
                    self.MatriceA[i] -= factor * self.MatriceA[iese_din_baza]
                    self.X_b[i] -= factor * self.X_b[iese_din_baza]

            self.iBaza[iese_din_baza] = intra_in_baza
            self.C_b[iese_din_baza]   = self.coef[intra_in_baza]
        
        self.Baza_I_stop    = np.copy(self.X_b)
        self.S_I_stop       = np.copy(self.iBaza)
        self.solutie        = np.zeros(self.coef.shape[0], dtype=data_type)

        for row_idx, var_idx in enumerate(self.iBaza):
            self.solutie[int(var_idx)] = self.X_b[row_idx]

        for row_idx, var_idx in enumerate(self.iBaza):
            if abs(self.coef[int(var_idx)]) == self.M and self.X_b[row_idx] > 1e-6:
                return "Problema nu are solutie admisibila (sistem incompatibil)."

        self.solutie_detaliata = {}
        for j, info in enumerate(self.istoric_variabile):
            self.solutie_detaliata[info["nume"]] = {
                "valoare": round(float(self.solutie[j]), 4),
                "tip": info["tip"],
                "coef_obiectiv": info["coeficient"]
            }

        return self.solutie_detaliata
    
    def verify(self) -> list[bool]:
        
        result = [False, False, False]

        if self.Baza_I_stop.size == 0:
            return result

        # Verificarea 1
        for x in self.solutie:
            if x < 0:
                result[0] = False
                break
            else:
                result[0] = True

        # Verificarea 2
        valori      = self.solutie[:self.nr_variabile]
        coeficienti = self.coef[:self.nr_variabile]
        Z_calculat  = np.float64(np.dot(valori, coeficienti.T))

        if abs(Z_calculat - np.float64(self.Z)) <= 1e-3:
            result[1] = True
        else:
            result[1] = False

        # Verificarea 3
        S = self.Matrix_initial[:, self.iBaza.astype(int)]

        if np.allclose(self.Baza_I0, np.dot(S, self.Baza_I_stop), atol=1e-3):
            result[2] = True
        else:
            result[2] = False

        return result

if __name__ == '__main__':
    
    solver = Simplex()

    for problem in problems.keys():
        print(problem, end='\n')
        sol = solver.solve(data_type, **problems[problem])
        result = solver.verify()
        print("Solutia: ", sol)
        print("Verificarea: ", result, end='\n\n')
