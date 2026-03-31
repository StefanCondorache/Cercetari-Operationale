import numpy as np

MIN = 1
MAX = -1

MM = 0 # exp >= b  SAU  x >= 0
mm = 1 # exp <= b  SAU  x <= 0
eg = 2 # exp = b   SAU  x apartine R

data_type = np.float64

problems = {
    "problema1" : {
        "OPT":          MAX,                                            
        "coef":         np.array([4, 3, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 3, 2], 
                                  [4, 2, 2], 
                                  [1, 1, 3]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([12, 15, 12], dtype=data_type)
    },
    
    "problema2" : {
        "OPT":          MAX,                                            
        "coef":         np.array([4, 1, 2], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 3], 
                                  [1, 1, 1], 
                                  [2, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([12, 10, 8], dtype=data_type)
    },

    "problema3" : {
        "OPT":          MAX,                                            
        "coef":         np.array([1, -3], dtype=data_type),
        "MatriceA":     np.array([[1, 1], 
                                  [2, -1]], dtype=data_type), 
        "inegalitate":  np.array([MM, mm], dtype=int),     
        "b":            np.array([-1, 2], dtype=data_type)
    },

    "problema4" : {
        "OPT":          MIN,                                            
        "coef":         np.array([1, 1, -1], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 1], 
                                  [-2, 0, 3], 
                                  [0, 1, -3]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, eg], dtype=int),     
        "b":            np.array([1, -2, 5], dtype=data_type)
    },

    "problema5" : {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 2, 3], dtype=data_type),
        "MatriceA":     np.array([[2, 3, 2], 
                                  [3, 2, 1], 
                                  [2, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([15, 15, 15], dtype=data_type)
    },
    
    "problema6" : {
        "OPT":          MIN,                                            
        "coef":         np.array([1, 3, -2], dtype=data_type),
        "MatriceA":     np.array([[1, 1, 1], 
                                  [1, 2, 3], 
                                  [-1, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([eg, mm, MM], dtype=int),     
        "b":            np.array([2, 5, 1], dtype=data_type)
    },

    "problema7" : {
        "OPT":          MIN,                                            
        "coef":         np.array([3, -2, 7], dtype=data_type),
        "MatriceA":     np.array([[1, 3, -1], 
                                  [2, 2, 2], 
                                  [3, 2, -1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, MM], dtype=int),     
        "b":            np.array([3, 2, 4], dtype=data_type)
    },

    "problema_4x4_max_1" : {
        "OPT":          MAX,                                            
        "coef":         np.array([5, 4, 3, 6], dtype=data_type),
        "MatriceA":     np.array([[2, 3, 1, 2], 
                                  [1, 2, 2, 1], 
                                  [3, 1, 1, 2], 
                                  [1, 1, 3, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm, mm], dtype=int),     
        "b":            np.array([20, 15, 18, 14], dtype=data_type)
    },

    "problema_4x4_max_2" : {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 2, 5, 4], dtype=data_type),
        "MatriceA":     np.array([[1, 1, 1, 1], 
                                  [2, 1, 0, 1], 
                                  [0, 1, 2, 1], 
                                  [1, 0, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, MM, eg, mm], dtype=int),     
        "b":            np.array([10, 5, 8, 12], dtype=data_type)
    },

    "problema_4x4_min_1" : {
        "OPT":          MIN,                                            
        "coef":         np.array([8, 6, 4, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 1, 3], 
                                  [2, 1, 1, 1], 
                                  [1, 1, 2, 1], 
                                  [3, 1, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([MM, MM, MM, MM], dtype=int),     
        "b":            np.array([15, 12, 10, 18], dtype=data_type)
    },

    "problema_4x4_min_2" : {
        "OPT":          MIN,                                            
        "coef":         np.array([2, 3, 1, 4], dtype=data_type),
        "MatriceA":     np.array([[1, 1, 2, 1], 
                                  [1, -1, 1, 0], 
                                  [0, 2, 1, 3], 
                                  [2, 1, 0, 1]], dtype=data_type), 
        "inegalitate":  np.array([eg, mm, MM, mm], dtype=int),     
        "b":            np.array([8, 2, 6, 10], dtype=data_type)
    },
    "problema_5x5_max_1" : {
        "OPT":          MAX,                                            
        "coef":         np.array([10, 8, 6, 7, 9], dtype=data_type),
        "MatriceA":     np.array([[2, 1, 1, 3, 1], 
                                  [1, 2, 3, 1, 2], 
                                  [3, 1, 2, 1, 1], 
                                  [1, 1, 1, 2, 3], 
                                  [2, 3, 1, 1, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm, mm, mm], dtype=int),     
        "b":            np.array([30, 40, 35, 25, 30], dtype=data_type)
    },

    "problema_5x5_max_2" : {
        "OPT":          MAX,                                            
        "coef":         np.array([5, 4, 6, 3, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 1, 1, 1, 1], 
                                  [2, 0, 1, 2, 1], 
                                  [1, 2, 0, 1, 1], 
                                  [0, 1, 2, 1, 0], 
                                  [1, 1, 0, 0, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, eg, MM, mm, MM], dtype=int),     
        "b":            np.array([20, 15, 12, 10, 8], dtype=data_type)
    },

    "problema_5x5_min_1" : {
        "OPT":          MIN,                                            
        "coef":         np.array([12, 15, 10, 11, 14], dtype=data_type),
        "MatriceA":     np.array([[3, 2, 1, 1, 2], 
                                  [1, 3, 2, 1, 1], 
                                  [2, 1, 3, 2, 1], 
                                  [1, 1, 1, 3, 2], 
                                  [2, 2, 1, 1, 3]], dtype=data_type), 
        "inegalitate":  np.array([MM, MM, MM, MM, MM], dtype=int),     
        "b":            np.array([50, 45, 60, 40, 55], dtype=data_type)
    },

    "problema_5x5_min_2" : {
        "OPT":          MIN,                                            
        "coef":         np.array([3, -2, 4, 1, 5], dtype=data_type),
        "MatriceA":     np.array([[1, -1, 2, 1, 0], 
                                  [0, 1, 1, -1, 2], 
                                  [2, 0, 1, 1, 1], 
                                  [1, 1, 0, 2, 1], 
                                  [1, 2, 1, 0, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, MM, eg, mm, MM], dtype=int),     
        "b":            np.array([10, 5, 12, 15, 8], dtype=data_type)
    },

    # 1. Standard 2 variables, 3 constraints (Maximization)
    "problema_2x3_standard" : {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 0], 
                                  [0, 2], 
                                  [3, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([4, 12, 18], dtype=data_type)
    },

    # 2. 3 variables, 3 constraints with mixed inequalities (Minimization)
    "problema_3x3_min_mix" : {
        "OPT":          MIN,                                            
        "coef":         np.array([2, 3, 4], dtype=data_type),
        "MatriceA":     np.array([[3, 2, 1], 
                                  [2, 5, 3], 
                                  [1, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([MM, MM, mm], dtype=int),     
        "b":            np.array([10, 15, 20], dtype=data_type)
    },

    # 3. 4 variables, 4 constraints (Maximization)
    "problema_4x4_max" : {
        "OPT":          MAX,                                            
        "coef":         np.array([10, 20, 15, 12], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 2, 1], 
                                  [2, 1, 3, 2], 
                                  [3, 3, 1, 1],
                                  [1, 1, 1, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm, mm], dtype=int),     
        "b":            np.array([40, 50, 60, 20], dtype=data_type)
    },

    # 4. 4 variables, 3 constraints featuring an equality (Minimization)
    "problema_4x3_min_eq" : {
        "OPT":          MIN,                                            
        "coef":         np.array([5, 2, 6, 1], dtype=data_type),
        "MatriceA":     np.array([[2, 1, 3, 4], 
                                  [1, -1, 2, 1], 
                                  [3, 2, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([MM, mm, eg], dtype=int),     
        "b":            np.array([20, 10, 15], dtype=data_type)
    },

    # 5. 5 variables, 2 constraints (Maximization)
    "problema_5x2_wide" : {
        "OPT":          MAX,                                            
        "coef":         np.array([2, 4, 1, 3, 2], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 1, 1, 3], 
                                  [2, 1, 3, 1, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([30, 40], dtype=data_type)
    },

    # 6. EDGE CASE: Unbounded Solution (Z tinde la infinit)
    "problema_nemarginita" : {
        "OPT":          MAX,                                            
        "coef":         np.array([2, 1], dtype=data_type),
        "MatriceA":     np.array([[1, -1], 
                                  [-2, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([10, 20], dtype=data_type)
    },

    # 7. EDGE CASE: Infeasible Solution (Sistem incompatibil / No feasible region)
    "problema_incompatibila" : {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 2], dtype=data_type),
        "MatriceA":     np.array([[1, 1], 
                                  [1, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, MM], dtype=int),     
        "b":            np.array([5, 10], dtype=data_type)
    },
    # 8. 3 variables, 4 constraints (Maximization) - Classic production mix problem
    "problema_3x4_max" : {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 2, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 1], 
                                  [3, 0, 2], 
                                  [1, 4, 0],
                                  [0, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm, mm], dtype=int),     
        "b":            np.array([430, 460, 420, 400], dtype=data_type)
    },

    # 9. 2 variables, 4 constraints (Minimization) - Heavy mix of all 3 constraint types
    "problema_2x4_min_toate_semnele" : {
        "OPT":          MIN,                                            
        "coef":         np.array([4, 5], dtype=data_type),
        "MatriceA":     np.array([[2, 1], 
                                  [1, 2], 
                                  [1, 1],
                                  [1, 0]], dtype=data_type), 
        "inegalitate":  np.array([MM, mm, eg, MM], dtype=int),     
        "b":            np.array([80, 60, 50, 10], dtype=data_type)
    },

    # 10. 4 variables, 2 constraints (Minimization) - Classic diet/blending problem
    "problema_4x2_min_MM" : {
        "OPT":          MIN,                                            
        "coef":         np.array([8, 6, 7, 5], dtype=data_type),
        "MatriceA":     np.array([[4, 2, 3, 1], 
                                  [1, 5, 2, 3]], dtype=data_type), 
        "inegalitate":  np.array([MM, MM], dtype=int),     
        "b":            np.array([120, 150], dtype=data_type)
    },

    # 11. 3 variables, 3 constraints (Maximization) - Equality and Greater-than combo
    "problema_3x3_max_mix" : {
        "OPT":          MAX,                                            
        "coef":         np.array([5, 3, 4], dtype=data_type),
        "MatriceA":     np.array([[2, 1, 1], 
                                  [1, 1, 2], 
                                  [1, 0, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, MM, eg], dtype=int),     
        "b":            np.array([20, 15, 10], dtype=data_type)
    },

    # 12. EDGE CASE: Degeneracy (Tie in the ratio test)
    "problema_degenerata" : {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 9], dtype=data_type),
        "MatriceA":     np.array([[1, 4], 
                                  [1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([8, 4], dtype=data_type)
    },

    # 13. EDGE CASE: Alternative/Multiple Optimal Solutions
    "problema_solutii_multiple" : {
        "OPT":          MAX,                                            
        "coef":         np.array([2, 4], dtype=data_type),
        "MatriceA":     np.array([[1, 2], 
                                  [1, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([5, 4], dtype=data_type)
    },

    # 14. 6 variables, 3 constraints (Maximization) - Wider matrix stress test
    "problema_6x3_max_wide" : {
        "OPT":          MAX,                                            
        "coef":         np.array([10, 12, 15, 8, 6, 9], dtype=data_type),
        "MatriceA":     np.array([[2, 1, 3, 1, 2, 1], 
                                  [1, 3, 2, 2, 1, 2], 
                                  [3, 2, 1, 1, 2, 3]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([100, 120, 150], dtype=data_type)
    },
    # 15. TIE IN DELTAS (Different coefficients, but Deltas tie after a pivot)
    "problema_delta_egale" : {
        "OPT":          MAX,                                            
        "coef":         np.array([5, 3, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 3], 
                                  [2, 1, 1], 
                                  [1, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([15, 12, 10], dtype=data_type)
    },

    # 16. EQUAL COEFFICIENTS (All decision variables have the same profit)
    "problema_coef_egali" : {
        "OPT":          MAX,                                            
        "coef":         np.array([4, 4, 4], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 1], 
                                  [2, 1, 3]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([8, 10], dtype=data_type)
    },

    # 17. THE "DOUBLE TIE" (Equal Coefficients + Equal constraints)
    "problema_dubla_egalitate" : {
        "OPT":          MAX,                                            
        "coef":         np.array([6, 6], dtype=data_type),
        "MatriceA":     np.array([[2, 1], 
                                  [1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([8, 8], dtype=data_type)
    },

    # 18. MINIMIZATION TIE (Equal coefficients triggering equal negative Deltas)
    "problema_delta_egale_min" : {
        "OPT":          MIN,                                            
        "coef":         np.array([2, 2, 3], dtype=data_type),
        "MatriceA":     np.array([[1, 2, 1], 
                                  [2, 1, 2]], dtype=data_type), 
        "inegalitate":  np.array([MM, MM], dtype=int),     
        "b":            np.array([10, 10], dtype=data_type)
    },

    # 19. UNRESTRICTED VARIABLE (Variabilă liberă de semn)
    "problema_variabila_libera" : {
        "OPT":          MAX,                                            
        "coef":         np.array([2, 1, -1], dtype=data_type),
        "MatriceA":     np.array([[1, 1, -1]], dtype=data_type), 
        "inegalitate":  np.array([mm], dtype=int),     
        "b":            np.array([5], dtype=data_type)
    },

    # 20. BIG-M SWAMPING (Instabilitate Numerică)
    "problema_big_m_swamping" : {
        "OPT":          MAX,                                            
        "coef":         np.array([2000000, 3000000], dtype=data_type),
        "MatriceA":     np.array([[1, 1],
                                  [2, 1]], dtype=data_type), 
        "inegalitate":  np.array([MM, mm], dtype=int),     
        "b":            np.array([10, 20], dtype=data_type)
    },

    # 21. REDUNDANT EQUALITY CONSTRAINTS (Restricții Redundante)
    "problema_egalitati_redundante" : {
        "OPT":          MIN,                                            
        "coef":         np.array([3, 2], dtype=data_type),
        "MatriceA":     np.array([[1, 1], 
                                  [2, 2]], dtype=data_type), 
        "inegalitate":  np.array([eg, eg], dtype=int),     
        "b":            np.array([5, 10], dtype=data_type)
    },

    # 22. DEGENERACY AT THE ORIGIN (b_i = 0)
    "problema_b_zero" : {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 0], 
                                  [0, 2], 
                                  [3, -2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([4, 12, 0], dtype=data_type)
    },

    "problema_fabrica_de_lana" : {
        "OPT":          MAX,                                            
        "coef":         np.array([15, 20, 18], dtype=data_type),
        "MatriceA":     np.array([[2, 3, 2], 
                                  [1, 1, 1.5], 
                                  [0, 1, 0],
                                  [1, 0, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, MM, eg], dtype=int),     
        "b":            np.array([120, 80, 10, 30], dtype=data_type)
    },

    "problema_fabrica_lana_complexa" : {
        "OPT":          MAX,                                            
        "coef":         np.array([30, 45, 15, 25], dtype=data_type),
        "MatriceA":     np.array([[10, 20, 5, 12], 
                                  [3,  3,  1,  1], 
                                  [0,  2,  0,  1],
                                  [1,  1,  0,  0],
                                  [0,  1,  0, -1],
                                  [1,  1,  0,  0]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm, MM, eg, mm], dtype=int),     
        "b":            np.array([2000, 400, 100, 30, 0, 100], dtype=data_type)
    },

    "problema_corporatia_globaltex_10x10" : {
        "OPT":          MAX,                                            
        "coef":         np.array([20, 35, 50, 80, 100, 250, 70, 90, 120, 200], dtype=data_type),
        "MatriceA":     np.array([
            # x1   x2   x3   x4   x5   x6   x7   x8   x9  x10
            [0.5, 0.8, 1.0, 1.5, 1.2, 2.0, 1.5, 2.0, 2.5, 4.0],  # 1. Croitorie
            [1.0, 1.5, 2.0, 2.5, 2.0, 3.0, 2.5, 3.5, 4.0, 6.0],  # 2. Cusut
            [0.2, 0.5, 0.5, 1.0, 0.8, 1.5, 1.0, 1.5, 1.5, 2.5],  # 3. Control Calitate
            [1.5, 2.0, 2.5, 0.0, 0.0, 0.0, 3.0, 0.0, 1.0, 2.0],  # 4. Bumbac
            [0.0, 0.0, 0.0, 2.5, 2.0, 3.0, 0.0, 2.5, 0.0, 1.0],  # 5. Materiale Premium
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 4.0],  # 6. Sintetic/Fâș
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],  # 7. Export Geci Iarnă (>=)
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,-2.0, 0.0, 0.0],  # 8. Colecție Blugi=Stofă (=)
            [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 9. Campanie Tricouri (>=)
            [0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]   # 10. Logistică VIP (<=)
        ], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm, mm, mm, mm, MM, eg, MM, mm], dtype=int),     
        "b":            np.array([5000, 8000, 3000, 10000, 2000, 4000, 200, 0, 1000, 500], dtype=data_type)
    },

    "problema_ciclu_beale": {
    "OPT":         MAX,
    "coef":        np.array([-2, 150, -1/50, 6], dtype=data_type),
    "MatriceA":    np.array([
        [ 0.25,  -8,   -1,    9],
        [ 0.5,  -12,  -0.5,  12],
        [ 0,      0,   1,     0]
    ], dtype=data_type),
    "inegalitate": np.array([mm, mm, mm], dtype=int),
    "b":           np.array([0, 0, 1], dtype=data_type)
    },

    "problema_ciclu_bland": {
    "OPT":         MAX,
    "coef":        np.array([10, -57, -9, -24], dtype=data_type),
    "MatriceA":    np.array([
        [ 0.5,  -5.5,  -2.5,   9],
        [ 0.5,  -1.5,  -0.5,   1],
        [ 1,     0,     0,     0]
    ], dtype=data_type),
    "inegalitate": np.array([mm, mm, mm], dtype=int),
    "b":           np.array([0, 0, 1], dtype=data_type)
    },

    "problema_ciclu_minimal_2x4": {
        "OPT":         MAX,
        "coef":        np.array([1, -2, 1, -2], dtype=data_type),
        "MatriceA":    np.array([
            [ 0.5, -3.5, -2.0,  4.0],
            [ 0.5, -1.0, -0.5,  0.5],
            [ 1.0,  0.0,  0.0,  0.0]
        ], dtype=data_type),
        "inegalitate": np.array([mm, mm, mm], dtype=int),
        "b":           np.array([0, 0, 1], dtype=data_type)
    },

    "problema_degenerare_complexa_4x4": {
        "OPT":         MAX,
        "coef":        np.array([10, -4, 5, -6], dtype=data_type),
        "MatriceA":    np.array([
            [ 1.0, -1.0,  2.0, -1.0],
            [ 2.0, -1.0,  0.0,  1.0],
            [ 0.0,  2.0, -1.0,  2.0],
            [ 1.0,  1.0,  1.0,  1.0]
        ], dtype=data_type),
        "inegalitate": np.array([mm, mm, mm, mm], dtype=int),
        "b":           np.array([0, 0, 0, 10], dtype=data_type)
    },

    "problema_ciclu_marshall": {
        "OPT":         MAX,
        "coef":        np.array([2, -3, 1, -12], dtype=data_type),
        "MatriceA":    np.array([
            [-2.0, -9.0,  1.0,  9.0],
            [ 1/3,  1.0, -1/3, -2.0],
            [ 1.0,  0.0,  0.0,  0.0]
        ], dtype=data_type),
        "inegalitate": np.array([mm, mm, mm], dtype=int),
        "b":           np.array([0, 0, 2], dtype=data_type)
    },
    "problema_toate_semnele" : {
        "OPT":          MAX,                                            
        "coef":         np.array([2, 3, -4], dtype=data_type),
        "MatriceA":     np.array([[1,  2, -1], 
                                  [1, -1,  1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([10, 5], dtype=data_type),
        "x":            np.array([MM, eg, mm], dtype=int) 
    },
    "problema_trading_short" : {
        "OPT":          MAX,                                            
        "coef":         np.array([10, -5], dtype=data_type),
        "MatriceA":     np.array([[1, -1],   # Expunere totala (Long + Short) <= 1000$
                                  [1,  0]], dtype=data_type), # Limita de buget pentru Long <= 800$
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([1000, 800], dtype=data_type),
        "x":            np.array([MM, mm], dtype=int) 
    },

    "p1_standard_max": {
        "OPT":          MAX,                                            
        "coef":         np.array([3, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 0], [0, 2], [3, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm], dtype=int),     
        "b":            np.array([4, 12, 18], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },
    
    "p2_standard_min": {
        "OPT":          MIN,                                            
        "coef":         np.array([2, 3, 4], dtype=data_type),
        "MatriceA":     np.array([[3, 2, 1], [2, 5, 3]], dtype=data_type), 
        "inegalitate":  np.array([MM, MM], dtype=int),     
        "b":            np.array([10, 15], dtype=data_type),
        "x":            np.array([MM, MM, MM], dtype=int)
    },

    "p3_mix_restrictii": {
        "OPT":          MAX,                                            
        "coef":         np.array([5, 3, 4], dtype=data_type),
        "MatriceA":     np.array([[2, 1, 1], [1, 1, 2], [1, 0, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, MM, eg], dtype=int),     
        "b":            np.array([20, 15, 10], dtype=data_type),
        "x":            np.array([MM, MM, MM], dtype=int)
    },

    "p4_faza0_negativ_b": {
        # Testeaza inmultirea ecuatiei cu -1 inainte de algoritm
        "OPT":          MAX,                                            
        "coef":         np.array([1, -3], dtype=data_type),
        "MatriceA":     np.array([[1, 1], [2, -1]], dtype=data_type), 
        "inegalitate":  np.array([MM, mm], dtype=int),     
        "b":            np.array([-1, 2], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },

    "p5_variabila_negativa": {
        # x2 trebuie sa fie <= 0. Optimizarea va forta x2 spre o valoare negativa.
        "OPT":          MAX,                                            
        "coef":         np.array([4, -2], dtype=data_type),
        "MatriceA":     np.array([[1, -1], [2, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([10, 8], dtype=data_type),
        "x":            np.array([MM, mm], dtype=int) 
    },

    "p6_variabila_libera_R": {
        # x1 apartine R. Poate fi atat pozitiv cat si negativ.
        "OPT":          MIN,                                            
        "coef":         np.array([2, 1], dtype=data_type),
        "MatriceA":     np.array([[1, 1], [1, -1]], dtype=data_type), 
        "inegalitate":  np.array([MM, mm], dtype=int),     
        "b":            np.array([5, -2], dtype=data_type),
        "x":            np.array([eg, MM], dtype=int)
    },

    "p7_toate_domeniile_mixate": {
        # x1 >= 0, x2 apartine R, x3 <= 0
        "OPT":          MAX,                                            
        "coef":         np.array([2, 3, -4], dtype=data_type),
        "MatriceA":     np.array([[1,  2, -1], 
                                  [1, -1,  1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([10, 5], dtype=data_type),
        "x":            np.array([MM, eg, mm], dtype=int) 
    },

    "p8_trading_long_short": {
        # x1: Long (MM), x2: Short (mm). Buget long = 800, Expunere totala = 1000
        "OPT":          MAX,                                            
        "coef":         np.array([10, -5], dtype=data_type),
        "MatriceA":     np.array([[1, -1], [1, 0]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([1000, 800], dtype=data_type),
        "x":            np.array([MM, mm], dtype=int) 
    },

    "p9_dieta_nutritionala": {
        # Minimam costul hranei respectand necesarul de vitamine (Toate MM)
        "OPT":          MIN,                                            
        "coef":         np.array([8, 6, 7, 5], dtype=data_type),
        "MatriceA":     np.array([[4, 2, 3, 1], [1, 5, 2, 3]], dtype=data_type), 
        "inegalitate":  np.array([MM, MM], dtype=int),     
        "b":            np.array([120, 150], dtype=data_type),
        "x":            np.array([MM, MM, MM, MM], dtype=int)
    },

    "p10_fabrica_complexa": {
        # Productie MAX cu x3 (materie prima care poate fi si vanduta inapoi in piata -> R)
        "OPT":          MAX,                                            
        "coef":         np.array([15, 20, 5], dtype=data_type),
        "MatriceA":     np.array([[2, 3, 1], [1, 1, 0], [0, 1, -1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, eg], dtype=int),     
        "b":            np.array([120, 80, 10], dtype=data_type),
        "x":            np.array([MM, MM, eg], dtype=int)
    },

    "p11_sistem_incompatibil": {
        # Regiune fezabila vida (x1+x2 <= 5 AND x1+x2 >= 10)
        "OPT":          MAX,                                            
        "coef":         np.array([3, 2], dtype=data_type),
        "MatriceA":     np.array([[1, 1], [1, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, MM], dtype=int),     
        "b":            np.array([5, 10], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },

    "p12_solutie_nemarginita": {
        # Z tinde la infinit.
        "OPT":          MAX,                                            
        "coef":         np.array([2, 1], dtype=data_type),
        "MatriceA":     np.array([[1, -1], [-2, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([10, 20], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },

    "p13_degenerare": {
        # Tie in the ratio test. Algoritmul trebuie sa aleaga corect iesirea.
        "OPT":          MAX,                                            
        "coef":         np.array([3, 9], dtype=data_type),
        "MatriceA":     np.array([[1, 4], [1, 2]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm], dtype=int),     
        "b":            np.array([8, 4], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },
    
    "p14_restrictii_redundante": {
        # Doua inegalitati identice. Baza artificiala trebuie sa stie sa le elimine.
        "OPT":          MIN,                                            
        "coef":         np.array([3, 2], dtype=data_type),
        "MatriceA":     np.array([[1, 1], [2, 2]], dtype=data_type), 
        "inegalitate":  np.array([eg, eg], dtype=int),     
        "b":            np.array([5, 10], dtype=data_type), # Sistem incompatibil ascuns! 1x+1y=5 vs 2x+2y=10 e ok, dar hai sa punem 5 si 10 sa dea bine
        "x":            np.array([MM, MM], dtype=int)
    },

    "p15_beale_cycle_test": {
        # Celebrul exemplu al lui Beale care face Simplex-ul neoptimizat sa cicleze la infinit.
        "OPT":         MAX,
        "coef":        np.array([-2, 150, -1/50, 6], dtype=data_type),
        "MatriceA":    np.array([[ 0.25, -8, -1, 9],
                                 [ 0.5, -12, -0.5, 12],
                                 [ 0, 0, 1, 0]], dtype=data_type),
        "inegalitate": np.array([mm, mm, mm], dtype=int),
        "b":           np.array([0, 0, 1], dtype=data_type),
        "x":           np.array([MM, MM, MM, MM], dtype=int)
    },

    "p16_marshall_cycle": {
        # Un alt exemplu clasic de degenerare extrema
        "OPT":         MAX,
        "coef":        np.array([2, -3, 1, -12], dtype=data_type),
        "MatriceA":    np.array([[-2.0, -9.0,  1.0,  9.0],
                                 [ 1/3,  1.0, -1/3, -2.0],
                                 [ 1.0,  0.0,  0.0,  0.0]], dtype=data_type),
        "inegalitate": np.array([mm, mm, mm], dtype=int),
        "b":           np.array([0, 0, 2], dtype=data_type),
        "x":           np.array([MM, MM, MM, MM], dtype=int)
    },

    "p17_bland_tie_rule": {
        # Egalitate perfecta pe linia Delta.
        "OPT":         MAX,
        "coef":        np.array([5, 3, 5], dtype=data_type),
        "MatriceA":    np.array([[1, 2, 3], [2, 1, 1], [1, 1, 2]], dtype=data_type),
        "inegalitate": np.array([mm, mm, mm], dtype=int),
        "b":           np.array([15, 12, 10], dtype=data_type),
        "x":           np.array([MM, MM, MM], dtype=int)
    },

    "p18_dense_4x4_max": {
        "OPT":          MAX,                                            
        "coef":         np.array([5, 4, 3, 6], dtype=data_type),
        "MatriceA":     np.array([[2, 3, 1, 2], 
                                  [1, 2, 2, 1], 
                                  [3, 1, 1, 2], 
                                  [1, 1, 3, 1]], dtype=data_type), 
        "inegalitate":  np.array([mm, mm, mm, mm], dtype=int),     
        "b":            np.array([20, 15, 18, 14], dtype=data_type),
        "x":            np.array([MM, MM, MM, MM], dtype=int)
    },

    "p19_dense_5x5_min": {
        "OPT":          MIN,                                            
        "coef":         np.array([12, 15, 10, 11, 14], dtype=data_type),
        "MatriceA":     np.array([[3, 2, 1, 1, 2], 
                                  [1, 3, 2, 1, 1], 
                                  [2, 1, 3, 2, 1], 
                                  [1, 1, 1, 3, 2], 
                                  [2, 2, 1, 1, 3]], dtype=data_type), 
        "inegalitate":  np.array([MM, MM, MM, MM, MM], dtype=int),     
        "b":            np.array([50, 45, 60, 40, 55], dtype=data_type),
        "x":            np.array([MM, MM, MM, MM, MM], dtype=int)
    },

    "p20_the_boss_level": {
        # 5 Variabile. Toate tipurile de inegalitati. Toate tipurile de restrictii x. b negativ.
        "OPT":          MAX,                                            
        "coef":         np.array([10, -5, 8, 2, -1], dtype=data_type),
        "MatriceA":     np.array([[ 2, -1,  1,  3,  0], 
                                  [ 1,  2, -1,  0,  1], 
                                  [-1,  0,  2,  1,  2],
                                  [ 0,  1,  1,  1, -1]], dtype=data_type), 
        "inegalitate":  np.array([mm, eg, MM, mm], dtype=int),     
        "b":            np.array([20, 15, -10, 12], dtype=data_type), # -10 va declansa Faza 0
        "x":            np.array([MM, mm, eg, MM, eg], dtype=int)     # Mix complet de domenii
    },

    "problema_extreme_scaling": {
        # Amestecam milioanele cu zecimalele. Testeaza toleranta de 1e-6.
        "OPT":          MAX,
        "coef":         np.array([1000000, 0.00001], dtype=data_type),
        "MatriceA":     np.array([[1.0, 1.0], 
                                  [0.00001, 10000.0]], dtype=data_type),
        "inegalitate":  np.array([mm, mm], dtype=int),
        "b":            np.array([100, 1.0], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },

    "problema_box_constraints": {
        # Optimizam 3 variabile, dar fiecare are un plafon strict.
        # Genereaza multe variabile Slack (y) care vor ingreuna baza.
        "OPT":          MAX,
        "coef":         np.array([10, 15, 20], dtype=data_type),
        "MatriceA":     np.array([[1, 1, 1],   # Restrictie principala
                                  [1, 0, 0],   # x1 <= 15
                                  [0, 1, 0],   # x2 <= 20
                                  [0, 0, 1]], dtype=data_type), # x3 <= 10
        "inegalitate":  np.array([mm, mm, mm, mm], dtype=int),
        "b":            np.array([40, 15, 20, 10], dtype=data_type),
        "x":            np.array([MM, MM, MM], dtype=int)
    },

    "problema_transport_2x2": {
        # 2 Depozite, 2 Magazine. Var: x11, x12, x21, x22. 
        # Matrice formata doar din 1 si 0. Solutia garanteaza numere intregi.
        "OPT":          MIN,
        "coef":         np.array([2, 4, 3, 1], dtype=data_type), # Costuri transport
        "MatriceA":     np.array([[1, 1, 0, 0],   # Capacitate Depozit 1 (<= 30)
                                  [0, 0, 1, 1],   # Capacitate Depozit 2 (<= 40)
                                  [1, 0, 1, 0],   # Cerere Magazin 1 (>= 20)
                                  [0, 1, 0, 1]], dtype=data_type), # Cerere Magazin 2 (>= 50)
        "inegalitate":  np.array([mm, mm, MM, MM], dtype=int),
        "b":            np.array([30, 40, 20, 50], dtype=data_type),
        "x":            np.array([MM, MM, MM, MM], dtype=int)
    },

    "problema_trivial_origin": {
        # Incercam sa maximizam profitul, dar coeficientii aduc pierdere (-).
        # Cel mai bine e sa nu producem nimic. Z optim = 0.
        "OPT":          MAX,
        "coef":         np.array([-5, -2], dtype=data_type),
        "MatriceA":     np.array([[1, 2], 
                                  [3, 1]], dtype=data_type),
        "inegalitate":  np.array([mm, mm], dtype=int),
        "b":            np.array([10, 15], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },

    "problema_zero_rhs": {
        # Tot vectorul de resurse (b) este 0 de la bun inceput.
        "OPT":          MAX,
        "coef":         np.array([3, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 2], 
                                  [2, 1]], dtype=data_type),
        "inegalitate":  np.array([mm, mm], dtype=int),
        "b":            np.array([0, 0], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },

    "problema_dynamic_m_stress": {
        "OPT":          MAX,
        "coef":         np.array([10000000, 5], dtype=data_type),
        "MatriceA":     np.array([[1, 0], 
                                  [0, 1],
                                  [1, 1]], dtype=data_type),
        "inegalitate":  np.array([eg, mm, mm], dtype=int),
        "b":            np.array([5, 10, 12], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },
    "problema_aliaj_metalic": {
        "OPT":          MIN,
        "coef":         np.array([20, 25, 15], dtype=data_type), # Cost per kg
        "MatriceA":     np.array([[1.0, 1.0, 1.0],         # Total masa = 100
                                  [0.1, 0.2, 0.1],         # Impuritati <= 12
                                  [0.3, 0.4, 0.2]], dtype=data_type), # Puritate = 30
        "inegalitate":  np.array([eg, mm, eg], dtype=int),
        "b":            np.array([100, 12, 30], dtype=data_type),
        "x":            np.array([MM, MM, MM], dtype=int)
    },
    "problema_cutii_incompatibile": {
        "OPT":          MAX,
        "coef":         np.array([1, 1], dtype=data_type),
        "MatriceA":     np.array([[1, 1],   # Target: x1 + x2 >= 20
                                  [1, 0],   # Limita: x1 <= 5
                                  [0, 1]], dtype=data_type), # Limita: x2 <= 10
        "inegalitate":  np.array([MM, mm, mm], dtype=int),
        "b":            np.array([20, 5, 10], dtype=data_type),
        "x":            np.array([MM, MM], dtype=int)
    },
    "problema_abyssal_unbounded": {
        # O problema de MAX care pare marginita (<= 10), dar pentru ca x2 este libera (in R),
        # algoritmul isi va da seama ca o poate duce pe x2 catre MINUS infinit
        # pentru a forta Z catre PLUS infinit, respectand inegalitatea.
        "OPT":          MAX,
        "coef":         np.array([5, -2], dtype=data_type), # Profit din x1, si profit din "scaderea" lui x2
        "MatriceA":     np.array([[1, -1]], dtype=data_type), # x1 - x2 <= 10
        "inegalitate":  np.array([mm], dtype=int),
        "b":            np.array([10], dtype=data_type),
        "x":            np.array([MM, eg], dtype=int) # x2 este libera (R)
    },
    "problema_flux_retea_3_noduri": {
        # O problema de conservare a fluxului (Nod 1 -> Nod 2 -> Nod 3).
        # x12 = flux 1->2, x13 = flux 1->3, x23 = flux 2->3.
        # Target: Minimizam costul transportului. Toate ecuatiile sunt egalitati de conservare (=).
        "OPT":          MIN,
        "coef":         np.array([2, 5, 1], dtype=data_type), # Costuri pe muchii
        "MatriceA":     np.array([[ 1,  1,  0],   # Nod 1 (Sursa): Iese 1 unitate
                                  [-1,  0,  1],   # Nod 2 (Tranzit): Ce intra = ce iese (Suma = 0)
                                  [ 0, -1, -1]], dtype=data_type), # Nod 3 (Destinatie): Intra 1 unitate (Suma = -1)
        "inegalitate":  np.array([eg, eg, eg], dtype=int),
        "b":            np.array([1, 0, -1], dtype=data_type), # Observa b negativ care activeaza Faza 0!
        "x":            np.array([MM, MM, MM], dtype=int)
    },

    "problema_cadranul_trei": {
        "OPT":          MIN,
        "coef":         np.array([1, 1], dtype=data_type),
        "MatriceA":     np.array([[1, 1],
                                  [2, 1]], dtype=data_type),
        "inegalitate":  np.array([mm, mm], dtype=int), # <=
        "b":            np.array([-15, -20], dtype=data_type), # Din start Faza 0 le face >= 15 si >= 20
        "x":            np.array([mm, mm], dtype=int) # Ambele <= 0
    },
    "problema_hipercub_3D": {

        "OPT":          MAX,
        "coef":         np.array([1, 1, 1], dtype=data_type),
        "MatriceA":     np.array([[1, 0, 0],
                                  [0, 1, 0],
                                  [0, 0, 1]], dtype=data_type),
        "inegalitate":  np.array([mm, mm, mm], dtype=int),
        "b":            np.array([1, 1, 1], dtype=data_type),
        "x":            np.array([MM, MM, MM], dtype=int)
    },

    "problema_teoria_jocurilor": {
        "OPT":          MAX,
        "coef":         np.array([0, 0, 0, 1], dtype=data_type), # Maximizam doar x4 (valoarea jocului)
        "MatriceA":     np.array([[ 1, -1,  0, -1],  # Strategiile adversarului comparate cu valoarea
                                  [-1,  1,  2, -1],
                                  [ 0, -2,  1, -1],
                                  [ 1,  1,  1,  0]], dtype=data_type), # Suma probabilitatilor trebuie sa fie 1
        "inegalitate":  np.array([MM, MM, MM, eg], dtype=int),
        "b":            np.array([0, 0, 0, 1], dtype=data_type),
        "x":            np.array([MM, MM, MM, eg], dtype=int) # x1,x2,x3 sunt probabilitati (>=0), x4 e valoarea (R)
    }
}

__all__ = ["MIN", "MAX", "mm", "MM", "eg", "data_type", "problems"]