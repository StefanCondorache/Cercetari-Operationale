# Copyright (c) 2026. All rights reserved.
import sys
import re
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                               QLabel, QLineEdit, QMessageBox, 
                               QHBoxLayout, QSpinBox, QTableWidget, QTableWidgetItem,
                               QHeaderView, QGroupBox, QScrollArea)
from PySide6.QtGui import QFont, QColor  # CORECTARE: QColor a fost mutat corect în QtGui
from PySide6.QtCore import Qt

# Importuri pachete interne
try:
    from TeoriaGrafurilor.AFF_front import FlowNetworkView
    from TeoriaGrafurilor.AU_front import HungarianView
    from TeoriaGrafurilor.BK_front import BellmanKalabaView
except ImportError as e:
    print(f"Eroare la importul modulelor front: {e}")
    sys.exit(1)

# Stilizare globală uniformă
STYLESHEET = """
QWidget {
    font-size: 14px;
}
QPushButton {
    background-color: #f0f0f0;
    border: 1px solid #ababab;
    border-radius: 4px;
    padding: 5px 15px;
    min-height: 25px;
}
QPushButton:hover {
    background-color: #e0e0e0;
}
QPushButton:pressed {
    background-color: #d0d0d0;
}
QTableWidget {
    gridline-color: #d0d0d0;
}
QHeaderView::section {
    background-color: #f0f0f0;
    padding: 4px;
    border: 1px solid #ababab;
    font-weight: bold;
}
QGroupBox {
    font-weight: bold;
}
"""

