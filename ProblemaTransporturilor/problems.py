# Set extins de probleme standard pentru testarea modulului de Transport
# Contine 35 de probleme impartite pe categorii (Echilibrate, Dezechilibrate, Degenerate, Ciclare)

probleme_test = {
    # ==========================================
    # 1. PROBLEME ORIGINALE
    # ==========================================
    "problema_1_echilibrata": {
        "costuri": [
            [8, 6, 10, 9],
            [9, 12, 13, 7],
            [14, 9, 16, 5]
        ],
        "disponibil": [20, 30, 25],
        "necesitate": [10, 25, 15, 25]
    },
    
    "problema_2_oferta_exces": {
        "costuri": [
            [5, 2, 7],
            [3, 6, 6],
            [6, 1, 2]
        ],
        "disponibil": [50, 60, 40],
        "necesitate": [30, 40, 50]
    },

    "problema_3_cerere_exces": {
        "costuri": [
            [4, 3, 5, 2],
            [6, 5, 4, 7]
        ],
        "disponibil": [15, 25],
        "necesitate": [10, 15, 15, 20]
    },

    "problema_4_degenerata": {
        "costuri": [
            [2, 4, 1, 6],
            [4, 3, 3, 3],
            [1, 2, 5, 2]
        ],
        "disponibil": [10, 20, 30],
        "necesitate": [10, 20, 20, 10]
    },

    # ==========================================
    # 2. PROBLEME ECHILIBRATE (Suma S == Suma D)
    # ==========================================
    "problema_5_echilibrata_3x3": {
        "costuri": [[2, 3, 1], [5, 4, 8], [5, 6, 8]],
        "disponibil": [10, 20, 30],
        "necesitate": [15, 15, 30]
    },
    "problema_6_echilibrata_2x3": {
        "costuri": [[10, 20, 30], [30, 20, 10]],
        "disponibil": [50, 50],
        "necesitate": [30, 30, 40]
    },
    "problema_7_echilibrata_3x2": {
        "costuri": [[4, 5], [6, 3], [2, 8]],
        "disponibil": [40, 40, 20],
        "necesitate": [50, 50]
    },
    "problema_8_echilibrata_2x2": {
        "costuri": [[1, 2], [3, 1]],
        "disponibil": [100, 200],
        "necesitate": [150, 150]
    },
    "problema_9_echilibrata_costuri_mari": {
        "costuri": [[150, 200, 120], [300, 100, 250], [180, 220, 140]],
        "disponibil": [30, 50, 20],
        "necesitate": [40, 30, 30]
    },
    "problema_10_echilibrata_5x5": {
        "costuri": [
            [4, 5, 2, 8, 1],
            [2, 3, 6, 4, 5],
            [7, 1, 3, 5, 2],
            [3, 8, 4, 1, 6],
            [5, 2, 7, 3, 4]
        ],
        "disponibil": [100, 150, 200, 50, 100],
        "necesitate": [120, 80, 150, 100, 150]
    },

    # ==========================================
    # 3. EXCES DE OFERTA (Suma S > Suma D)
    # ==========================================
    "problema_11_oferta_3x3": {
        "costuri": [[2, 5, 3], [4, 1, 6], [3, 7, 2]],
        "disponibil": [100, 100, 100],
        "necesitate": [50, 50, 50]
    },
    "problema_12_oferta_2x4": {
        "costuri": [[8, 4, 5, 2], [3, 6, 7, 1]],
        "disponibil": [80, 80],
        "necesitate": [20, 30, 40, 20]
    },
    "problema_13_oferta_4x3": {
        "costuri": [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 1, 1]],
        "disponibil": [20, 20, 20, 20],
        "necesitate": [10, 10, 10]
    },
    "problema_14_oferta_3x2": {
        "costuri": [[10, 12], [14, 11], [9, 15]],
        "disponibil": [50, 50, 50],
        "necesitate": [60, 60]
    },
    "problema_15_oferta_5x4": {
        "costuri": [
            [2, 4, 1, 6], [4, 3, 3, 3], [1, 2, 5, 2], [5, 1, 2, 4], [3, 3, 1, 2]
        ],
        "disponibil": [20, 20, 20, 20, 20],
        "necesitate": [10, 10, 10, 10]
    },

    # ==========================================
    # 4. EXCES DE CERERE (Suma D > Suma S)
    # ==========================================
    "problema_16_cerere_3x3": {
        "costuri": [[5, 2, 4], [1, 6, 3], [7, 4, 2]],
        "disponibil": [50, 50, 50],
        "necesitate": [100, 100, 100]
    },
    "problema_17_cerere_2x3": {
        "costuri": [[8, 9, 7], [4, 5, 6]],
        "disponibil": [30, 40],
        "necesitate": [40, 40, 40]
    },
    "problema_18_cerere_4x3": {
        "costuri": [[2, 1, 3], [4, 2, 5], [3, 6, 1], [5, 3, 2]],
        "disponibil": [10, 10, 10, 10],
        "necesitate": [20, 20, 20]
    },
    "problema_19_cerere_3x2": {
        "costuri": [[10, 20], [15, 25], [12, 18]],
        "disponibil": [60, 60, 60],
        "necesitate": [100, 100]
    },
    "problema_20_cerere_4x5": {
        "costuri": [
            [1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [2, 3, 1, 5, 4], [3, 1, 4, 2, 5]
        ],
        "disponibil": [10, 10, 10, 10],
        "necesitate": [20, 20, 20, 20, 20]
    },

    # ==========================================
    # 5. PROBLEME PUTERNIC DEGENERATE
    # (Oferta si cererea se anuleaza frecvent simultan)
    # ==========================================
    "problema_21_degenerata_2x2": {
        "costuri": [[2, 3], [4, 1]],
        "disponibil": [100, 100],
        "necesitate": [100, 100]
    },
    "problema_22_degenerata_3x3": {
        "costuri": [[5, 2, 3], [1, 6, 4], [7, 8, 2]],
        "disponibil": [5, 10, 15],
        "necesitate": [5, 10, 15]
    },
    "problema_23_degenerata_4x4": {
        "costuri": [
            [1, 2, 1, 2], [2, 1, 2, 1], [1, 2, 1, 2], [2, 1, 2, 1]
        ],
        "disponibil": [50, 50, 50, 50],
        "necesitate": [50, 50, 50, 50]
    },
    "problema_24_degenerata_3x4": {
        "costuri": [[3, 2, 5, 4], [1, 6, 2, 3], [4, 1, 7, 2]],
        "disponibil": [10, 20, 30],
        "necesitate": [10, 20, 15, 15]
    },
    "problema_25_degenerata_4x3": {
        "costuri": [[2, 4, 1], [3, 2, 5], [6, 1, 2], [4, 3, 3]],
        "disponibil": [15, 15, 20, 10],
        "necesitate": [15, 15, 30]
    },
    "problema_26_degenerata_2x4": {
        "costuri": [[10, 20, 30, 40], [40, 30, 20, 10]],
        "disponibil": [50, 50],
        "necesitate": [25, 25, 25, 25]
    },
    "problema_27_degenerata_4x2": {
        "costuri": [[1, 2], [2, 1], [1, 2], [2, 1]],
        "disponibil": [25, 25, 25, 25],
        "necesitate": [50, 50]
    },
    "problema_28_degenerata_3x3_simetrica": {
        "costuri": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "disponibil": [7, 14, 21],
        "necesitate": [7, 14, 21]
    },
    "problema_29_degenerata_3x3_mari": {
        "costuri": [[15, 25, 35], [45, 55, 65], [75, 85, 95]],
        "disponibil": [100, 200, 300],
        "necesitate": [100, 200, 300]
    },
    "problema_30_degenerata_5x5": {
        "costuri": [
            [2, 4, 6, 8, 10], [1, 3, 5, 7, 9], [10, 8, 6, 4, 2],
            [9, 7, 5, 3, 1], [5, 5, 5, 5, 5]
        ],
        "disponibil": [10, 10, 10, 10, 10],
        "necesitate": [10, 10, 10, 10, 10]
    },

    # ==========================================
    # 6. PROBLEME DE CICLARE (Stress Test Epsilon / Ties)
    # ==========================================
    "problema_31_ciclare_1_triunghiulara": {
        "costuri": [
            [1, 2, 3],
            [3, 1, 2],
            [2, 3, 1]
        ],
        "disponibil": [10, 10, 10],
        "necesitate": [10, 10, 10]
    },
    "problema_32_ciclare_2_zero_cycle": {
        "costuri": [
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [1, 1, 1, 0]
        ],
        "disponibil": [20, 20, 20, 20],
        "necesitate": [20, 20, 20, 20]
    },
    "problema_33_ciclare_3_blocuri": {
        "costuri": [
            [1, 2, 2, 1],
            [2, 1, 1, 2],
            [2, 1, 1, 2],
            [1, 2, 2, 1]
        ],
        "disponibil": [15, 15, 15, 15],
        "necesitate": [15, 15, 15, 15]
    },
    "problema_34_ciclare_4_alternanta": {
        "costuri": [
            [10, 5, 5, 10],
            [5, 10, 10, 5],
            [5, 10, 10, 5],
            [10, 5, 5, 10]
        ],
        "disponibil": [25, 25, 25, 25],
        "necesitate": [25, 25, 25, 25]
    },
    "problema_35_ciclare_5_adanca": {
        "costuri": [
            [1, 2, 3, 4, 5],
            [5, 1, 2, 3, 4],
            [4, 5, 1, 2, 3],
            [3, 4, 5, 1, 2],
            [2, 3, 4, 5, 1]
        ],
        "disponibil": [10, 10, 10, 10, 10],
        "necesitate": [10, 10, 10, 10, 10]
    },
    "Problema_36_ciclare": {
        "costuri": [
            [ 1,  2,  3 ],
            [ 3,  1,  2 ],
            [ 2,  3,  1 ]
        ],
        "disponibil": [10, 10, 10],
        "necesitate": [10, 10, 10]
    },
    "Problema_37_ciclare_6_ties": {
        "costuri": [
            [ 1,  1,  1 ],
            [ 1,  1,  1 ],
            [ 1,  1,  1 ]
        ],
        "disponibil": [10, 10, 10],
        "necesitate": [10, 10, 10]
    }
}