@echo off
echo ========================================
echo KII Product Tag Generator - Build Script
echo ========================================
echo.
echo This script helps you build both Windows and macOS versions
echo.

echo [1] Building Windows version...
pyinstaller --clean --onefile --windowed --name "KII_ProductTagGenerator" --add-data "kii_logo.png;." --add-data "kiiqr.png;." --add-data "resources;resources" main.py

echo.
echo [2] Copying Windows executable to Universal folder...
copy "dist\KII_ProductTagGenerator.exe" "KII_ProductTagGenerator_Universal\"

echo.
echo [3] Creating universal distribution package...
cd "KII_ProductTagGenerator_Universal"
powershell -Command "Compress-Archive -Path '*' -DestinationPath '../KII_ProductTagGenerator_Universal.zip' -Force"
cd ..

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Windows version: dist\KII_ProductTagGenerator.exe
echo Universal package: KII_ProductTagGenerator_Universal.zip
echo.
echo For macOS version, use GitHub Actions or build on a Mac.
echo See README_Universal.md for instructions.
echo.
pause
