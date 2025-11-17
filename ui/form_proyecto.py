from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from .detalles_window import DetallesWindow
from .nuevo_proyecto import NuevoProyectoWindow
from .form_actualizar_proyecto import ActualizarProyectoWindow

from models.projects_model import get_all_projects, get_project_with_details, delete_project

class ProyectosWindow(QWidget):
    def __init__(self):
        super().__init__()
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
                min-width: 150px;
            }

            QPushButton:hover {
                background-color: #2f2f2f;
            }

            QFrame#line {
                background-color: #a0a0a0;
                max-height: 2px;
            }
        """)
        self.setWindowTitle("Lista de Proyectos")
        self.setFixedSize(900, 500)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Proyectos Comunitarios")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Inicio", "Fin", "Presupuesto", "Finalizado"]
        )
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setStyleSheet("""
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
      """)
        layout.addWidget(self.tabla)

        # Botones
        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        btn_crear = QPushButton("Crear proyecto")
        btn_crear.clicked.connect(self.show_crear)
        btn_actualizar = QPushButton("Actualizar Proyecto")
        btn_actualizar.clicked.connect(self.show_update)
        btn_delete = QPushButton("Eliminar Proyecto")
        btn_delete.clicked.connect(self.delete_project_id)
        btn_detalles = QPushButton("Ver Detalles")
        btn_detalles.clicked.connect(self.ver_detalles)

        for b in [btn_crear, btn_actualizar, btn_delete, btn_detalles]:
            b.setFixedSize(150, 45)
            btn_layout.addWidget(b)

        self.cargar_datos()

    def cargar_datos(self):
        '''proyectos = [
            {
                "id": 1,
                "nombre": "Proyecto Agua Viva",
                "inicio": "2025-01-05",
                "fin": "2025-07-10",
                "presupuesto": 45000.0,
                "finalizado": False,
                "encargado": {"id": "E001", "nombre": "María López"},
                "familias_beneficiadas": [
                    {"id": "F101", "direccion": "Zona 2, Retalhuleu", "ingreso": 1800.00},
                    {"id": "F102", "direccion": "Zona 5, Retalhuleu", "ingreso": 2100.00},
                    {"id": "F103", "direccion": "Cantón Las Victorias", "ingreso": 1650.00},
                ],
            },
            {
                "id": 2,
                "nombre": "Reforestación Urbana",
                "inicio": "2024-03-15",
                "fin": "2024-11-30",
                "presupuesto": 30000.0,
                "finalizado": True,
                "encargado": {"id": "E002", "nombre": "Carlos Gómez"},
                "familias_beneficiadas": [
                    {"id": "F201", "direccion": "Mixco, Guatemala", "ingreso": 2500.00},
                    {"id": "F202", "direccion": "San Juan Sacatepéquez", "ingreso": 2300.00},
                ],
            },
            {
                "id": 3,
                "nombre": "Huertos Familiares",
                "inicio": "2025-02-10",
                "fin": "2025-09-25",
                "presupuesto": 25000.0,
                "finalizado": False,
                "encargado": {"id": "E003", "nombre": "Ana Pérez"},
                "familias_beneficiadas": [
                    {"id": "F301", "direccion": "Zona 1, Quetzaltenango", "ingreso": 1750.00},
                    {"id": "F302", "direccion": "La Esperanza, Quetzaltenango", "ingreso": 1950.00},
                    {"id": "F303", "direccion": "Almolonga, Quetzaltenango", "ingreso": 1825.00},
                ],
            },
            {
                "id": 4,
                "nombre": "Energía Solar Comunitaria",
                "inicio": "2023-07-01",
                "fin": "2024-02-28",
                "presupuesto": 80000.0,
                "finalizado": True,
                "encargado": {"id": "E004", "nombre": "Javier Castillo"},
                "familias_beneficiadas": [
                    {"id": "F401", "direccion": "Santa Lucía Cotzumalguapa", "ingreso": 2600.00},
                    {"id": "F402", "direccion": "Escuintla Centro", "ingreso": 2400.00},
                    {"id": "F403", "direccion": "Palín, Escuintla", "ingreso": 2250.00},
                ],
            },
        ]'''

        proyectos = get_all_projects()
        self.tabla.setRowCount(len(proyectos))
        for row, p in enumerate(proyectos):
            self.tabla.setItem(row, 0, QTableWidgetItem(str(p["_id"])))
            self.tabla.setItem(row, 1, QTableWidgetItem(p["nombre"]))
            self.tabla.setItem(row, 2, QTableWidgetItem(p["inicio"]))
            self.tabla.setItem(row, 3, QTableWidgetItem(p["fin"]))
            self.tabla.setItem(row, 4, QTableWidgetItem(f"Q{p['presupuesto']:.2f}"))
            self.tabla.setItem(row, 5, QTableWidgetItem("Sí" if p["finalizado"] else "No"))

    def ver_detalles(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            proyecto_id = self.tabla.item(fila, 0).text()
            self.detalles = DetallesWindow(proyecto_id)
            self.detalles.show()
        else:
            QMessageBox.warning(self, "Seleccione un proyecto", f"Debe seleccionar un proyecto.")


    
    def show_crear(self):
        self.crear_proyecto_window = NuevoProyectoWindow()
        self.crear_proyecto_window.inserted.connect(self.cargar_datos)
        self.crear_proyecto_window.show()

    def show_update(self):
        row = self.tabla.currentRow()
        if row >= 0:
            item_id = self.tabla.item(row, 0).text()
            proyecto_data = get_project_with_details(item_id)
            if proyecto_data["finalizado"]:
                QMessageBox.warning(self, "Proyecto ya finalizado", f"No es posible editar proyectos finalizados.")
                return

            self.actualizar_proyecto = ActualizarProyectoWindow(item_id)
            self.actualizar_proyecto.updated.connect(self.cargar_datos)
            self.actualizar_proyecto.show()
        else:
            QMessageBox.warning(self, "Seleccione un proyecto", f"Debe seleccionar un proyecto.")
    

    def delete_project_id(self):
        fila = self.tabla.currentRow()

        if fila < 0:
            QMessageBox.warning(self, "Seleccione un proyecto", "Debe seleccionar un proyecto.")
            return

        proyecto_id = self.tabla.item(fila, 0).text()
        nombre = self.tabla.item(fila, 1).text()

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar el proyecto:\n\n"
            f"'{nombre}'\n\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return
        try:
            delete_project(proyecto_id)
            QMessageBox.information(
                self,
                "Proyecto eliminado",
                "El proyecto ha sido eliminado correctamente."
            )
            self.cargar_datos()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el proyecto:\n{str(e)}")
