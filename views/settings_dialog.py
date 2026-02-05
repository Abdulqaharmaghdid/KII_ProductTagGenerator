"""
Settings dialog UI: configure output size (inches), DPI, default format, default output folder.
Uses AppSettings through controller to persist.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt
import os

class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.settings = settings
        self._build_ui()
        self._load_settings()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Output size
        h = QHBoxLayout()
        h.addWidget(QLabel("Width (in):"))
        self.width_input = QLineEdit()
        self.width_input.setFixedWidth(80)
        h.addWidget(self.width_input)
        h.addWidget(QLabel("Height (in):"))
        self.height_input = QLineEdit()
        self.height_input.setFixedWidth(80)
        h.addWidget(self.height_input)
        layout.addLayout(h)

        # DPI
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("DPI:"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 1200)
        self.dpi_spin.setValue(300)
        h2.addWidget(self.dpi_spin)
        layout.addLayout(h2)

        # Default format
        h3 = QHBoxLayout()
        h3.addWidget(QLabel("Default export format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["pdf","png","jpg"])
        h3.addWidget(self.format_combo)
        layout.addLayout(h3)

        # Default output folder
        h4 = QHBoxLayout()
        h4.addWidget(QLabel("Default output folder:"))
        self.folder_input = QLineEdit()
        h4.addWidget(self.folder_input)
        self.browse_btn = QPushButton("Browse")
        h4.addWidget(self.browse_btn)
        layout.addLayout(h4)

        # Buttons
        btn_h = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_h.addStretch()
        btn_h.addWidget(self.save_btn)
        btn_h.addWidget(self.cancel_btn)
        layout.addLayout(btn_h)

        # Connections
        self.browse_btn.clicked.connect(self._on_browse)
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def _load_settings(self):
        if not self.settings:
            return
        w, h = self.settings.get_output_size()
        self.width_input.setText(str(w))
        self.height_input.setText(str(h))
        self.dpi_spin.setValue(self.settings.get_dpi())
        self.format_combo.setCurrentText(self.settings.get_default_format())
        self.folder_input.setText(self.settings.get_default_output_folder() or os.path.expanduser("~"))

    def _on_browse(self):
        folder = QFileDialog.getExistingDirectory(self, "Select default output folder", os.path.expanduser("~"))
        if folder:
            self.folder_input.setText(folder)

    def get_values(self):
        try:
            w = float(self.width_input.text())
            h = float(self.height_input.text())
        except ValueError:
            w, h = 4.0, 3.0
        dpi = int(self.dpi_spin.value())
        fmt = self.format_combo.currentText()
        folder = self.folder_input.text().strip() or os.path.expanduser("~")
        return w, h, dpi, fmt, folder