# Copyright (c) 2026 Condorache Ștefan-Eugen. All rights reserved.
# Licensed under the MIT License.

import numpy as np
from problems import *
from problem_generator import generate_problem
from fractions import Fraction
from math import comb

class Simplex:

    def afisare(self):
        n_var = len(self.coef)
        n_con = self.MatriceA.shape[0]
        # Preluam valoarea M folosita in algoritm
        M_val = getattr(self, 'M', 1e7)

        def format_val(val):
            """Converteste float in fractie simbolica, gestionand zgomotul Big-M."""
            if abs(val) > M_val * 0.1:  # Prag pentru a detecta prezenta lui M
                # Calculam de cate ori intra M in valoare
                multi = round(val / M_val)
                rem = val - (multi * M_val)

                # Construim string-ul pentru componenta M
                if multi == 1: sign = "M"
                elif multi == -1: sign = "-M"
                else: sign = f"{multi}M"

                # Adaugam restul daca este semnificativ
                if abs(rem) < 1e-4:
                    return sign
                else:
                    frac_part = Fraction(float(rem)).limit_denominator(1000)
                    return f"{sign}{'+' if rem > 0 else ''}{frac_part}"

            # Formatare standard pentru numere fara M
            if abs(val) < 1e-9: return "0"
            return str(Fraction(float(val)).limit_denominator(1000))

        # --- Pasul 1: Calculam latimile coloanelor pentru aliniere perfecta ---
        col_widths = []
        for j in range(n_var):
            content = [f"a{j+1}", format_val(self.coef[j]), format_val(self.Delta[j])]
            content += [format_val(self.MatriceA[i, j]) for i in range(n_con)]
            col_widths.append(max(len(c) for c in content) + 2)

        xb_width = max(len(format_val(x)) for x in self.X_b) + 2
        xb_width = max(xb_width, len(format_val(self.Z)) + 2, 10)

        # --- Pasul 2: Constructie Tabel ---
        header = f"{'Baza':<7} | {'Cb':<10} |"
        for j in range(n_var):
            header += f"{'a'+str(j+1):>{col_widths[j]}}"
        header += f" | {'Xb':>{xb_width}}"

        sep = "-" * len(header)

        print(f"\n{header}")
        print(sep)

        # Randul coeficientilor c
        c_line = f"{'':<7} | {'c':<10} |"
        for j in range(n_var):
            c_line += f"{format_val(self.coef[j]):>{col_widths[j]}}"
        print(c_line)
        print(sep)

        # Liniile matricii (Corpul)
        for i in range(n_con):
            var_name = f"a{int(self.iBaza[i])+1}"
            cb_val = format_val(self.C_b[i])

            row_str = f"{var_name:<7} | {cb_val:<10} |"
            for j in range(n_var):
                row_str += f"{format_val(self.MatriceA[i, j]):>{col_widths[j]}}"
            row_str += f" | {format_val(self.X_b[i]):>{xb_width}}"
            print(row_str)

        print(sep)

        # Randul Delta (acum Delta este sub coloane, Z este la final sub Xb)
        delta_line = f"{'Delta':<7} | {'':<10} |"
        for j in range(n_var):
            delta_line += f"{format_val(self.Delta[j]):>{col_widths[j]}}"
        delta_line += f" | {'Z = ' + format_val(self.Z):>{xb_width}}"
        print(delta_line)
        print("=" * len(header) + "\n")

    def solve(self, data_type, with_table: bool = False, **prob):

        """
        "instance_of_problem" : {
            "OPT":          MAX,                                            
            "coef":         np.array([c_1, c_2, ... , c_n], dtype=data_type),
            "MatriceA":     np.array([[a_11, a_12, ... , a_1n], 
                                      [a_21, a_22, ... , a_2n], 
                                      
                                      ...
                                      
                                      [a_m1, a_m2, ... , a_mn]], dtype=data_type), 
            "inegalitate":  np.array([ mm/MM/eg x m-times ], dtype=int),     
            "b":            np.array([b_1, b_2, ... , b_m], dtype=data_type),
            "x":            np.array([ mm/MM/eg(='R') x n-times], dtype=int)
        },
        """

        coef_initial        = prob["coef"].astype(data_type)
        MatriceA_initial    = prob["MatriceA"].astype(data_type)
    
        self.b              = prob["b"].astype(data_type)
        self.inegalitate    = prob["inegalitate"]
        self.OPT            = prob["OPT"]
        
        self.nr_variabile = coef_initial.shape[0]
        self.x              = prob.get('x', np.full(self.nr_variabile, MM, dtype=int)) # default x >= 0

        assert MatriceA_initial.shape[0] == prob["b"].shape[0],          'Numarul de ecuatii trebuie sa coincida cu numarul de elemente din b'
        assert MatriceA_initial.shape[1] == prob["coef"].shape[0],       'Dimensiunea lui x trebuie sa fie egala cu dimensiunea lui c'
        assert MatriceA_initial.shape[0] == prob["inegalitate"].shape[0],'Trebuie sa fie acelasi numar de inegalitati ca si numarul de ecuatii'
        assert self.x.shape[0]           == prob["coef"].shape[0],       'Trebuie sa fie acelasi numar de variabile pentru conditia 3'
        assert self.OPT                  in (-1, 1),                     'Optimul poate fi doar 1 (MIN) sau -1 (MAX)'
        assert np.all(np.isin(self.inegalitate, [0, 1, 2])),             'Exista doar mai mare egal (0); mai mic egal (1); egal (2)'
        assert np.all(np.isin(self.x, [0, 1, 2])),                       'Semnele lui x pot fi doar: >= 0 (MM=0), <= 0 (mm=1), sau R (eg=2)'

        # Verificarea b_i >= 0, pentru toate i >= 0
        for i, b_i in enumerate(self.b):
            if b_i < 0:
                self.b[i] = np.abs(self.b[i])
                MatriceA_initial[i] = -MatriceA_initial[i]
                print(f"ecuatia {i} a fost inmultita cu -1", end="\n")
                if self.inegalitate[i] in (MM, mm):
                    self.inegalitate[i] = mm if self.inegalitate[i] == MM else MM

        # Regula 1
        self.mapare_decizie = {}
        
        new_coef = []
        new_MatriceA_cols = []
        new_x = []
        
        col_curenta = 0

        for i in range(self.nr_variabile):
            semn  = self.x[i] 
            c_val = coef_initial[i] 
            col_A = MatriceA_initial[:, i] 

            if semn == MM:
                # Cazul 1: x >= 0
                new_coef.append(c_val)
                new_MatriceA_cols.append(col_A)
                new_x.append(MM)
                
                self.mapare_decizie[i] = {'tip': 'normal', 'idx': [col_curenta]}
                col_curenta += 1

            elif semn == mm:
                # Cazul 2: x <= 0
                new_coef.append(-c_val)
                new_MatriceA_cols.append(-col_A)
                new_x.append(MM) # Variabila transformata este acum >= 0
                
                self.mapare_decizie[i] = {'tip': 'negativ', 'idx': [col_curenta]}
                col_curenta += 1

            elif semn == eg:
                # Cazul 3: x apartine R
                # (x')
                new_coef.append(c_val)
                new_MatriceA_cols.append(col_A)
                new_x.append(MM)
                
                # (x'')
                new_coef.append(-c_val)
                new_MatriceA_cols.append(-col_A)
                new_x.append(MM)
                
                self.mapare_decizie[i] = {'tip': 'libera', 'idx': [col_curenta, col_curenta + 1]}
                col_curenta += 2

        self.coef = np.array(new_coef, dtype=data_type)
        self.MatriceA = np.column_stack(new_MatriceA_cols)
        self.x = np.array(new_x, dtype=int)
        
        self.nr_variabile = col_curenta 
        self.M              = max(np.max(np.abs(self.coef)), 
                                  np.max(np.abs(self.MatriceA)),
                                  np.max(np.abs(self.b))) * 10**6
                                  
        self.Baza_I0        = np.array([])
        self.S_I_stop       = np.array([])
        self.Baza_I_stop    = np.array([])
        
        self.istoric_variabile = []

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
                self.istoric_variabile.append({"nume": f"z{i+1}", "tip": "artificial (>=)", "coeficient": self.OPT*self.M})

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
            msg                     = "z nu evolueaza corect"

            if temp is not None:
                if self.OPT == MAX: assert self.Z >= temp, msg
                elif self.OPT == MIN: assert self.Z <= temp, msg

            produs      = np.dot(self.C_b, self.MatriceA)
            self.Delta  = self.coef - produs

            if self.OPT == MAX:
                optim = all(d <= 0 for d in self.Delta)
            elif self.OPT == MIN:
                optim = all(d >= 0 for d in self.Delta)
            
            if with_table: self.afisare()
            if optim : break

            # Conditia de intrare in baza
            MaxMin                          = max(self.Delta) if self.OPT == MAX else min(self.Delta)
            intra_in_baza                   = np.where(self.Delta == MaxMin)[0][0]

            # Conditia de iesire din baza
            pivot_col                       = self.MatriceA[:, intra_in_baza]
            list1                           = [ (self.X_b[i] / pivot_col[i]) if pivot_col[i] > 1e-9 else np.inf for i in range(self.X_b.shape[0]) ]

            if all(ratio == np.inf for ratio in list1):
                return "Problema are solutie nemarginita (Z tinde la infinit)."

            Min                             = min(list1)
            iese_din_baza                   = list1.index(Min)
            
            Pivot                           = self.MatriceA[iese_din_baza, intra_in_baza]
            assert Pivot > 0,               'Pivotul nu poate fi negativ'

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
        for i in range(prob["coef"].shape[0]):
            info = self.mapare_decizie[i]
            tip = info['tip']
            indici = info['idx']
            nume = f"x{i+1}"
            coef_orig = prob["coef"][i]

            if tip == 'normal':
                val = self.solutie[indici[0]]
                tip_str = "decizie (>= 0)"
            elif tip == 'negativ':
                val = -self.solutie[indici[0]]
                tip_str = "decizie (<= 0)"
            elif tip == 'libera':
                val = self.solutie[indici[0]] - self.solutie[indici[1]]
                tip_str = "decizie (∈ R)"

            self.solutie_detaliata[nume] = {
                "valoare": round(float(val), 4), #type: ignore[tip va fi mereu normal, negativ sau libera] 
                "tip": tip_str,                  #type: ignore[de aceea error alert poate fi ignorata]
                "coef_obiectiv": coef_orig
            }

        for j, info in enumerate(self.istoric_variabile):
            idx_solutie = self.nr_variabile + j
            self.solutie_detaliata[info["nume"]] = {
                "valoare": round(float(self.solutie[idx_solutie]), 4),
                "tip": info["tip"],
                "coef_obiectiv": info["coeficient"]
            }

        return self.solutie_detaliata
    
    def verify(self):
        
        result = [False, False, False]

        if self.Baza_I_stop.size == 0 or not hasattr(self, 'solutie_detaliata'):
            return {"result": result, "msg": "Solutia detaliata nu a fost generata."}

        msg1 = "Toate variabilele interne respecta conditia x >= 0."
        result[0] = True
        for i, x in enumerate(self.solutie):
            if x < -1e-6:
                result[0] = False
                msg1 = f"Eroare: Variabila interna {i} are valoarea {x} < 0"
                break

        # Verificarea 2
        valori      = self.solutie[:self.nr_variabile]
        coeficienti = self.coef[:self.nr_variabile]
        Z_calculat  = np.float64(np.dot(valori, coeficienti.T))
        msg2        = ("".join(f"{valori[i]}*{coeficienti[i]} + " for i in range(len(valori))))[:-3]

        if abs(Z_calculat - np.float64(self.Z)) <= 1e-6:
            result[1] = True
            msg2     += " = " + str(Z_calculat) + " = Z "
        else:
            result[1] = False
            msg2     += " != " + str(Z_calculat) + " = Z "

        # Verificarea 3 (ramane identica)
        S    = self.Matrix_initial[:, self.iBaza.astype(int)]

        if np.allclose(self.Baza_I0, np.dot(S, self.Baza_I_stop), atol=1e-6):
            result[2] = True
        else:
            result[2] = False

        return {"result": result,
                "Verificarea1:": msg1,
                "Verificarea2:": msg2,
                "Verificarea3:": {"Baza_I0": self.Baza_I0, "S": S, "Baza_I0_stop": self.Baza_I_stop}
                }

if __name__ == '__main__':
    
    solver = Simplex()

    if eval(input("1 - test cases; 2 - random problem :   ")) == 1:
        for problem in problems.keys():
            print(problem, end='\n')
            sol = solver.solve(data_type, **problems[problem])
            result = solver.verify()
            #print("Solutia: ", sol)
            #print("Verificarea: ", result, end='\n\n')
            solver.afisare()
    else:
        m = int(input("Dimensiunea m: "))
        n = int(input("Dimensiunea n: "))
        sol = solver.solve(data_type, **generate_problem(m,n))
        ver = solver.verify()
        print("Solutia: ", sol)
        print("Verificarea: ", ver, end='\n\n')