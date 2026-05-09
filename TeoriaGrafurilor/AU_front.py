import sys
from PySide6.QtWidgets import (QMainWindow, QGraphicsScene, QGraphicsView, 
                               QVBoxLayout, QHBoxLayout, QWidget, 
                               QPushButton, QLabel, QTextEdit, QApplication)
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QPainter
from PySide6.QtCore import Qt, QPointF

from TeoriaGrafurilor.AU_back import HungarianAlgorithm

class HungarianView(QMainWindow):
    def __init__(self, matrice):
        super().__init__()
        self.setWindowTitle("Algoritmul Ungar - Vizualizare Afectare")
        self.resize(1200, 800)

        self.matrice_initiala = matrice
        self.backend = HungarianAlgorithm()
        self.rezultat = self.backend.solve(matrice)
        self.iteratii = self.rezultat['iteratii']
        
        self.pas_curent = -1
        self._init_ui()
        self._deseneaza_graf(None, False)

    def _init_ui(self):
        widget_central = QWidget()
        layout_principal = QHBoxLayout(widget_central)

        self.scena = QGraphicsScene()
        self.view = QGraphicsView(self.scena)
        self.view.setRenderHint(QPainter.Antialiasing)
        layout_principal.addWidget(self.view, stretch=3)

        panou_control = QVBoxLayout()
        
        self.lbl_status = QLabel("Stare: Pregatit.\nApasati 'Urmatorul Pas'.")
        self.lbl_status.setFont(QFont("Arial", 11, QFont.Bold))
        panou_control.addWidget(self.lbl_status)

        self.btn_urmatorul = QPushButton("Urmatorul Pas")
        self.btn_urmatorul.clicked.connect(self.pas_urmator)
        panou_control.addWidget(self.btn_urmatorul)

        self.btn_inapoi = QPushButton("Pas Inapoi")
        self.btn_inapoi.clicked.connect(self.pas_inapoi)
        panou_control.addWidget(self.btn_inapoi)

        self.btn_reset = QPushButton("Reseteaza")
        self.btn_reset.clicked.connect(self.reseteaza)
        panou_control.addWidget(self.btn_reset)

        self.consola = QTextEdit()
        self.consola.setReadOnly(True)
        self.consola.setFont(QFont("Courier New", 10))
        panou_control.addWidget(self.consola)

        layout_principal.addLayout(panou_control, stretch=1)
        self.setCentralWidget(widget_central)

    def _deseneaza_graf(self, muchii_incadrate, optimal):
        self.scena.clear()
        n = len(self.matrice_initiala)
        raza = 20
        distanta_y = 100
        start_y = 100
        x_stanga = 200
        x_dreapta = 600

        if muchii_incadrate:
            for r, c in muchii_incadrate:
                p1 = QPointF(x_stanga, start_y + r * distanta_y)
                p2 = QPointF(x_dreapta, start_y + c * distanta_y)
                culoare = QColor(0, 180, 0) if optimal else QColor(0, 100, 255)
                grosime = 4 if optimal else 2
                pen = QPen(culoare, grosime)
                self.scena.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
                
                cost = self.matrice_initiala[r][c]
                mid_x = (p1.x() + p2.x()) / 2
                mid_y = (p1.y() + p2.y()) / 2
                text_cost = self.scena.addText(str(cost), QFont("Arial", 11, QFont.Bold))
                text_cost.setPos(mid_x, mid_y - 20)

        for i in range(n):
            # L-uri
            ys = start_y + i * distanta_y
            self.scena.addEllipse(x_stanga - raza, ys - raza, raza * 2, raza * 2, QPen(Qt.black), QBrush(QColor(200, 220, 255)))
            t1 = self.scena.addText(f"L{i}", QFont("Arial", 10, QFont.Bold))
            t1.setPos(x_stanga - raza - 40, ys - 12)
            # R-uri
            yd = start_y + i * distanta_y
            self.scena.addEllipse(x_dreapta - raza, yd - raza, raza * 2, raza * 2, QPen(Qt.black), QBrush(QColor(255, 200, 200)))
            t2 = self.scena.addText(f"R{i}", QFont("Arial", 10, QFont.Bold))
            t2.setPos(x_dreapta + raza + 10, yd - 12)

    def pas_urmator(self):
        if self.pas_curent < len(self.iteratii) - 1:
            self.pas_curent += 1
            it = self.iteratii[self.pas_curent]
            self._update_ui(it)

    def pas_inapoi(self):
        if self.pas_curent > 0:
            self.pas_curent -= 1
            self._update_ui(self.iteratii[self.pas_curent])
        elif self.pas_curent == 0:
            self.reseteaza()

    def _update_ui(self, it):
        n = len(self.matrice_initiala)
        self.consola.append(f"\n--- Iterația {it['iteratie']} ---")
        
        # Afișarea matricei în consolă (codul existent)
        for i in range(n):
            row = []
            stea_linie = "*" if "linii_marcate" in it and i in it["linii_marcate"] else " "
            for j in range(n):
                val = it['matrice'][i][j]
                if (i, j) in it['incadrate']: row.append(f"[{val:2}]")
                elif (i, j) in it['taiate']: row.append(f" {val:2}x")
                else: row.append(f" {val:2} ")
            self.consola.append(f"{stea_linie}  " + "  ".join(row))
        
        if "coloane_marcate" in it:
            stele_col = ["   * " if j in it["coloane_marcate"] else "     " for j in range(n)]
            self.consola.append("   " + "".join(stele_col))
        
        # --- SECȚIUNEA NOUĂ: AFIȘARE REZULTATE FINALE ---
        if it['optimal']:
            self.lbl_status.setText(f"SOLUȚIE OPTIMĂ GĂSITĂ!\nCost Minim: {self.rezultat['cost_minim']}")
            self._deseneaza_graf(it['incadrate'], True)

            self.consola.append("\n" + "="*30)
            self.consola.append("       REZULTATE FINALE       ")
            self.consola.append("="*30)
            
            # 1. Cuplajul maxim (Wmax) formatat frumos (ex: L1-R2, L2-R1...)
            # Sortăm după linii pentru o citire mai ușoară
            cuplaj_ordonat = sorted(self.rezultat['w_max'])
            cuplaj_str = ", ".join([f"L{r+1}-R{c+1}" for r, c in cuplaj_ordonat])
            self.consola.append(f"Cuplaj Maxim (Arce): {cuplaj_str}")
            
            # 2. Valoarea minimă a cuplajului
            self.consola.append(f"Cost Minim Afectare: {self.rezultat['cost_minim']}")
            
            # 3. Rezultatul verificării
            verificare_val = self.rezultat['verificare']
            este_corect = "CORECT" if self.rezultat['cost_minim'] == verificare_val else "NECORESPUNZĂTOR"
            self.consola.append(f"Verificare: {verificare_val} -> [{este_corect}]")
            self.consola.append("="*30)
        else:
            self.lbl_status.setText(f"Iterația {it['iteratie']}\nZero-uri încadrate: {it['n0']} / {n}")
            self._deseneaza_graf(it['incadrate'], False)

    def reseteaza(self):
        self.pas_curent = -1
        self.consola.clear()
        self.lbl_status.setText("Stare: Resetat.")
        self._deseneaza_graf(None, False)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = [[58, 29, 88, 77, 68, 68], 
         [38, 92, 16, 66, 26, 19], 
         [33, 16, 95, 91, 14, 31], 
         [64, 88, 13, 98, 57, 27], 
         [94, 93, 88, 61, 59, 27], 
         [68, 77, 46, 21, 88, 31]]
    w = HungarianView(m)
    w.show()
    sys.exit(app.exec())