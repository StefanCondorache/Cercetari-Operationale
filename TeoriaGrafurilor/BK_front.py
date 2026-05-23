# Copyright (c) 2026. All rights reserved.
import sys
import re
import math
from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QSpinBox, QGroupBox, 
                               QScrollArea, QMessageBox, QTextEdit, QGraphicsScene, 
                               QGraphicsView, QLineEdit) # <-- CORECTAT: QLineEdit este importat corect acum
from PySide6.QtGui import QFont, QPen, QBrush, QColor, QPainter, QPolygonF
from PySide6.QtCore import Qt, QPointF, QRectF

# Importăm motorul de calcul din backend
from TeoriaGrafurilor.BK_back import BellmanKalaba

# Stilizare globală pentru o estetică profesională uniformă
STYLESHEET = """
QWidget {
    font-size: 14px;
    background-color: #f8f9fa;
}
QGroupBox {
    font-weight: bold;
    border: 1px solid #ababab;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 15px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
QPushButton {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px 15px;
    font-weight: bold;
    color: #34495e;
}
QPushButton:hover {
    background-color: #eaf2f8;
    border-color: #3498db;
}
QPushButton:pressed {
    background-color: #d6eaf8;
}
QTableWidget {
    background-color: #ffffff;
    gridline-color: #d0d0d0;
}
QHeaderView::section {
    background-color: #f0f0f0;
    padding: 5px;
    border: 1px solid #d0d0d0;
    font-weight: bold;
}
"""

