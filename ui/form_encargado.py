from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QFormLayout, QPushButton,
    QMessageBox, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt
from datetime import datetime


class EncargadoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Encargado")
        self.setGeometry(250, 150, 500, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #e6e6e6;
                font-family: 'Segoe UI';
                color: #2e2e2e;
            }
            QLabel#titleLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2b2b2b;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #a0a0a0;
                border-radius: 6px;
                background-color: #fff;
            }
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #2f2f2f;
            }
            QFrame#line {
                background-color: #a0a0a0;
                max-height: 2px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Registrar Encargado")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line = QFrame()
        line.setObjectName("line")
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)

        # Campos de texto
        self.nombre_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.dpi_input = QLineEdit()
        self.proyectos_activos_input = QLineEdit()
        self.proyectos_finalizados_input = QLineEdit()
        self.presupuesto_total_input = QLineEdit()

        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Dirección:", self.direccion_input)
        form_layout.addRow("DPI:", self.dpi_input)
        form_layout.addRow("Proyectos Activos:", self.proyectos_activos_input)
        form_layout.addRow("Proyectos Finalizados:", self.proyectos_finalizados_input)
        form_layout.addRow("Presupuesto Total (Q):", self.presupuesto_total_input)

        # Botones de acción
        btn_guardar = QPushButton("Guardar Encargado")
        btn_guardar.clicked.connect(self.guardar_encargado)

        btn_limpiar = QPushButton("Limpiar Campos")
        btn_limpiar.clicked.connect(self.limpiar_campos)

        btn_volver = QPushButton("Volver al Menú Principal")
        btn_volver.clicked.connect(self.volver_menu)

        # Layout de botones principales
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()
        button_layout.addWidget(btn_guardar)
        button_layout.addWidget(btn_limpiar)
        button_layout.addStretch()

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(line)
        layout.addSpacing(10)
        layout.addLayout(form_layout)
        layout.addSpacing(15)
        layout.addLayout(button_layout)

        # Botón de volver (centrado)
        layout.addSpacing(25)
        layout.addWidget(btn_volver, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.direccion_input.clear()
        self.dpi_input.clear()
        self.proyectos_activos_input.clear()
        self.proyectos_finalizados_input.clear()
        self.presupuesto_total_input.clear()

    def guardar_encargado(self):
        try:
            nombre = self.nombre_input.text().strip()
            direccion = self.direccion_input.text().strip()
            dpi = self.dpi_input.text().strip()
            proyectos_activos = float(self.proyectos_activos_input.text().strip() or 0)
            proyectos_finalizados = float(self.proyectos_finalizados_input.text().strip() or 0)
            presupuesto_total = float(self.presupuesto_total_input.text().strip() or 0)
            creado_en = datetime.now().isoformat()

            if not nombre or not direccion or not dpi:
                raise ValueError("Por favor complete los campos obligatorios.")

            encargado = {
                "_id": "ObjectId()",
                "nombre": nombre,
                "direccion": direccion,
                "dpi": dpi,
                "proyectos_activos": proyectos_activos,
                "proyectos_finalizados": proyectos_finalizados,
                "presupuesto_total_manejado": presupuesto_total,
                "creado_en": creado_en
            }

            QMessageBox.information(
                self, "Encargado guardado",
                f"Encargado '{nombre}' registrado correctamente.\n\nDatos:\n{encargado}"
            )
            self.limpiar_campos()

        except ValueError as e:
            QMessageBox.warning(self, "Error de validación", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def volver_menu(self):
        self.hide()
