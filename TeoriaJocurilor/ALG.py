import numpy as np
from ProblemaLineara.problems import MAX, data_type
from ProblemaLineara.ASP_back import Simplex
from TeoriaJocurilor.utils import afisare_tabel

from fractions import Fraction

def format_joc_val(val):
    if abs(val) < 1e-9: return "0"
    return str(Fraction(float(val)).limit_denominator(1000))

class Joc:
    def solve(self, data_type, Matrice, with_table:bool = False,):

        self.MatriceQ = Matrice.astype(data_type)

        self.alpha          = [min(linie) for linie in self.MatriceQ]
        self.beta           = [max(coloana) for coloana in self.MatriceQ.T]
        self.v1, self.v2    = max(self.alpha), min(self.beta)

        if with_table: self.afisare()

        if self.v1 == self.v2: 
            self.v = self.v1

            alpha = np.array(self.alpha)
            beta = np.array(self.beta)

            self.X_optim = np.zeros(self.MatriceQ.shape[0])
            self.X_optim[np.where(alpha == self.v1)] = 1

            self.Y_optim = np.zeros(self.MatriceQ.shape[1])
            self.Y_optim[np.where(beta == self.v2)] = 1

            # Normalizare in caz ca exista mai multe puncte sa
            self.X_optim = self.X_optim / np.sum(self.X_optim)
            self.Y_optim = self.Y_optim / np.sum(self.Y_optim)

            return {
                "status": "success",
                "tip_strategie": "pura",
                "sol": {
                    "v"      : self.v, 
                    "X_optim": self.X_optim, 
                    "Y_optim": self.Y_optim
                },
                "msg": {
                    "A": f"Primul jucător câștigă {self.v} unități.",
                    "B": f"Al doilea jucător pierde {self.v} unități."
                }
            }

        else:
            assert self.v1 < self.v2,             'v1 trebuie sa fie mai mic decat v2'
            assert self.v1 >= 0 and self.v2 >= 0, 'v1, v2 trebuie sa fie pozitivi.'

            Problema_liniara_b = {
                "OPT"        : MAX,
                "coef"       : np.ones(self.MatriceQ.shape[1]),
                "MatriceA"   : self.MatriceQ, 
                "inegalitate": np.ones(self.MatriceQ.shape[0]), # 1 = mm (mai mic sau egal)
                "b"          : np.ones(self.MatriceQ.shape[0])
            }

            solver = Simplex()
            solution = solver.solve(data_type, with_table, **Problema_liniara_b)
            
            # Tratare erori algoritm Simplex (ciclare, nemarginit, etc.)
            if isinstance(solution, str):
                return {
                    "status": "other",
                    "msg": f"Simplex output: {solution}"
                }

            self.FG_max = solver.Z            
            self.v      = 1 / np.float64(self.FG_max)
            
            assert self.v >= self.v1 and self.v <= self.v2, f'v ({self.v}) trebuie sa fie in intervalul [{self.v1}, {self.v2}]'

            n_vars = Problema_liniara_b["coef"].shape[0]
            X_A = np.abs(solver.Delta[n_vars:])
            self.X_optim = self.v * X_A

            Y_B = np.array([info['valoare'] for info in list(solution.values())[:n_vars]])
            self.Y_optim = self.v * Y_B

            return {
                "status": "success",
                "tip_strategie": "mixta",
                "sol": {
                    "v"      : self.v, 
                    "X_optim": self.X_optim, 
                    "Y_optim": self.Y_optim
                },
                "msg": {
                    "A": f"Valoarea jocului este {self.v:.4f} unități.",
                    "B": "Ambele părți folosesc strategii mixte."
                }
            }

    def verify(self):
        result = [False, False, False]

        def to_frac_array(arr):
            return np.array([Fraction(float(x)).limit_denominator(1000) for x in arr])

        X_frac = to_frac_array(self.X_optim)
        Y_frac = to_frac_array(self.Y_optim)
        v_frac = Fraction(float(self.v)).limit_denominator(1000)
        
        Q_frac = np.array([[Fraction(float(val)).limit_denominator(1000) for val in row] 
                           for row in self.MatriceQ])

        # Verificarea 1: Probabilitati pozitive
        msg1 = "Toate probabilitatile jucatorilor sunt >= 0."
        if np.all(X_frac >= 0) and np.all(Y_frac >= 0):
            result[0] = True
        else:
            msg1 = f"Eroare: Exista probabilitati negative. X: {X_frac}, Y: {Y_frac}"

        # Verificarea 2: Suma probabilitatilor este 1
        sum_x = np.sum(X_frac)
        sum_y = np.sum(Y_frac)
        msg2 = f"Suma prob. X = {sum_x}, Suma prob. Y = {sum_y} "

        if sum_x == 1 and sum_y == 1:
            result[1] = True
            msg2 += "(Corect.)"
        else:
            msg2 += "(!= 1. Incorect.)"

        # Verificarea 3: Valoarea jocului
        prod1 = np.dot(X_frac, Q_frac)
        prod2 = np.dot(prod1, Y_frac)

        msg3 = f"X_o * Q * Y_o = {prod2} "
        if prod2 == v_frac:
            result[2] = True
            msg3 += f"== v ({v_frac})."
        else:
            msg3 += f"!= v ({v_frac})."

        return {
            "result": result,
            "Verificarea1:": msg1,
            "Verificarea2:": msg2,
            "Verificarea3:": msg3
        }
    
    def afisare(self):
        afisare_tabel(self)

if __name__ == '__main__':

    Matrice = np.array([
            [1, 1, 2],
            [3, 2, 1],
            [2, 4, 5]
        ], dtype=np.float64)

    joc = Joc()
    sol = joc.solve(data_type, Matrice=Matrice, with_table=True)
    ver = joc.verify()
    print(sol, sep='\n')
    print(ver)