# ==============================================================================
# FEREASTRA DE VIZUALIZARE (OUTPUT / EXECUȚIE)
# ==============================================================================
class BellmanKalabaView(QMainWindow):
    def __init__(self, date_intrare, sursa, destinatie):
        super().__init__()
        self.setWindowTitle("Bellman-Kalaba - Soluție Matriceală și Graf")
        self.resize(1300, 850)
        self.setStyleSheet(STYLESHEET)

        self.sursa = sursa
        self.destinatie = destinatie
        
        self.backend = BellmanKalaba()
        self.rezultat = self.backend.solve(date_intrare, sursa, destinatie)
        
        self.noduri = self.rezultat["noduri"]
        self.iteratii = self.rezultat["tabel_iteratii"]
        
        self.pas_curent = -1
        self.pozitii_noduri = {}
        
        self._init_ui()
        self._calculeaza_layout_graf()
        self._deseneaza_graf(evidentiaza_drum=False)

    def _init_ui(self):
        widget_central = QWidget()
        layout_principal = QHBoxLayout(widget_central)

        self.scena = QGraphicsScene()
        self.view = QGraphicsView(self.scena)
        self.view.setRenderHint(QPainter.Antialiasing)
        layout_principal.addWidget(self.view, stretch=3)

        panou_control = QVBoxLayout()
        
        self.lbl_status = QLabel("Stare: Pregătit.\nApasă 'Următorul Pas' pentru a începe.")
        self.lbl_status.setFont(QFont("Arial", 11, QFont.Bold))
        self.lbl_status.setStyleSheet("color: #2c3e50;")
        panou_control.addWidget(self.lbl_status)

        layout_butoane = QHBoxLayout()
        self.btn_inapoi = QPushButton("Pas Înapoi")
        self.btn_inapoi.clicked.connect(self.pas_inapoi)
        layout_butoane.addWidget(self.btn_inapoi)

        self.btn_urmatorul = QPushButton("Următorul Pas")
        self.btn_urmatorul.clicked.connect(self.pas_urmator)
        layout_butoane.addWidget(self.btn_urmatorul)
        panou_control.addLayout(layout_butoane)

        self.btn_reset = QPushButton("Resetează")
        self.btn_reset.clicked.connect(self.reseteaza)
        panou_control.addWidget(self.btn_reset)

        panou_control.addWidget(QLabel("Tabel de Calcul (Iterații):"))
        self.consola = QTextEdit()
        self.consola.setReadOnly(True)
        self.consola.setFont(QFont("Courier New", 11))
        self.consola.setStyleSheet("background-color: #ffffff; border: 1px solid #bdc3c7;")
        panou_control.addWidget(self.consola)

        layout_principal.addLayout(panou_control, stretch=1)
        self.setCentralWidget(widget_central)

    def _calculeaza_layout_graf(self):
        n = len(self.noduri)
        raza_X, raza_Y = 350, 280
        centru_X, centru_Y = 450, 380
        for i, nod in enumerate(self.noduri):
            unghi = 2 * math.pi * i / n
            x = centru_X + raza_X * math.cos(unghi)
            y = centru_Y + raza_Y * math.sin(unghi)
            self.pozitii_noduri[nod] = QPointF(x, y)

    def _deseneaza_graf(self, evidentiaza_drum=False):
        self.scena.clear()
        raza_nod = 22
        matrice = self.rezultat["matrice_initiala"]
        nod_to_idx = {nod: idx for idx, nod in enumerate(self.noduri)}
        
        muchii_drum = set()
        if evidentiaza_drum and self.rezultat["validare_succes"]:
            drum = self.rezultat["drum_optim"]
            for idx in range(len(drum) - 1):
                muchii_drum.add((drum[idx], drum[idx+1]))

        for u in self.noduri:
            for v in self.noduri:
                idx_u, idx_v = nod_to_idx[u], nod_to_idx[v]
                cost = matrice[idx_u][idx_v]
                if idx_u == idx_v or cost == float('inf'): continue
                
                p1, p2 = self.pozitii_noduri[u], self.pozitii_noduri[v]
                este_arc_optim = (u, v) in muchii_drum
                
                culoare = QColor(46, 204, 113) if este_arc_optim else QColor(149, 165, 166)
                grosime = 4 if este_arc_optim else 1.5
                pen = QPen(culoare, grosime)
                
                dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
                dist = math.hypot(dx, dy)
                if dist == 0: continue
                
                p1_ajustor = QPointF(p1.x() + (raza_nod * dx / dist), p1.y() + (raza_nod * dy / dist))
                p2_ajustor = QPointF(p2.x() - (raza_nod * dx / dist), p2.y() - (raza_nod * dy / dist))
                
                self.scena.addLine(p1_ajustor.x(), p1_ajustor.y(), p2_ajustor.x(), p2_ajustor.y(), pen)
                
                unghi = math.atan2(dy, dx)
                dim_sageata = 12
                p_sag1 = QPointF(p2_ajustor.x() - dim_sageata * math.cos(unghi - math.pi / 6), p2_ajustor.y() - dim_sageata * math.sin(unghi - math.pi / 6))
                p_sag2 = QPointF(p2_ajustor.x() - dim_sageata * math.cos(unghi + math.pi / 6), p2_ajustor.y() - dim_sageata * math.sin(unghi + math.pi / 6))
                self.scena.addPolygon(QPolygonF([p2_ajustor, p_sag1, p_sag2]), pen, QBrush(culoare))
                
                mid_x = (p1.x() + p2.x()) / 2 + 8 * math.sin(unghi)
                mid_y = (p1.y() + p2.y()) / 2 - 8 * math.cos(unghi)
                text_cost = self.scena.addText(str(cost), QFont("Arial", 10, QFont.Bold))
                text_cost.setDefaultTextColor(QColor(192, 57, 43) if este_arc_optim else QColor(44, 62, 80))
                text_cost.setPos(mid_x - 10, mid_y - 10)

        for nod, pos in self.pozitii_noduri.items():
            rect = QRectF(pos.x() - raza_nod, pos.y() - raza_nod, raza_nod * 2, raza_nod * 2)
            culoare_fond = QColor(235, 245, 251)
            if nod == self.sursa: culoare_fond = QColor(169, 223, 191)
            elif nod == self.destinatie: culoare_fond = QColor(245, 183, 177)
            
            self.scena.addEllipse(rect, QPen(QColor(44, 62, 80), 2), QBrush(culoare_fond))
            t_item = self.scena.addText(nod, QFont("Arial", 10, QFont.Bold))
            t_rect = t_item.boundingRect()
            t_item.setPos(pos.x() - t_rect.width() / 2, pos.y() - t_rect.height() / 2)

    def pas_urmator(self):
        if self.pas_curent < len(self.iteratii) - 1:
            self.pas_curent += 1
            it = self.iteratii[self.pas_curent]
            
            self.consola.append(f"\n[ Pasul k = {it['k']} ]")
            m_formatat = [str(x) if x != float('inf') else "∞" for x in it["m"]]
            self.consola.append(f" m^({it['k']}) : " + " ".join([f"{x:>4}" for x in m_formatat]))
            
            if it["succ"] is not None:
                self.consola.append(f" succ^({it['k']}): " + " ".join([f"{str(x):>4}" for x in it["succ"]]))
            
            if self.pas_curent == len(self.iteratii) - 1:
                self.lbl_status.setText("Stare: STABILIZARE COMPLETĂ.")
                self.consola.append("\n" + "="*35)
                self.consola.append(f" d_it (Distanțe Finale):")
                self.consola.append(" " + " ".join([f"{self.noduri[i]}:{val}" for i, val in enumerate(self.rezultat['d_it'])]))
                self.consola.append("="*35)
                
                if self.rezultat["validare_succes"]:
                    drum_str = " -> ".join(self.rezultat["drum_optim"])
                    self.consola.append(f" Drum Minim: {drum_str}")
                    self.consola.append(f" Cost Grafic Sumă == Cost Tabel: {self.rezultat['cost_total']}")
                    self.consola.append(f" Validare Structură: [CORECTĂ]")
                    self.lbl_status.setText(f"Soluție Optimă Găsită!\nCost de la {self.sursa} la {self.destinatie}: {self.rezultat['cost_total']}")
                    self._deseneaza_graf(evidentiaza_drum=True)
                else:
                    self.consola.append(" Drum Inaccesibil / Validare Eșuată.")
            else:
                self.lbl_status.setText(f"Iterația k = {it['k']} calculată.")
                
    def pas_inapoi(self):
        if self.pas_curent >= 0:
            self.consola.clear()
            self._deseneaza_graf(evidentiaza_drum=False)
            self.lbl_status.setText("Stare: Resetat.")
            pași_tinta = self.pas_curent - 1
            self.pas_curent = -1
            for _ in range(pași_tinta + 1):
                self.pas_urmator()

    def reseteaza(self):
        self.pas_curent = -1
        self.consola.clear()
        self._deseneaza_graf(evidentiaza_drum=False)
        self.lbl_status.setText("Stare: Resetat.")


