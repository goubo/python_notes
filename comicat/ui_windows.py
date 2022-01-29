from typing import List

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox, QScrollArea, QTabWidget, QTabBar, QHBoxLayout, \
    QCheckBox, QPushButton, QMessageBox, QProgressBar

import constant
from download_task import DownloadTask
from entity import ComicInfo, ChapterInfo
from extend_widgets import ButtonQLabel


class DownLoadTaskWidget(QWidget):
    update_task_signa = QtCore.pyqtSignal()

    def __init__(self, task: DownloadTask):
        super().__init__()
        self.task = task
        task.widget = self
        self.setMinimumHeight(40)
        self.groupBox = QGroupBox(self)

        self.title = QLabel(self.groupBox)
        self.title.setText(task.comicInfo.title + task.chapterInfo.title)
        self.title.setGeometry(10, 5, 300, 20)
        # 下载进度
        self.schedule = QLabel(self.groupBox)
        self.schedule.setText(
            f"总页数:{len(self.task.imageInfos)}  已下载:{len(self.task.success)}  下载失败:{len(self.task.error)}")
        self.schedule.setGeometry(310, 5, 200, 20)
        # 进度条
        self.pbar = QProgressBar(self.groupBox)
        self.pbar.setGeometry(10, 25, 600, 10)
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(len(task.imageInfos))
        self.pbar.setValue(0)
        self.update_task_signa.connect(self.update_task_thread)
        # 状态
        self.status = QLabel(self.groupBox)
        self.status.setGeometry(620, 12, 70, 20)
        self.status.setText("等待下载")
        # 按钮
        self.button = ButtonQLabel(self.groupBox)
        self.button.setGeometry(700, 12, 100, 20)
        self.button.setText("暂停")
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        button_font = QtGui.QFont()
        button_font.setUnderline(True)
        self.button.setFont(button_font)
        self.button.onclick(self.button_click)

    def change_status(self):
        # 按钮逻辑
        if self.task.status == 0:
            self.status.setText("等待下载")
            self.button.setVisible(False)
        elif self.task.status == 1:
            self.button.setVisible(True)
            self.button.setText("暂停")
            self.status.setText("正在下载")
        elif self.task.status == 2:
            self.button.setVisible(True)
            self.button.setText("继续")
            self.status.setText("暂停")
        elif self.task.status == -1:
            # 判断是否下载完成
            if len(self.task.error) < 1:
                self.button.setVisible(False)
                self.status.setText("下载完成")
            else:
                self.button.setVisible(True)
                self.button.setText("下载错误")
                self.status.setText("重试")

    def button_click(self):
        if self.task.status == 1:
            self.task.status = 2
        elif self.task.status == 2:
            self.task.status = 0
            constant.SERVICE.add_task(self.task)
        elif self.task.status == -1:
            constant.SERVICE.add_task(self.task)
        self.change_status()

    def update_task_thread(self):
        self.schedule.setText(
            f"总页数:{len(self.task.imageInfos)}  已下载:{len(self.task.success)}  下载失败:{len(self.task.error)}")
        self.pbar.setValue(self.task.doneNum)
        self.change_status()

    def update_task(self, task: DownloadTask):
        self.task = task
        self.update_task_signa.emit()


