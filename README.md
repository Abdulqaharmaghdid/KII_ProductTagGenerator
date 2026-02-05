# KII Product Tag Generator (Offline, Windows & macOS)

Offline cross-platform desktop application for generating manufacturing-quality product tags with embedded QR codes.

Key features
- Fully offline, no authentication.
- Cross-platform: Windows & macOS (Python + PySide6).
- High-resolution QR codes with embedded KII logo (error correction H).
- Multiple layouts (Vertical, Horizontal) and themes (Light, Dark, Industrial).
- Real-time preview, pixel-perfect alignment.
- Exports: PNG, JPG, PDF (print-ready at configurable DPI / physical size).
- Batch CSV importer for print-runs.
- Settings dialog: default size, DPI, default format, output folder.
- Packaging examples: PyInstaller spec, GitHub Actions workflow.

Prerequisites
- Python 3.10+ (3.11 recommended)
- Place `kii_logo.png` in the project root (next to `main.py`).

Install & run
1. Create & activate venv
   - python -m venv venv
   - Windows: venv\Scripts\activate
   - macOS/Linux: source venv/bin/activate
2. Install requirements
   - pip install -r requirements.txt
3. Run
   - python main.py

CSV batch format
CSV header must include these columns (case-insensitive):
- product_name
- part_number
- qc_status (Approved | Not Approved | Prototype)
- made_in
- catalog_url
Optional:
- output_basename (used as filename base; otherwise sanitized part_number + product_name used)

Packaging
- See `pyinstaller.spec` for a sample spec file.
- GitHub Actions workflow in `.github/workflows/build.yml` demonstrates building with PyInstaller for Windows/macOS.

Notes
- The QR content includes readable product info lines and the catalog URL; scanning opens the link on devices that support it.
- Logo embedding uses a small white background to keep QR scannable.
- No internet access required.

If you want, I can:
- Add an "automatic label sheet" layout for multiple tags on one PDF sheet for printing runs.
- Add a CSV preview/validation screen before batch run.
- Create an installer script (NSIS on Windows, DMG bundling on macOS).
