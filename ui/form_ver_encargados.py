from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from ui.form_agregar_encargado import cargar_datos

class VerEncargadosWindow(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.setWindowTitle("Ver Encargados")
        self.setGeometry(250, 150, 700, 400)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget { 
                background-color: #f2f2f2; 
                font-family: 'Segoe UI'; 
                color: black; 
            }
            QLabel { 
                color: black; 
            }
            QTableWidget { 
                background-color: white; 
                color: black; 
                gridline-color: #ccc; 
                border: 1px solid #aaa;
                border-radius: 6px;
                alternate-background-color: #fafafa;
            }
            QHeaderView::section { 
                background-color: #e0e0e0; 
                color: black; 
                font-weight: bold; 
                border: 1px solid #aaa;
                padding: 4px;
            }
            QPushButton { 
                background-color: #4a4a4a; 
                color: white; 
                border-radius: 10px; 
                padding: 8px 12px; 
            }
            QPushButton:hover { 
                background-color: #2f2f2f; 
            }
        """)

        title = QLabel("Encargados Registrados")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Dirección", "DPI", "Activos", "Finalizados", "Presupuesto (Q)"
        ])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setAlternatingRowColors(True)

        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.volver_menu)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.tabla)
        layout.addWidget(btn_volver)
        self.setLayout(layout)
        self.cargar_tabla()

    def cargar_tabla(self):
        datos = cargar_datos()
        self.tabla.setRowCount(len(datos))
        for fila, e in enumerate(datos):
            self.tabla.setItem(fila, 0, QTableWidgetItem(e["nombre"]))
            self.tabla.setItem(fila, 1, QTableWidgetItem(e["direccion"]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(e["dpi"]))
            self.tabla.setItem(fila, 3, QTableWidgetItem(e["proyectos_activos"]))
            self.tabla.setItem(fila, 4, QTableWidgetItem(e["proyectos_finalizados"]))
            self.tabla.setItem(fila, 5, QTableWidgetItem(e["presupuesto_total"]))

    def volver_menu(self):
        self.hide()
        self.menu.show()
