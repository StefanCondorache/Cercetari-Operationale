import sys
import numpy as np
from fractions import Fraction
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QDialog, QTextEdit, QMessageBox,
    QScrollArea
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Importam backend-ul creat de tine
from TeoriaJocurilor.JOC_back import Joc

# ----------------------------
# Fereastra output solutie
# ----------------------------
class OutputWindow(QDialog):
    def __init__(self, sol_dict, verify_dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rezultat Teoria Jocurilor")
        self.resize(650, 550)

        layout = QVBoxLayout()
        text = QTextEdit()
        text.setReadOnly(True)
        
        font = QFont("Courier", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        text.setFont(font)

        # --- Extragere date ---
        msg_A = sol_dict["msg"]["A"]
        msg_B = sol_dict["msg"]["B"]
        tip   = sol_dict["tip_strategie"]
        v     = sol_dict["sol"]["v"]
        X_opt = sol_dict["sol"]["X_optim"]
        Y_opt = sol_dict["sol"]["Y_optim"]

        # --- Formatare Text Solutie ---
        result_text = f"Tip Strategie: {tip.upper()}\n"
        result_text += "-"*60 + "\n"
        result_text += f"Valoarea jocului (v) = {v}\n\n"
        result_text += f"{msg_A}\n{msg_B}\n\n"

        result_text += "Probabilitati Strategii Jucatorul A (X):\n"
        result_text += "[ " + "  ".join([str(x) for x in X_opt]) + " ]\n\n"

        result_text += "Probabilitati Strategii Jucatorul B (Y):\n"
        result_text += "[ " + "  ".join([str(y) for y in Y_opt]) + " ]\n"

        # --- Formatare Text Verificari ---
        result_text += "\n" + "="*60 + "\n\nVerificari Matematice:\n"
        result_text += "-"*60 + "\n"
        
        verify_bools = verify_dict.get("result", [False, False, False])
        test_names = [
            "Verificare 1 (Probabilitati >= 0)",
            "Verificare 2 (Suma probabilitatilor = 1)",
            "Verificare 3 (Valoarea jocului V = X*Q*Y)"
        ]

        for i, status_bool in enumerate(verify_bools):
            status = 'OK' if status_bool else 'FAIL'
            result_text += f"{test_names[i]:<45}: {status}\n"
            
        if "Verificarea1:" in verify_dict:
             result_text += f"\nV1: {verify_dict['Verificarea1:']}\n"
        if "Verificarea2:" in verify_dict:
             result_text += f"V2: {verify_dict['Verificarea2:']}\n"
        if "Verificarea3:" in verify_dict:
             result_text += f"V3: {verify_dict['Verificarea3:']}\n"

        text.setText(result_text)

        close_btn = QPushButton("Inchide")
        close_btn.clicked.connect(self.close)

        layout.addWidget(text)
        layout.addWidget(close_btn)
        self.setLayout(layout)


# ----------------------------
# GUI MAIN
# ----------------------------
class GameUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Teoria Jocurilor - Rezolvitor Matriceal")
        self.main_layout = QVBoxLayout()

        self.matrix_entries = [] # Va stoca un array 2D de QLineEdit
        self.grid_widgets = []   # Pentru curatarea layout-ului

        self.solver = Joc()

        # ---------------------------------------------------------
        # 1. INPUT DIMENSIUNI (Dinamic, cu Stretch)
        # ---------------------------------------------------------
        input_layout = QHBoxLayout()
        
        input_layout.addWidget(QLabel("Strategii Jucatorul A (Linii):"))
        self.rows_input = QLineEdit()
        self.rows_input.setText("3") 
        input_layout.addWidget(self.rows_input)

        input_layout.addWidget(QLabel("Strategii Jucatorul B (Coloane):"))
        self.cols_input = QLineEdit()
        self.cols_input.setText("3") 
        input_layout.addWidget(self.cols_input)

        self.gen_button = QPushButton("Genereaza Matrice")
        self.gen_button.clicked.connect(self.genereaza)
        input_layout.addWidget(self.gen_button)

        # Arcul invizibil care impinge totul spre stanga
        input_layout.addStretch() 
        self.main_layout.addLayout(input_layout)
        
        # ---------------------------------------------------------
        # 2. CONTAINER MATRICE (Russian Doll Layout)
        # ---------------------------------------------------------
        self.form_container = QWidget()
        self.v_layout = QVBoxLayout(self.form_container)
        
        # Layout orizontal pentru a centra stanga-dreapta
        self.h_layout = QHBoxLayout()
        
        # Arc invizibil in stanga (impinge spre dreapta)
        self.h_layout.addStretch()
        
        # Widget-ul interior care tine celulele stranse laolalta
        self.matrix_widget = QWidget()
        self.grid_layout = QGridLayout(self.matrix_widget)
        self.grid_layout.setSpacing(5) 
        
        # Bagam matricea in layout-ul orizontal
        self.h_layout.addWidget(self.matrix_widget)
        
        # Arc invizibil in dreapta (impinge spre stanga)
        self.h_layout.addStretch()
        
        # Acum centram sus-jos cu layout-ul vertical
        self.v_layout.addStretch()          # Arc invizibil sus
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addStretch()          # Arc invizibil jos
        
        # Adaugam scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.form_container)
        
        self.main_layout.addWidget(self.scroll_area)

        # ---------------------------------------------------------
        # 3. BUTON REZOLVARE
        # ---------------------------------------------------------
        self.solve_btn = QPushButton("Rezolva Jocul")
        self.solve_btn.clicked.connect(self.rezolva)
        self.solve_btn.setEnabled(False) 
        self.main_layout.addWidget(self.solve_btn)

        self.setLayout(self.main_layout)
        
        # Fereastra porneste compacta ca un panou de control
        self.resize(550, 150)

    # ----------------------------
    # Generare Matrice Input
    # ----------------------------
    def genereaza(self):
        try:
            m = int(self.rows_input.text())
            n = int(self.cols_input.text())
            if n <= 0 or m <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Eroare Input", "Introduceti numere intregi pozitive pentru dimensiuni.")
            return

        self.clear_form()

        # Etichete coloane (Jucatorul B)
        for j in range(n):
            lbl = QLabel(f"B{j+1}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(lbl, 0, j+1)
            self.grid_widgets.append(lbl)

        # Generare Grid
        for i in range(m):
            # Eticheta linie (Jucatorul A)
            lbl = QLabel(f"A{i+1}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.grid_layout.addWidget(lbl, i+1, 0)
            self.grid_widgets.append(lbl)

            row_entries = []
            for j in range(n):
                entry = QLineEdit()
                entry.setFixedWidth(60) # Aici e ok fix width ca sa fie patratele uniforme
                entry.setText("0")
                self.grid_layout.addWidget(entry, i+1, j+1)
                
                row_entries.append(entry)
                self.grid_widgets.append(entry)
                
            self.matrix_entries.append(row_entries)

        self.solve_btn.setEnabled(True)

        # ---------------------------------------------------------
        # NOU: MARIREA DINAMICA A FERESTREI
        # ---------------------------------------------------------
        # Calculam de cat spatiu are nevoie noua matrice
        # Latime: ~70 pixeli pe coloana + spatiu pentru margini/butoane
        # Inaltime: ~40 pixeli pe linie + spatiu pentru meniul de sus si butonul de jos
        target_width = max(550, n * 70 + 150)
        target_height = max(300, m * 40 + 200)

        # Punem o limita maxima ca sa nu iasa in afara monitorului la o matrice 50x50
        target_width = min(target_width, 1000)
        target_height = min(target_height, 800)

        # Executam redimensionarea
        self.resize(target_width, target_height)

    def clear_form(self):
        self.matrix_entries.clear()
        for widget in self.grid_widgets:
            widget.deleteLater()
        self.grid_widgets.clear()

    # ----------------------------
    # Preluare Date si Rezolvare
    # ----------------------------
    def get_numpy_data(self):
        try:
            m = len(self.matrix_entries)
            n = len(self.matrix_entries[0])
            
            Q_matrix = np.zeros((m, n), dtype=np.float64)
            
            for i in range(m):
                for j in range(n):
                    # Citim string-ul, convertim intai la Fraction pt exactitate (ex: "1/2"), apoi la float pt NumPy
                    val_str = self.matrix_entries[i][j].text()
                    Q_matrix[i, j] = float(Fraction(val_str))
                    
            return Q_matrix
        except ValueError:
            return None

    def rezolva(self):
        Q_matrix = self.get_numpy_data()
        
        if Q_matrix is None:
            QMessageBox.warning(self, "Eroare Input", "Toate celulele matricei trebuie sa contina numere sau fractii valide (ex: 3, -1.5, 1/2).")
            return
    
        try:
            # Apelam backend-ul (Joc.solve)
            sol_dict = self.solver.solve(np.float64, Matrice=Q_matrix, with_table=False)
            
            if sol_dict["status"] != "success":
                QMessageBox.warning(self, "Eroare Algoritm", sol_dict["msg"])
                return
                
            verify_dict = self.solver.verify()
            
            # Deschidem fereastra cu rezultate
            self.output_window = OutputWindow(sol_dict, verify_dict)
            self.output_window.show()
            
        except Exception as e:
            QMessageBox.critical(self, "Eroare Fatala", f"A aparut o eroare neasteptata:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameUI()
    window.show()
    sys.exit(app.exec())