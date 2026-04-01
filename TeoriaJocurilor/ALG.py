import numpy as np
from ProblemaLineara.problems import MIN, MAX, mm, MM, eg, data_type
from ProblemaLineara.ASP_back import Simplex

from math import comb
from fractions import Fraction
from typing import Dict, Union

class Joc:
    def solve(self, data_type, with_table:bool = False, **problem):
        """
        problem = {
            "MatriceQ":     np.array([[a_11, a_12, ... , a_1n], 
                                      [a_21, a_22, ... , a_2n], 
                                      
                                      ...
                                      
                                      [a_m1, a_m2, ... , a_mn]], dtype=data_type), 
        }
        """

        self.MatriceQ    = problem["Matrice"].astype(data_type)

        self.alpha          = [min(linie) for linie in self.MatriceQ]
        self.beta           = [max(coloana) for coloana in self.MatriceQ.T]
        self.v1, self.v2    = max(self.alpha), min(self.beta)

        if self.v1 == self.v2: 
            self.v = self.v1
            self.X_optim = np.zeros(self.MatriceQ.shape[0])
            self.X_optim [np.where(self.alpha == self.v1)] = 1

            self.Y_optim = np.zeros(self.MatriceQ.shape[1])
            self.Y_optim [np.where(self.beta == self.v2)] = 1

            return {"sol" : {"v"      : self.v1, 
                             "X_optim": self.X_optim, 
                             "Y_optim": self.Y_optim},
                    "msg" : {"A" : f"Primul jucător câștigă {self.v1} unități dacă aplică...",
                             "B" : f"Al doilea jucător pierde {self.v1} unități dacă aplică...",}
                    }
        else:
            assert self.v1 < self.v2,               'v1 trebuie sa fie mai mic decat v2'
            assert self.v1 >= 0 and self.v2 <= 0,   'v1, v2 trebuie sa fie pozitivi'

            Problema_liniara_b = {
                "OPT"        : MAX,
                "coef"       : np.ones(self.MatriceQ.shape[1]),
                "MatriceA"  : self.MatriceQ,
                "inegalitate": np.ones(self.MatriceQ.shape[0]),
                "b"          : np.ones(self.MatriceQ.shape[0])
            }

            solver      = Simplex()
            solution    = solver.solve(data_type, with_table, **Problema_liniara_b)
            assert type(solution) == Dict[str, Dict[str, Union[float, str]]], solution

            self.FG_max = solver.Z            
            self.v      = 1/np.float64(self.FG_max)
            assert self.v >= self.v1 and self.v >= self.v2, 'v trebuie sa fie in intervalul [v1, v2]'

            X_A          = solver.Delta[Problema_liniara_b["coef"].shape[0]:]
            self.X_optim = self.v * X_A

            n_vars       = Problema_liniara_b["coef"].shape[0]
            Y_B          = Y_B = np.array([info['valoare'] for info in list(solution.values())[:n_vars]])
            self.Y_optim = self.v * Y_B


    def verify(self):
        
        result = [False, False, False]
        
        # Verificarea 1
        if np.all(self.X_optim >= 0) and np.all(self.Y_optim >= 0):
            result[0] = True
        
        # Verificarea 2
        if np.sum(self.X_optim) == 1 and np.sum(self.Y_optim) == 1:
            result[1] = True
        
        #Verificarea 3
        prod1 = np.dot(self.X_optim, self.MatriceQ)
        prod2 = np.dot(prod1, self.Y_optim)
        if prod2 == self.v:
            result[2] = True
        
        return result