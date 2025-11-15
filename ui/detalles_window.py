from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

from models.projects_model import get_project_with_details

class DetallesWindow(QWidget):
    def __init__(self, proyecto_id):
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
        self.setWindowTitle("Detalles del Proyecto")
        self.setFixedSize(700, 500)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        datos = get_project_with_details(proyecto_id)

        title = QLabel(f"Proyecto: {datos['nombre']}")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Encargado
        encargado = {}
        try:
            encargado = datos["encargado"]
        except:
            encargado["id"] = "N/A"
            encargado["nombre"] = "Sin encargado"
        
        enc_label = QLabel(f"Encargado: {encargado['nombre']} (ID: {encargado['id']})")
        enc_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(enc_label)

        # Tabla de familias beneficiadas
        fam_label = QLabel("Familias Beneficiadas:")
        fam_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(fam_label)

        tabla = QTableWidget()
        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels(["ID", "Dirección", "Ingreso"])
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(tabla)
        tabla.setStyleSheet("""
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

        familias = []
        try:
            familias = datos["familias_beneficiadas"]
        except:
            familias = []

        tabla.setRowCount(len(familias))
        for i, f in enumerate(familias):
            tabla.setItem(i, 0, QTableWidgetItem(str(f["id"])))
            tabla.setItem(i, 1, QTableWidgetItem(f["direccion"]))
            tabla.setItem(i, 2, QTableWidgetItem(f"Q{f['ingreso']:.2f}"))
