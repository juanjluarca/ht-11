import json, os
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QFormLayout, QLineEdit, QMessageBox, QFrame
)
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


class EncargadosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Encargados")
        self.setFixedSize(900, 500)

        self.setStyleSheet("""
            QWidget {
                background-color: #e6e6e6;
                font-family: 'Segoe UI';
                color: #2e2e2e;
            }
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2f2f2f;
            }
            QLabel#titleLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2b2b2b;
            }
            QTableWidget {
                background-color: #f8f9fa;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: #444;
                color: white;
                padding: 4px;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título
        title = QLabel("Gestión de Encargados")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title)

        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Botones
        btn_layout = QHBoxLayout()

        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.form_agregar)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.form_eliminar)

        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.clicked.connect(self.cargar_tabla)

        for b in [btn_agregar, btn_eliminar, btn_actualizar]:
            b.setFixedSize(150, 35)
            btn_layout.addWidget(b)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Dirección", "DPI", "Activos", "Finalizados", "Presupuesto"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        # Contenedor de formularios
        self.form_container = QVBoxLayout()
        layout.addLayout(self.form_container)
        layout.addLayout(btn_layout)

        self.cargar_tabla()

    def form_agregar(self):
        self.limpiar_formulario()

        form = QFormLayout()
        form.setContentsMargins(20, 10, 20, 10)

        self.f_nombre = QLineEdit()
        self.f_direccion = QLineEdit()
        self.f_dpi = QLineEdit()
        self.f_activos = QLineEdit()
        self.f_finalizados = QLineEdit()
        self.f_presupuesto = QLineEdit()

        form.addRow("Nombre:", self.f_nombre)
        form.addRow("Dirección:", self.f_direccion)
        form.addRow("DPI:", self.f_dpi)
        form.addRow("Proyectos activos:", self.f_activos)
        form.addRow("Proyectos finalizados:", self.f_finalizados)
        form.addRow("Presupuesto (Q):", self.f_presupuesto)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_encargado)

        self.form_container.addLayout(form)
        self.form_container.addWidget(btn_guardar)

    def guardar_encargado(self):
        nombre = self.f_nombre.text().strip()
        direccion = self.f_direccion.text().strip()
        dpi = self.f_dpi.text().strip()

        if not nombre or not direccion or not dpi:
            QMessageBox.warning(self, "Error", "Nombre, Dirección y DPI son obligatorios.")
            return

        datos = cargar_datos()
        datos.append({
            "nombre": nombre,
            "direccion": direccion,
            "dpi": dpi,
            "proyectos_activos": self.f_activos.text() or "0",
            "proyectos_finalizados": self.f_finalizados.text() or "0",
            "presupuesto_total": self.f_presupuesto.text() or "0",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        guardar_datos(datos)
        QMessageBox.information(self, "Éxito", "Encargado guardado.")
        self.cargar_tabla()
        self.limpiar_formulario()

    def form_eliminar(self):
        self.limpiar_formulario()

        form = QFormLayout()
        self.f_eliminar = QLineEdit()
        form.addRow("Nombre a eliminar:", self.f_eliminar)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_encargado)

        self.form_container.addLayout(form)
        self.form_container.addWidget(btn_eliminar)

    def eliminar_encargado(self):
        nombre = self.f_eliminar.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "Ingrese un nombre.")
            return

        datos = cargar_datos()
        nuevos = [e for e in datos if e["nombre"].lower() != nombre.lower()]

        if len(nuevos) == len(datos):
            QMessageBox.information(self, "No encontrado", "No existe ese encargado.")
        else:
            guardar_datos(nuevos)
            QMessageBox.information(self, "Eliminado", "Encargado eliminado.")
            self.cargar_tabla()

        self.limpiar_formulario()

    def cargar_tabla(self):
        datos = cargar_datos()
        self.tabla.setRowCount(len(datos))

        for f, e in enumerate(datos):
            self.tabla.setItem(f, 0, QTableWidgetItem(e["nombre"]))
            self.tabla.setItem(f, 1, QTableWidgetItem(e["direccion"]))
            self.tabla.setItem(f, 2, QTableWidgetItem(e["dpi"]))
            self.tabla.setItem(f, 3, QTableWidgetItem(e["proyectos_activos"]))
            self.tabla.setItem(f, 4, QTableWidgetItem(e["proyectos_finalizados"]))
            self.tabla.setItem(f, 5, QTableWidgetItem(e["presupuesto_total"]))

    def limpiar_formulario(self):
        while self.form_container.count():
            item = self.form_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
