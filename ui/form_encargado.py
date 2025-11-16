from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from models.encargados_model import get_all_encargados, delete_encargado
from .form_agregar_encargado import FormAgregarEncargado
from .form_editar_encargado import FormEditarEncargado


class EncargadosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Encargados")
        self.setFixedSize(1000, 600)

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
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2f2f2f;
            }
            QPushButton:disabled {
                background-color: #999;
            }
            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2b2b2b;
            }
            QTableWidget {
                background-color: #f8f9fa;
                gridline-color: #ccc;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #444;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4a4a4a;
                color: white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Gestión de Encargados")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.btn_agregar = QPushButton("Agregar Encargado")
        self.btn_agregar.clicked.connect(self.abrir_form_agregar)
        self.btn_agregar.setFixedSize(180, 40)

        self.btn_editar = QPushButton("Editar Encargado")
        self.btn_editar.clicked.connect(self.abrir_form_editar)
        self.btn_editar.setFixedSize(180, 40)
        self.btn_editar.setEnabled(False)

        self.btn_eliminar = QPushButton("Eliminar Encargado")
        self.btn_eliminar.clicked.connect(self.eliminar_encargado)
        self.btn_eliminar.setFixedSize(180, 40)
        self.btn_eliminar.setEnabled(False)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.cargar_tabla)
        self.btn_actualizar.setFixedSize(150, 40)

        btn_layout.addWidget(self.btn_agregar)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_actualizar)

        layout.addLayout(btn_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Dirección", "DPI", 
            "Proyectos Activos", "Proyectos Finalizados", 
            "Presupuesto Total (Q)", "Fecha Registro"
        ])
        
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(2, 120)  
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(3, 120)  
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(4, 140)  
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(5, 150)  
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(6, 150)  
        
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla.itemSelectionChanged.connect(self.on_seleccion_changed)
        
        layout.addWidget(self.tabla)

        self.cargar_tabla()

    def abrir_form_agregar(self):
        dialog = FormAgregarEncargado(self)
        dialog.encargado_agregado.connect(self.cargar_tabla)
        dialog.exec()

    def abrir_form_editar(self):
        selected_row = self.tabla.currentRow()
        
        if selected_row < 0:
            QMessageBox.warning(self, "Aviso", "Seleccione un encargado para editar.")
            return
        
        encargado_id = self.tabla.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        
        dialog = FormEditarEncargado(encargado_id, self)
        dialog.encargado_actualizado.connect(self.cargar_tabla)
        dialog.exec()

    def eliminar_encargado(self):
        selected_row = self.tabla.currentRow()
        
        if selected_row < 0:
            QMessageBox.warning(self, "Aviso", "Seleccione un encargado para eliminar.")
            return
        
        nombre = self.tabla.item(selected_row, 0).text()
        encargado_id = self.tabla.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar al encargado '{nombre}'?\n\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                if delete_encargado(encargado_id):
                    QMessageBox.information(self, "Éxito", "Encargado eliminado correctamente.")
                    self.cargar_tabla()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el encargado.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar el encargado:\n{str(e)}")

    def cargar_tabla(self):
        try:
            encargados = get_all_encargados()
            self.tabla.setRowCount(len(encargados))

            for fila, encargado in enumerate(encargados):
                item_nombre = QTableWidgetItem(encargado.get("nombre", ""))
                item_nombre.setData(Qt.ItemDataRole.UserRole, str(encargado["_id"]))
                self.tabla.setItem(fila, 0, item_nombre)
                
                self.tabla.setItem(fila, 1, QTableWidgetItem(encargado.get("direccion", "")))
                
                self.tabla.setItem(fila, 2, QTableWidgetItem(encargado.get("dpi", "")))
                
                activos = encargado.get("proyectos_activos", 0)
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(int(activos))))
                
                finalizados = encargado.get("proyectos_finalizados", 0)
                self.tabla.setItem(fila, 4, QTableWidgetItem(str(int(finalizados))))
                
                presupuesto = encargado.get("presupuesto_total_manejado", 0)
                self.tabla.setItem(fila, 5, QTableWidgetItem(f"Q {presupuesto:,.2f}"))
                
                fecha = encargado.get("creado_en")
                if fecha:
                    fecha_str = fecha.strftime("%d/%m/%Y %H:%M")
                    self.tabla.setItem(fila, 6, QTableWidgetItem(fecha_str))
                else:
                    self.tabla.setItem(fila, 6, QTableWidgetItem("N/A"))
                
                for col in [3, 4, 5, 6]:
                    if self.tabla.item(fila, col):
                        self.tabla.item(fila, col).setTextAlignment(
                            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                        )
            
            self.btn_editar.setEnabled(False)
            self.btn_eliminar.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los datos:\n{str(e)}")

    def on_seleccion_changed(self):
        hay_seleccion = len(self.tabla.selectedItems()) > 0
        self.btn_editar.setEnabled(hay_seleccion)
        self.btn_eliminar.setEnabled(hay_seleccion)