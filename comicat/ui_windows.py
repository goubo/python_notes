from typing import List

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox, QScrollArea, QTabWidget, QTabBar, QHBoxLayout, \
    QCheckBox, QPushButton, QMessageBox

from constant import open_tab, service
from entity import ComicInfo, ChapterInfo
from extend_widgets import ButtonQLabel


class UIComicInfoWidget(QWidget):
    load_chapter_list_signa = QtCore.pyqtSignal(ChapterInfo)

    def __init__(self, comic_info: ComicInfo):
        super().__init__()
        self.comic_info = comic_info
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
        self.domain.setText("查看原网页 : " + comic_info.domain)
        self.domain.setText('查看原网页 : <a href="{}">{}</a>'.format(comic_info.url, comic_info.domain))
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

        self.down_button.clicked.connect(self.download)

        self.load_chapter_list_signa.connect(self.load_chapter)

        # 调用对应的service的接口,获取章节列表
        service.chapter(comic_info, self.load_chapter_list_signa.emit)

    i = 0
    searchVBoxLayout: QVBoxLayout
    check_box_list: List[QCheckBox] = []

    def check_all_fun(self):
        for check_box in self.check_box_list:
            check_box.setChecked(self.check_all.isChecked())

    def download(self):
        flag = False
        for check_box in self.check_box_list:
            if check_box.isChecked():
                service.parse_download(self.comic_info, check_box.property("chapter_info"))
                flag = True

        if flag:
            QMessageBox.information(self, "下载通知", "正在解析选中章节", QMessageBox.StandardButton.Yes)

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
    def __init__(self, comic_info: ComicInfo, tab_widget: QTabWidget):
        super().__init__()
        self.tabWidget = tab_widget
        self.comicInfo = comic_info
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
        self.domain.setText("查看原网页 : " + comic_info.domain)
        self.domain.setText('查看原网页 : <a href="{}">{}</a>'.format(comic_info.url, comic_info.domain))
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
        if self.comicInfo.url in open_tab:
            self.tabWidget.setCurrentIndex(open_tab.index(self.comicInfo.url) + 2)
        else:
            info = UIComicInfoWidget(self.comicInfo)
            self.tabWidget.setCurrentIndex(self.tabWidget.addTab(info, self.comicInfo.title))
            open_tab.append(self.comicInfo.url)


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

        self.souInput.returnPressed.connect(self.input_return_pressed)  # 回车搜索

        self.load_comic_list_signa.connect(self.load_comic_list)  # 更新ui的插槽

    def tab_close(self, index):
        self.tabWidget.removeTab(index)
        del open_tab[index - 2]

    def input_return_pressed(self):
        for i in range(self.searchVBoxLayout.count()):
            self.searchVBoxLayout.itemAt(i).widget().deleteLater()
        service.search(self.souInput.text(), self.load_comic_list_signa.emit)  # 查询回调出发插槽
        self.tabWidget.setCurrentIndex(1)

    def load_comic_list(self, info: ComicInfo):
        comic_info_widget = UIComicListWidget(info, self.tabWidget)
        self.searchVBoxLayout.addWidget(comic_info_widget)
