"""
Updated professional themes:

- Light: beautiful Ocean Azure background with white inputs and modern blue accents.
- Dark: professional Midnight Blue palette with elegant dark tones and blue accents.
- Industrial: plain white background with subtle factory-style accents.

Replace the existing resources/styles.py with this file.
"""
THEMES = {
    "Light": """
        /* Light theme — Ocean Azure */
        QMainWindow { background: #E6F7FF; color: #0A2E4A; font-family: "Inter", "Roboto", "Segoe UI", Arial, sans-serif; font-size: 13px; }
        QWidget { background: transparent; }

        /* Card title */
        QLabel#cardTitle { font-size: 20px; font-weight: 700; color: #0A2E4A; padding-bottom: 6px; }

        /* Groups & labels */
        QGroupBox { font-weight: 700; color: #0A2E4A; margin-top: 8px; }
        QLabel { color: #0A2E4A; }

        /* Inputs */
        QLineEdit, QComboBox {
            background: #FFFFFF; /* pure white for contrast */
            border: 1px solid #A8D0E6; /* ocean azure border */
            padding: 8px;
            border-radius: 8px;
            min-height: 34px;
            color: #0A2E4A;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #3B82C4; /* ocean azure focus */
            outline: none;
        }

        /* Buttons */
        QPushButton {
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #5DADE2, stop:1 #2E86AB);
            color: #FFFFFF;
            border-radius: 8px;
            padding: 8px 12px;
            min-height: 36px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #4A9FD8, stop:1 #2471A3);
        }
        QPushButton:disabled {
            background: #B8D4E8;
            color: #F0F8FF;
        }

        /* Toolbar & ToolButtons */
        QToolBar { background: #F0F8FF; border-bottom: 1px solid #A8D0E6; padding: 6px; }
        QToolButton { padding: 6px 10px; margin: 2px; border-radius: 8px; color: #0A2E4A; }
        QToolButton:hover { background: rgba(93,173,226,0.1); }

        /* Preview */
        QLabel#preview { background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #FFFFFF, stop:1 #F0F8FF); border-radius: 8px; border: 1px solid #A8D0E6; }

        /* Status bar */
        QStatusBar { background: #E6F7FF; border-top: 1px solid #A8D0E6; min-height: 28px; color: #0A2E4A; }

        /* Slider */
        QSlider::groove:horizontal { height: 6px; background: #D0E8F5; border-radius: 4px; }
        QSlider::handle:horizontal { width: 14px; background: #3B82C4; border-radius: 7px; margin: -5px 0; }
    """,

    "Dark": """
        /* Dark theme — Midnight Blue */
        QMainWindow { background: #1A2332; color: #E8EEF7; font-family: "Inter", "Roboto", "Segoe UI", Arial, sans-serif; font-size: 13px; }
        QWidget { background: transparent; }

        /* Card title */
        QLabel#cardTitle { font-size: 20px; font-weight: 700; color: #E8EEF7; padding-bottom: 6px; }

        QGroupBox { font-weight: 700; color: #DCE4F0; margin-top: 8px; }
        QLabel { color: #E8EEF7; }

        /* Inputs */
        QLineEdit, QComboBox {
            background: #2A3441; /* midnight blue input */
            border: 1px solid #3D4A5C; /* midnight blue border */
            padding: 8px;
            border-radius: 8px;
            min-height: 34px;
            color: #E8EEF7;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #5A7FDB; /* midnight blue focus */
            outline: none;
        }

        /* Buttons */
        QPushButton {
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #4A6FA5, stop:1 #2C4B7C);
            color: #FFFFFF;
            border-radius: 8px;
            padding: 8px 12px;
            min-height: 36px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #3D5E94, stop:1 #233D6B);
        }
        QPushButton:disabled {
            background: #3A4556;
            color: #9CA8B8;
        }

        /* Toolbar */
        QToolBar { background: #1A2332; border-bottom: 1px solid #3D4A5C; padding: 6px; }
        QToolButton { padding: 6px 10px; margin: 2px; border-radius: 8px; color: #E8EEF7; }
        QToolButton:hover { background: rgba(90,127,219,0.1); }

        /* Preview */
        QLabel#preview { background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #1A2332, stop:1 #242F3F); border-radius: 8px; border: 1px solid #3D4A5C; }

        /* Status bar */
        QStatusBar { background: #1A2332; border-top: 1px solid #3D4A5C; min-height: 28px; color: #DCE4F0; }

        /* Slider */
        QSlider::groove:horizontal { height: 6px; background: #2A3441; border-radius: 4px; }
        QSlider::handle:horizontal { width: 14px; background: #5A7FDB; border-radius: 7px; margin: -5px 0; }
    """,

    "Industrial": """
        /* Industrial theme — plain white background with subtle factory accents */
        QMainWindow { background: #FFFFFF; color: #0B1B24; font-family: "Roboto", "Inter", "Segoe UI", Arial, sans-serif; font-size: 13px; }
        QWidget { background: transparent; }

        QLabel#cardTitle { font-size: 20px; font-weight: 700; color: #0B1B24; padding-bottom: 6px; }
        QGroupBox { font-weight: 700; color: #0B1B24; margin-top: 8px; }
        QLabel { color: #0B1B24; }

        /* Inputs */
        QLineEdit, QComboBox {
            background: #FFFFFF;
            border: 1px solid #E6EEF2;
            padding: 8px;
            border-radius: 6px;
            min-height: 34px;
            color: #0B1B24;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #2F97A8;
            outline: none;
        }

        /* Buttons */
        QPushButton {
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #1F6F8B, stop:1 #154F63);
            color: #FFFFFF;
            border-radius: 8px;
            padding: 8px 12px;
            min-height: 36px;
        }
        QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #185260, stop:1 #123f47); }
        QPushButton:disabled { background: #B7D0D6; color: #F0F8F9; }

        /* Toolbar */
        QToolBar { background: #FFFFFF; border-bottom: 1px solid #EAEFF1; padding: 6px; }
        QToolButton { padding: 6px 10px; margin: 2px; border-radius: 8px; color: #0B1B24; }
        QToolButton:hover { background: rgba(31,111,139,0.04); }

        /* Preview */
        QLabel#preview { background: #FFFFFF; border-radius: 6px; border: 1px solid #E6EEF2; }

        /* Status bar */
        QStatusBar { background: #FFFFFF; border-top: 1px solid #EAEFF1; min-height: 28px; color: #0B1B24; }

        /* Slider */
        QSlider::groove:horizontal { height: 6px; background: #EEF6F8; border-radius: 4px; }
        QSlider::handle:horizontal { width: 14px; background: #1F6F8B; border-radius: 7px; margin: -5px 0; }
    """,
}