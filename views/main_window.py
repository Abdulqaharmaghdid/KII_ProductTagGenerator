"""
Main application window — fully updated.

Features:
- Modern, professional UI (menu, toolbar with icon+label, left form card, resizable preview)
- Theme handling uses Fusion style + QPalette + stylesheet override to avoid pure-black fallbacks
- Layout switching (Vertical/Horizontal) updates preview immediately
- Preview zoom, quick-export buttons, CSV batch runner integration
- Uses resources/styles.THEMES for stylesheet content and controller for business logic

Note: This file expects the following project files to exist and provide the referenced APIs:
 - controllers/main_controller.MainController
 - resources/styles.THEMES (dict of stylesheets)
 - views/settings_dialog.SettingsDialog
 - Optional icons under resources/icons/
 - Optional logo files 'kii_logo.png' and 'kiiqr.png' at project root
"""
import os
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QGroupBox,
    QRadioButton, QButtonGroup, QApplication, QProgressDialog, QDialog,
    QSplitter, QScrollArea, QToolBar, QSizePolicy, QSlider, QGraphicsDropShadowEffect,
    QToolButton
)
from PySide6.QtGui import QPixmap, QIcon, QAction, QPalette, QColor
from PySide6.QtCore import Qt, QThread, QSize

from resources.styles import THEMES
from controllers.main_controller import MainController
from views.settings_dialog import SettingsDialog

ICON_SIZE = 22
ICONS_PATH = os.path.join("resources", "icons")


def load_icon(name: str) -> QIcon:
    """Load icon from resources/icons; return empty QIcon if not found."""
    p = os.path.join(ICONS_PATH, name)
    return QIcon(p) if os.path.exists(p) else QIcon()