class MainLauncher(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Selectați Problema de Rezolvat")
        self.setFixedSize(500, 400)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Sistem de Gestiune Algoritmi pe Grafuri")
        # CORECTARE: În PySide6 se folosește QFont.Weight.Bold pentru setarea stilului gros
        font_titlu = QFont("Arial", 16)
        font_titlu.setWeight(QFont.Weight.Bold)
        title.setFont(font_titlu)
        # CORECTARE: Qt.AlignmentFlag pentru alinierea corectă din punct de vedere static
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.btn_ff = QPushButton("1. Ford-Fulkerson (Flux Maxim în Rețea)")
        self.btn_ff.setMinimumHeight(45)
        self.btn_ff.clicked.connect(self.open_ff_config)
        layout.addWidget(self.btn_ff)
        
        self.btn_au = QPushButton("2. Algoritmul Ungar (Problema Afectării)")
        self.btn_au.setMinimumHeight(45)
        self.btn_au.clicked.connect(self.open_au_config)
        layout.addWidget(self.btn_au)

        self.btn_bk = QPushButton("3. Bellman-Kalaba (Matriceal - Drum Minim)")
        self.btn_bk.setMinimumHeight(45)
        self.btn_bk.clicked.connect(self.open_bk_config)
        layout.addWidget(self.btn_bk)
        
        layout.addStretch()
        
        footer = QLabel("Suport complet pentru configurare dinamică prin tabele")
        footer.setFont(QFont("Arial", 9))
        footer.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(footer)

        self.config_win: QWidget | None = None

    def open_ff_config(self) -> None:
        self.config_win = FFConfigWindow(self)
        self.config_win.show()
        self.hide()

    def open_au_config(self) -> None:
        self.config_win = AUConfigWindow(self)
        self.config_win.show()
        self.hide()

    def open_bk_config(self) -> None:
        self.config_win = BKConfigWindow(self)
        self.config_win.show()
        self.hide()


# ==============================================================================
# CONFIGURARE FORD-FULKERSON
# ==============================================================================
class FFConfigWindow(QWidget):
    def __init__(self, launcher: MainLauncher) -> None:
        super().__init__()
        self.launcher = launcher
        self.setWindowTitle("Configurare Ford-Fulkerson")
        self.resize(650, 500)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout(self)
        
        gb_dim = QGroupBox("1. Dimensiune Rețea")
        ly_dim = QHBoxLayout(gb_dim)
        ly_dim.addWidget(QLabel("Număr de arce (muchii):"))
        self.spin_arce = QSpinBox()
        self.spin_arce.setRange(1, 100)
        self.spin_arce.setValue(5)
        ly_dim.addWidget(self.spin_arce)
        
        btn_gen = QPushButton("Generează Tabel Arce")
        btn_gen.clicked.connect(self.generate_table)
        ly_dim.addWidget(btn_gen)
        layout.addWidget(gb_dim)
        
        self.gb_table = QGroupBox("2. Date Rețea și Capacități")
        self.gb_table.setHidden(True)
        ly_table = QVBoxLayout(self.gb_table)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nod Sursă (u)", "Nod Destinație (v)", "Capacitate"])
        # CORECTARE: QHeaderView.ResizeMode.Stretch
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.table)
        ly_table.addWidget(scroll)
        
        ly_sd = QHBoxLayout()
        ly_sd.addWidget(QLabel("Sursă Globală (xs):"))
        self.txt_sursa = QLineEdit("x1")
        ly_sd.addWidget(self.txt_sursa)
        ly_sd.addWidget(QLabel("Destinație Globală (xt):"))
        self.txt_dest = QLineEdit("x4")
        ly_sd.addWidget(self.txt_dest)
        ly_table.addLayout(ly_sd)
        layout.addWidget(self.gb_table)
        
        ly_actions = QHBoxLayout()
        btn_back = QPushButton("Înapoi")
        btn_back.clicked.connect(self.go_back)
        ly_actions.addWidget(btn_back)
        ly_actions.addStretch()
        self.btn_run = QPushButton("Rulează Algoritmul")
        self.btn_run.setHidden(True)
        self.btn_run.clicked.connect(self.run_algorithm)
        ly_actions.addWidget(self.btn_run)
        layout.addLayout(ly_actions)

    def generate_table(self) -> None:
        n = self.spin_arce.value()
        self.table.setRowCount(n)
        for i in range(n):
            self.table.setItem(i, 0, QTableWidgetItem(f"x{i+1}"))
            self.table.setItem(i, 1, QTableWidgetItem(f"x{i+2}"))
            item_val = QTableWidgetItem("10")
            self.table.setItem(i, 2, item_val)
        self.gb_table.setHidden(False)
        self.btn_run.setHidden(False)

    def run_algorithm(self) -> None:
        try:
            date_intrare = {}
            for i in range(self.table.rowCount()):
                item_u = self.table.item(i, 0)
                item_v = self.table.item(i, 1)
                item_val = self.table.item(i, 2)
                
                # CORECTARE: Verificare de siguranță împotriva valorilor opționale (None)
                if not item_u or not item_v or not item_val:
                    raise ValueError("Toate celulele trebuie completate!")
                    
                u = item_u.text().strip()
                v = item_v.text().strip()
                val_text = item_val.text().strip()
                
                if not u or not v or not val_text:
                    raise ValueError("Toate celulele trebuie completate!")
                val = int(val_text)
                date_intrare[f"c{i+1}"] = {'node': (u, v), 'value': val}
            
            problema = {
                'date_intrare': date_intrare,
                'sursa': self.txt_sursa.text().strip(),
                'destinatie': self.txt_dest.text().strip()
            }
            self.output_win = FlowNetworkView(problema)
            self.output_win.show()
            self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Eroare Validare", str(e))

    def go_back(self) -> None:
        self.launcher.show()
        self.close()


