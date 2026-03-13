import numpy as np

MIN = 1
MAX = -1

MM = 0 # exp >= b
mm = 1 # exp <= b
eg = 2 # exp = b

M = np.float64(10**6)

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
        self.inegalitate    = prob["inegalitate"]
        self.OPT            = prob["OPT"]

        self.Baza_I0        = np.array([])
        self.S_I_stop       = np.array([])
        self.Baza_I_stop    = np.array([])

        assert self.MatriceA.shape[0] == self.b.shape[0],             'numarul de ecuatii trebuie sa coincida cu numarul de elemnte din b'
        assert self.MatriceA.shape[1] == self.coef.shape[0],          'dimensiunea lui x trebuie sa fie egala cu dimensiunea lui c'
        assert self.MatriceA.shape[0] == self.inegalitate.shape[0],   'trebuie sa fiu acelasi numar de inegalitati ca si numarul de ecuatii '
        assert self.OPT in (-1, 1),                              'Optimul poate fi doar 1 (MIN) sau -1 (MAX)'

        print("Algoritmul Simplex Primal presupune ca in conditia-3: x >= 0; (default)", end='\n')

        # Verificarea b_i >= 0, pentru toate i >= 0
        for i, b_i in enumerate(self.b):
            if b_i < 0:
                self.b[i] = np.abs(self.b[i])
                self.MatriceA[i] = -self.MatriceA[i]
                print(f"ecuatia {i} a fost inmultita cu -1", end="\n")
                if self.inegalitate[i] in (MM, mm):
                    self.inegalitate[i] = mm if self.inegalitate[i] == MM else MM

        # Regula 1: skip deoarece se considera implicit x >= 0
        # Regula 2

        for i, semn in enumerate(self.inegalitate):
            if semn == mm:
                self.coef = np.append(self.coef, 0)
                col = np.zeros((len(self.inegalitate)), dtype=data_type);  col[i] = 1
                self.MatriceA = np.column_stack([self.MatriceA, col])
            elif semn == MM:
                self.coef = np.append(self.coef, np.array([0, self.OPT*M], dtype=data_type))
                col1 = np.zeros((len(self.inegalitate),), dtype=data_type); col1[i] = -1
                col2 = np.zeros((len(self.inegalitate),), dtype=data_type); col2[i] = 1
                self.MatriceA = np.column_stack([self.MatriceA, col1])
                self.MatriceA = np.column_stack([self.MatriceA, col2])
            else: 
                self.coef = np.append(self.coef, self.OPT*M)
                col = np.zeros((len(self.inegalitate),), dtype=data_type); col[i] = 1
                self.MatriceA = np.column_stack([self.MatriceA, col])

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

        while not optim:
            for j, victor in enumerate(self.MatriceA.T):
                if np.all(np.sort(victor) == victor_unique):
                    filtru              = np.all(Identitate == victor, axis=1)
                    index               = np.where(filtru)[0]
                    self.iBaza[index]   = j
                    self.C_b[index]     = self.coef[j]
            
            temp                        = self.Z
            self.Z                      = np.dot(self.C_b, self.X_b.T)
            
            if temp is not None:
                if self.OPT == MAX and self.Z >= temp: print("z descreste - corect")
                elif self.OPT == MIN and self.Z <= temp: print("z creste - corect")
                else: 
                    print("z nu evolueaza corect")
                    return -1

            produs      = np.dot(self.C_b, self.MatriceA)
            self.Delta  = self.coef - produs

            for j in range(self.coef.shape[0]):
                if self.OPT == MAX:
                    if self.Delta[j] > 0:
                        optim = False
                        break
                    optim = True
                elif self.OPT == MIN:
                    if self.Delta[j] < 0:
                        optim = False
                        break
                    optim = True

            #self.afisare()
            if optim : break

            # Conditia de intrare in baza
            MaxMin                          = max(self.Delta) if self.OPT == MAX else min(self.Delta)
            intra_in_baza                   = np.where(self.Delta == MaxMin)[0][0]

            # Conditia de iesire din baza
            pivot_col                       = self.MatriceA[:, intra_in_baza]
            list1                           = [ (self.X_b[i] / pivot_col[i]) if pivot_col[i] > 0 else np.inf for i in range(self.X_b.shape[0]) ]

            if all(ratio == np.inf for ratio in list1):
                print("Problema are solutie nemarginita (Z tinde la infinit).")
                break

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

            self.afisare()
        
        self.Baza_I_stop    = np.copy(self.X_b)
        self.S_I_stop       = np.copy(self.iBaza)
        self.solutie        = np.zeros(self.coef.shape[0], dtype=data_type)

        for row_idx, var_idx in enumerate(self.iBaza):
            self.solutie[int(var_idx)] = self.X_b[row_idx]

        return self.solutie
    
    def verify(self) -> list[bool]:
        
        result = [False, False, False]

        # Verificarea 1
        for x in self.solutie:
            if x < 0:
                result[0] = False
                break
            else:
                result[0] = True

        # Verificarea 2
        if np.dot(self.solutie[:3], self.coef[:3].T) == self.Z:
            result[1] = True
        else:
            result[1] = False

        # Verificarea 3
        S = np.column_stack([
            self.Matrix_initial[:, int(self.iBaza[0])],
            self.Matrix_initial[:, int(self.iBaza[1])],
            self.Matrix_initial[:, int(self.iBaza[2])]
        ])

        if np.all(self.Baza_I0 == np.dot(S, self.Baza_I_stop)):
            result[2] = True
        else:
            result[2] = False

        return result

if __name__ == '__main__':
    
    solver = Simplex()
    data_type = np.float64
    
    problema1 = {
        "OPT":          MAX,                                            
        "coef":         np.array([4, 3, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 3, 2], [4, 2, 2], [1, 1, 3]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([12, 15, 12], dtype=data_type)
    }
    
    problema2 = {
        "OPT":          MAX,                                            
        "coef":         np.array([4, 1, 2], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 3], [1, 1, 1], [2, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([12, 10, 8], dtype=data_type)
    }

    problema3 = {
        "OPT":          MAX,                                            
        "coef":         np.array([1, -3], dtype=data_type),
        "MatriceA":     np.array([[1, 1], [2, -1]], dtype=data_type), 
        "inegalitate":  np.array([MM, mm], dtype=int),     
        "b":            np.array([-1, 2], dtype=data_type)
    }

    problema4 = {
        "OPT":          MIN,                                            
        "coef":         np.array([1, 1, -1], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 1], [-2, 0, 3], [0, 1, -3]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, eg], dtype=int),     
        "b":            np.array([1, -2, 5], dtype=data_type)
    }

    problema5 = {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 2, 3], dtype=data_type),
        "MatriceA":     np.array([[2, 3, 2], [3, 2, 1], [2, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([15, 15, 15], dtype=data_type)
    }


    sol = solver.solve(data_type, **problema5)
    result = solver.verify()
    print("Solutia: ", sol)
    print("Verificarea: ", result)
    #solver.afisare()