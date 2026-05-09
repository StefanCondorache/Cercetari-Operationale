import sys
import re
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                               QLabel, QLineEdit, QMessageBox, 
                               QHBoxLayout, QSpinBox, QTableWidget, QTableWidgetItem,
                               QHeaderView, QGroupBox, QScrollArea)
from PySide6.QtGui import QFont, QIntValidator
from PySide6.QtCore import Qt

# Importuri folosind structura de pachet TeoriaGrafurilor
try:
    from TeoriaGrafurilor.AFF_front import FlowNetworkView
    from TeoriaGrafurilor.AU_front import HungarianView
except ImportError as e:
    print(f"Eroare la importul modulelor front. Asigurați-vă că fișierele există și importurile interne sunt actualizate: {e}")
    sys.exit(1)

# Stilizare globală similară cu exemplele
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
    border: 1px solid #d0d0d0;
    font-weight: bold;
}
"""

class FFConfigWindow(QWidget):
    """Fereastră profesională pentru configurarea datelor Ford-Fulkerson."""
    def __init__(self, parent_launcher):
        super().__init__()
        self.launcher = parent_launcher
        self.setWindowTitle("Configurare Rețea de Flux (Ford-Fulkerson)")
        self.resize(800, 600)
        self.setStyleSheet(STYLESHEET)
        
        main_layout = QVBoxLayout(self)
        
        # --- Secțiunea 1: Definire Dimensiuni ---
        group_dims = QGroupBox("1. Definire Structură Graf")
        dims_layout = QHBoxLayout(group_dims)
        
        dims_layout.addWidget(QLabel("Număr Noduri (N):"))
        self.spin_nodes = QSpinBox()
        self.spin_nodes.setRange(2, 50)
        self.spin_nodes.setValue(5)
        dims_layout.addWidget(self.spin_nodes)
        
        dims_layout.addWidget(QLabel("Număr Arce (M):"))
        self.spin_edges = QSpinBox()
        self.spin_edges.setRange(1, 200)
        self.spin_edges.setValue(6)
        dims_layout.addWidget(self.spin_edges)
        
        btn_gen_table = QPushButton("Generează Tabel Arce")
        btn_gen_table.clicked.connect(self.generate_table)
        dims_layout.addWidget(btn_gen_table)
        
        main_layout.addWidget(group_dims)
        
        # --- Secțiunea 2: Tabel Introducere Date ---
        self.group_table = QGroupBox("2. Introducere Arce și Capacități")
        self.group_table.setHidden(True) # Ascuns inițial
        table_layout = QVBoxLayout(self.group_table)
        
        self.table_edges = QTableWidget()
        self.table_edges.setColumnCount(3)
        self.table_edges.setHorizontalHeaderLabels(["Nod Sursă", "Nod Destinație", "Capacitate"])
        self.table_edges.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.table_edges)
        
        # Setări Sursă/Destinație Globală
        sd_layout = QHBoxLayout()
        self.txt_source = QLineEdit("x1")
        self.txt_sink = QLineEdit("x5")
        sd_layout.addWidget(QLabel("Nod Sursă Rețea:"))
        sd_layout.addWidget(self.txt_source)
        sd_layout.addWidget(QLabel("Nod Destinație Rețea:"))
        sd_layout.addWidget(self.txt_sink)
        table_layout.addLayout(sd_layout)
        
        main_layout.addWidget(self.group_table)
        
        # --- Secțiunea 3: Acțiuni ---
        action_layout = QHBoxLayout()
        btn_back = QPushButton("Înapoi la Meniu")
        btn_back.clicked.connect(self.back_to_menu)
        action_layout.addWidget(btn_back)
        
        action_layout.addStretch()
        
        self.btn_run = QPushButton("Lansează Vizualizarea")
        self.btn_run.setMinimumWidth(200)
        self.btn_run.setHidden(True)
        self.btn_run.clicked.connect(self.parse_and_run)
        action_layout.addWidget(self.btn_run)
        
        main_layout.addLayout(action_layout)

    def generate_table(self):
        m = self.spin_edges.value()
        n = self.spin_nodes.value()
        self.table_edges.setRowCount(m)
        
        # Setăm validator pentru capacități (doar numere pozitive)
        int_validator = QIntValidator(1, 100000)
        
        for row in range(m):
            # Nod Sursă implicit (ex: x1, x2...)
            u_item = QTableWidgetItem(f"x{min(row + 1, n)}")
            self.table_edges.setItem(row, 0, u_item)
            
            # Nod Destinație implicit
            v_item = QTableWidgetItem(f"x{min(row + 2, n)}")
            self.table_edges.setItem(row, 1, v_item)
            
            # Capacitate implicită 10
            cap_item = QTableWidgetItem("10")
            cap_item.setTextAlignment(Qt.AlignCenter)
            self.table_edges.setItem(row, 2, cap_item)

        # Actualizăm nodul sink implicit în funcție de N
        self.txt_sink.setText(f"x{n}")
        
        self.group_table.setHidden(False)
        self.btn_run.setHidden(False)

    def parse_and_run(self):
        try:
            m = self.table_edges.rowCount()
            date_intrare = {}
            nodes_found = set()
            
            for row in range(m):
                u_item = self.table_edges.item(row, 0)
                v_item = self.table_edges.item(row, 1)
                cap_item = self.table_edges.item(row, 2)
                
                if not u_item or not v_item or not cap_item: raise ValueError(f"Completatți toate celulele la rândul {row+1}")
                
                u = u_item.text().strip()
                v = v_item.text().strip()
                cap_str = cap_item.text().strip()
                
                if not u or not v or not cap_str: raise ValueError(f"Date lipsă la rândul {row+1}")
                if not cap_str.isdigit(): raise ValueError(f"Capacitatea la rândul {row+1} trebuie să fie număr.")
                
                cap = int(cap_str)
                if cap <= 0: raise ValueError(f"Capacitatea la rândul {row+1} trebuie să fie > 0.")
                
                date_intrare[f'c{row+1}'] = {'node': (u, v), 'value': cap}
                nodes_found.add(u)
                nodes_found.add(v)
            
            sursa = self.txt_source.text().strip()
            destinatie = self.txt_sink.text().strip()
            
            # Validări logice
            if sursa not in nodes_found: raise ValueError(f"Nodul sursă '{sursa}' nu există în arcele introduse.")
            if destinatie not in nodes_found: raise ValueError(f"Nodul destinație '{destinatie}' nu există în arcele introduse.")
            if sursa == destinatie: raise ValueError("Sursa nu poate fi egală cu destinația.")

            problema = {
                'date_intrare': date_intrare,
                'sursa': sursa,
                'destinatie': destinatie
            }
            
            self.view = FlowNetworkView(problema)
            self.view.show()
            self.close()
            self.launcher.close()
            
        except ValueError as e:
            QMessageBox.warning(self, "Eroare Validare", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Eroare Critică", f"A apărut o eroare neașteptată: {str(e)}")

    def back_to_menu(self):
        self.launcher.show()
        self.close()


class AUConfigWindow(QWidget):
    """Fereastră profesională pentru introducerea Matricei Algoritmului Ungar."""
    def __init__(self, parent_launcher):
        super().__init__()
        self.launcher = parent_launcher
        self.setWindowTitle("Configurare Algoritm Ungar (Matrice Costuri)")
        self.resize(700, 550)
        self.setStyleSheet(STYLESHEET)
        
        main_layout = QVBoxLayout(self)
        
        # --- Secțiunea 1: Dimensiune ---
        group_dims = QGroupBox("1. Definire Dimensiune Matrice (Păstratică N x N)")
        dims_layout = QHBoxLayout(group_dims)
        dims_layout.addWidget(QLabel("Dimensiune N:"))
        self.spin_n = QSpinBox()
        self.spin_n.setRange(2, 20)
        self.spin_n.setValue(4)
        dims_layout.addWidget(self.spin_n)
        
        btn_gen_matrix = QPushButton("Generează Matrice")
        btn_gen_matrix.clicked.connect(self.generate_matrix)
        dims_layout.addWidget(btn_gen_matrix)
        dims_layout.addStretch()
        
        main_layout.addWidget(group_dims)
        
        # --- Secțiunea 2: Tabel Introducere Costuri ---
        self.group_matrix = QGroupBox("2. Introducere Costuri Afectare")
        self.group_matrix.setHidden(True)
        matrix_layout = QVBoxLayout(self.group_matrix)
        
        self.table_matrix = QTableWidget()
        self.table_matrix.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Permitem scroll dacă e prea mare
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.table_matrix)
        matrix_layout.addWidget(scroll)
        
        main_layout.addWidget(self.group_matrix)
        
        # --- Secțiunea 3: Acțiuni ---
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

    def generate_matrix(self):
        n = self.spin_n.value()
        self.table_matrix.setRowCount(n)
        self.table_matrix.setColumnCount(n)
        
        # Header-e (L1, L2... pentru linii, R1, R2... pentru coloane)
        self.table_matrix.setVerticalHeaderLabels([f"L{i+1}" for i in range(n)])
        self.table_matrix.setHorizontalHeaderLabels([f"R{i+1}" for i in range(n)])
        
        for i in range(n):
            for j in range(n):
                # Inițializare cu 0 sau valori aleatorii
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.table_matrix.setItem(i, j, item)
        
        self.group_matrix.setHidden(False)
        self.btn_run.setHidden(False)

    def parse_and_run(self):
        try:
            n = self.table_matrix.rowCount()
            matrix = []
            for i in range(n):
                row = []
                for j in range(n):
                    item = self.table_matrix.item(i, j)
                    if not item: raise ValueError(f"Celula ({i+1},{j+1}) este goală.")
                    val_str = item.text().strip()
                    if not val_str.isdigit(): raise ValueError(f"Costul la ({i+1},{j+1}) trebuie să fie număr.")
                    row.append(int(val_str))
                matrix.append(row)
            
            # Matricea e garantat pătratică din QTableWidget
            self.view = HungarianView(matrix)
            self.view.show()
            self.close()
            self.launcher.close()
            
        except ValueError as e:
            QMessageBox.warning(self, "Eroare Validare", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Eroare Critică", f"A apărut o eroare neașteptată: {str(e)}")

    def back_to_menu(self):
        self.launcher.show()
        self.close()

class MainLauncher(QWidget):
    """Meniu principal îmbunătățit."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teoria Grafurilor - Selector Algoritm")
        self.setFixedSize(450, 250)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Selectați Problema de Rezolvat")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.btn_ff = QPushButton("1. Ford-Fulkerson (Flux Maxim în Rețea)")
        self.btn_ff.setMinimumHeight(45)
        self.btn_ff.clicked.connect(self.open_ff_config)
        layout.addWidget(self.btn_ff)
        
        self.btn_au = QPushButton("2. Algoritmul Ungar (Problema Afectării)")
        self.btn_au.setMinimumHeight(45)
        self.btn_au.clicked.connect(self.open_au_config)
        layout.addWidget(self.btn_au)
        
        layout.addStretch()
        
        footer = QLabel("Suport pentru input dynamic prin tabele")
        footer.setFont(QFont("Arial", 9))
        footer.setAlignment(Qt.AlignRight)
        layout.addWidget(footer)

    def open_ff_config(self):
        self.config_win = FFConfigWindow(self)
        self.config_win.show()
        self.hide()

    def open_au_config(self):
        self.config_win = AUConfigWindow(self)
        self.config_win.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Stil curat, compatibil cross-platform
    launcher = MainLauncher()
    launcher.show()
    sys.exit(app.exec())