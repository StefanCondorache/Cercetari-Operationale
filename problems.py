import numpy as np

MIN = 1
MAX = -1

MM = 0 # exp >= b
mm = 1 # exp <= b
eg = 2 # exp = b

M = np.float64(10**6)
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
    }
}

__all__ = ["MIN", "MAX", "mm", "MM", "eg", "M", "data_type", "problems"]