from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ui.form_proyecto import ProyectosWindow
from ui.form_encargado import  EncargadosWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Proyectos Comunitarios")
        self.setGeometry(200, 100, 700, 450)
        self.setStyleSheet("""
            QWidget {
                background-color: #e6e6e6; /* Gris claro elegante */
                font-family: 'Segoe UI';
                color: #2e2e2e;
            }

            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2b2b2b;
            }

            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                min-width: 160px;
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
        title = QLabel("Gestión de Proyectos Comunitarios")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line = QFrame()
        line.setObjectName("line")
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)

        btn_encargados = QPushButton("Encargados")
        btn_proyectos = QPushButton("Proyectos")

        btn_encargados.clicked.connect(self.show_encargado_message)
        btn_proyectos.clicked.connect(self.show_proyecto_message)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.addStretch()
        button_layout.addWidget(btn_encargados)
        button_layout.addWidget(btn_proyectos)
        button_layout.addStretch()

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(line)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    # === Mensajes temporales ===
    def show_encargado_message(self):
        self.encargado_window = EncargadosWindow()
        self.encargado_window.show()

    def show_proyecto_message(self):
        self.proyectos_window = ProyectosWindow()
        self.proyectos_window.show()
