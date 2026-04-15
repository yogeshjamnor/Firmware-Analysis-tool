from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QFileDialog, QTextEdit, QLabel, QFrame, QLineEdit
)
from PySide6.QtCore import Qt
from pathlib import Path
import subprocess
import shutil

class MountPage(QWidget):
    def __init__(self):
        super().__init__()

        # --- Configuration ---
        self.workspace_root = Path("workspace")
        self.workspace_root.mkdir(exist_ok=True)
        self.active_job_dir = None
        self.mount_point = None
        self.img_path = None

        # --- UI Setup ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # 1. Header Section
        header_container = QHBoxLayout()
        
        title_vbox = QVBoxLayout()
        header_title = QLabel("System Image Mounter")
        header_title.setStyleSheet("font-size: 26px; font-weight: bold; color: #cdd6f4;")
        
        status_hint = QLabel("Targeting: workspace/mount_job_name")
        status_hint.setStyleSheet("color: #89b4fa; font-size: 12px; font-weight: 500;")
        
        title_vbox.addWidget(header_title)
        title_vbox.addWidget(status_hint)
        
        # 2. Security/Sudo Section (Aligned Right)
        sudo_container = QFrame()
        sudo_container.setObjectName("sudoContainer")
        sudo_layout = QHBoxLayout(sudo_container)
        sudo_layout.setContentsMargins(5, 5, 5, 5)
        sudo_layout.setSpacing(0)

        self.sudo_input = QLineEdit()
        self.sudo_input.setPlaceholderText("Sudo Password...")
        self.sudo_input.setEchoMode(QLineEdit.Password)
        self.sudo_input.setFixedWidth(200)
        self.sudo_input.setObjectName("sudoInput")
        
        self.btn_toggle_pw = QPushButton("👁️")
        self.btn_toggle_pw.setCheckable(True)
        self.btn_toggle_pw.setFixedWidth(40)
        self.btn_toggle_pw.setObjectName("toggleBtn")
        self.btn_toggle_pw.toggled.connect(self.toggle_password)

        sudo_layout.addWidget(self.sudo_input)
        sudo_layout.addWidget(self.btn_toggle_pw)

        header_container.addLayout(title_vbox)
        header_container.addStretch()
        header_container.addWidget(sudo_container)
        main_layout.addLayout(header_container)

        # 3. Action Toolbox (Grouped Card)
        toolbox_card = QFrame()
        toolbox_card.setObjectName("toolboxCard")
        toolbox_layout = QHBoxLayout(toolbox_card)
        toolbox_layout.setContentsMargins(15, 15, 15, 15)
        toolbox_layout.setSpacing(15)

        self.btn_mount = QPushButton("🚀 Mount Image")
        self.btn_download = QPushButton("💾 Export Archive")
        self.btn_unmount = QPushButton("🧹 Secure Cleanup")

        for btn in [self.btn_mount, self.btn_download, self.btn_unmount]:
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            toolbox_layout.addWidget(btn)

        main_layout.addWidget(toolbox_card)

        # 4. Terminal Section
        terminal_header = QLabel("PROCESS LOGS")
        terminal_header.setStyleSheet("color: #6c7086; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        main_layout.addWidget(terminal_header)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setObjectName("terminal")
        self.log.setPlaceholderText("Ready for instructions...")
        main_layout.addWidget(self.log)

        # Logic Connections
        self.btn_mount.clicked.connect(self.mount_process)
        self.btn_download.clicked.connect(self.download_archive)
        self.btn_unmount.clicked.connect(self.cleanup)

        # Initial Button States
        self.btn_download.setEnabled(False)
        self.btn_unmount.setEnabled(False)
        
        self.apply_styles()

    def toggle_password(self, visible):
        self.sudo_input.setEchoMode(QLineEdit.Normal if visible else QLineEdit.Password)
        self.btn_toggle_pw.setText("🔒" if visible else "👁️")

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #1e1e2e; }
            
            #sudoContainer {
                background-color: #181825;
                border: 1px solid #45475a;
                border-radius: 8px;
            }
            
            #sudoInput {
                background-color: transparent;
                color: #cdd6f4;
                border: none;
                padding: 8px;
                font-family: 'Consolas';
            }
            
            #toggleBtn {
                background-color: #313244;
                border: none;
                border-radius: 4px;
                margin: 2px;
                color: #cdd6f4;
            }
            #toggleBtn:hover { background-color: #45475a; }

            #toolboxCard {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 15px;
            }
            
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                padding: 0 20px;
            }
            QPushButton:hover { background-color: #45475a; }
            
            /* Primary Action */
            QPushButton[text="🚀 Mount Image"] {
                background-color: #89b4fa;
                color: #11111b;
            }
            QPushButton[text="🚀 Mount Image"]:hover { background-color: #b4befe; }

            /* Destructive Action */
            QPushButton[text="🧹 Secure Cleanup"] {
                color: #f38ba8;
                border: 1px solid #f38ba8;
                background-color: transparent;
            }
            QPushButton[text="🧹 Secure Cleanup"]:hover { 
                background-color: #f38ba8; 
                color: #11111b; 
            }

            QPushButton:disabled {
                background-color: #11111b;
                color: #585b70;
                border: 1px solid #313244;
            }

            #terminal {
                background-color: #11111b;
                color: #a6e3a1;
                border: 1px solid #313244;
                border-radius: 10px;
                font-family: 'Consolas', 'Courier New';
                font-size: 13px;
                padding: 15px;
                line-height: 1.5;
            }
        """)

    # -------------------------
    # Execution Logic (No Changes)
    # -------------------------
    def run_sudo_cmd(self, cmd_list):
        password = self.sudo_input.text()
        full_cmd = ["sudo", "-S", "-p", ""] + cmd_list
        process = subprocess.Popen(
            full_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate(input=f"{password}\n")
        if process.returncode != 0:
            raise Exception(stderr.strip() if stderr else "System error occurred.")
        return stdout

    def mount_process(self):
        if not self.sudo_input.text():
            self.log.append("<b style='color: #f38ba8;'>❌ ERROR: Sudo Password Required</b>")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select System Image (.img)")
        if not file_path: return

        self.img_path = Path(file_path).resolve()
        self.active_job_dir = self.workspace_root / f"mount_{self.img_path.stem}"
        self.mount_point = self.active_job_dir / "rootfs"
        
        if self.active_job_dir.exists():
            shutil.rmtree(self.active_job_dir, ignore_errors=True)
        self.active_job_dir.mkdir(parents=True)
        self.mount_point.mkdir()

        self.tar_output = self.active_job_dir / "extracted_content.tar"

        try:
            self.log.append(f"<font color='#89b4fa'>[JOB]</font> Started: {self.active_job_dir.name}")
            self.log.append(f"⏳ Mounting <i color='#fab387'>{self.img_path.name}</i> to rootfs...")
            self.run_sudo_cmd(["mount", "-o", "loop,ro", str(self.img_path), str(self.mount_point)])

            self.log.append("⏳ Generating TAR archive in workspace...")
            self.run_sudo_cmd(["tar", "-cf", str(self.tar_output), "-C", str(self.mount_point), "."])

            self.log.append(f"<b style='color: #a6e3a1;'>✅ SUCCESS:</b> Files mapped to workspace/{self.active_job_dir.name}")
            self.btn_download.setEnabled(True)
            self.btn_unmount.setEnabled(True)
        except Exception as e:
            self.log.append(f"<b style='color: #f38ba8;'>❌ MOUNT FAILED:</b> {str(e)}")
            self.cleanup()

    def download_archive(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Archive", f"{self.img_path.stem}.tar", "Tar Files (*.tar)")
        if save_path:
            shutil.copy(self.tar_output, save_path)
            self.log.append(f"<font color='#a6e3a1'>💾 Exported:</font> {save_path}")

    def cleanup(self):
        try:
            if self.mount_point and self.mount_point.exists():
                self.run_sudo_cmd(["umount", str(self.mount_point)])
            
            if self.active_job_dir and self.active_job_dir.exists():
                shutil.rmtree(self.active_job_dir, ignore_errors=True)
                
            self.log.append("<i style='color: #94e2d5;'>🧹 Cleanup complete. Workspace environment reset.</i>")
        except Exception as e:
            self.log.append(f"<font color='#f38ba8'>Cleanup Warning: {str(e)}</font>")
        
        self.btn_download.setEnabled(False)
        self.btn_unmount.setEnabled(False)