# ==============================================================================
# CONFIGURARE ALGORITMUL UNGAR
# ==============================================================================
class AUConfigWindow(QWidget):
    def __init__(self, launcher: MainLauncher) -> None:
        super().__init__()
        self.launcher = launcher
        self.setWindowTitle("Configurare Algoritmul Ungar")
        self.resize(600, 500)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout(self)
        
        gb_dim = QGroupBox("1. Dimensiune Problemă (Matrice Pătratică)")
        ly_dim = QHBoxLayout(gb_dim)
        ly_dim.addWidget(QLabel("Număr de elemente (N x N):"))
        self.spin_n = QSpinBox()
        self.spin_n.setRange(2, 20)
        self.spin_n.setValue(4)
        ly_dim.addWidget(self.spin_n)
        
        btn_gen = QPushButton("Generează Matrice")
        btn_gen.clicked.connect(self.generate_matrix)
        ly_dim.addWidget(btn_gen)
        layout.addWidget(gb_dim)
        
        self.gb_matrix = QGroupBox("2. Matricea de Costuri")
        self.gb_matrix.setHidden(True)
        ly_matrix = QVBoxLayout(self.gb_matrix)
        
        self.table = QTableWidget()
        # CORECTARE: QHeaderView.ResizeMode.Stretch
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        ly_matrix.addWidget(self.table)
        layout.addWidget(self.gb_matrix)
        
        ly_actions = QHBoxLayout()
        btn_back = QPushButton("Înapoi")
        btn_back.clicked.connect(self.go_back)
        ly_actions.addWidget(btn_back)
        ly_actions.addStretch()
        self.btn_run = QPushButton("Rulează Algoritmul")
        self.btn_run.setHidden(True)
        self.btn_run.clicked.connect(self.run_algorithm)
        ly_actions.addWidget(self.btn_run)
        layout.addLayout(ly_actions)

    def generate_matrix(self) -> None:
        n = self.spin_n.value()
        self.table.setRowCount(n)
        self.table.setColumnCount(n)
        
        labels = [f"Sarcina {i+1}" for i in range(n)]
        self.table.setHorizontalHeaderLabels(labels)
        self.table.setVerticalHeaderLabels([f"Muncitor {i+1}" for i in range(n)])
        
        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem("10")
                # CORECTARE: Qt.AlignmentFlag.AlignCenter
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, j, item)
                
        self.gb_matrix.setHidden(False)
        self.btn_run.setHidden(False)

    def run_algorithm(self) -> None:
        try:
            n = self.table.rowCount()
            matrice = []
            for i in range(n):
                rand = []
                for j in range(n):
                    cell_item = self.table.item(i, j)
                    # CORECTARE: Verificare prezență celulă pentru Pylance optional check
                    if not cell_item:
                        raise ValueError("Toate celulele matricei trebuie completate!")
                    val_text = cell_item.text().strip()
                    if not val_text:
                        raise ValueError("Toate celulele matricei trebuie completate!")
                    rand.append(int(val_text))
                matrice.append(rand)
                
            self.output_win = HungarianView(matrice)
            self.output_win.show()
            self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Eroare Validare", str(e))

    def go_back(self) -> None:
        self.launcher.show()
        self.close()


