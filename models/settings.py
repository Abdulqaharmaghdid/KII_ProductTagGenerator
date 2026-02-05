"""
Persistent settings via QSettings (cross-platform).
Holds default output size (inches), DPI, default export format and default output folder.
"""
from PySide6.QtCore import QSettings

class AppSettings:
    def __init__(self):
        # Organization and application names used by QSettings for platform-specific storage
        QSettings.setDefaultFormat(QSettings.NativeFormat)
        self._settings = QSettings("KII", "ProductTagGenerator")

    def get_output_size(self):
        # stored as "width,height" in inches
        s = self._settings.value("output_size", "4.0,3.0")
        w, h = s.split(",")
        return float(w), float(h)

    def set_output_size(self, width: float, height: float):
        self._settings.setValue("output_size", f"{width},{height}")

    def get_dpi(self):
        # Increased default DPI to 600 for higher-resolution exports
        return int(self._settings.value("dpi", 600))

    def set_dpi(self, dpi: int):
        self._settings.setValue("dpi", dpi)

    def get_default_format(self):
        return self._settings.value("default_format", "pdf")

    def set_default_format(self, fmt: str):
        self._settings.setValue("default_format", fmt)

    def get_default_output_folder(self):
        return self._settings.value("default_output_folder", "")

    def set_default_output_folder(self, folder: str):
        self._settings.setValue("default_output_folder", folder)