class ModernPreview(QLabel):
    """Preview canvas with subtle drop shadow."""
    def __init__(self):
        super().__init__()
        self.setObjectName("preview")
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(720, 540)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 70))
        self.setGraphicsEffect(shadow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KII Product Tag Generator — Professional")
        if os.path.exists("kii_logo.png"):
            self.setWindowIcon(QIcon("kii_logo.png"))
        self.resize(1360, 880)

        # Controller (handles rendering, export, batch)
        self.controller = MainController(self)

        # Build UI
        self._build_ui()

        # Apply default theme
        self.apply_theme("Light")

        # Initialize layout state in controller and render preview
        initial_layout = "Vertical" if self.layout_vertical.isChecked() else "Horizontal"
        self.controller.on_layout_changed(initial_layout)
        self.controller.on_form_changed()

        # Batch placeholders
        self._batch_thread: Optional[QThread] = None
        self._batch_worker = None
        self._batch_progress: Optional[QProgressDialog] = None

    # ---------------- UI construction ----------------
    def _build_ui(self):
        self._create_actions()
        self._create_menubar()
        self._create_toolbar()

        central = QWidget()
        main_h = QHBoxLayout(central)
        main_h.setContentsMargins(12, 12, 12, 12)
        self.splitter = QSplitter(Qt.Horizontal)
        main_h.addWidget(self.splitter)
        self.setCentralWidget(central)

        # Left form (scrollable)
        form_card = self._build_form_card()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(form_card)
        scroll.setMinimumWidth(460)
        scroll.setMaximumWidth(540)
        self.splitter.addWidget(scroll)

        # Right preview
        preview_panel = self._build_preview_panel()
        self.splitter.addWidget(preview_panel)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([500, 820])

        # Status bar
        self.status = self.statusBar()
        self.status.showMessage("Ready")

    def _create_actions(self):
        self.act_export_png = QAction(load_icon("export-png.svg"), "Export PNG", self)
        self.act_export_png.setShortcut("Ctrl+S")
        self.act_export_png.triggered.connect(self.on_export_png)

        self.act_export_pdf = QAction(load_icon("export-pdf.svg"), "Export PDF", self)
        self.act_export_pdf.setShortcut("Ctrl+P")
        self.act_export_pdf.triggered.connect(self.on_export_pdf)

        self.act_import_csv = QAction(load_icon("import.svg"), "Import CSV", self)
        self.act_import_csv.setShortcut("Ctrl+I")
        self.act_import_csv.triggered.connect(self.on_import_csv)

        self.act_settings = QAction(load_icon("settings.svg"), "Settings", self)
        self.act_settings.setShortcut("Ctrl+,")
        self.act_settings.triggered.connect(self.on_settings)

        self.act_toggle_layout = QAction(load_icon("layout.svg"), "Toggle Layout", self)
        self.act_toggle_layout.triggered.connect(self._toggle_layout)

    def _create_menubar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.act_export_png)
        file_menu.addAction(self.act_export_pdf)
        file_menu.addSeparator()
        file_menu.addAction(self.act_import_csv)
        file_menu.addSeparator()
        file_menu.addAction(QAction("Quit", self, triggered=self.close))

        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction(self.act_settings)

        view_menu = menubar.addMenu("&View")
        view_menu.addAction(self.act_toggle_layout)

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(QAction("About", self, triggered=self._show_about))

    def _create_toolbar(self):
        tb = QToolBar("Main")
        tb.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        tb.setMovable(False)
        self.addToolBar(tb)

        def add_toolbutton(icon_name, text, handler):
            btn = QToolButton()
            btn.setIcon(load_icon(icon_name))
            btn.setText(text)
            btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            btn.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
            btn.clicked.connect(handler)
            btn.setCursor(Qt.PointingHandCursor)
            tb.addWidget(btn)
            return btn

        add_toolbutton("export-png.svg", "Export PNG", self.on_export_png)
        add_toolbutton("export-pdf.svg", "Export PDF", self.on_export_pdf)
        add_toolbutton("import.svg", "Import CSV", self.on_import_csv)
        tb.addSeparator()
        add_toolbutton("settings.svg", "Settings", self.on_settings)
        tb.addSeparator()
        add_toolbutton("layout.svg", "Toggle Layout", self._toggle_layout)

        # Theme combo in toolbar
        self.tb_theme_combo = QComboBox()
        self.tb_theme_combo.addItems(list(THEMES.keys()))
        self.tb_theme_combo.setFixedWidth(130)
        self.tb_theme_combo.currentTextChanged.connect(lambda t: self.controller.on_theme_changed(t))
        tb.addWidget(self.tb_theme_combo)

    def _build_form_card(self) -> QWidget:
        card = QWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        title = QLabel("Product Tag")
        title.setObjectName("cardTitle")
        card_layout.addWidget(title)

        def add_labelled(widget, label_text):
            card_layout.addWidget(QLabel(label_text))
            card_layout.addWidget(widget)

        # Product Name
        self.product_name_input = QLineEdit()
        self.product_name_input.setPlaceholderText("Product Name")
        self.product_name_input.textChanged.connect(self.controller.on_form_changed)
        add_labelled(self.product_name_input, "Product Name")

        # Part Number
        self.part_number_input = QLineEdit()
        self.part_number_input.setPlaceholderText("Part Number")
        self.part_number_input.textChanged.connect(self.controller.on_form_changed)
        add_labelled(self.part_number_input, "Part Number")

        # QC Status
        self.qc_status_combo = QComboBox()
        self.qc_status_combo.addItems(["Approved", "Not Approved", "Prototype"])
        self.qc_status_combo.currentTextChanged.connect(self.controller.on_form_changed)
        add_labelled(self.qc_status_combo, "QC Status")

        # Made In
        self.made_in_input = QLineEdit()
        self.made_in_input.setPlaceholderText("Made in Kurdistan – Iraq")
        self.made_in_input.textChanged.connect(self.controller.on_form_changed)
        add_labelled(self.made_in_input, "Made In")

        # Catalog / URL
        self.catalog_input = QLineEdit()
        self.catalog_input.setPlaceholderText("https://example.com/catalog")
        self.catalog_input.textChanged.connect(self.controller.on_form_changed)
        add_labelled(self.catalog_input, "Catalog / Product Info (URL)")

        # Layout group
        layout_group = QGroupBox("Layout")
        hl = QHBoxLayout()
        self.layout_vertical = QRadioButton("Vertical")
        self.layout_horizontal = QRadioButton("Horizontal")
        self.layout_vertical.setChecked(True)
        # Use clicked signal to ensure explicit selection handling
        self.layout_vertical.clicked.connect(lambda: self.controller.on_layout_changed("Vertical"))
        self.layout_horizontal.clicked.connect(lambda: self.controller.on_layout_changed("Horizontal"))
        hl.addWidget(self.layout_vertical)
        hl.addWidget(self.layout_horizontal)
        layout_group.setLayout(hl)
        card_layout.addWidget(layout_group)

        # Theme group
        theme_group = QGroupBox("Theme")
        thl = QHBoxLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()))
        self.theme_combo.currentTextChanged.connect(lambda t: self.controller.on_theme_changed(t))
        thl.addWidget(self.theme_combo)
        theme_group.setLayout(thl)
        card_layout.addWidget(theme_group)

        # Export buttons
        export_row = QHBoxLayout()
        self.export_png_btn = QPushButton("Export PNG")
        self.export_jpg_btn = QPushButton("Export JPG")
        self.export_pdf_btn = QPushButton("Export PDF")
        export_row.addWidget(self.export_png_btn)
        export_row.addWidget(self.export_jpg_btn)
        export_row.addWidget(self.export_pdf_btn)
        card_layout.addLayout(export_row)
        self.export_png_btn.clicked.connect(self.on_export_png)
        self.export_jpg_btn.clicked.connect(self.on_export_jpg)
        self.export_pdf_btn.clicked.connect(self.on_export_pdf)

        # Settings & Batch
        bottom_row = QHBoxLayout()
        self.settings_btn = QPushButton("Settings")
        self.import_csv_btn = QPushButton("Import CSV & Run")
        bottom_row.addWidget(self.settings_btn)
        bottom_row.addWidget(self.import_csv_btn)
        card_layout.addLayout(bottom_row)
        self.settings_btn.clicked.connect(self.on_settings)
        self.import_csv_btn.clicked.connect(self.on_import_csv)

        card_layout.addStretch(1)
        return card

    def _build_preview_panel(self) -> QWidget:
        panel = QWidget()
        v = QVBoxLayout(panel)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.addStretch(1)
        zoom_label = QLabel("Zoom")
        top_row.addWidget(zoom_label)
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(25, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(200)
        self.zoom_slider.valueChanged.connect(self._on_zoom_changed)
        top_row.addWidget(self.zoom_slider)
        self.quick_png_btn = QPushButton("PNG")
        self.quick_pdf_btn = QPushButton("PDF")
        self.quick_png_btn.clicked.connect(self.on_export_png)
        self.quick_pdf_btn.clicked.connect(self.on_export_pdf)
        top_row.addWidget(self.quick_png_btn)
        top_row.addWidget(self.quick_pdf_btn)
        v.addLayout(top_row)

        self.preview_widget = ModernPreview()
        self.preview_widget.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #ffffff, stop:1 #fbfdff);"
            "border: 1px solid rgba(14,47,84,0.06); padding: 18px; border-radius: 8px;"
        )
        v.addWidget(self.preview_widget, stretch=1)

        info_row = QHBoxLayout()
        self.preview_info = QLabel("Preview 100%")
        info_row.addWidget(self.preview_info)
        info_row.addStretch(1)
        v.addLayout(info_row)
        return panel

    # ---------------- Preview & theme handling ----------------
    def set_preview_qimage(self, qimage):
        """Set the preview QImage (controller provides). Scales respecting zoom value."""
        zoom = self.zoom_slider.value() / 100.0
        pix = QPixmap.fromImage(qimage)
        w = max(2, int(pix.width() * zoom))
        h = max(2, int(pix.height() * zoom))
        scaled = pix.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview_widget.setPixmap(scaled)
        self.preview_info.setText(f"Preview ({int(zoom*100)}%) — {pix.width()}x{pix.height()} px")

    def _on_zoom_changed(self, _):
        # Re-render a fresh QImage via controller and scale for preview
        self.controller.on_form_changed()

    def apply_theme(self, theme_name: str):
        """
        Apply theme:
         - Force Fusion style for consistent rendering
         - Build and set a comprehensive QPalette to avoid pure-black fallbacks
         - Apply stylesheet from resources.styles and append an override that forces
           widget background colors so nothing falls back to system black.
        """
        app = QApplication.instance()
        if not app:
            return

        # Use Fusion for consistent cross-platform look
        try:
            app.setStyle("Fusion")
        except Exception:
            pass

        name = (theme_name or "Light").strip().lower()

        # Tokenize core colors per theme
        if name == "dark":
            window_color = "#021428"   # dark navy
            base_color = "#0B1B2A"
            text_color = "#E6EEF7"
            accent = "#4BA3FF"
        elif name == "industrial":
            window_color = "#FFFFFF"
            base_color = "#FFFFFF"
            text_color = "#0B1B24"
            accent = "#1F6F8B"
        else:  # light
            window_color = "#F8F8FF"
            base_color = "#F0FFF0"
            text_color = "#0B2B3B"
            accent = "#7EC8FF"

        # Build palette covering many roles to avoid fallbacks
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(window_color))
        palette.setColor(QPalette.WindowText, QColor(text_color))
        palette.setColor(QPalette.Base, QColor(base_color))
        palette.setColor(QPalette.AlternateBase, QColor(window_color))
        palette.setColor(QPalette.ToolTipBase, QColor(text_color))
        palette.setColor(QPalette.ToolTipText, QColor(text_color))
        palette.setColor(QPalette.Text, QColor(text_color))
        palette.setColor(QPalette.Button, QColor(window_color))
        palette.setColor(QPalette.ButtonText, QColor(text_color))
        palette.setColor(QPalette.BrightText, QColor("#ff5555"))
        palette.setColor(QPalette.Link, QColor(accent))
        palette.setColor(QPalette.Highlight, QColor(accent))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))

        # Additional role adjustments
        palette.setColor(QPalette.Light, QColor(window_color).lighter(110))
        palette.setColor(QPalette.Mid, QColor(window_color).darker(110))
        palette.setColor(QPalette.Dark, QColor(window_color).darker(130))
        palette.setColor(QPalette.Shadow, QColor(window_color).darker(150))

        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(text_color).darker(140))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(text_color).darker(140))

        app.setPalette(palette)

        # Apply stylesheet and then a strong override to prevent any leftover black
        stylesheet = THEMES.get(theme_name, "")
        app.setStyleSheet(stylesheet)

        # Force background colors for major widget classes (ensures no hard black)
        override = f"""
        QMainWindow, QWidget, QScrollArea, QFrame {{
            background-color: {window_color} !important;
        }}
        QLineEdit, QPlainTextEdit, QTextEdit, QComboBox {{
            background-color: {base_color} !important;
            color: {text_color} !important;
        }}
        """
        app.setStyleSheet(app.styleSheet() + "\n" + override)

        # Keep theme selectors in sync if UI elements exist
        try:
            self.theme_combo.setCurrentText(theme_name)
            self.tb_theme_combo.setCurrentText(theme_name)
        except Exception:
            pass

    def set_status_message(self, msg: str, error: bool = False):
        self.status.showMessage(msg)
        if error:
            self.status.setStyleSheet("color: #c0392b;")
        else:
            self.status.setStyleSheet("")

    def clear_status(self):
        self.status.clearMessage()

    def show_error_dialog(self, message: str):
        QMessageBox.critical(self, "Error", message)

    # ---------------- Handlers ----------------
    def on_settings(self):
        try:
            self.controller.open_settings()
        except Exception as e:
            QMessageBox.critical(self, "Settings Error", f"Failed to open settings: {e}")

    def on_export_png(self):
        part = self.part_number_input.text().strip() or "product_tag"
        default = os.path.join(self.controller.default_output_folder, f"{part}.png")
        path, _ = QFileDialog.getSaveFileName(self, "Export PNG", default, "PNG Files (*.png)")
        if path:
            ok = self.controller.export(path, "png")
            if ok:
                QMessageBox.information(self, "Export", f"PNG exported successfully:\n{os.path.basename(path)}")

    def on_export_jpg(self):
        part = self.part_number_input.text().strip() or "product_tag"
        default = os.path.join(self.controller.default_output_folder, f"{part}.jpg")
        path, _ = QFileDialog.getSaveFileName(self, "Export JPG", default, "JPEG Files (*.jpg *.jpeg)")
        if path:
            ok = self.controller.export(path, "jpg")
            if ok:
                QMessageBox.information(self, "Export", f"JPG exported successfully:\n{os.path.basename(path)}")

    def on_export_pdf(self):
        part = self.part_number_input.text().strip() or "product_tag"
        default = os.path.join(self.controller.default_output_folder, f"{part}.pdf")
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF", default, "PDF Files (*.pdf)")
        if path:
            ok = self.controller.export(path, "pdf")
            if ok:
                QMessageBox.information(self, "Export", f"PDF exported successfully:\n{os.path.basename(path)}")

    def on_import_csv(self):
        csv_path, _ = QFileDialog.getOpenFileName(self, "Select CSV file", os.path.expanduser("~"), "CSV Files (*.csv)")
        if not csv_path:
            return
        folder = QFileDialog.getExistingDirectory(self, "Select output folder", self.controller.default_output_folder or os.path.expanduser("~"))
        if not folder:
            return
        output_format = self.controller.default_format
        reply = QMessageBox.question(self, "Run Batch", f"Start batch from:\n{csv_path}\nExport format: {output_format}\nOutput folder: {folder}\nProceed?", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        self.setEnabled(False)
        self.controller.import_csv_and_run(csv_path, folder, output_format)

    def _toggle_layout(self):
        if self.layout_vertical.isChecked():
            self.layout_horizontal.setChecked(True)
            self.controller.on_layout_changed("Horizontal")
        else:
            self.layout_vertical.setChecked(True)
            self.controller.on_layout_changed("Vertical")

    def _show_about(self):
        QMessageBox.information(self, "About", "KII Product Tag Generator\nProfessional UI\nOffline • Cross-platform\nBuilt with PySide6")

    # ---------------- Batch lifecycle ----------------
    def batch_running(self, thread: QThread, worker):
        self._batch_thread = thread
        self._batch_worker = worker
        self._batch_progress = QProgressDialog("Running batch...", "Cancel", 0, 100, self)
        self._batch_progress.setWindowModality(Qt.WindowModal)
        self._batch_progress.canceled.connect(self._on_batch_cancel)
        self._batch_progress.show()

    def update_batch_progress(self, pct: int):
        if self._batch_progress:
            self._batch_progress.setValue(pct)

    def _on_batch_cancel(self):
        if self._batch_thread and self._batch_thread.isRunning():
            QMessageBox.information(self, "Cancel", "Batch cancellation requested. Current item will finish.")
        else:
            if self._batch_progress:
                self._batch_progress.close()

    def batch_finished(self, results):
        if self._batch_progress:
            self._batch_progress.setValue(100)
            self._batch_progress.close()
        self._batch_thread = None
        self._batch_worker = None
        self.setEnabled(True)
        success = sum(1 for r in results if r[1])
        failed = [r for r in results if not r[1]]
        msg = f"Batch finished. Success: {success}. Failed: {len(failed)}"
        if failed:
            details = "\n".join(f"{os.path.basename(p)}: {m}" for p, ok, m in failed[:10])
            if len(failed) > 10:
                details += f"\n...and {len(failed)-10} more."
            QMessageBox.warning(self, "Batch Results", f"{msg}\n\nErrors (first 10):\n{details}")
        else:
            QMessageBox.information(self, "Batch Results", msg)