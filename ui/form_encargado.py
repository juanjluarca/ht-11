from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from ui.form_agregar_encargado import AgregarEncargadoWindow
from ui.form_eliminar_encargado import EliminarEncargadoWindow
from ui.form_ver_encargados import VerEncargadosWindow

class MainMenuEncargados(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Encargados")
        self.setGeometry(300, 200, 400, 300)
        self.setStyleSheet("""
            QWidget { background-color: #e6e6e6; font-family: 'Segoe UI'; }
            QPushButton {
                background-color: #4a4a4a; color: white; border-radius: 10px;
                padding: 10px; font-size: 15px;
            }
            QPushButton:hover { background-color: #2f2f2f; }
            QLabel { font-size: 20px; font-weight: bold; color: #2b2b2b; }
        """)
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Menú Encargados")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_agregar = QPushButton("Agregar Encargado")
        btn_agregar.clicked.connect(self.abrir_agregar)

        btn_eliminar = QPushButton("Eliminar Encargado")
        btn_eliminar.clicked.connect(self.abrir_eliminar)

        btn_ver = QPushButton("Ver Encargados")
        btn_ver.clicked.connect(self.abrir_ver)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(btn_agregar)
        layout.addWidget(btn_eliminar)
        layout.addWidget(btn_ver)
        layout.addStretch()
        self.setLayout(layout)

    def abrir_agregar(self):
        self.hide()
        self.agregar = AgregarEncargadoWindow(self)
        self.agregar.show()

    def abrir_eliminar(self):
        self.hide()
        self.eliminar = EliminarEncargadoWindow(self)
        self.eliminar.show()

    def abrir_ver(self):
        self.hide()
        self.ver = VerEncargadosWindow(self)
        self.ver.show()
