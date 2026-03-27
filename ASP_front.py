import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDialog, QTextEdit, QMessageBox
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
        self.setWindowTitle("Rezultat Simplex")
        self.resize(600, 550) # Putin mai lata pentru a incapea matricile

        layout = QVBoxLayout()
        text = QTextEdit()
        text.setReadOnly(True)
        
        # Setam un font Monospace pentru ca matricile si textul sa fie perfect aliniate!
        font = QFont("Courier", 10)
        font.setStyleHint(QFont.Monospace)
        text.setFont(font)

        result_text = "Solutia optima:\n\n"

        for var_name, info in solution_detaliata.items():
            result_text += f"{var_name:<4} = {info['valoare']:>8.4f}  |  Tip: {info['tip']:<15}  |  Coef: {info['coef_obiectiv']}\n"

        result_text += "\n" + "="*60 + "\n\nVerificari Matematice:\n"
        
        verify_bools = verify_dict.get("result", [False, False, False])
        
        test_names = [
            "Test 1 (Nenegativitate x >= 0)",
            "Test 2 (Potrivire Functie Obiectiv Z)",
            "Test 3 (Consistenta Algebrica a Bazei)"
        ]

        for i, v in enumerate(verify_bools):
            status = 'OK' if v else 'FAIL'
            result_text += f"{test_names[i]:<40}: {status}\n"
            
        # Afisarea detaliilor pentru Testul 1 si 2
        if "Verificarea1:" in verify_dict:
             result_text += f"\nDetalii T1: {verify_dict['Verificarea1:']}\n"
        if "Verificarea2:" in verify_dict:
             result_text += f"\nDetalii T2: Z = {verify_dict['Verificarea2:']}"

        # ---------------------------------------------------------
        # NOU: Afisarea vizuala a ecuației matriciale pentru Testul 3
        # ---------------------------------------------------------
        if "Verificarea3:" in verify_dict:
            v3 = verify_dict["Verificarea3:"]
            S = v3["S"]                         # Matricea
            xb_final = v3["Baza_I0_stop"]       # Vector coloana
            b_init = v3["Baza_I0"]              # Vector coloana
            
            result_text += "\n\nDetalii T3: S * X_b_final = b_initial (Reconstructia bazei)\n"
            
            n_rows = len(b_init)
            for i in range(n_rows):
                # Formateaza elementele de pe randul 'i' din matricea S
                row_s = " ".join([f"{val:5.2f}" for val in S[i]])
                
                # Punem operatorii de inmultire si egalitate doar la jumatatea inaltimii matricei 
                # pentru a arata estetic ca o ecuatie
                op_mul = " * " if i == n_rows // 2 else "   "
                op_eq  = " = " if i == n_rows // 2 else "   "
                
                # Construim linia: [ S_row ] * [ X_b ] = [ b ]
                result_text += f"[ {row_s} ]{op_mul}[ {xb_final[i]:8.4f} ]{op_eq}[ {b_init[i]:8.4f} ]\n"
        # ---------------------------------------------------------

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

        self.setWindowTitle("Programare liniara - ASP")
        self.layout = QVBoxLayout()

        self.obj_entries = []
        self.constraints = []
        self.constraint_widgets = [] # Keep track of widgets to clear them properly

        self.solver = Simplex()

        # Input pentru variabile și restrictii
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Numar variabile"))
        self.var_input = QLineEdit()
        self.var_input.setFixedWidth(50)
        self.var_input.setText("2") # Default value
        input_layout.addWidget(self.var_input)

        input_layout.addWidget(QLabel("Numar restrictii"))
        self.res_input = QLineEdit()
        self.res_input.setFixedWidth(50)
        self.res_input.setText("2") # Default value
        input_layout.addWidget(self.res_input)

        self.gen_button = QPushButton("Genereaza model")
        self.gen_button.clicked.connect(self.genereaza)
        input_layout.addWidget(self.gen_button)

        self.layout.addLayout(input_layout)

        # MAX/MIN
        opt_layout = QHBoxLayout()
        opt_layout.addWidget(QLabel("Optimizare"))
        self.opt_combo = QComboBox()
        self.opt_combo.addItems(["MAX", "MIN"])
        opt_layout.addWidget(self.opt_combo)
        
        self.solve_btn = QPushButton("Rezolva")
        self.solve_btn.clicked.connect(self.rezolva)
        self.solve_btn.setEnabled(False) # Disable until model is generated
        
        self.layout.addLayout(opt_layout)
        
        # Container for the dynamic form
        self.form_layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.solve_btn)

        self.setLayout(self.layout)


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

        # Sterge campurile vechi
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

        # Conditii nenegativitate
        cond_lbl = QLabel(", ".join([f"x{i+1} ≥ 0" for i in range(n)]))
        self.form_layout.addWidget(cond_lbl)
        self.constraint_widgets.append(cond_lbl)

        self.solve_btn.setEnabled(True)

    def clear_form(self):
        self.obj_entries.clear()
        self.constraints.clear()
        for widget in self.constraint_widgets:
            widget.deleteLater()
        self.constraint_widgets.clear()
        
        # Also need to clear the layouts themselves if possible, but deleteLater on widgets usually suffices for UI cleanup

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
                
            return c, np.array(A, dtype=np.float64), np.array(s, dtype=int), np.array(b, dtype=np.float64)
            
        except ValueError:
            return None, None, None, None


    # ----------------------------
    # Solver + Output
    # ----------------------------
    def rezolva(self):
        
        c, A, s, b = self.get_numpy_data()
        
        if c is None:
            QMessageBox.warning(self, "Eroare Input", "Toate campurile trebuie sa contina numere valide.")
            return
    
        # Determine OPT (-1 for MAX, 1 for MIN based on backend constants)
        opt_str = self.opt_combo.currentText()
        OPT = MAX if opt_str == "MAX" else MIN 
    
        prob = {
            "coef": c,
            "MatriceA": A,
            "b": b,
            "inegalitate": s,
            "OPT": OPT
        }
    
        try:
            # Note the False parameter for with_table is deafult in the backend
            solution_detaliata = self.solver.solve(np.float64, **prob)
            
            # Check if the solver returned an error string (incompatible, unbounded, cycling)
            if isinstance(solution_detaliata, str):
                QMessageBox.warning(self, "Eroare Simplex", solution_detaliata)
                return
                
            verify_dict = self.solver.verify()
            
            # Show output window if solution is valid
            self.output_window = OutputWindow(solution_detaliata, verify_dict)
            self.output_window.show()
            
        except Exception as e:
            QMessageBox.critical(self, "Eroare Fatala", f"A aparut o eroare neasteptata:\n{str(e)}")


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinearUI()
    window.show()
    sys.exit(app.exec())
