from PyQt6 import QtWidgets, QtCore, QtGui


class ButtonQLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    button_clicked_signal = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, me):
        self.button_clicked_signal.emit()

    # 可在外部与槽函数连接
    def onclick(self, func):
        self.button_clicked_signal.connect(func)


class CheckableComboBox(QtWidgets.QComboBox):
    # once there is a checkState set, it is rendered
    # here we assume default Unchecked
    def addItem(self, state, *__args):
        super(CheckableComboBox, self).addItem(*__args)
        item = self.model().item(self.count() - 1, 0)
        item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        item.setCheckState(state)

    def item_checked(self, index):
        item: QtGui.QStandardItem = self.model().item(index, 0)
        return item.checkState() == QtCore.Qt.CheckState.Checked
