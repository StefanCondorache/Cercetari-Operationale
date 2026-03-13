import sys
import numpy as np

from ASP_back import Simplex
from problems import mm, MM, eg

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDialog, QTextEdit
)

class OutputWindow(QDialog):

    def __init__(self, solution, Z, verify_result, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Rezultat Simplex")
        self.resize(400, 300)

        layout = QVBoxLayout()

        text = QTextEdit()
        text.setReadOnly(True)

        result_text = "Solutia optima:\n\n"

        for i, val in enumerate(solution):
            result_text += f"x{i+1} = {val:.4f}\n"

        result_text += f"\nZ = {Z:.4f}\n\n"
        result_text += "Verificari:\n"

        for i, v in enumerate(verify_result):
            result_text += f"Test {i+1}: {'OK' if v else 'FAIL'}\n"

        text.setText(result_text)

        close_btn = QPushButton("Inchide")
        close_btn.clicked.connect(self.close)

        layout.addWidget(text)
        layout.addWidget(close_btn)

        self.setLayout(layout)


class LinearUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Programare liniara - ASP")

        self.layout = QVBoxLayout()

        self.obj_entries = []
        self.constraints = []

        # input variabile / restrictii
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

        self.solver = Simplex()

    def genereaza(self):

        n = int(self.var_input.text())
        m = int(self.res_input.text())

        # functia obiectiv
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

        # restrictii
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

        # conditii nenegativitate
        cond = ", ".join([f"x{i+1} ≥ 0" for i in range(n)])
        self.layout.addWidget(QLabel(cond))

        # buton rezolva
        solve_btn = QPushButton("Rezolva")
        solve_btn.clicked.connect(self.rezolva)

        self.layout.addWidget(solve_btn)

    def get_numpy_data(self):

        # vector coeficienti functie obiectiv
        c = np.array([float(e.text()) for e in self.obj_entries])

        A = []
        b = []
        s = []

        sign_map = {
            "<=": mm,
            "=": eg,
            ">=": MM
}

        for row, combo, rhs in self.constraints:

            coef_row = [float(e.text()) for e in row]

            A.append(coef_row)
            b.append(float(rhs.text()))
            s.append(sign_map[combo.currentText()])

        A = np.array(A)
        b = np.array(b)
        s = np.array(s)

        return c, A, s, b

    def rezolva(self):

        from ASP_back import Simplex

        solver = Simplex()

        c, A, s, b = self.get_numpy_data()

        prob = {
            "coef": c,
            "MatriceA": A,
            "b": b,
            "inegalitate": s,
            "OPT": -1
        }

        sol = solver.solve(np.float64, **prob)
        verify = solver.verify()

        Z = solver.Z

        self.output_window = OutputWindow(sol, Z, verify)
        self.output_window.show()


app = QApplication(sys.argv)

window = LinearUI()
window.show()

sys.exit(app.exec())