import json, os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from ui.form_agregar_encargado import cargar_datos, guardar_datos

class EliminarEncargadoWindow(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.setWindowTitle("Eliminar Encargado")
        self.setGeometry(300, 200, 400, 250)
        self.setStyleSheet("""
            QWidget { background-color: #f2f2f2; font-family: 'Segoe UI'; color: black; }
            QLabel { color: black; }
            QLineEdit { padding: 8px; border: 1px solid #aaa; border-radius: 6px; background: white; color: black; }
            QPushButton { background-color: #4a4a4a; color: white; border-radius: 10px; padding: 8px; }
            QPushButton:hover { background-color: #2f2f2f; }
        """)
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Eliminar Encargado")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")

        self.nombre = QLineEdit()

        form = QFormLayout()
        form.addRow("Nombre del Encargado:", self.nombre)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar)
        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.volver_menu)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(btn_eliminar)
        layout.addWidget(btn_volver)
        self.setLayout(layout)

    def eliminar(self):
        nombre = self.nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "Ingrese un nombre para eliminar.")
            return

        datos = cargar_datos()
        nuevos = [e for e in datos if e["nombre"].lower() != nombre.lower()]

        if len(nuevos) == len(datos):
            QMessageBox.information(self, "No encontrado", f"No se encontró a '{nombre}'.")
        else:
            guardar_datos(nuevos)
            QMessageBox.information(self, "Eliminado", f"Encargado '{nombre}' eliminado correctamente.")
            self.nombre.clear()

    def volver_menu(self):
        self.hide()
        self.menu.show()
