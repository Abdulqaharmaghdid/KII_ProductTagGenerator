"""
Rendering and export utilities — supports both Vertical and Horizontal professional layouts.

Behavior:
- QR content: Part Number + Catalog URL only.
- Supports layout="Vertical" (stacked top logo + QR, rows below) and layout="Horizontal"
  (two-column professional layout: left = logo + label/value rows, right = large QR).
- High-resolution defaults (dpi=600) and large QR pixel generation for crisp printing.
- QR center image uses 'kiiqr.png' if present, otherwise falls back to 'kii_logo.png'.
- Values use monospace for consistent appearance; labels and values are aligned side-by-side.
- Subtle frame and separators for a clean industrial look.
- Robust QImage <-> PIL conversion using QBuffer to avoid memoryview/asstring issues.
"""
from typing import Tuple
import os
import io

from PySide6.QtGui import QImage, QPainter, QColor, QFont, QPixmap
from PySide6.QtCore import Qt, QBuffer, QIODevice, QByteArray
from PIL import Image
from PIL.ImageQt import ImageQt
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

from utils.qr_generator import generate_qr

# QC colors
QC_COLORS = {
    "Approved": QColor("#2ecc71"),
    "Not Approved": QColor("#e74c3c"),
    "Prototype": QColor("#e67e22"),
}


def build_qr_pil_for_product(product_data: dict, qr_pixels: int = 2400, qr_logo_path: str = "kiiqr.png"):
    """
    Build a QR PIL image containing:
      - Part Number
      - Catalog URL (if present)
    Uses qr_logo_path for center logo if available.
    """
    part = product_data.get("part_number", "")
    catalog = product_data.get("catalog_url", "")
    lines = [f"Part Number: {part}"]
    if catalog:
        lines.append(catalog)
    data = "\n".join(lines)

    logo_path = qr_logo_path if os.path.exists(qr_logo_path) else ("kii_logo.png" if os.path.exists("kii_logo.png") else "")
    qr = generate_qr(data, size_pixels=qr_pixels, logo_path=logo_path, logo_scale=0.18)
    return qr


def qimage_to_pil(qimage: QImage) -> Image.Image:
    """
    Convert QImage -> PIL.Image by saving PNG to QBuffer and opening with Pillow.
    """
    ba = QByteArray()
    buf = QBuffer(ba)
    buf.open(QIODevice.WriteOnly)
    qimage.save(buf, "PNG")
    buf.close()
    png_bytes = bytes(ba)
    pil = Image.open(io.BytesIO(png_bytes))
    return pil.convert("RGBA")


def pil_to_qimage(pil_img: Image.Image) -> QImage:
    qim = ImageQt(pil_img).copy()
    return QImage(qim)


def _draw_label_value(painter: QPainter, label: str, value: str,
                      label_rect: Tuple[int, int, int, int],
                      value_rect: Tuple[int, int, int, int],
                      label_font: QFont, value_font: QFont,
                      muted: QColor, text: QColor, qc=False):
    """
    Helper to draw a label (muted) and value (monospace) inside given rects.
    If qc=True, value contains QC status and we draw a colored indicator.
    """
    lx, ly, lw, lh = label_rect
    vx, vy, vw, vh = value_rect
    painter.setFont(label_font)
    painter.setPen(muted)
    painter.drawText(lx, ly, lw, lh, Qt.AlignLeft | Qt.AlignVCenter, label)

    painter.setFont(value_font)
    painter.setPen(text)
    if qc:
        qc_text = value
        indicator_r = max(6, int(lh * 0.28))
        ind_x = vx
        ind_y = vy + int((vh - indicator_r) / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QC_COLORS.get(qc_text, QColor("#083838")))
        painter.drawEllipse(ind_x, ind_y, indicator_r, indicator_r)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(text)
        painter.drawText(ind_x + indicator_r + 8, vy, vw - indicator_r - 12, vh, Qt.AlignLeft | Qt.AlignVCenter, qc_text)
    else:
        painter.drawText(vx, vy, vw, vh, Qt.AlignLeft | Qt.AlignVCenter, value)


