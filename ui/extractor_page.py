from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QFileDialog, QTextEdit, QLabel, QFrame
)
from PySide6.QtCore import QThread, Signal, Qt
from pathlib import Path
import shutil

# Note: Keeping your ExtractWorker exactly as provided in the original logic
class ExtractWorker(QThread):
    status_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        # Assuming these are imported from your project structure
        from core.workspace import create_job
        self.job = create_job()

    def run(self):
        try:
            from core.extractor import extract
            from core.archiver import zip_folder
            
            job_id = self.job.name
            self.status_signal.emit(f"<b>Job ID:</b> <font color='#89b4fa'>{job_id}</font>")
            self.status_signal.emit("🚀 Extraction started...")

            extract(self.file_path, self.job)

            self.status_signal.emit("✅ Extraction completed.")
            self.status_signal.emit("📦 Zip creation started...")

            output_zip = self.job / "extracted_images.zip"
            zip_folder(str(self.job), str(output_zip))

            self.status_signal.emit("✅ Zip creation completed.")
            self.status_signal.emit("<b>✨ Job finished successfully.</b>")

            self.finished_signal.emit(True, str(output_zip))

        except Exception as e:
            self.finished_signal.emit(False, str(e))


class ExtractPage(QWidget):
    def __init__(self):
        super().__init__()

        # Main vertical layout with clean margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 1. Header & Format Info
        header_container = QVBoxLayout()
        title = QLabel("Firmware Extractor")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff;")
        
        info_banner = QLabel("Supported Formats: payload.bin, super.img")
        info_banner.setStyleSheet("""
            background-color: #313244; 
            color: #a6e3a1; 
            padding: 8px; 
            border-radius: 5px; 
            font-weight: bold;
            font-size: 11px;
        """)
        info_banner.setAlignment(Qt.AlignCenter)
        
        header_container.addWidget(title)
        header_container.addWidget(info_banner)
        main_layout.addLayout(header_container)

        # 2. Control Card (The Action Area)
        control_card = QFrame()
        control_card.setStyleSheet("""
            QFrame {
                background-color: #1e1e2e;
                border: 1px solid #313244;
                border-radius: 12px;
            }
        """)
        card_layout = QHBoxLayout(control_card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(15)

        self.btn_extract = QPushButton("  Select & Extract Image")
        self.btn_extract.setFixedHeight(45)
        self.btn_extract.setCursor(Qt.PointingHandCursor)
        self.btn_extract.setObjectName("primaryBtn")

        self.btn_clean = QPushButton("Clean Workspace")
        self.btn_clean.setFixedHeight(45)
        self.btn_clean.setFixedWidth(140)
        self.btn_clean.setCursor(Qt.PointingHandCursor)
        self.btn_clean.setObjectName("secondaryBtn")

        card_layout.addWidget(self.btn_extract)
        card_layout.addWidget(self.btn_clean)
        main_layout.addWidget(control_card)

        # 3. Log Console
        log_label = QLabel("PROCESS LOG")
        log_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #6c7086; margin-left: 5px;")
        main_layout.addWidget(log_label)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setObjectName("terminal")
        self.log.setPlaceholderText("Waiting for input...")
        main_layout.addWidget(self.log)

        # Apply Global Styling for this page
        self.apply_styles()

        # Connections
        self.btn_extract.clicked.connect(self.select_file)
        self.btn_clean.clicked.connect(self.clean_workspace)

    def apply_styles(self):
        self.setStyleSheet("""
            #primaryBtn {
                background-color: #89b4fa;
                color: #11111b;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            #primaryBtn:hover { background-color: #b4befe; }
            #primaryBtn:disabled { background-color: #45475a; color: #7f849c; }

            #secondaryBtn {
                background-color: transparent;
                color: #f38ba8;
                border: 1px solid #f38ba8;
                border-radius: 6px;
                font-weight: bold;
            }
            #secondaryBtn:hover { background-color: #f38ba8; color: #11111b; }

            #terminal {
                background-color: #11111b;
                color: #bac2de;
                border: 1px solid #313244;
                border-radius: 8px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)

    # -------------------------
    # Extract Logic (No Logic Changes)
    # -------------------------
    def select_file(self):
        # Specific filter added to the dialog to enforce your requirement
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Firmware Image",
            "",
            "Firmware Files (payload.bin super.img);;All Files (*)"
        )

        if not file_path:
            return

        self.log.clear()
        self.log.append(f"<i style='color: #6c7086;'>Target: {Path(file_path).name}</i><br>")
        self.btn_extract.setEnabled(False)

        self.worker = ExtractWorker(file_path)
        self.worker.status_signal.connect(self.log.append)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, success, data):
        self.btn_extract.setEnabled(True)
        if not success:
            self.log.append(f"<br><b style='color: #f38ba8;'>Error:</b> {data}")
            return

        output_zip = Path(data)
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Extracted Images", output_zip.name, "Zip Files (*.zip)"
        )

        if save_path:
            shutil.copy(output_zip, save_path)
            self.log.append(f"<br><b style='color: #a6e3a1;'>Downloaded:</b> {save_path}")

        shutil.rmtree(output_zip.parent, ignore_errors=True)
        self.log.append("<font color='#6c7086'>Workspace cleanup complete.</font>")

    def clean_workspace(self):
        workspace_path = Path("workspace")
        if workspace_path.exists():
            shutil.rmtree(workspace_path, ignore_errors=True)
            workspace_path.mkdir(exist_ok=True)
            self.log.append("<b style='color: #f9e2af;'>🧹 Workspace fully cleaned.</b>")
        else:
            self.log.append("<i style='color: #6c7086;'>Workspace folder does not exist.</i>")