class UIComicInfoWidget(QWidget):
    load_chapter_list_signa = QtCore.pyqtSignal(ChapterInfo)
    load_download_task_signa = QtCore.pyqtSignal(DownloadTask)

    def __init__(self, comic_info: ComicInfo, down_v_box_layout: QVBoxLayout):
        super().__init__()
        self.comic_info = comic_info
        self.down_v_box_layout = down_v_box_layout
        self.img_label = QLabel(self)
        self.img_label.setScaledContents(True)
        w, h = 200, 300
        # w, h = utils.image_resize(comic_info.cover, height=200)
        self.img_label.resize(QtCore.QSize(w, h))
        self.img_label.setGeometry(10, 10, w, h)
        # self.img_label.setPixmap(QPixmap.fromImage(img))
        self.img_label.setPixmap(QtGui.QPixmap("/Users/bo/my/tmp/老夫子2/第1卷/1.jpg"))

        self.title = QLabel(self)
        self.title.setGeometry(220, 10, 100, 40)
        title_font = QtGui.QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_font.setUnderline(True)
        self.title.setFont(title_font)
        self.title.setText(comic_info.title)
        self.title.setWordWrap(True)

        info_font = QtGui.QFont()
        info_font.setPointSize(14)
        # 作者
        self.author = QLabel(self)
        self.author.setText("作者 : " + comic_info.author)
        self.author.setGeometry(220, 50, 150, 40)
        self.author.setWordWrap(True)
        self.author.setFont(info_font)
        # 状态
        self.status = QLabel(self)
        self.status.setText("更新状态 : " + comic_info.status)
        self.status.setGeometry(220, 90, 150, 40)
        self.status.setFont(info_font)

        # 热度
        self.heat = QLabel(self)
        self.heat.setText("热度 : " + str(comic_info.heat))
        self.heat.setGeometry(220, 130, 150, 40)
        self.heat.setFont(info_font)

        # 类型
        self.tip = QLabel(self)
        self.tip.setText("类型 : " + comic_info.tip)
        self.tip.setGeometry(220, 170, 150, 40)
        self.tip.setWordWrap(True)
        self.tip.setFont(info_font)

        # web
        self.domain = QLabel(self)
        self.domain.setText(f"查看原网页 : {comic_info.domain}")
        self.domain.setText(f'查看原网页 : <a href="{comic_info.url}">{comic_info.domain}</a>')
        self.domain.setGeometry(220, 210, 150, 40)
        self.domain.setOpenExternalLinks(True)
        self.domain.setFont(info_font)

        # 描述
        self.describe = QLabel(self)
        self.describe.setText("  " + comic_info.describe)
        self.describe.setGeometry(10, 320, 350, 330)
        self.describe.setWordWrap(True)
        # 对齐方式
        self.describe.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)

        # 章节列表,创建一个区域

        self.searchHBoxLayout = QHBoxLayout()
        # self.searchHBoxLayout.addSpacing()
        self.searchGroupBox = QGroupBox()
        self.searchGroupBox.setLayout(self.searchHBoxLayout)

        self.searchScroll = QScrollArea(self)
        self.searchScroll.setGeometry(370, 10, 574, 590)
        self.searchScroll.setWidget(self.searchGroupBox)
        self.searchScroll.setWidgetResizable(True)

        # 全选
        self.check_all = QCheckBox(self)
        self.check_all.setText("全选")
        self.check_all.setGeometry(700, 610, 100, 20)
        self.check_all.stateChanged.connect(self.check_all_fun)

        # 下载
        self.down_button = QPushButton(self)
        self.down_button.setText("下载")
        self.down_button.setGeometry(780, 605, 50, 30)

        self.down_button.clicked.connect(self.download_button_click)

        self.load_chapter_list_signa.connect(self.load_chapter)
        self.load_download_task_signa.connect(self.download_callback)

        # 调用对应的service的接口,获取章节列表
        constant.SERVICE.chapter(comic_info, self.load_chapter_list_signa.emit)

    i = 0
    searchVBoxLayout: QVBoxLayout
    check_box_list: List[QCheckBox] = []

    def check_all_fun(self):
        for check_box in self.check_box_list:
            check_box.setChecked(self.check_all.isChecked())

    def download_callback(self, task: DownloadTask):
        widget = DownLoadTaskWidget(task)
        self.down_v_box_layout.addWidget(widget)

    def download_button_click(self):
        flag = False
        for check_box in self.check_box_list:
            if check_box.isChecked():
                constant.SERVICE.parse_image(self.comic_info, check_box.property("chapter_info"),
                                             self.load_download_task_signa.emit)
                if not flag:
                    QMessageBox.information(self, "下载通知", "正在解析选中章节", QMessageBox.StandardButton.Yes)
                    flag = True

    def load_chapter(self, chapter_info: ChapterInfo):
        if self.i % 23 == 0:
            self.searchVBoxLayout = QVBoxLayout()
            self.searchVBoxLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)  # 对齐方式,研究了3个小时 o(╥﹏╥)o
            self.searchHBoxLayout.addLayout(self.searchVBoxLayout)

        check_box = QCheckBox()
        self.check_box_list.append(check_box)
        check_box.setText(chapter_info.title)
        check_box.setProperty("chapter_info", chapter_info)
        self.searchVBoxLayout.addWidget(check_box)
        self.i += 1


class UIComicListWidget(QWidget):
    def __init__(self, comic_info: ComicInfo, tab_widget: QTabWidget, down_v_box_layout: QVBoxLayout):
        super().__init__()
        self.tabWidget = tab_widget
        self.comicInfo = comic_info
        self.down_v_box_layout = down_v_box_layout
        self.setMinimumHeight(200)
        # g_layout = QGridLayout(self)
        # 图片
        # img = QImage.fromData(comic_info.cover)
        self.img_label = QLabel(self)
        self.img_label.setScaledContents(True)
        w, h = 150, 300
        # w, h = utils.image_resize(comic_info.cover, height=200)
        self.img_label.resize(QtCore.QSize(w, h))
        self.img_label.setGeometry(5, 5, w, h)
        # self.img_label.setPixmap(QPixmap.fromImage(img))
        self.img_label.setPixmap(QtGui.QPixmap("/Users/bo/my/tmp/老夫子2/第1卷/1.jpg"))
        # 标题
        self.title = ButtonQLabel(self)
        self.title.onclick(self.add_tab)
        self.title.setText(comic_info.title)
        self.title.setGeometry(180, 10, 550, 35)
        title_font = QtGui.QFont()
        title_font.setPointSize(30)
        title_font.setBold(True)
        title_font.setUnderline(True)
        self.title.setFont(title_font)
        self.title.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # 作者
        self.author = QLabel(self)
        self.author.setText("作者 : " + comic_info.author)
        self.author.setGeometry(180, 50, 250, 20)
        # 状态
        self.status = QLabel(self)
        self.status.setText("更新状态 : " + comic_info.status)
        self.status.setGeometry(500, 50, 150, 20)
        # 热度
        self.status = QLabel(self)
        self.status.setText("热度 : " + str(comic_info.heat))
        self.status.setGeometry(800, 50, 100, 20)

        # 类型
        self.tip = QLabel(self)
        self.tip.setText("类型 : " + comic_info.tip)
        self.tip.setGeometry(180, 70, 250, 20)

        # web
        self.domain = QLabel(self)
        self.domain.setText(f"查看原网页 : {comic_info.domain}")
        self.domain.setText(f'查看原网页 : <a href="{comic_info.url}">{comic_info.domain}</a>')
        self.domain.setGeometry(500, 70, 250, 20)
        self.domain.setOpenExternalLinks(True)

        # 描述
        self.describe = QLabel(self)
        self.describe.setText("  " + comic_info.describe)
        self.describe.setGeometry(180, 90, 664, 110)
        self.describe.setWordWrap(True)
        # 对齐方式
        self.describe.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)

    def add_tab(self):
        if self.comicInfo.url in constant.OPEN_TAB:
            self.tabWidget.setCurrentIndex(constant.OPEN_TAB.index(self.comicInfo.url) + 2)
        else:
            info = UIComicInfoWidget(self.comicInfo, self.down_v_box_layout)
            self.tabWidget.setCurrentIndex(self.tabWidget.addTab(info, self.comicInfo.title))
            constant.OPEN_TAB.append(self.comicInfo.url)