# ==============================================================================
# CONFIGURARE BELLMAN-KALABA
# ==============================================================================
class BKConfigWindow(QWidget):
    def __init__(self, launcher: MainLauncher) -> None:
        super().__init__()
        self.launcher = launcher
        self.setWindowTitle("Configurare Bellman-Kalaba")
        self.resize(650, 500)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout(self)
        
        gb_dim = QGroupBox("1. Definire Dimensiune Rețea (Număr Noduri)")
        ly_dim = QHBoxLayout(gb_dim)
        ly_dim.addWidget(QLabel("Număr de noduri N:"))
        self.spin_n = QSpinBox()
        self.spin_n.setRange(2, 50)
        self.spin_n.setValue(4)
        ly_dim.addWidget(self.spin_n)
        
        btn_gen = QPushButton("Generează Matrice de Costuri")
        btn_gen.clicked.connect(self.generate_matrix_table)
        ly_dim.addWidget(btn_gen)
        layout.addWidget(gb_dim)
        
        self.gb_matrix = QGroupBox("2. Completare Matrice de Costuri C (introduceți numere sau 'inf')")
        self.gb_matrix.setHidden(True)
        ly_matrix = QVBoxLayout(self.gb_matrix)
        
        self.table_c = QTableWidget()
        # CORECTARE: QHeaderView.ResizeMode.Stretch
        self.table_c.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.table_c)
        ly_matrix.addWidget(scroll)
        
        ly_sd = QHBoxLayout()
        self.txt_sursa = QLineEdit("x1")
        self.txt_dest = QLineEdit("x4")
        ly_sd.addWidget(QLabel("Nod de Start (xs):"))
        ly_sd.addWidget(self.txt_sursa)
        ly_sd.addWidget(QLabel("Nod Destinație (xN):"))
        ly_sd.addWidget(self.txt_dest)
        ly_matrix.addLayout(ly_sd)
        layout.addWidget(self.gb_matrix)
        
        ly_actions = QHBoxLayout()
        btn_back = QPushButton("Înapoi")
        btn_back.clicked.connect(self.go_back)
        ly_actions.addWidget(btn_back)
        ly_actions.addStretch()
        self.btn_run = QPushButton("Rulează Algoritmul")
        self.btn_run.setHidden(True)
        self.btn_run.clicked.connect(self.run_algorithm)
        ly_actions.addWidget(self.btn_run)
        layout.addLayout(ly_actions)

    def generate_matrix_table(self) -> None:
        n = self.spin_n.value()
        self.table_c.setRowCount(n)
        self.table_c.setColumnCount(n)
        
        etichete = [f"x{i+1}" for i in range(n)]
        self.table_c.setVerticalHeaderLabels(etichete)
        self.table_c.setHorizontalHeaderLabels(etichete)
        
        for i in range(n):
            for j in range(n):
                val_implicita = "0" if i == j else "inf"
                item = QTableWidgetItem(val_implicita)
                # CORECTARE: Qt.AlignmentFlag.AlignCenter
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if i == j:
                    # CORECTARE: În PySide6 se folosește direct structura internă fără operatorul ~ pe tip incert
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setBackground(QColor(240, 240, 240))
                self.table_c.setItem(i, j, item)
                
        self.txt_sursa.setText("x1")
        self.txt_dest.setText(f"x{n}")
        self.gb_matrix.setHidden(False)
        self.btn_run.setHidden(False)

    def run_algorithm(self) -> None:
        try:
            n = self.table_c.rowCount()
            etichete_noduri = [f"x{i+1}" for i in range(n)]
            sursa = self.txt_sursa.text().strip()
            destinatie = self.txt_dest.text().strip()
            
            if sursa not in etichete_noduri: raise ValueError(f"Nodul de start '{sursa}' nu există.")
            if destinatie not in etichete_noduri: raise ValueError(f"Nodul destinație '{destinatie}' nu există.")
            if sursa == destinatie: raise ValueError("Nodul de start și destinația nu pot fi identice.")

            date_intrare = {}
            id_arc = 1
            for i in range(n):
                for j in range(n):
                    if i == j: continue
                    item = self.table_c.item(i, j)
                    # CORECTARE: Verificare de tip explicit pentru a asigura eliminarea erorii de Optional
                    if not item: continue
                    text_val = item.text().strip().lower()
                    if text_val in ["inf", "∞", ""]: continue
                    if not text_val.isdigit(): raise ValueError(f"Valoare nepermisă la celula ({i+1},{j+1}).")
                    
                    date_intrare[f"a{id_arc}"] = {"node": (f"x{i+1}", f"x{j+1}"), "value": int(text_val)}
                    id_arc += 1

            self.output_win = BellmanKalabaView(date_intrare, sursa, destinatie)
            self.output_win.show()
            self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Eroare Validare", str(e))

    def go_back(self) -> None:
        self.launcher.show()
        self.close()


# ==============================================================================
# LANSATOR
# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    launcher = MainLauncher()
    launcher.show()
    sys.exit(app.exec())