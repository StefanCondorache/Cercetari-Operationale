# Copyright (c) 2026 Condorache Ștefan-Eugen. All rights reserved.
# Licensed under the MIT License.

import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDialog, QTextEdit, QMessageBox,
    QScrollArea
)
from PySide6.QtGui import QFont
from ASP_back import Simplex
from problems import mm, MM, eg, MAX, MIN

# ----------------------------
# Fereastra output solutie
# ----------------------------
class OutputWindow(QDialog):
    def __init__(self, solution_detaliata, verify_dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rezultat Simplex Detaliat")
        self.resize(650, 600) 

        layout = QVBoxLayout()
        text = QTextEdit()
        text.setReadOnly(True)
        
        # Setam un font Monospace pentru ca matricile si textul sa fie perfect aliniate!
        font = QFont("Courier", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        text.setFont(font)

        result_text = "Solutia optima detaliata:\n"
        result_text += "-"*60 + "\n"

        # Afisare detaliata si aliniata pentru fiecare variabila
        for var_name, info in solution_detaliata.items():
            result_text += f"Var {var_name:<4} = {info['valoare']:>10.4f}  |  Tip: {info['tip']:<16}  |  Coef. Obj: {info['coef_obiectiv']}\n"

        result_text += "\n" + "="*60 + "\n\nVerificari Matematice:\n"
        result_text += "-"*60 + "\n"
        
        verify_bools = verify_dict.get("result", [False, False, False])
        
        test_names = [
            "Verificare 1 (Pozitivitate)",
            "Verificare 2 (Potrivire Functie Obiectiv)",
            "Verificare 3 (Consistenta Algebrica a Bazei)"
        ]

        for i, v in enumerate(verify_bools):
            status = 'OK' if v else 'FAIL'
            result_text += f"{test_names[i]:<40}: {status}\n"
            
        # Afisarea detaliilor pentru Testul 1 si 2
        if "Verificarea1:" in verify_dict:
             result_text += f"\nV1: {verify_dict['Verificarea1:']}\n"
        if "Verificarea2:" in verify_dict:
             result_text += f"\nV2: Z = {verify_dict['Verificarea2:']}"

        # Afisarea vizuala a ecuației matriciale pentru Testul 3
        if "Verificarea3:" in verify_dict:
            v3 = verify_dict["Verificarea3:"]
            S = v3["S"]                         
            xb_final = v3["Baza_I0_stop"]       
            b_init = v3["Baza_I0"]              
            
            result_text += "\n\nV3: S * X_b_final = b_initial (Reconstructia bazei)\n"
            
            n_rows = len(b_init)
            for i in range(n_rows):
                row_s = " ".join([f"{val:5.2f}" for val in S[i]])
                
                op_mul = " * " if i == n_rows // 2 else "   "
                op_eq  = " = " if i == n_rows // 2 else "   "
                
                result_text += f"[ {row_s} ]{op_mul}[ {xb_final[i]:8.4f} ]{op_eq}[ {b_init[i]:8.4f} ]\n"

        text.setText(result_text)

        close_btn = QPushButton("Inchide")
        close_btn.clicked.connect(self.close)

        layout.addWidget(text)
        layout.addWidget(close_btn)
        self.setLayout(layout)


# ----------------------------
# GUI MAIN
# ----------------------------
class LinearUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Programare liniara - ASP (Suport Domenii Mixte)")
        self.main_layout = QVBoxLayout()

        self.obj_entries = []
        self.constraints = []
        self.constraint_widgets = [] 
        self.var_cond_combos = [] # NOU: pastreaza referintele comboboxurilor pentru domeniul variabilelor

        self.solver = Simplex()

        # Input pentru variabile și restrictii
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Numar variabile"))
        self.var_input = QLineEdit()
        self.var_input.setFixedWidth(50)
        self.var_input.setText("2") 
        input_layout.addWidget(self.var_input)

        input_layout.addWidget(QLabel("Numar restrictii"))
        self.res_input = QLineEdit()
        self.res_input.setFixedWidth(50)
        self.res_input.setText("2") 
        input_layout.addWidget(self.res_input)

        self.gen_button = QPushButton("Genereaza model")
        self.gen_button.clicked.connect(self.genereaza)
        input_layout.addWidget(self.gen_button)

        self.main_layout.addLayout(input_layout)

        # MAX/MIN
        opt_layout = QHBoxLayout()
        opt_layout.addWidget(QLabel("Optimizare"))
        self.opt_combo = QComboBox()
        self.opt_combo.addItems(["MAX", "MIN"])
        opt_layout.addWidget(self.opt_combo)
        
        self.solve_btn = QPushButton("Rezolva")
        self.solve_btn.clicked.connect(self.rezolva)
        self.solve_btn.setEnabled(False) 
        
        self.main_layout.addLayout(opt_layout)
        
        self.form_container = QWidget()
        self.form_layout = QVBoxLayout(self.form_container)
        
        # Creaza zona de scroll si pune containerul in ea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) # Permite redimensionarea automata
        self.scroll_area.setWidget(self.form_container)
        
        # Adauga scroll-ul in layout-ul principal
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.solve_btn)

        self.setLayout(self.main_layout)
        
        # Seteaza o dimensiune de pornire decenta pentru fereastra
        self.resize(700, 500)

    # ----------------------------
    # Campuri input
    # ----------------------------
    def genereaza(self):
        try:
            n = int(self.var_input.text())
            m = int(self.res_input.text())
            if n <= 0 or m <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Eroare Input", "Introduceti numere intregi pozitive pentru variabile si restrictii.")
            return

        self.clear_form()

        # Functia obiectiv
        obj_layout = QHBoxLayout()
        obj_label = QLabel("OPT f(x) = ")
        obj_layout.addWidget(obj_label)
        self.constraint_widgets.append(obj_label)

        for i in range(n):
            entry = QLineEdit()
            entry.setFixedWidth(50)
            entry.setText("0")
            self.obj_entries.append(entry)
            obj_layout.addWidget(entry)
            
            lbl = QLabel(f"x{i+1}")
            obj_layout.addWidget(lbl)
            self.constraint_widgets.append(entry)
            self.constraint_widgets.append(lbl)
            
            if i < n-1:
                plus = QLabel("+")
                obj_layout.addWidget(plus)
                self.constraint_widgets.append(plus)

        self.form_layout.addLayout(obj_layout)

        # Restrictii
        res_label = QLabel("Restricții:")
        self.form_layout.addWidget(res_label)
        self.constraint_widgets.append(res_label)

        for r in range(m):
            line = QHBoxLayout()
            row_entries = []

            for i in range(n):
                entry = QLineEdit()
                entry.setFixedWidth(50)
                entry.setText("0")
                row_entries.append(entry)
                line.addWidget(entry)
                
                lbl = QLabel(f"x{i+1}")
                line.addWidget(lbl)
                
                self.constraint_widgets.append(entry)
                self.constraint_widgets.append(lbl)

                if i < n-1:
                    plus = QLabel("+")
                    line.addWidget(plus)
                    self.constraint_widgets.append(plus)

            combo = QComboBox()
            combo.addItems(["<=", ">=", "="])
            self.constraint_widgets.append(combo)

            rhs = QLineEdit()
            rhs.setFixedWidth(60)
            rhs.setText("0")
            self.constraint_widgets.append(rhs)

            line.addWidget(combo)
            line.addWidget(rhs)

            self.constraints.append((row_entries, combo, rhs))
            self.form_layout.addLayout(line)

        # ---------------------------------------------------------
        # NOU: Domeniul Variabilelor (Permite >=0, <=0, si R)
        # ---------------------------------------------------------
        var_cond_label = QLabel("Domeniul variabilelor de decizie:")
        var_cond_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.form_layout.addWidget(var_cond_label)
        self.constraint_widgets.append(var_cond_label)

        var_cond_layout = QHBoxLayout()
        for i in range(n):
            lbl = QLabel(f"x{i+1}:")
            combo = QComboBox()
            combo.addItems([">= 0", "<= 0", "∈ R"])
            
            self.var_cond_combos.append(combo)
            var_cond_layout.addWidget(lbl)
            var_cond_layout.addWidget(combo)
            
            self.constraint_widgets.append(lbl)
            self.constraint_widgets.append(combo)
            
            # Adaugam un pic de spatiu intre dropdowns daca nu e ultimul element
            if i < n - 1:
                spacer = QLabel("   ")
                var_cond_layout.addWidget(spacer)
                self.constraint_widgets.append(spacer)

        self.form_layout.addLayout(var_cond_layout)
        # ---------------------------------------------------------

        self.solve_btn.setEnabled(True)

    def clear_form(self):
        self.obj_entries.clear()
        self.constraints.clear()
        self.var_cond_combos.clear() # Curatam si listele noi
        for widget in self.constraint_widgets:
            widget.deleteLater()
        self.constraint_widgets.clear()

    # ----------------------------
    # GUI -> Numpy
    # ----------------------------
    def get_numpy_data(self):
        try:
            c = np.array([float(e.text()) for e in self.obj_entries], dtype=np.float64)
            A = []
            b = []
            s = []
    
            sign_map = {"<=": mm, ">=": MM, "=": eg}
    
            for row, combo, rhs in self.constraints:
                coef_row = [float(e.text()) for e in row]
                A.append(coef_row)
                b.append(float(rhs.text()))
                s.append(sign_map[combo.currentText()])
            
            # NOU: Extragem domeniile setate in UI pentru variabile
            var_sign_map = {">= 0": MM, "<= 0": mm, "∈ R": eg}
            x_conds = []
            for combo in self.var_cond_combos:
                x_conds.append(var_sign_map[combo.currentText()])
                
            x_array = np.array(x_conds, dtype=int)
                
            return c, np.array(A, dtype=np.float64), np.array(s, dtype=int), np.array(b, dtype=np.float64), x_array
            
        except ValueError:
            return None, None, None, None, None

    # ----------------------------
    # Solver + Output
    # ----------------------------
    def rezolva(self):
        
        c, A, s, b, x_array = self.get_numpy_data()
        
        if c is None:
            QMessageBox.warning(self, "Eroare Input", "Toate campurile trebuie sa contina numere valide.")
            return
    
        opt_str = self.opt_combo.currentText()
        OPT = MAX if opt_str == "MAX" else MIN 
    
        # NOU: Adaugam x_array in dictionarul problemei trimis spre backend
        prob = {
            "coef": c,
            "MatriceA": A,
            "b": b,
            "inegalitate": s,
            "x": x_array, 
            "OPT": OPT
        }
    
        try:
            solution_detaliata = self.solver.solve(np.float64, **prob)
            
            if isinstance(solution_detaliata, str):
                QMessageBox.warning(self, "Eroare Simplex", solution_detaliata)
                return
                
            verify_dict = self.solver.verify()
            
            self.output_window = OutputWindow(solution_detaliata, verify_dict)
            self.output_window.show()
            
        except Exception as e:
            QMessageBox.critical(self, "Eroare Fatala", f"A aparut o eroare neasteptata:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinearUI()
    window.show()
    sys.exit(app.exec())