# Copyright (c) 2026. All rights reserved.
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                               QLabel, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt

# --- STILIZARE GLOBALA ---
STYLESHEET = """
QWidget {
    font-size: 14px;
    background-color: #f8f9fa;
}
QLabel#titlu_principal {
    font-size: 22px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 20px;
}
QPushButton {
    background-color: #ffffff;
    border: 2px solid #bdc3c7;
    border-radius: 8px;
    padding: 15px;
    font-size: 15px;
    font-weight: bold;
    color: #34495e;
}
QPushButton:hover {
    background-color: #eaf2f8;
    border-color: #3498db;
    color: #2980b9;
}
QPushButton:pressed {
    background-color: #d6eaf8;
}
"""

class CentralLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem de Optimizare și Algoritmi")
        self.setFixedSize(500, 450)
        self.setStyleSheet(STYLESHEET)
        
        self.current_window = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Titlu
        titlu = QLabel("Colecție Algoritmi de Optimizare")
        titlu.setObjectName("titlu_principal")
        titlu.setAlignment(Qt.AlignCenter)
        layout.addWidget(titlu)

        subtitlu = QLabel("Alegeți problema pe care doriți să o rezolvați:")
        subtitlu.setAlignment(Qt.AlignCenter)
        subtitlu.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(subtitlu)

        layout.addSpacing(10)

        # Grila de butoane
        grid = QGridLayout()
        grid.setSpacing(15)

        # 1. Problema Liniară
        btn_liniara = QPushButton("1. Problema Liniară\n(Algoritmul Simplex)")
        btn_liniara.clicked.connect(self.deschide_liniara)
        grid.addWidget(btn_liniara, 0, 0)

        # 2. Problema Transporturilor
        btn_transport = QPushButton("2. Problema Transporturilor\n(Cost Minim)")
        btn_transport.clicked.connect(self.deschide_transport)
        grid.addWidget(btn_transport, 0, 1)

        # 3. Teoria Grafurilor
        btn_grafuri = QPushButton("3. Teoria Grafurilor\n(Flux & Ungar)")
        btn_grafuri.clicked.connect(self.deschide_grafuri)
        grid.addWidget(btn_grafuri, 1, 0)

        # 4. Teoria Jocurilor
        btn_jocuri = QPushButton("4. Teoria Jocurilor\n(Strategii Optime)")
        btn_jocuri.clicked.connect(self.deschide_jocuri)
        grid.addWidget(btn_jocuri, 1, 1)

        layout.addLayout(grid)
        layout.addStretch()

        footer = QLabel("Rulare din root: .venv/bin/python3 -m main")
        footer.setAlignment(Qt.AlignRight)
        footer.setStyleSheet("font-size: 11px; color: #bdc3c7;")
        layout.addWidget(footer)

    def afiseaza_fereastra(self, fereastra_noua):
        """Metodă generală pentru a lansa interfețele copil și a ascunde launcher-ul."""
        self.current_window = fereastra_noua
        self.current_window.show()
        self.hide()

    # --- METODE PENTRU FIECARE MODUL ---
    
    def deschide_liniara(self):
        try:
            from ProblemaLineara.ASP_front import LinearUI
            self.afiseaza_fereastra(LinearUI())
        except Exception as e:
            QMessageBox.critical(self, "Eroare", f"Eroare la încărcarea Problemei Liniare:\n{e}")

    def deschide_transport(self):
        try:
            from ProblemaTransporturilor.Transport_front import TransportUI
            self.afiseaza_fereastra(TransportUI())
        except Exception as e:
            QMessageBox.critical(self, "Eroare", f"Eroare la încărcarea Problemei Transporturilor:\n{e}")

    def deschide_grafuri(self):
        try:
            from TeoriaGrafurilor.main import MainLauncher
            self.afiseaza_fereastra(MainLauncher())
        except Exception as e:
            QMessageBox.critical(self, "Eroare", f"Eroare la încărcarea Teoriei Grafurilor:\n{e}")

    def deschide_jocuri(self):
        try:
            from TeoriaJocurilor.JOC_front import GameUI
            self.afiseaza_fereastra(GameUI())
        except Exception as e:
            QMessageBox.critical(self, "Eroare", f"Eroare la încărcarea Teoriei Jocurilor:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    launcher = CentralLauncher()
    launcher.show()
    
    sys.exit(app.exec())