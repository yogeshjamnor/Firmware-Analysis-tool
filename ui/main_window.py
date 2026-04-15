from PySide6.QtWidgets import QMainWindow, QTabWidget
from ui.extractor_page import ExtractPage
from ui.mount_page import MountPage
from ui.analyze_page import AnalyzePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Firmware Lab")
        self.resize(1000, 700) # Give the app a professional default size

        # Initialize the Tab Widget
        tabs = QTabWidget()
        
        # Keep your exact logic/imports
        tabs.addTab(ExtractPage(), "Extract")
        tabs.addTab(MountPage(), "Mount")
        tabs.addTab(AnalyzePage(), "Analyze")

        self.setCentralWidget(tabs)
        
        # Apply the "Pro" UI Styling
        self.apply_modern_styling(tabs)

    def apply_modern_styling(self, tabs):
        self.setStyleSheet("""
            /* Main Window Background */
            QMainWindow {
                background-color: #121212;
            }

            /* Tab Bar Styling */
            QTabWidget::pane {
                border: 1px solid #2d2d2d;
                background-color: #1e1e1e;
                top: -1px; /* Overlap border to look seamless */
                border-radius: 4px;
            }

            QTabBar::tab {
                background-color: #252526;
                color: #969696;
                padding: 12px 25px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-family: "Segoe UI", sans-serif;
                font-size: 13px;
                font-weight: 500;
            }

            QTabBar::tab:hover {
                background-color: #2d2d30;
                color: #ffffff;
            }

            QTabBar::tab:selected {
                background-color: #1e1e1e;
                color: #007acc; /* Modern Blue accent */
                border-bottom: 2px solid #007acc;
                font-weight: bold;
            }

            /* Style for the content area of each page */
            QWidget {
                color: #e1e1e1;
                font-family: "Segoe UI";
            }
        """)