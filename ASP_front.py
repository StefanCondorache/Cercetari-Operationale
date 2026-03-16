import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDialog, QTextEdit
)
from ASP_back import Simplex


# ----------------------------
# Fereastra output solutie
# ----------------------------
class OutputWindow(QDialog):
    def __init__(self, solution_detaliata, verify_result, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rezultat Simplex")
        self.resize(400, 400)

        layout = QVBoxLayout()
        text = QTextEdit()
        text.setReadOnly(True)

        result_text = "Solutia optima:\n\n"

        for var_name, info in solution_detaliata.items():
            result_text += f"{var_name} ({info['tip']}): {info['valoare']} (coef = {info['coef_obiectiv']})\n"

        result_text += "\nVerificari:\n"
        for i, v in enumerate(verify_result):
            result_text += f"Test {i+1}: {'OK' if v else 'FAIL'}\n"

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

        self.solver = Simplex()

        # Input pentru variabile și restrictii
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Numar variabile"))
        self.var_input = QLineEdit()
        self.var_input.setFixedWidth(50)
        input_layout.addWidget(self.var_input)

        input_layout.addWidget(QLabel("Numar restrictii"))
        self.res_input = QLineEdit()
        self.res_input.setFixedWidth(50)
        input_layout.addWidget(self.res_input)

        self.gen_button = QPushButton("Genereaza model")
        self.gen_button.clicked.connect(self.genereaza)
        input_layout.addWidget(self.gen_button)

        self.layout.addLayout(input_layout)

        self.setLayout(self.layout)

        # MAX/MIN
        opt_layout = QHBoxLayout()
        opt_layout.addWidget(QLabel("Optimizare"))
        self.opt_combo = QComboBox()
        self.opt_combo.addItems(["MAX", "MIN"])
        opt_layout.addWidget(self.opt_combo)
        self.layout.addLayout(opt_layout)

    # ----------------------------
    # Campuri input
    # ----------------------------
    def genereaza(self):
        # Sterge campuri
        for entry in self.obj_entries:
            entry.deleteLater()
        for row_entries, combo, rhs in self.constraints:
            for e in row_entries:
                e.deleteLater()
            combo.deleteLater()
            rhs.deleteLater()
        self.obj_entries.clear()
        self.constraints.clear()

        n = int(self.var_input.text())
        m = int(self.res_input.text())

        # Functia obiectiv
        obj_layout = QHBoxLayout()
        obj_layout.addWidget(QLabel("Z ="))

        for i in range(n):
            entry = QLineEdit()
            entry.setFixedWidth(40)
            self.obj_entries.append(entry)
            obj_layout.addWidget(entry)
            obj_layout.addWidget(QLabel(f"x{i+1}"))
            if i < n-1:
                obj_layout.addWidget(QLabel("+"))

        self.layout.addLayout(obj_layout)

        # Restrictii
        for r in range(m):
            line = QHBoxLayout()
            row_entries = []

            for i in range(n):
                entry = QLineEdit()
                entry.setFixedWidth(40)
                row_entries.append(entry)
                line.addWidget(entry)
                line.addWidget(QLabel(f"x{i+1}"))
                if i < n-1:
                    line.addWidget(QLabel("+"))

            combo = QComboBox()
            combo.addItems(["<=", ">=", "="])

            rhs = QLineEdit()
            rhs.setFixedWidth(60)

            line.addWidget(combo)
            line.addWidget(rhs)

            self.constraints.append((row_entries, combo, rhs))
            self.layout.addLayout(line)

        # Conditii nenegativitate
        cond = ", ".join([f"x{i+1} ≥ 0" for i in range(n)])
        self.layout.addWidget(QLabel(cond))

        solve_btn = QPushButton("Rezolva")
        solve_btn.clicked.connect(self.rezolva)
        self.layout.addWidget(solve_btn)

    # ----------------------------
    # GUI -> Numpy
    # ----------------------------
    def get_numpy_data(self):
        c = np.array([float(e.text()) for e in self.obj_entries])
        A = []
        b = []
        s = []

        from problems import mm, MM, eg

        sign_map = {"<=": mm, ">=": MM, "=": eg}

        for row, combo, rhs in self.constraints:
            coef_row = [float(e.text()) for e in row]
            A.append(coef_row)
            b.append(float(rhs.text()))
            s.append(sign_map[combo.currentText()])

        return np.array(c), np.array(A), np.array(s), np.array(b)

    # ----------------------------
    # Solver + Output
    # ----------------------------
    def rezolva(self):
        
        c, A, s, b = self.get_numpy_data()
    
        # Determine OPT
        opt_str = self.opt_combo.currentText()
        OPT = -1 if opt_str == "MAX" else 1  # matches Simplex expectation
    
        prob = {
            "coef": c,
            "MatriceA": A,
            "b": b,
            "inegalitate": s,
            "OPT": OPT
        }
    
        solution_detaliata = self.solver.solve(np.float64, **prob)
        verify_result = self.solver.verify()
    
        # Check if the solver returned an error string
        if isinstance(solution_detaliata, str):
            from PySide6.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setWindowTitle("Eroare")
            msg.setText(solution_detaliata)
            msg.exec()
            return
    
        # Show output window if solution is valid
        self.output_window = OutputWindow(solution_detaliata, verify_result)
        self.output_window.show()


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinearUI()
    window.show()
    sys.exit(app.exec())