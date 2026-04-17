# Copyright (c) 2026 Condorache Ștefan-Eugen. All rights reserved.
# Licensed under the MIT License.

import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QDialog, QTextEdit, QMessageBox,
    QScrollArea
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from ProblemaTransporturilor.Transport_back import Transport

class OutputWindow(QDialog):
    def __init__(self, result_dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rezultat Problema Transporturilor (MODI)")
        self.resize(750, 650)

        layout = QVBoxLayout()
        text = QTextEdit()
        text.setReadOnly(True)
        
        font = QFont("Courier", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        text.setFont(font)

        # ---------------- FORMAT OUTPUT ----------------
        if result_dict.get("status") == "error":
            text.setText(f"EROARE FATALĂ:\n{result_dict['msg']}")
        else:
            out_str = f"Status: REZOLVAT CU SUCCES\n"
            out_str += f"Echilibrare: {result_dict['echilibrare']}\n"
            out_str += f"Test Degenerare: {result_dict['degenerare']}\n"
            out_str += "-" * 65 + "\n"
            
            out_str += f"Costul Minim Optim (f_MIN) = {result_dict['cost_final']}\n"
            out_str += f"Numar de iteratii: {result_dict['iteratii']}\n\n"

            out_str += "Matricea Finala de Repartitie (X_optim):\n"
            mat = result_dict['solutie_X']
            for row in mat:
                out_str += "[ " + "  ".join([f"{val:8.2f}" for val in row]) + " ]\n"

            out_str += "\n" + "=" * 65 + "\nJurnal Iteratii (Matrici, u, v, Delta):\n" + "=" * 65 + "\n"
            
            for ist in result_dict['istoric']:
                out_str += f"\nITERATIA {ist['iteratie']} | Cost Curent = {ist['cost']}\n"
                out_str += "-" * 35 + "\n"
                out_str += f"Vector u (Multiplicatori Linii)   : {np.round(ist['u'], 2)}\n"
                out_str += f"Vector v (Multiplicatori Coloane) : {np.round(ist['v'], 2)}\n\n"
                
                out_str += "Matricea Delta (Cel mai negativ intra in baza):\n"
                for d_row in ist['Delta']:
                    out_str += "[ " + "  ".join([f"{val:8.2f}" for val in d_row]) + " ]\n"
            
            text.setText(out_str)

        close_btn = QPushButton("Inchide si revino")
        close_btn.clicked.connect(self.close)

        layout.addWidget(text)
        layout.addWidget(close_btn)
        self.setLayout(layout)

class TransportUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problema Transporturilor - Metoda MODI & Nord-Vest")
        self.main_layout = QVBoxLayout()

        self.solver = Transport()
        
        self.matrix_entries = [] 
        self.supply_entries = []
        self.demand_entries = []
        self.grid_widgets = []

        # ------------- 1. INPUT DIMENSIUNI -------------
        input_layout = QHBoxLayout()
        
        input_layout.addWidget(QLabel("Furnizori (Linii):"))
        self.rows_input = QLineEdit("3")
        self.rows_input.setFixedWidth(50)
        input_layout.addWidget(self.rows_input)

        input_layout.addWidget(QLabel("Beneficiari (Coloane):"))
        self.cols_input = QLineEdit("4")
        self.cols_input.setFixedWidth(50)
        input_layout.addWidget(self.cols_input)

        self.gen_button = QPushButton("Genereaza Tabel Costuri")
        self.gen_button.clicked.connect(self.genereaza)
        input_layout.addWidget(self.gen_button)

        input_layout.addStretch() 
        self.main_layout.addLayout(input_layout)
        
        # ------------- 2. MATRICE (Layout Russian Doll) -------------
        self.form_container = QWidget()
        self.v_layout = QVBoxLayout(self.form_container)
        self.h_layout = QHBoxLayout()
        
        self.h_layout.addStretch()
        self.matrix_widget = QWidget()
        self.grid_layout = QGridLayout(self.matrix_widget)
        self.grid_layout.setSpacing(6) 
        
        self.h_layout.addWidget(self.matrix_widget)
        self.h_layout.addStretch()
        
        self.v_layout.addStretch()
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addStretch()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.form_container)
        
        self.main_layout.addWidget(self.scroll_area)

        # ------------- 3. BUTON REZOLVARE -------------
        self.solve_btn = QPushButton("Rezolva Problema / Echilibreaza")
        self.solve_btn.setStyleSheet("font-weight: bold; padding: 10px;")
        self.solve_btn.clicked.connect(self.rezolva)
        self.solve_btn.setEnabled(False) 
        self.main_layout.addWidget(self.solve_btn)

        self.setLayout(self.main_layout)
        self.resize(750, 450)

    def genereaza(self):
        try:
            m = int(self.rows_input.text())
            n = int(self.cols_input.text())
            if m <= 0 or n <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Eroare Input", "Dimensiuni invalide. Introduceti intregi pozitivi.")
            return

        self.clear_form()

        # Header Coloane (Beneficiari)
        for j in range(n):
            lbl = QLabel(f"B{j+1}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(lbl, 0, j+1)
            self.grid_widgets.append(lbl)

        lbl_disp = QLabel("Disponibil (S)")
        lbl_disp.setStyleSheet("font-weight: bold; color: #0055ff;")
        self.grid_layout.addWidget(lbl_disp, 0, n+1)
        self.grid_widgets.append(lbl_disp)

        # Grid Costuri + Disponibil
        for i in range(m):
            lbl = QLabel(f"F{i+1}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.grid_layout.addWidget(lbl, i+1, 0)
            self.grid_widgets.append(lbl)

            row_entries = []
            for j in range(n):
                entry = QLineEdit("0")
                entry.setFixedWidth(55)
                entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.grid_layout.addWidget(entry, i+1, j+1)
                row_entries.append(entry)
                self.grid_widgets.append(entry)
            self.matrix_entries.append(row_entries)

            s_entry = QLineEdit("0")
            s_entry.setFixedWidth(65)
            s_entry.setStyleSheet("background-color: #e6f2ff; font-weight: bold;")
            s_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(s_entry, i+1, n+1)
            self.supply_entries.append(s_entry)
            self.grid_widgets.append(s_entry)

        # Footer (Necesitate)
        lbl_nec = QLabel("Necesitate (D)")
        lbl_nec.setStyleSheet("font-weight: bold; color: #e60000;")
        self.grid_layout.addWidget(lbl_nec, m+1, 0)
        self.grid_widgets.append(lbl_nec)

        for j in range(n):
            d_entry = QLineEdit("0")
            d_entry.setFixedWidth(55)
            d_entry.setStyleSheet("background-color: #ffe6e6; font-weight: bold;")
            d_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(d_entry, m+1, j+1)
            self.demand_entries.append(d_entry)
            self.grid_widgets.append(d_entry)

        self.solve_btn.setEnabled(True)
        
        # Redimensionare dinamică
        target_width = min(1000, n * 65 + 250)
        target_height = min(800, m * 45 + 200)
        self.resize(target_width, target_height)

    def clear_form(self):
        self.matrix_entries.clear()
        self.supply_entries.clear()
        self.demand_entries.clear()
        for widget in self.grid_widgets:
            widget.deleteLater()
        self.grid_widgets.clear()

    def rezolva(self):
        try:
            m = len(self.matrix_entries)
            n = len(self.matrix_entries[0])
            
            C = np.zeros((m, n), dtype=np.float64)
            S = np.zeros(m, dtype=np.float64)
            D = np.zeros(n, dtype=np.float64)

            # Citire din UI
            for i in range(m):
                S[i] = float(self.supply_entries[i].text())
                for j in range(n):
                    C[i, j] = float(self.matrix_entries[i][j].text())
            for j in range(n):
                D[j] = float(self.demand_entries[j].text())

            # Apelare Backend Matematic
            rezultat = self.solver.solve(C, S, D, cu_afisare=False)

            # Lnsare UI Secundar
            self.output_window = OutputWindow(rezultat)
            self.output_window.show()

        except ValueError:
            QMessageBox.warning(self, "Eroare Input", "Tabelul trebuie sa contina strict numere valide (ex: 10, 5.5).")
        except Exception as e:
            QMessageBox.critical(self, "Eroare Internă", f"A apărut o eroare neașteptată:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportUI()
    window.show()
    sys.exit(app.exec())