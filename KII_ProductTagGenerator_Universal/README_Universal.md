# KII Product Tag Generator - Universal Distribution

## 🌐 Cross-Platform Application

This folder contains the KII Product Tag Generator for both Windows and macOS platforms.

---

## 📁 Files Included

### Windows Version
- **File**: `KII_ProductTagGenerator.exe`
- **Platform**: Windows 10/11 (64-bit)
- **Size**: 65 MB
- **Type**: Portable executable (no installation required)

### macOS Version
- **Status**: Build via GitHub Actions
- **Platform**: macOS 10.15+ (Intel & Apple Silicon)
- **Instructions**: See "Build macOS Version" below

---

## 🚀 Quick Start

### Windows Users
1. Double-click `KII_ProductTagGenerator.exe`
2. Application starts immediately
3. No installation required

### macOS Users
1. Build the macOS version (see instructions below)
2. Or download from GitHub Releases
3. Drag to Applications folder

---

## 🍎 How to Build macOS Version

Since we're on Windows, use GitHub Actions to build the macOS version:

### Method 1: GitHub Actions (Recommended)
1. Push your code to GitHub repository
2. Go to **Actions** tab in your GitHub repo
3. Click **"Build Artifacts"** workflow
4. Click **"Run workflow"**
5. Wait for build to complete
6. Download the macOS executable from artifacts
7. Copy to this folder

### Method 2: Manual Build (if you have Mac)
```bash
# On macOS terminal:
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --add-data "kii_logo.png:." --add-data "kiiqr.png:." --add-data "resources:resources" main.py
# Copy the resulting executable from dist/ folder
```

---

## 📦 Distribution Package

### Complete Package (when both versions are present):
```
KII_ProductTagGenerator_Universal/
├── KII_ProductTagGenerator.exe          (Windows)
├── KII_ProductTagGenerator.app          (macOS - after build)
├── README_Universal.md                  (this file)
└── assets/                              (logos and resources)
    ├── kii_logo.png
    ├── kiiqr.png
    └── resources/
```

---

## 🎨 Features (Both Platforms)

- ✅ Beautiful Ocean Azure & Midnight Blue themes
- ✅ Professional product tag generation
- ✅ High-resolution QR codes with embedded logos
- ✅ Export to PNG, JPG, PDF (600 DPI)
- ✅ CSV batch processing
- ✅ Real-time preview with zoom
- ✅ Persistent settings
- ✅ Fully offline application

---

## 💻 System Requirements

### Windows
- Windows 10 or later (64-bit)
- No additional dependencies
- 100 MB free disk space

### macOS
- macOS 10.15 (Catalina) or later
- Intel or Apple Silicon Mac
- 100 MB free disk space

---

## 🔧 Settings & Data

### Windows
- Settings stored in: Windows Registry
- Default output folder: Documents folder

### macOS
- Settings stored in: ~/Library/Preferences/
- Default output folder: Documents folder

---

## 📞 Support

For technical support or questions:
- Check the application help menu
- Contact the development team

---

## 📄 Version Information

- **Version**: 1.0
- **Build Date**: February 2026
- **Platforms**: Windows 64-bit, macOS Universal
- **Type**: Desktop Application
- **License**: Proprietary

---

**🎉 Your universal cross-platform application is ready for distribution!**
