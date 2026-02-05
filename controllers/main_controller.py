"""
Controller: connects UI events with model & utils.
Ensures layout state is normalized and preview refresh is immediate on layout change.
"""
from PySide6.QtCore import Slot, QThread, Signal, QObject
from models.product import Product
from models.settings import AppSettings
from utils.exporter import render_tag_image, export_png_qimage, export_jpg_qimage, export_pdf
from utils.csv_batch import read_csv, run_batch
import os

class BatchWorker(QObject):
    finished = Signal(list)
    progress = Signal(int)

    def __init__(self, rows, out_folder, output_format, layout, theme, output_inches, dpi, logo_path):
        super().__init__()
        self.rows = rows
        self.out_folder = out_folder
        self.output_format = output_format
        self.layout = layout
        self.theme = theme
        self.output_inches = output_inches
        self.dpi = dpi
        self.logo_path = logo_path

    def run(self):
        results = []
        total = len(self.rows)
        for idx, r in enumerate(self.rows):
            res = run_batch([r], self.out_folder, self.output_format, self.layout, self.theme, self.output_inches, self.dpi, self.logo_path)
            results.extend(res)
            self.progress.emit(int(((idx+1)/total)*100))
        self.finished.emit(results)

class MainController:
    def __init__(self, view):
        self.view = view
        self.model = Product()
        self.settings = AppSettings()
        self.layout = "Vertical"   # normalized stored layout
        self.theme = "Light"
        self.output_size_inches = self.settings.get_output_size()
        self.dpi = self.settings.get_dpi()
        self.default_format = self.settings.get_default_format()
        self.default_output_folder = self.settings.get_default_output_folder() or os.path.expanduser("~")

    def update_model_from_view(self):
        self.model.product_name = self.view.product_name_input.text().strip()
        self.model.part_number = self.view.part_number_input.text().strip()
        self.model.qc_status = self.view.qc_status_combo.currentText()
        self.model.made_in = self.view.made_in_input.text().strip()
        self.model.catalog_url = self.view.catalog_input.text().strip()

    def validate_and_get_error(self):
        ok, msg = self.model.validate()
        return ok, msg

    @Slot()
    def on_form_changed(self):
        self.update_model_from_view()
        ok, msg = self.validate_and_get_error()
        if not ok:
            self.view.set_status_message(msg, error=True)
        else:
            self.view.clear_status()
        product_dict = {
            "product_name": self.model.product_name,
            "part_number": self.model.part_number,
            "qc_status": self.model.qc_status,
            "made_in": self.model.made_in,
            "catalog_url": self.model.catalog_url,
        }
        # Render with explicit layout and dpi/settings
        qimage = render_tag_image(product_dict, layout=self.layout, theme=self.theme,
                                  output_inches=self.output_size_inches, dpi=self.dpi)
        self.view.set_preview_qimage(qimage)

    def on_layout_changed(self, layout_name: str):
        # normalize layout name and store
        if not layout_name:
            return
        name = layout_name.strip().capitalize()
        if name not in ("Vertical", "Horizontal"):
            name = "Vertical"
        self.layout = name
        # Immediately re-render preview with new layout
        self.on_form_changed()

    def on_theme_changed(self, theme_name: str):
        self.theme = theme_name
        self.view.apply_theme(theme_name)
        self.on_form_changed()

    def open_settings(self):
        self.view.show_settings_dialog(self.settings)

    def save_settings(self, width: float, height: float, dpi: int, default_format: str, default_folder: str):
        self.settings.set_output_size(width, height)
        self.settings.set_dpi(dpi)
        self.settings.set_default_format(default_format)
        self.settings.set_default_output_folder(default_folder)
        self.output_size_inches = (width, height)
        self.dpi = dpi
        self.default_format = default_format
        self.default_output_folder = default_folder
        self.on_form_changed()

    def export(self, file_path: str, fmt: str, output_inches=None, dpi=None):
        self.update_model_from_view()
        ok, msg = self.validate_and_get_error()
        if not ok:
            self.view.show_error_dialog(msg)
            return False
        output_inches = output_inches or self.output_size_inches
        dpi = dpi or self.dpi
        product_dict = {
            "product_name": self.model.product_name,
            "part_number": self.model.part_number,
            "qc_status": self.model.qc_status,
            "made_in": self.model.made_in,
            "catalog_url": self.model.catalog_url,
        }
        qimage = render_tag_image(product_dict, layout=self.layout, theme=self.theme,
                                  output_inches=output_inches, dpi=dpi)
        try:
            if fmt.lower() == "png":
                export_png_qimage(qimage, file_path, dpi=dpi)
            elif fmt.lower() in ("jpg","jpeg"):
                export_jpg_qimage(qimage, file_path, dpi=dpi)
            elif fmt.lower() == "pdf":
                export_pdf(qimage, file_path, output_inches=output_inches, dpi=dpi)
            else:
                self.view.show_error_dialog(f"Unsupported export format: {fmt}")
                return False
            self.view.set_status_message(f"Exported to {file_path}", error=False)
            return True
        except Exception as e:
            self.view.show_error_dialog(f"Export failed: {e}")
            return False

    def import_csv_and_run(self, csv_path: str, out_folder: str, output_format: str):
        rows, errors = read_csv(csv_path)
        if errors:
            self.view.show_error_dialog("\n".join(errors))
            return
        worker = BatchWorker(rows, out_folder, output_format, self.layout, self.theme, self.output_size_inches, self.dpi, logo_path="kii_logo.png")
        thread = QThread()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(lambda results: self._on_batch_finished(results, thread, worker))
        worker.progress.connect(self.view.update_batch_progress)
        thread.start()
        self.view.batch_running(thread, worker)

    def _on_batch_finished(self, results, thread, worker):
        thread.quit()
        thread.wait()
        self.view.batch_finished(results)