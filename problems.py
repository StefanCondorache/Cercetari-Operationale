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
    }
}

__all__ = ["MIN", "MAX", "mm", "MM", "eg", "M", "data_type", "problems"]