# ==============================================================================
# ECRANUL DE CONFIGURARE (INPUT WINDOW)
# ==============================================================================
class BKConfigWindow(QWidget):
    def __init__(self, parent_launcher=None):
        super().__init__()
        self.launcher = parent_launcher
        self.setWindowTitle("Configurare Algoritm Bellman-Kalaba")
        self.resize(700, 550)
        self.setStyleSheet(STYLESHEET)
        
        main_layout = QVBoxLayout(self)
        
        group_dims = QGroupBox("1. Definire Dimensiune Matrice (Noduri)")
        dims_layout = QHBoxLayout(group_dims)
        dims_layout.addWidget(QLabel("Număr Noduri N:"))
        self.spin_n = QSpinBox()
        self.spin_n.setValue(4)
        dims_layout.addWidget(self.spin_n)
        
        btn_gen = QPushButton("Generează Matrice Costuri")
        btn_gen.clicked.connect(self.generate_matrix_table)
        dims_layout.addWidget(btn_gen)
        dims_layout.addStretch()
        main_layout.addWidget(group_dims)
        
        self.group_matrix = QGroupBox("2. Completare Matrice de Costuri C (introduceți numere sau 'inf')")
        self.group_matrix.setHidden(True)
        matrix_layout = QVBoxLayout(self.group_matrix)
        
        self.table_c = QTableWidget()
        self.table_c.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.table_c)
        matrix_layout.addWidget(scroll)
        
        sd_layout = QHBoxLayout()
        self.txt_sursa = QLineEdit("x1")
        self.txt_destinatie = QLineEdit("x4")
        sd_layout.addWidget(QLabel("Nod de Start (xs):"))
        sd_layout.addWidget(self.txt_sursa)
        sd_layout.addWidget(QLabel("Nod Destinație (xN):"))
        sd_layout.addWidget(self.txt_destinatie)
        matrix_layout.addLayout(sd_layout)
        main_layout.addWidget(self.group_matrix)
        
        action_layout = QHBoxLayout()
        btn_back = QPushButton("Înapoi la Meniu")
        btn_back.clicked.connect(self.back_to_menu)
        action_layout.addWidget(btn_back)
        action_layout.addStretch()
        
        self.btn_run = QPushButton("Lansează Rezolvarea")
        self.btn_run.setMinimumWidth(200)
        self.btn_run.setHidden(True)
        self.btn_run.clicked.connect(self.parse_and_run)
        action_layout.addWidget(self.btn_run)
        main_layout.addLayout(action_layout)

    def generate_matrix_table(self):
        n = self.spin_n.value()
        self.table_c.setRowCount(n)
        self.table_c.setColumnCount(n)
        
        etichete = [f"x{i+1}" for i in range(n)]
        self.table_c.setVerticalHeaderLabels(etichete)
        self.table_c.setHorizontalHeaderLabels(etichete)
        
        for i in range(n):
            for j in range(n):
                valoare_implicita = "0" if i == j else "inf"
                item = QTableWidgetItem(valoare_implicita)
                item.setTextAlignment(Qt.AlignCenter)
                if i == j:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    item.setBackground(QColor(240, 240, 240))
                self.table_c.setItem(i, j, item)
                
        self.txt_sursa.setText("x1")
        self.txt_destinatie.setText(f"x{n}")
        self.group_matrix.setHidden(False)
        self.btn_run.setHidden(False)

    def parse_and_run(self):
        try:
            n = self.table_c.rowCount()
            etichete_noduri = [f"x{i+1}" for i in range(n)]
            sursa = self.txt_sursa.text().strip()
            destinatie = self.txt_destinatie.text().strip()
            
            if sursa not in etichete_noduri: raise ValueError(f"Nodul de start '{sursa}' nu există.")
            if destinatie not in etichete_noduri: raise ValueError(f"Nodul destinație '{destinatie}' nu există.")
            if sursa == destinatie: raise ValueError("Nodurile nu pot fi identice.")

            date_intrare = {}
            id_arc = 1
            for i in range(n):
                for j in range(n):
                    if i == j: continue
                    item = self.table_c.item(i, j)
                    if not item: continue
                    text_val = item.text().strip().lower()
                    if text_val in ["inf", "∞", ""]: continue
                    if not text_val.isdigit(): raise ValueError(f"Valoare invalidă la ({i+1},{j+1}).")
                    
                    date_intrare[f"a{id_arc}"] = {"node": (f"x{i+1}", f"x{j+1}"), "value": int(text_val)}
                    id_arc += 1

            self.view = BellmanKalabaView(date_intrare, sursa, destinatie)
            self.view.show()
            self.close()
            if self.launcher: self.launcher.close()

        except ValueError as e:
            QMessageBox.warning(self, "Eroare Validare", str(e))

    def back_to_menu(self):
        if self.launcher: self.launcher.show()
        self.close()

# ==============================================================================
# BLOCUL DE PORNIRE DIRECTĂ (PENTRU TEST INDEPENDENT)
# ==============================================================================
if __name__ == "__main__":
    # Rulând acest fișier direct, blocul de mai jos asigură că instanța QApplication pornește motorul Qt
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    config_window = BKConfigWindow()
    config_window.show()
    
    sys.exit(app.exec())