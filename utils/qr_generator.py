"""
QR generation utilities.
Generates high-resolution QR images (PIL) with embedded logo at center,
using high error correction (H) to ensure scannability after overlay.
"""
from PIL import Image
import qrcode
import os

def generate_qr(data: str, size_pixels: int = 2000, logo_path: str = "kii_logo.png", logo_scale: float = 0.18) -> Image.Image:
    """
    Generate a high-res QR code PIL.Image containing `data`.
    - size_pixels: final QR pixel size (square)
    - logo_path: path to logo to embed at center
    - logo_scale: fraction of QR width the logo should occupy (0.12-0.25 recommended)
    Returns a PIL.Image (RGBA).
    """
    # Build QR code with error correction H
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img = qr_img.resize((size_pixels, size_pixels), resample=Image.NEAREST)

    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_max_size = int(size_pixels * logo_scale)
        logo.thumbnail((logo_max_size, logo_max_size), Image.LANCZOS)

        lx = (size_pixels - logo.width) // 2
        ly = (size_pixels - logo.height) // 2

        # Small white rounded rectangle behind logo to improve contrast
        background = Image.new("RGBA", qr_img.size, (255,255,255,0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(background)
        pad = max(6, logo.width // 10)
        rect_box = (lx - pad, ly - pad, lx + logo.width + pad, ly + logo.height + pad)
        radius = max(8, pad//2)
        draw.rounded_rectangle(rect_box, radius=radius, fill=(255,255,255,235))
        qr_img = Image.alpha_composite(qr_img, background)
        qr_img.paste(logo, (lx, ly), logo)

    return qr_img