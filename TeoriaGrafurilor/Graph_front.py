import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, 
                               QGraphicsView, QVBoxLayout, QHBoxLayout, 
                               QWidget, QPushButton, QLabel, QTextEdit)
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QPainter
from PySide6.QtCore import Qt, QPointF, QRectF

from Graph_back import Graph

class FlowNetworkView(QMainWindow):
    def __init__(self, problema):
        super().__init__()
        self.setWindowTitle("Ford-Fulkerson - Vizualizare")
        self.resize(1100, 750)

        self.problema = problema
        self.backend = Graph()
        
        # Setul de muchii originale pentru a detecta când algoritmul folosește arce inverse
        self.muchii_originale = set(date['node'] for date in self.problema['date_intrare'].values())
        
        # Rulăm algoritmul o singură dată pentru a obține toate iterațiile
        self.flux_maxim_final, self.iteratii, self.muchii_taiate = self.backend.solve(**self.problema)
        
        self.pas_curent = -1
        self.flux_curent_afisat = 0
        self.pozitii_noduri = {}
        
        # Istoricul fluxului reține o listă de adăugări/scăderi pe fiecare muchie: {u: {v: [20, 1]}}
        self.istoric_fluxuri = self._init_istoric()

        self._init_ui()
        self._calculeaza_layout_noduri()
        self._deseneaza_graf()

    def _init_istoric(self):
        """Inițializează liste goale pentru fiecare muchie originală."""
        istoric = {}
        for date in self.problema['date_intrare'].values():
            u, v = date['node']
            if u not in istoric: istoric[u] = {}
            istoric[u][v] = []
        return istoric

    def _init_ui(self):
        widget_central = QWidget()
        layout_principal = QHBoxLayout(widget_central)

        # 1. Panoul Grafic
        self.scena = QGraphicsScene()
        self.view = QGraphicsView(self.scena)
        self.view.setRenderHint(QPainter.Antialiasing)
        layout_principal.addWidget(self.view, stretch=3)

        # 2. Panoul de Control
        panou_control = QVBoxLayout()
        
        self.lbl_status = QLabel("Stare: Pregătit.\nApasă 'Următorul Pas' pentru a începe.")
        self.lbl_status.setFont(QFont("Arial", 12, QFont.Bold))
        panou_control.addWidget(self.lbl_status)

        self.btn_urmatorul = QPushButton("Următorul Pas")
        self.btn_urmatorul.clicked.connect(self.pas_urmator)
        panou_control.addWidget(self.btn_urmatorul)

        self.btn_reset = QPushButton("Resetează")
        self.btn_reset.clicked.connect(self.reseteaza)
        panou_control.addWidget(self.btn_reset)

        self.consola = QTextEdit()
        self.consola.setReadOnly(True)
        panou_control.addWidget(self.consola)

        layout_principal.addLayout(panou_control, stretch=1)
        self.setCentralWidget(widget_central)

    def _calculeaza_layout_noduri(self):
        """Așază nodurile în layere bazat pe distanța de la sursă."""
        sursa = self.problema['sursa']
        
        adancimi = {sursa: 0}
        coada = [(sursa, 0)]
        while coada:
            u, depth = coada.pop(0)
            for date in self.problema['date_intrare'].values():
                node_u, node_v = date['node']
                if node_u == u and node_v not in adancimi:
                    adancimi[node_v] = depth + 1
                    coada.append((node_v, depth + 1))

        layere = {}
        for nod, depth in adancimi.items():
            if depth not in layere:
                layere[depth] = []
            layere[depth].append(nod)

        latime = 750
        inaltime = 650
        nr_layere = len(layere)
        
        for adancime, noduri_layer in layere.items():
            x = 50 + (latime / max(1, nr_layere - 1)) * adancime
            spatiere_y = inaltime / (len(noduri_layer) + 1)
            for i, nod in enumerate(noduri_layer):
                y = spatiere_y * (i + 1)
                self.pozitii_noduri[nod] = QPointF(x, y)

    def pas_urmator(self):
        if self.pas_curent < len(self.iteratii) - 1:
            self.pas_curent += 1
            it = self.iteratii[self.pas_curent]
            
            drum_evidentiat = []
            if it['drum_xt_xs'] is not None:
                drum = list(reversed(it['drum_xt_xs'])) 
                flux_adaugat = it['minim_valori']
                
                # Adăugăm elementele în istoricul de formare a sumei text
                for i in range(len(drum) - 1):
                    u = drum[i]
                    v = drum[i+1]
                    
                    if (u, v) in self.muchii_originale:
                        self.istoric_fluxuri[u][v].append(flux_adaugat)
                    elif (v, u) in self.muchii_originale:
                        # Dacă am folosit muchia inversă, o scădem din text (ex: - 1)
                        self.istoric_fluxuri[v][u].append(-flux_adaugat)
                        
                    drum_evidentiat.append((u, v))
                
                mesaj = f"Drum găsit: {' -> '.join(drum)}\nFlux adăugat: {flux_adaugat}"
            else:
                mesaj = "Nu s-au mai găsit drumuri. Algoritm terminat."

            self.flux_curent_afisat = it['flux_maxim_moment']
            
            self.lbl_status.setText(f"Iterația {self.pas_curent + 1}\nFlux Maxim Curent: {self.flux_curent_afisat}")
            self.consola.append(f"--- Iterația {self.pas_curent + 1} ---")
            self.consola.append(mesaj)
            self.consola.append(f"Test: {it['test_optimalitate']}\n")

            self._deseneaza_graf(drum_evidentiat)
        else:
            self.lbl_status.setText(f"Optimizare completă.\nFlux Maxim: {self.flux_maxim_final}")

    def reseteaza(self):
        self.pas_curent = -1
        self.flux_curent_afisat = 0
        self.istoric_fluxuri = self._init_istoric()
        self.lbl_status.setText("Stare: Pregătit.\nApasă 'Următorul Pas' pentru a începe.")
        self.consola.clear()
        self._deseneaza_graf()

    def _deseneaza_graf(self, muchii_evidentiate=None):
        self.scena.clear()
        if muchii_evidentiate is None:
            muchii_evidentiate = []

        raza = 20

        # Desenăm muchiile și textul sumarizat
        for date in self.problema['date_intrare'].values():
            u, v = date['node']
            capacitate = date['value']
            istoric = self.istoric_fluxuri[u][v]
            flux_total = sum(istoric)
            
            p1 = self.pozitii_noduri[u]
            p2 = self.pozitii_noduri[v]

            # Linia grafică
            culoare = QColor(255, 0, 0) if (u, v) in muchii_evidentiate or (v, u) in muchii_evidentiate else QColor(100, 100, 100)
            grosime = 3 if (u, v) in muchii_evidentiate else 2
            pen = QPen(culoare, grosime)
            self.scena.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)

            # --- Construirea string-ului istoric ---
            if not istoric:
                text_flux = "0"
            else:
                elemente = []
                for val in istoric:
                    if not elemente:
                        elemente.append(str(val))
                    else:
                        semn = "+" if val >= 0 else "-"
                        elemente.append(f"{semn} {abs(val)}")
                        
                text_flux = f"{flux_total} = {' '.join(elemente)}"
            
            # Adăugăm sufixul de validare (saturat/nesaturat)
            if flux_total == capacitate:
                text_flux += " ●"
            else:
                text_flux += " +"
            # ----------------------------------------

            mid_x = (p1.x() + p2.x()) / 2
            mid_y = (p1.y() + p2.y()) / 2
            
            text_item = self.scena.addText(text_flux, QFont("Arial", 10, QFont.Bold))
            text_item.setDefaultTextColor(QColor(0, 0, 255))
            text_item.setPos(mid_x - 15, mid_y - 20)

        # Desenăm nodurile
        for nod, pos in self.pozitii_noduri.items():
            rect = QRectF(pos.x() - raza, pos.y() - raza, raza * 2, raza * 2)
            
            culoare_nod = QColor(200, 220, 255)
            if nod == self.problema['sursa']: culoare_nod = QColor(150, 255, 150)
            if nod == self.problema['destinatie']: culoare_nod = QColor(255, 150, 150)
            
            self.scena.addEllipse(rect, QPen(Qt.black, 2), QBrush(culoare_nod))
            
            text = self.scena.addText(nod, QFont("Arial", 10, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(pos.x() - text_rect.width() / 2, pos.y() - text_rect.height() / 2)


if __name__ == "__main__":
    problema_test = {
        'date_intrare': {
            'c1': {'node': ('x1', 'x2'), 'value': 20},
            'c2': {'node': ('x1', 'x3'), 'value': 30},
            'c3': {'node': ('x1', 'x4'), 'value': 40},
            'c4': {'node': ('x2', 'x7'), 'value': 21},
            'c5': {'node': ('x2', 'x5'), 'value': 22},
            'c6': {'node': ('x3', 'x5'), 'value': 11},
            'c7': {'node': ('x3', 'x8'), 'value': 23},
            'c8': {'node': ('x3', 'x6'), 'value': 8},
            'c9': {'node': ('x4', 'x6'), 'value': 24},
            'c10': {'node': ('x4', 'x9'), 'value': 25},
            'c11': {'node': ('x5', 'x7'), 'value': 10},
            'c12': {'node': ('x5', 'x8'), 'value': 9},
            'c13': {'node': ('x6', 'x8'), 'value': 12},
            'c14': {'node': ('x6', 'x9'), 'value': 8},
            'c15': {'node': ('x7', 'x10'), 'value': 31},
            'c16': {'node': ('x8', 'x10'), 'value': 26},
            'c17': {'node': ('x9', 'x10'), 'value': 42}
        },
        'sursa': 'x1',
        'destinatie': 'x10'
    }

    app = QApplication(sys.argv)
    fereastra = FlowNetworkView(problema_test)
    fereastra.show()
    sys.exit(app.exec())