def render_tag_image(
    product: dict,
    layout: str = "Vertical",
    theme: str = "Light",
    output_inches: Tuple[float, float] = (4.0, 3.0),
    dpi: int = 600,
    logo_path: str = "kii_logo.png",
    qr_logo_path: str = "kiiqr.png",
) -> QImage:
    """
    Render professional product tag as QImage.

    layout: "Vertical" or "Horizontal" (case-insensitive)
    """
    layout = (layout or "Vertical").lower()
    width_in, height_in = output_inches
    px_w = int(width_in * dpi)
    px_h = int(height_in * dpi)

    img = QImage(px_w, px_h, QImage.Format_ARGB32)

    # Theme palette
    if theme and theme.lower() == "dark":
        bg = QColor("#1A2332")
        text = QColor("#E8EEF7")
        muted = QColor("#DCE4F0")
        separator = QColor(255, 255, 255, 30)
        frame_color = QColor(255, 255, 255, 120)
    elif theme and theme.lower() == "industrial":
        bg = QColor("#ffffff")
        text = QColor("#083838")
        muted = QColor("#6b7478")
        separator = QColor(0, 0, 0, 30)
        frame_color = QColor(8, 56, 56, 150)
    else:  # Light
        bg = QColor("#ffffff")
        text = QColor("#083838")
        muted = QColor("#6b7478")
        separator = QColor(0, 0, 0, 30)
        frame_color = QColor(8, 56, 56, 150)

    img.fill(bg)
    painter = QPainter(img)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)

    # Draw rounded frame
    frame_padding = max(4, int(px_w * 0.01))
    frame_rect_x = frame_padding
    frame_rect_y = frame_padding
    frame_rect_w = px_w - 2 * frame_padding
    frame_rect_h = px_h - 2 * frame_padding
    frame_pen = painter.pen()
    frame_pen.setWidth(max(2, int(px_w * 0.004)))
    frame_pen.setColor(frame_color)
    painter.setPen(frame_pen)
    painter.setBrush(Qt.NoBrush)
    painter.drawRoundedRect(frame_rect_x, frame_rect_y, frame_rect_w, frame_rect_h, 12, 12)

    # Inner area
    pad_x = int(px_w * 0.04)
    pad_y = int(px_h * 0.04)
    inner_x = frame_rect_x + pad_x
    inner_y = frame_rect_y + pad_y
    inner_w = frame_rect_w - 2 * pad_x
    inner_h = frame_rect_h - 2 * pad_y

    # Fonts
    label_font = QFont("Sans Serif", max(8, int(px_w * 0.028)))
    label_font.setBold(False)
    value_font = QFont("Monospace", max(10, int(px_w * 0.035)))
    value_font.setStyleHint(QFont.Monospace)
    value_font.setBold(False)

    # Shared row settings
    rows = ["Product Name", "Part Number", "QC Status", "Made In"]
    num_rows = len(rows)

    if layout == "horizontal":
        # Horizontal layout:
        # Left column: logo at top (smaller, nudged left), below it label/value rows (two-column inside left column)
        # Right column: large QR centered vertically.
        left_w = int(inner_w * 0.60)
        right_w = inner_w - left_w
        left_x = inner_x
        left_y = inner_y
        right_x = inner_x + left_w
        right_y = inner_y

        # Logo area in left column - top portion (approx 40% of left column height)
        logo_area_h = int(inner_h * 0.40)
        logo_max_w = int(left_w * 0.78)
        logo_max_h = int(logo_area_h * 0.78)
        center_x = left_x + int((left_w - logo_max_w) / 2)
        nudge_left = max(0, int(left_w * 0.08))
        logo_x = max(left_x + 2, center_x - nudge_left)
        logo_y = left_y + int((logo_area_h - logo_max_h) / 2)
        if os.path.exists(logo_path):
            logo_pix = QPixmap(logo_path)
            logo_pix = logo_pix.scaled(logo_max_w, logo_max_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(logo_x, logo_y, logo_pix)
        else:
            painter.setPen(muted)
            ph_font = QFont("Sans Serif", max(10, int(px_w * 0.032)))
            ph_font.setBold(False)
            painter.setFont(ph_font)
            painter.drawText(logo_x, logo_y, logo_max_w, logo_max_h, Qt.AlignCenter, "KII Logo")

        # Prepare rows area inside left column below logo
        rows_y = left_y + logo_area_h + int(px_h * 0.02)
        total_row_area = inner_h - logo_area_h - int(px_h * 0.02)
        row_h = int(total_row_area / num_rows)

        label_col_w = int(left_w * 0.45)
        gutter = int(px_w * 0.04)
        value_col_x = left_x + label_col_w + gutter
        value_col_w = left_w - label_col_w - gutter - 6

        # Draw each label/value row inside left column
        for i, label in enumerate(rows):
            ry = rows_y + i * row_h
            label_rect = (left_x + 4, ry, label_col_w - 8, row_h)
            value_rect = (value_col_x + 2, ry, value_col_w, row_h)
            if label == "QC Status":
                _draw_label_value(painter, label, product.get("qc_status", ""), label_rect, value_rect, label_font, value_font, muted, text, qc=True)
            else:
                _draw_label_value(painter, label, product.get(label.lower().replace(" ", "_"), ""), label_rect, value_rect, label_font, value_font, muted, text, qc=False)
            # separator
            sep_y = ry + row_h
            sep_pen = painter.pen()
            sep_pen.setColor(separator)
            sep_pen.setWidth(1)
            painter.setPen(sep_pen)
            painter.drawLine(left_x, sep_y, left_x + left_w, sep_y)
            painter.setPen(text)

        # Right column: draw large QR
        qr_margin = int(min(right_w, inner_h) * 0.06)
        qr_area_w = right_w - 2 * qr_margin
        qr_area_h = inner_h - 2 * qr_margin
        qr_pixels = max(2600, int(min(qr_area_w, qr_area_h) * 4))
        qr_pil = build_qr_pil_for_product(product, qr_pixels=qr_pixels, qr_logo_path=qr_logo_path)
        qr_qimg = ImageQt(qr_pil).copy()
        qr_pix = QPixmap.fromImage(qr_qimg)
        qr_pix = qr_pix.scaled(qr_area_w, qr_area_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # center QR in right column with slight right offset for balance
        qr_offset = int(left_w * 0.03)
        qx = right_x + qr_margin + int((qr_area_w - qr_pix.width()) / 2) + qr_offset
        qy = right_y + qr_margin + int((qr_area_h - qr_pix.height()) / 2)
        painter.drawPixmap(qx, qy, qr_pix)

    else:
        # Vertical layout (stacked top area logo + QR, followed by label/value rows in two columns)
        top_h = int(inner_h * 0.38)
        bottom_y = inner_y + top_h + int(px_h * 0.02)
        # Top split: left logo, right QR
        left_w = int(inner_w * 0.58)
        right_w = inner_w - left_w
        top_x = inner_x
        top_y = inner_y

        # Logo smaller and nudged left
        logo_max_w = int(left_w * 0.70)
        logo_max_h = int(top_h * 0.70)
        center_x = top_x + int((left_w - logo_max_w) / 2)
        nudge_left = max(0, int(left_w * 0.10))
        logo_x = max(top_x + 2, center_x - nudge_left)
        logo_y = top_y + int((top_h - logo_max_h) / 2)
        if os.path.exists(logo_path):
            logo_pix = QPixmap(logo_path)
            logo_pix = logo_pix.scaled(logo_max_w, logo_max_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(logo_x, logo_y, logo_pix)
        else:
            painter.setPen(muted)
            ph_font = QFont("Sans Serif", max(10, int(px_w * 0.032)))
            ph_font.setBold(False)
            painter.setFont(ph_font)
            painter.drawText(logo_x, logo_y, logo_max_w, logo_max_h, Qt.AlignCenter, "KII Logo")

        # QR on right of top area
        qr_margin = int(min(right_w, top_h) * 0.08)
        qr_area_w = right_w - 2 * qr_margin
        qr_area_h = top_h - 2 * qr_margin
        qr_pixels = max(2400, int(min(qr_area_w, qr_area_h) * 4))
        qr_pil = build_qr_pil_for_product(product, qr_pixels=qr_pixels, qr_logo_path=qr_logo_path)
        qr_qimg = ImageQt(qr_pil).copy()
        qr_pix = QPixmap.fromImage(qr_qimg)
        qr_pix = qr_pix.scaled(qr_area_w, qr_area_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        qr_x = top_x + left_w + qr_margin + int((qr_area_w - qr_pix.width()) / 2)
        qr_y = top_y + qr_margin + int((qr_area_h - qr_pix.height()) / 2)
        painter.drawPixmap(qr_x, qr_y, qr_pix)

        # Bottom rows area (two-column rows: label left, value right)
        total_row_area = inner_h - top_h - int(px_h * 0.02)
        row_h = int(total_row_area / num_rows)
        label_col_w = int(inner_w * 0.36)
        gutter = int(px_w * 0.05)
        value_col_x = inner_x + label_col_w + gutter
        value_col_w = inner_w - label_col_w - gutter

        for i, label in enumerate(rows):
            ry = bottom_y + i * row_h
            label_rect = (inner_x + 4, ry, label_col_w - 8, row_h)
            value_rect = (value_col_x + 2, ry, value_col_w - 8, row_h)
            if label == "QC Status":
                _draw_label_value(painter, label, product.get("qc_status", ""), label_rect, value_rect, label_font, value_font, muted, text, qc=True)
            else:
                key = label.lower().replace(" ", "_")
                _draw_label_value(painter, label, product.get(key, ""), label_rect, value_rect, label_font, value_font, muted, text, qc=False)
            # separator
            sep_y = ry + row_h
            sep_pen = painter.pen()
            sep_pen.setColor(separator)
            sep_pen.setWidth(1)
            painter.setPen(sep_pen)
            painter.drawLine(inner_x, sep_y, inner_x + inner_w, sep_y)
            painter.setPen(text)

    painter.end()
    return img


def export_png_qimage(qimage: QImage, path: str, dpi: int = 600):
    pil = qimage_to_pil(qimage)
    pil.save(path, format="PNG", dpi=(dpi, dpi))


def export_jpg_qimage(qimage: QImage, path: str, dpi: int = 600, quality: int = 95):
    pil = qimage_to_pil(qimage)
    if pil.mode == "RGBA":
        pil = pil.convert("RGB")
    pil.save(path, format="JPEG", dpi=(dpi, dpi), quality=quality)


def export_pdf(qimage: QImage, path: str, output_inches: Tuple[float, float] = (4.0, 3.0), dpi: int = 600):
    pil = qimage_to_pil(qimage)
    buf = io.BytesIO()
    pil.save(buf, format="PNG", dpi=(dpi, dpi))
    buf.seek(0)
    w_in, h_in = output_inches
    c = canvas.Canvas(path, pagesize=(w_in * inch, h_in * inch))
    img_reader = ImageReader(buf)
    c.drawImage(img_reader, 0, 0, width=w_in * inch, height=h_in * inch, preserveAspectRatio=True, mask="auto")
    c.showPage()
    c.save()