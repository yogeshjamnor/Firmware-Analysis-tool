from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QFileDialog, QTextEdit, QLabel, QFrame, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from core.analyzer import file_info, strings_dump, readelf_header
from pathlib import Path

class AnalyzePage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.last_action = None

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # 1. File Status Header
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("fileHeader")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setFixedHeight(40)
        main_layout.addWidget(self.file_label)

        # 2. Controls Card (Quick Actions)
        controls_card = QFrame()
        controls_card.setObjectName("controlsCard")
        controls_layout = QHBoxLayout(controls_card)
        controls_layout.setContentsMargins(10, 10, 10, 10)

        btn_select = QPushButton("📁 Upload File")
        btn_file = QPushButton("File Info")
        btn_strings = QPushButton("Strings")
        btn_readelf = QPushButton("ReadELF")
        self.btn_save = QPushButton("💾 Download")

        # Connect Logic
        btn_select.clicked.connect(self.select_file)
        btn_file.clicked.connect(self.run_file)
        btn_strings.clicked.connect(self.run_strings)
        btn_readelf.clicked.connect(self.run_readelf)
        self.btn_save.clicked.connect(self.save_output)

        for btn in [btn_select, btn_file, btn_strings, btn_readelf, self.btn_save]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(35)
            controls_layout.addWidget(btn)

        main_layout.addWidget(controls_card)

        # 3. Output Console
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setObjectName("terminal")
        self.output.setPlaceholderText("Analysis results will appear here...")
        main_layout.addWidget(self.output)

        # 4. Manual Command Input Row (The "Dynamic" part)
        cmd_layout = QHBoxLayout()
        cmd_layout.setSpacing(10)
        
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter manual arguments or flags (e.g., -a --wide)...")
        self.cmd_input.setObjectName("cmdInput")
        self.cmd_input.returnPressed.connect(self.run_manual_cmd) # Run on Enter key

        btn_run_cmd = QPushButton("Run Command")
        btn_run_cmd.setObjectName("runBtn")
        btn_run_cmd.setFixedWidth(120)
        btn_run_cmd.clicked.connect(self.run_manual_cmd)

        cmd_layout.addWidget(self.cmd_input)
        cmd_layout.addWidget(btn_run_cmd)
        main_layout.addLayout(cmd_layout)

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            #fileHeader {
                background-color: #313244;
                color: #a6e3a1;
                border-radius: 6px;
                font-weight: bold;
                border: 1px solid #45475a;
            }
            #controlsCard {
                background-color: #1e1e2e;
                border-radius: 8px;
                border: 1px solid #313244;
            }
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover { background-color: #45475a; }
            
            #runBtn {
                background-color: #f9e2af;
                color: #11111b;
                font-weight: bold;
            }
            #runBtn:hover { background-color: #fab387; }

            #terminal {
                background-color: #11111b;
                color: #bac2de;
                border: 1px solid #313244;
                border-radius: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
            #cmdInput {
                background-color: #181825;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas';
            }
        """)

    # --- Logic Methods ---
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f"Selected: {Path(file_path).name}")
            self.output.setHtml("<b style='color: #89b4fa;'>File loaded. Select an action above or enter manual flags.</b>")

    def run_file(self):
        if self.selected_file:
            self.last_action = "fileinfo"
            self.output.setPlainText(file_info(self.selected_file))

    def run_strings(self):
        if self.selected_file:
            self.last_action = "strings"
            self.output.setPlainText(strings_dump(self.selected_file))

    def run_readelf(self):
        if self.selected_file:
            self.last_action = "readelf"
            self.output.setPlainText(readelf_header(self.selected_file))

    def run_manual_cmd(self):
        """Logic for processing the manual QLineEdit input"""
        cmd_text = self.cmd_input.text().strip()
        if not self.selected_file:
            self.output.append("<font color='#f38ba8'>Error: No file selected for command.</font>")
            return
        if not cmd_text:
            return

        self.last_action = "manual"
        # Example: You can append this to your core analyzer or handle it here
        self.output.append(f"\n<b style='color: #f9e2af;'>Executing:</b> {cmd_text} on {Path(self.selected_file).name}")
        
        # Here you would typically pass cmd_text to a function in your 'core'
        # For now, we'll simulate output:
        self.output.append("<i>[Manual command output simulation]</i>")
        self.cmd_input.clear()

    def save_output(self):
        content = self.output.toPlainText()
        if not content or not self.selected_file:
            return

        base_name = Path(self.selected_file).name
        suffix = self.last_action if self.last_action else "analysis"
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Output", f"{base_name}_{suffix}.txt", "Text Files (*.txt)")

        if save_path:
            with open(save_path, "w") as f:
                f.write(content)
            self.output.append(f"\n<b>✅ Saved to:</b> {save_path}")