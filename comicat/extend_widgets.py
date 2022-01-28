from PyQt6 import QtWidgets, QtCore


class ButtonQLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    button_clicked_signal = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()

    # 可在外部与槽函数连接
    def onclick(self, func):
        self.button_clicked_signal.connect(func)
