from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QDateEdit,
    QDoubleSpinBox, QCheckBox, QPushButton, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal

from models.projects_model import update_project, get_project_with_details
from models.encargados_model import get_all_encargados, get_encargado_by_id, update_encargado_stats
from bson import ObjectId


class ActualizarProyectoWindow(QWidget):
    updated = pyqtSignal()
    def __init__(self, item_id):
        super().__init__()
        self.item_id = item_id
        self.setWindowTitle("Actualizar Proyecto")
        self.setFixedSize(700, 600)
        self.encargados = get_all_encargados()
        self.proyecto_original = None

        self.setStyleSheet("""
            QWidget {
                background-color: #e6e6e6; 
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
                min-width: 150px;
            }

            QPushButton:hover {
                background-color: #2f2f2f;
            }

            QFrame#line {
                background-color: #a0a0a0;
                max-height: 2px;
            }
            QTableWidget {
                background-color: #f8f9fa;
                gridline-color: #ccc;
                selection-background-color: #d0d0d0; 
            }

            QHeaderView::section {
                background-color: #444;
                color: white;
                padding: 4px;
                border: none;
            }

            QTableWidget::item:selected {
                background-color: #bfbfbf;   
                color: black;                
            }

            QTableWidget::item {
                padding: 6px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #555;
                border-radius: 5px;
                background-color: #eee;
            }

            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #2e8b57;
            }

            QCheckBox::indicator:unchecked:hover {
                border-color: #888;
            }

            QCheckBox::indicator:checked:hover {
                background-color: #66BB6A;
            }

            QCheckBox::indicator:disabled {
                background-color: #ccc;
                border-color: #aaa;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Actualizar proyectos")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        self.input_fin = QDateEdit()
        self.input_fin.setCalendarPopup(True)
        self.input_fin.setDate(QDate.currentDate().addDays(30))
        form_layout.addRow("Fecha de Fin:", self.input_fin)

        self.input_presupuesto = QDoubleSpinBox()
        self.input_presupuesto.setRange(0, 9999999)
        self.input_presupuesto.setPrefix("Q")
        self.input_presupuesto.setDecimals(2)
        form_layout.addRow("Presupuesto:", self.input_presupuesto)

        self.checkbox_finalizado = QCheckBox("Proyecto Finalizado")
        form_layout.addRow(self.checkbox_finalizado)

        layout.addSpacing(15)
        enc_label = QLabel("Datos del Encargado")
        enc_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(enc_label)

        self.input_enc_nombre = QComboBox()
        self.input_enc_nombre.addItem("-- Sin encargado --", None)
        for enc in self.encargados:
            self.input_enc_nombre.addItem(enc["nombre"], str(enc["_id"]))
        self.input_enc_nombre.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.input_enc_nombre)
        
        enc_form = QFormLayout()
        enc_form.addRow("Nombre Encargado:", self.input_enc_nombre)
        layout.addLayout(enc_form)

        fam_label = QLabel("Familias Beneficiadas")
        fam_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(fam_label)

        self.tabla_familias = QTableWidget(0, 2)
        self.tabla_familias.setHorizontalHeaderLabels(["Dirección", "Ingreso"])
        self.tabla_familias.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla_familias)

        btns_fam = QHBoxLayout()
        btn_add = QPushButton("+ Agregar Familia")
        btn_del = QPushButton("Eliminar Seleccionada")
        btns_fam.addWidget(btn_add)
        btns_fam.addWidget(btn_del)
        layout.addLayout(btns_fam)

        btn_add.clicked.connect(self.agregar_familia)
        btn_del.clicked.connect(self.eliminar_familia)

        layout.addSpacing(15)
        btn_guardar = QPushButton("Guardar Proyecto")
        btn_guardar.setFixedHeight(40)
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #10ac84;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1dd1a1;
            }
        """)
        btn_guardar.clicked.connect(self.guardar)
        layout.addWidget(btn_guardar, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.cargar_datos_proyecto()
    
    def cargar_datos_proyecto(self):
        data = get_project_with_details(self.item_id)

        if not data:
            QMessageBox.warning(self, "Error", "No se encontraron datos del proyecto.")
            return

        self.proyecto_original = data

        try:
            fecha_fin = QDate.fromString(data.get("fin", ""), "yyyy-MM-dd")
            if fecha_fin.isValid():
                self.input_fin.setDate(fecha_fin)
        except:
            pass

        self.input_presupuesto.setValue(float(data.get("presupuesto", 0)))
        self.checkbox_finalizado.setChecked(bool(data.get("finalizado", False)))

        encargado = data.get("encargado", {})
        if encargado and "_id" in encargado:
            enc_id = str(encargado["_id"])
            index = self.input_enc_nombre.findData(enc_id)
            if index >= 0:
                self.input_enc_nombre.setCurrentIndex(index)

        familias = data.get("familias_beneficiadas", [])
        self.tabla_familias.setRowCount(0)

        for fam in familias:
            row = self.tabla_familias.rowCount()
            self.tabla_familias.insertRow(row)

            dir_item = QTableWidgetItem(fam.get("direccion", ""))
            ing_item = QTableWidgetItem(str(fam.get("ingreso", 0)))

            self.tabla_familias.setItem(row, 0, dir_item)
            self.tabla_familias.setItem(row, 1, ing_item)

    def agregar_familia(self):
        row = self.tabla_familias.rowCount()
        self.tabla_familias.insertRow(row)
        for col in range(2):
            self.tabla_familias.setItem(row, col, QTableWidgetItem(""))

    def eliminar_familia(self):
        row = self.tabla_familias.currentRow()
        if row >= 0:
            self.tabla_familias.removeRow(row)

    def guardar(self):
        fin = self.input_fin.date().toString("yyyy-MM-dd")
        presupuesto_nuevo = float(self.input_presupuesto.value())
        finalizado_nuevo = self.checkbox_finalizado.isChecked()
        encargado_nuevo_id = self.input_enc_nombre.currentData()

        presupuesto_original = float(self.proyecto_original.get("presupuesto", 0))
        finalizado_original = bool(self.proyecto_original.get("finalizado", False))
        encargado_original = self.proyecto_original.get("encargado", {})
        encargado_original_id = str(encargado_original["_id"]) if encargado_original and "_id" in encargado_original else None

        familias = []
        for row in range(self.tabla_familias.rowCount()):
            dir_item = self.tabla_familias.item(row, 0)
            ing_item = self.tabla_familias.item(row, 1)
            if not (dir_item and ing_item):
                continue
            try:
                ingreso = float(ing_item.text())
            except ValueError:
                ingreso = 0.0
            familias.append({
                "direccion": dir_item.text(),
                "ingreso": ingreso
            })

        update_data = {
            "fin": fin,
            "presupuesto": presupuesto_nuevo,
            "finalizado": finalizado_nuevo,
            "familias_beneficiadas": familias
        }

        if encargado_nuevo_id:
            update_data["encargado"] = {
                "_id": ObjectId(encargado_nuevo_id),
                "nombre": self.input_enc_nombre.currentText()
            }
        else:
            update_data["encargado"] = None

        
        if encargado_original_id != encargado_nuevo_id:
            
            if encargado_original_id:
                enc_anterior = get_encargado_by_id(encargado_original_id)
                if enc_anterior:
                    activos_ant = enc_anterior.get("proyectos_activos", 0)
                    finalizados_ant = enc_anterior.get("proyectos_finalizados", 0)
                    presupuesto_ant = enc_anterior.get("presupuesto_total_manejado", 0)
                    
                    if finalizado_original:
                        finalizados_ant = max(0, finalizados_ant - 1)
                    else:
                        activos_ant = max(0, activos_ant - 1)
                    
                    presupuesto_ant = max(0, presupuesto_ant - presupuesto_original)
                    
                    update_encargado_stats(
                        encargado_original_id,
                        activos_ant,
                        finalizados_ant,
                        presupuesto_ant
                    )
            
            if encargado_nuevo_id:
                enc_nuevo = get_encargado_by_id(encargado_nuevo_id)
                if enc_nuevo:
                    activos_nuevo = enc_nuevo.get("proyectos_activos", 0)
                    finalizados_nuevo = enc_nuevo.get("proyectos_finalizados", 0)
                    presupuesto_nuevo_enc = enc_nuevo.get("presupuesto_total_manejado", 0)
                    
                    if finalizado_nuevo:
                        finalizados_nuevo += 1
                    else:
                        activos_nuevo += 1
                    
                    presupuesto_nuevo_enc += presupuesto_nuevo
                    
                    update_encargado_stats(
                        encargado_nuevo_id,
                        activos_nuevo,
                        finalizados_nuevo,
                        presupuesto_nuevo_enc
                    )
        
        elif encargado_original_id and encargado_original_id == encargado_nuevo_id:
            enc = get_encargado_by_id(encargado_original_id)
            if enc:
                activos = enc.get("proyectos_activos", 0)
                finalizados = enc.get("proyectos_finalizados", 0)
                presupuesto_enc = enc.get("presupuesto_total_manejado", 0)
                
                if finalizado_original != finalizado_nuevo:
                    if finalizado_nuevo:
                        activos = max(0, activos - 1)
                        finalizados += 1
                    else:
                        finalizados = max(0, finalizados - 1)
                        activos += 1
                
                diferencia_presupuesto = presupuesto_nuevo - presupuesto_original
                presupuesto_enc += diferencia_presupuesto
                presupuesto_enc = max(0, presupuesto_enc)
                
                update_encargado_stats(
                    encargado_original_id,
                    activos,
                    finalizados,
                    presupuesto_enc
                )
        
        elif not encargado_original_id and encargado_nuevo_id:
            enc_nuevo = get_encargado_by_id(encargado_nuevo_id)
            if enc_nuevo:
                activos_nuevo = enc_nuevo.get("proyectos_activos", 0)
                finalizados_nuevo = enc_nuevo.get("proyectos_finalizados", 0)
                presupuesto_nuevo_enc = enc_nuevo.get("presupuesto_total_manejado", 0)
                
                if finalizado_nuevo:
                    finalizados_nuevo += 1
                else:
                    activos_nuevo += 1
                
                presupuesto_nuevo_enc += presupuesto_nuevo
                
                update_encargado_stats(
                    encargado_nuevo_id,
                    activos_nuevo,
                    finalizados_nuevo,
                    presupuesto_nuevo_enc
                )

        update_project(self.item_id, update_data)

        QMessageBox.information(
            self, 
            "Proyecto guardado", 
            "El proyecto fue actualizado exitosamente."
        )
        self.updated.emit()
        self.close()