"""
CSV batch import and processing for print runs.
Reads a CSV, validates rows, and orchestrates export for each row.
"""
import csv
import os
import re
from typing import List, Dict, Tuple
from utils.exporter import render_tag_image, export_png_qimage, export_jpg_qimage, export_pdf

def sanitize_filename(name: str) -> str:
    # Remove problematic characters
    name = re.sub(r'[\\/:"*?<>|]+', "_", name)
    name = re.sub(r'\s+', "_", name).strip("_")
    return name[:200]

def read_csv(filepath: str) -> Tuple[List[Dict[str,str]], List[str]]:
    """
    Read CSV and return list of rows as dict (keys lower-cased).
    Also return list of errors (strings) if rows are malformed.
    """
    rows = []
    errors = []
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = [h.strip().lower() for h in reader.fieldnames or []]
        required = {"product_name", "part_number", "qc_status"}
        if not required.issubset(set(headers)):
            errors.append(f"CSV missing required headers: {required - set(headers)}")
            return [], errors
        for i, row in enumerate(reader, start=2):
            # normalize keys to lower-case
            r = {k.strip().lower(): (v or "").strip() for k, v in row.items()}
            # basic validation
            if not r.get("product_name") or not r.get("part_number"):
                errors.append(f"Row {i}: missing product_name or part_number")
                continue
            rows.append(r)
    return rows, errors

def run_batch(rows: List[Dict[str,str]], out_folder: str, output_format: str, layout: str, theme: str,
              output_inches: Tuple[float,float], dpi: int, logo_path: str = "kii_logo.png") -> List[Tuple[str, bool, str]]:
    """
    Run batch exports. Returns list of tuples: (output_path, success_bool, message)
    """
    results = []
    os.makedirs(out_folder, exist_ok=True)
    for r in rows:
        base = r.get("output_basename") or f"{r.get('part_number')}_{r.get('product_name')}"
        base = sanitize_filename(base)
        filename = f"{base}.{output_format.lower()}"
        out_path = os.path.join(out_folder, filename)
        try:
            product_dict = {
                "product_name": r.get("product_name", ""),
                "part_number": r.get("part_number", ""),
                "qc_status": r.get("qc_status", ""),
                "made_in": r.get("made_in", ""),
                "catalog_url": r.get("catalog_url", ""),
            }
            qimage = render_tag_image(product_dict, layout=layout, theme=theme,
                                      output_inches=output_inches, dpi=dpi, logo_path=logo_path)
            if output_format.lower() == "png":
                export_png_qimage(qimage, out_path, dpi=dpi)
            elif output_format.lower() in ("jpg","jpeg"):
                export_jpg_qimage(qimage, out_path, dpi=dpi)
            elif output_format.lower() == "pdf":
                export_pdf(qimage, out_path, output_inches=output_inches, dpi=dpi)
            else:
                results.append((out_path, False, f"Unsupported format {output_format}"))
                continue
            results.append((out_path, True, "OK"))
        except Exception as ex:
            results.append((out_path, False, str(ex)))
    return results