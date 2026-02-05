"""
Product model: dataclass-like holder for product tag data and validation.
"""
from dataclasses import dataclass
from typing import Tuple
import validators

QC_STATUSES = ["Approved", "Not Approved", "Prototype"]

@dataclass
class Product:
    product_name: str = ""
    part_number: str = ""
    qc_status: str = QC_STATUSES[0]
    made_in: str = ""
    catalog_url: str = ""

    def validate(self) -> Tuple[bool, str]:
        if not self.product_name.strip():
            return False, "Product Name must not be empty."
        if not self.part_number.strip():
            return False, "Part Number must not be empty."
        if self.qc_status not in QC_STATUSES:
            return False, f"QC Status must be one of {QC_STATUSES}."
        if self.catalog_url.strip():
            if not validators.url(self.catalog_url.strip()):
                return False, "Catalog / Product Information Link must be a valid URL."
        return True, ""