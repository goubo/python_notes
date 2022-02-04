import sys

from PyQt6 import QtWidgets

from ui_windows import MainWindowWidget, MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindowWidget = MainWindowWidget(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
