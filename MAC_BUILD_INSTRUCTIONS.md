# 🍎 Building macOS Version - Step by Step

## 📋 GitHub Setup Required

Since we need to use GitHub Actions to build the macOS version, you'll need to:

### **Step 1: Create GitHub Repository**
1. Go to https://github.com
2. Click **"New repository"**
3. Repository name: `KII_ProductTagGenerator`
4. Description: `Professional Product Tag Generator with QR Codes`
5. Make it **Public** (free)
6. **DO NOT** initialize with README (we already have one)
7. Click **"Create repository"**

### **Step 2: Push Your Code**
After creating the repository, GitHub will show you commands. Run these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/KII_ProductTagGenerator.git
git branch -M main
git push -u origin main
```

### **Step 3: Build macOS Version**
1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. Click **"Build Artifacts"** workflow
4. Click **"Run workflow"**
5. Select branch: `main`
6. Click **"Run workflow"**
7. Wait 5-10 minutes for build to complete

### **Step 4: Download macOS Version**
1. When build finishes, go to Actions → Build Artifacts
2. Click on the completed workflow run
3. Download the **"macos-exec"** artifact
4. Extract the macOS executable

---

## 🚀 Alternative: Manual Instructions for macOS Users

If you can't use GitHub Actions, here are instructions for macOS users to build themselves:

### **For macOS Users (Technical Instructions):**

```bash
# Install Python 3.11 if not installed
# Install dependencies:
pip3 install -r requirements.txt
pip3 install pyinstaller

# Build the application:
pyinstaller --noconfirm --onefile --windowed --add-data "kii_logo.png:." --add-data "kiiqr.png:." --add-data "resources:resources" main.py

# The executable will be in dist/ folder
```

---

## 📦 Complete Universal Package

Once you have the macOS version, add it to the universal folder:

```
KII_ProductTagGenerator_Universal/
├── KII_ProductTagGenerator.exe    (Windows)
├── KII_ProductTagGenerator.app    (macOS - add this)
├── kii_logo.png
├── kiiqr.png
├── resources/
└── README_Universal.md
```

Then recreate the zip file with both versions!

---

## 🎯 Quick Solution

**For now, send the Windows version** - it works for 90% of users. You can build the macOS version later when needed, or when Mac users request it.

The current `KII_ProductTagGenerator_Universal.zip` is ready to share! 🚀
