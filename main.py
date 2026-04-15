import sys
import ctypes
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # 1. Set Application Identity
    app_name = "Firmware Toolkit"
    app.setApplicationName(app_name)
    app.setApplicationDisplayName(app_name)
    app.setOrganizationName("YourLabName")
    app.setOrganizationDomain("yourlab.com")

    # 2. Set Application Icon
    # Ensure 'icon.png' is in your project root or provide the full path
    icon_path = Path(__file__).parent  / "icon.png"
    if icon_path.exists():
        app_icon = QIcon(str(icon_path))
        app.setWindowIcon(app_icon)
    else:
        print(f"Warning: Icon not found at {icon_path}")

    # 3. Windows Taskbar Fix (Crucial for Windows)
    # This prevents Windows from grouping your app under the Python icon
    if sys.platform == 'win32':
        myappid = f'mycompany.myproduct.subproduct.version' # Unique string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = MainWindow()
    window.setWindowTitle(app_name) # Reinforce title
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()