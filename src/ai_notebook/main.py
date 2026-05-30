from PySide6.QtWidgets import QApplication, QMainWindow
import sys


app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("AI Notebook")
window.resize(800, 600)
window.show()

sys.exit(app.exec())