class MainWindowWidget(QWidget):
    load_comic_list_signa = QtCore.pyqtSignal(ComicInfo)

    def __init__(self, main_window: QWidget):
        super().__init__()
        self.search_callback = None
        main_window.setObjectName("MainWindow")
        main_window.setWindowTitle("abc")
        main_window.resize(1024, 768)
        main_window.setMinimumSize(QtCore.QSize(1024, 768))
        main_window.setMaximumSize(QtCore.QSize(1024, 768))
        # 主题空间 子组件都放这个Widget里
        self.centralWidget = QtWidgets.QWidget(main_window)
        self.centralWidget.setObjectName("centralWidget")
        # 搜索框
        self.souInput = QtWidgets.QLineEdit(self.centralWidget)
        self.souInput.setGeometry(QtCore.QRect(40, 30, 944, 30))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.souInput.setFont(font)
        self.souInput.setObjectName("souInput")
        self.souInput.setText("龙珠")
        # QTabWidget tab页签
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 70, 944, 668))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        # 下载页面
        self.down_tab = QtWidgets.QWidget()
        self.down_tab.setStatusTip("")
        self.down_tab.setAutoFillBackground(False)
        self.down_tab.setObjectName("down_tab")
        self.tabWidget.addTab(self.down_tab, "下载列表")
        # 搜索结果页面
        self.search_tab = QtWidgets.QWidget()
        self.search_tab.setObjectName("search_tab")
        self.tabWidget.addTab(self.search_tab, "搜索结果")

        self.tabWidget.tabBar().setTabButton(0, QTabBar.ButtonPosition.LeftSide, None)
        self.tabWidget.tabBar().setTabButton(1, QTabBar.ButtonPosition.LeftSide, None)

        self.tabWidget.tabCloseRequested.connect(self.tab_close)

        # 主体的centralWidget 放到主窗口中
        main_window.setCentralWidget(self.centralWidget)

        self.searchVBoxLayout = QVBoxLayout()
        self.searchGroupBox = QGroupBox()
        self.searchScroll = QScrollArea()
        self.searchLayout = QVBoxLayout(self.search_tab)
        self.searchVBoxLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.searchGroupBox.setLayout(self.searchVBoxLayout)
        self.searchScroll.setWidget(self.searchGroupBox)
        self.searchScroll.setWidgetResizable(True)
        self.searchLayout.addWidget(self.searchScroll)

        self.downVBoxLayout = QVBoxLayout()
        self.downGroupBox = QGroupBox()
        self.downScroll = QScrollArea()
        self.downLayout = QVBoxLayout(self.down_tab)
        self.downVBoxLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.downGroupBox.setLayout(self.downVBoxLayout)
        self.downScroll.setWidget(self.downGroupBox)
        self.downScroll.setWidgetResizable(True)
        self.downLayout.addWidget(self.downScroll)

        self.souInput.returnPressed.connect(self.input_return_pressed)  # 回车搜索

        self.load_comic_list_signa.connect(self.load_comic_list)  # 更新ui的插槽

    def tab_close(self, index):
        self.tabWidget.removeTab(index)
        del constant.OPEN_TAB[index - 2]

    def input_return_pressed(self):
        for i in range(self.searchVBoxLayout.count()):
            self.searchVBoxLayout.itemAt(i).widget().deleteLater()
        constant.SERVICE.search(self.souInput.text(), self.load_comic_list_signa.emit)  # 查询回调出发插槽
        self.tabWidget.setCurrentIndex(1)

    def load_comic_list(self, info: ComicInfo):
        comic_info_widget = UIComicListWidget(info, self.tabWidget, self.downVBoxLayout)
        self.searchVBoxLayout.addWidget(comic_info_widget)
