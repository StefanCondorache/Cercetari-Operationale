# Probleme standard de transport pentru testarea algoritmului MODI
# (Pot fi importate și rulate direct în backend pentru testare rapidă)

probleme_test = {
    # 1. Problema clasică echilibrată (Suma Disponibil = Suma Necesitate)
    "problema_standard_1": {
        "costuri": [
            [2, 2, 2, 1],
            [10, 8, 5, 4],
            [7, 6, 6, 8]
        ],
        "disponibil": [3, 7, 5],
        "necesitate": [4, 3, 4, 4]
    },
    
    # 2. Problema dezechilibrată (Oferta > Cererea) -> Va crea un beneficiar fictiv
    "problema_oferta_exces": {
        "costuri": [
            [4, 8, 8],
            [16, 24, 16],
            [8, 16, 24]
        ],
        "disponibil": [76, 82, 77], # Total = 235
        "necesitate": [72, 102, 41] # Total = 215 (Lipesc 20 cerere)
    },

    # 3. Problema dezechilibrată (Cererea > Oferta) -> Va crea un furnizor fictiv
    "problema_cerere_exces": {
        "costuri": [
            [3, 1, 7, 4],
            [2, 6, 5, 9],
            [8, 3, 3, 2]
        ],
        "disponibil": [300, 400, 500],   # Total = 1200
        "necesitate": [250, 350, 400, 300] # Total = 1300 (Lipesc 100 oferta)
    },

    # 4. Problema degenerată (Zero-uri care trebuiesc menținute în bază)
    "problema_degenerata": {
        "costuri": [
            [10, 20, 5, 7],
            [13, 9, 12, 8],
            [4, 15, 7, 9]
        ],
        "disponibil": [15, 25, 20],
        "necesitate": [15, 10, 15, 20] # Oferta si cererea se anuleaza simultan des
    }
}

if __name__ == "__main__":
    from ProblemaTransporturilor.Transport_back import Transport
    
    solver = Transport()
    for nume, date in probleme_test.items():
        print(f"\n--- Rezolvare: {nume} ---")
        rez = solver.solve(date["costuri"], date["disponibil"], date["necesitate"], cu_afisare=True)