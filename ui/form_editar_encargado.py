from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFormLayout, 
    QLineEdit, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from models.encargados_model import update_encargado, get_encargado_by_id

class FormEditarEncargado(QDialog):
    encargado_actualizado = pyqtSignal()
    
    def __init__(self, encargado_id, parent=None):
        super().__init__(parent)
        self.encargado_id = encargado_id
        self.setWindowTitle("Editar Encargado")
        self.setFixedSize(450, 350)
        self.setModal(True)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-family: 'Segoe UI';
            }
            QLabel#titleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2b2b2b;
            }
            QLabel {
                color: #2e2e2e;
                font-size: 13px;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #4a4a4a;
            }
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2f2f2f;
            }
            QPushButton#btnCancelar {
                background-color: #888;
            }
            QPushButton#btnCancelar:hover {
                background-color: #666;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("Editar Encargado")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        # Formulario
        form = QFormLayout()
        form.setSpacing(12)
        form.setContentsMargins(0, 10, 0, 10)
        
        self.f_nombre = QLineEdit()
        self.f_direccion = QLineEdit()
        self.f_dpi = QLineEdit()
        self.f_dpi.setMaxLength(13)
        
        form.addRow("Nombre:", self.f_nombre)
        form.addRow("Dirección:", self.f_direccion)
        form.addRow("DPI:", self.f_dpi)
        
        layout.addLayout(form)
        
        # Nota informativa
        nota = QLabel("* Los datos de proyectos no se pueden editar desde aquí")
        nota.setStyleSheet("color: #666; font-size: 11px; font-style: italic;")
        nota.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(nota)
        
        layout.addStretch()
        
        # Botones
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_guardar = QPushButton("Actualizar Encargado")
        btn_guardar.clicked.connect(self.actualizar_encargado)
        btn_guardar.setFixedHeight(40)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnCancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_cancelar.setFixedHeight(35)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addLayout(btn_layout)
        
        # Cargar datos del encargado
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            encargado = get_encargado_by_id(self.encargado_id)
            
            if not encargado:
                QMessageBox.critical(self, "Error", "No se encontró el encargado.")
                self.reject()
                return
            
            self.f_nombre.setText(encargado.get("nombre", ""))
            self.f_direccion.setText(encargado.get("direccion", ""))
            self.f_dpi.setText(encargado.get("dpi", ""))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los datos:\n{str(e)}")
            self.reject()
    
    def actualizar_encargado(self):
        nombre = self.f_nombre.text().strip()
        direccion = self.f_direccion.text().strip()
        dpi = self.f_dpi.text().strip()
        
        # Validaciones
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio.")
            self.f_nombre.setFocus()
            return
        
        if not direccion:
            QMessageBox.warning(self, "Error", "La dirección es obligatoria.")
            self.f_direccion.setFocus()
            return
        
        if not dpi:
            QMessageBox.warning(self, "Error", "El DPI es obligatorio.")
            self.f_dpi.setFocus()
            return
        
        if len(dpi) != 13 or not dpi.isdigit():
            QMessageBox.warning(self, "Error", "El DPI debe tener 13 dígitos numéricos.")
            self.f_dpi.setFocus()
            return
        
        # Actualizar en la base de datos
        try:
            success, error = update_encargado(self.encargado_id, nombre, direccion, dpi)
            
            if error:
                QMessageBox.warning(self, "Error", error)
                return
            
            if success:
                QMessageBox.information(self, "Éxito", "Encargado actualizado correctamente.")
                self.encargado_actualizado.emit()
                self.accept()
            else:
                QMessageBox.warning(self, "Aviso", "No se realizaron cambios.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar el encargado:\n{str(e)}")