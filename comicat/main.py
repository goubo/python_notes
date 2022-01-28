import sys

from PyQt6 import QtWidgets

from ui_windows import MainWindowWidget

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    mainWindowWidget = MainWindowWidget(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
