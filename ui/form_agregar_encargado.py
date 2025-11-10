import json, os
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

DATA_FILE = "encargados.json"

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(encargados):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(encargados, f, indent=4, ensure_ascii=False)


class AgregarEncargadoWindow(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.setWindowTitle("Agregar Encargado")
        self.setGeometry(300, 150, 450, 500)
        self.setStyleSheet("""
            QWidget { background-color: #f2f2f2; font-family: 'Segoe UI'; color: black; }
            QLabel { color: black; }
            QLineEdit { padding: 8px; border: 1px solid #aaa; border-radius: 6px; background: white; color: black; }
            QPushButton { background-color: #4a4a4a; color: white; border-radius: 10px; padding: 8px; }
            QPushButton:hover { background-color: #2f2f2f; }
        """)
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Registrar Encargado")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.nombre = QLineEdit()
        self.direccion = QLineEdit()
        self.dpi = QLineEdit()
        self.proy_act = QLineEdit()
        self.proy_fin = QLineEdit()
        self.presupuesto = QLineEdit()

        form = QFormLayout()
        form.addRow("Nombre:", self.nombre)
        form.addRow("Dirección:", self.direccion)
        form.addRow("DPI:", self.dpi)
        form.addRow("Proyectos Activos:", self.proy_act)
        form.addRow("Proyectos Finalizados:", self.proy_fin)
        form.addRow("Presupuesto Total (Q):", self.presupuesto)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar)
        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.volver_menu)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(btn_guardar)
        layout.addWidget(btn_volver)
        self.setLayout(layout)

    def guardar(self):
        nombre = self.nombre.text().strip()
        direccion = self.direccion.text().strip()
        dpi = self.dpi.text().strip()

        if not nombre or not direccion or not dpi:
            QMessageBox.warning(self, "Error", "Los campos Nombre, Dirección y DPI son obligatorios.")
            return

        encargado = {
            "nombre": nombre,
            "direccion": direccion,
            "dpi": dpi,
            "proyectos_activos": self.proy_act.text().strip() or "0",
            "proyectos_finalizados": self.proy_fin.text().strip() or "0",
            "presupuesto_total": self.presupuesto.text().strip() or "0",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        datos = cargar_datos()
        datos.append(encargado)
        guardar_datos(datos)
        QMessageBox.information(self, "Éxito", f"Encargado '{nombre}' agregado correctamente.")
        self.limpiar()

    def limpiar(self):
        for campo in [self.nombre, self.direccion, self.dpi, self.proy_act, self.proy_fin, self.presupuesto]:
            campo.clear()

    def volver_menu(self):
        self.hide()
        self.menu.show()
