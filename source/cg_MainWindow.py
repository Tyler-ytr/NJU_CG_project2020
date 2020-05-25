import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem,
    QToolBar,
    QAction,
    QLabel,
    QSpinBox,
    QPushButton,
    QFrame,
    QColorDialog,
    QGridLayout,
    QButtonGroup,
    QDockWidget,
    QToolButton,
    QMenu
)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QIcon,QPalette
from cg_PaintWidget import MyCanvas, MyItem
from PyQt5.QtCore import *

class CusToolButton(QToolButton):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setPopupMode(QToolButton.MenuButtonPopup)
        self.triggered.connect(self.setDefaultAction)
class MainWindow(QMainWindow):
    def Menu_init(self):
        menubar = self.menuBar()
        # 菜单栏
        mfile = menubar.addMenu("文件")
        # 重置
        reset_canvas_act = QAction(QIcon("./picture/newer.png"), "重置画布", self)

        # reset_canvas_act.triggered.connect(self.reset_canvas_action) #To be done

        # 将action添加到file上面
        mfile.addAction(reset_canvas_act)
        # 工具栏
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        toolbar.addAction(reset_canvas_act)

    def pen_width(self):
        w = self.spinbox_penwidth.text()
        #w = int(w)
        #print("w:" + w)
        self.canvas_widget.setpenWidth(w)

    def pen_color(self):
        c=QColorDialog.getColor()
        self.frame_color.setPalette(QPalette(c))
        #assert(0)
        self.frame_color.setStyleSheet("QWidget { background-color: %s }"% c.name())
        #self.frame_color.setStyleSheet("QFrame{background-color: rgba("+c.red()+","+c.green()+","+c.blue()+",1);border:none}")
            #print(c.red())
        #参考了https://www.cnblogs.com/icat-510/p/10166882.html
        self.canvas_widget.setpenColor(c)



    def Color_init(self):
        colorbar = QToolBar("画笔属性栏")
        self.addToolBar(colorbar)
        colorbar.setMovable(True)

        label_penwidth = QLabel("画笔宽度")
        self.spinbox_penwidth = QSpinBox()
        self.spinbox_penwidth.setRange(1, 50)
        self.spinbox_penwidth.setValue(2)

        self.color_botton = QPushButton("画笔颜色")
        self.frame_color = QFrame(self)
        self.frame_color.setObjectName("colorframe")
        self.frame_color.setFrameShape(QFrame.Box)
        self.frame_color.setPalette(QPalette(Qt.black))
        self.frame_color.setAutoFillBackground(True)
        self.frame_color.setFixedSize(30, 30)
        self.frame_color.setStyleSheet("QFrame{background-color: rgba(0,0,0,1);border:none}")

        # 槽函数
        self.spinbox_penwidth.valueChanged[int].connect(self.pen_width)
        self.color_botton.clicked.connect(self.pen_color)

        #布局
        color_layout=QHBoxLayout()
        color_layout.setAlignment(Qt.AlignLeft)

        color_layout.addWidget(label_penwidth)
        color_layout.addWidget(self.spinbox_penwidth)
        color_layout.addWidget(self.color_botton)
        color_layout.addWidget(self.frame_color)

        color_widget=QWidget()
        color_widget.setLayout(color_layout)
        colorbar.addWidget(color_widget)
    def layout_init(self):
        #p=self.takeCentralWidget()
        self.setDockNestingEnabled(True) #允许嵌套


        self.Tool_window=QDockWidget("工具栏")

        self.setCentralWidget(self.Image_window)
        self.addDockWidget(Qt.TopDockWidgetArea,self.Tool_window)
        self.addDockWidget(Qt.RightDockWidgetArea,self.List_window)

    def test1(self):
        a=1
    def test2(self):
        a=2
    def tool_init(self):
        self.line_action_1=QAction("DDA line")
        self.line_action_2=QAction("Bresenham line")
        self.line_action_1.setIcon(QIcon("./picture/line.png"))
        self.line_action_2.setIcon(QIcon("./picture/line.png"))

        self.line_menu=QMenu()
        self.line_menu.addAction(self.line_action_1)
        self.line_menu.addAction(self.line_action_2)
        self.line_tool_button=CusToolButton()
        self.line_tool_button.setMenu(self.line_menu)
        self.line_tool_button.setDefaultAction(self.line_action_1)
        self.line_tool_bar=QToolBar(self)
        self.line_tool_bar.addWidget(self.line_tool_button)




    #     #直线
    #     line_button_1=QPushButton(QIcon("./picture/line.png"),"",self)
    #     line_button_1.setToolTip("直线1")
    #     line_button_1.setObjectName("toolButton")
    #     line_button_1.setFixedSize(30,30)
    #     line_button_1.setStatusTip("DDA")
    #
    #
    #     #布局
        tools_layout=QGridLayout()
        tools_layout.setAlignment(Qt.AlignLeft)
        tools_layout.addWidget(self.line_tool_bar,0,0)
    #
        #加入tool_window
        #To be done
        tools_widget=QWidget(self.Tool_window)
        tools_widget.setLayout(tools_layout)
        self.Tool_window.setWidget(tools_widget)
    #
    #
    #     #按钮组 通过按钮组的值连接槽函数确定状态
    #     toolbuttons=QButtonGroup()
    #     toolbuttons.addButton(line_button_1,1)
    #
    #
    #     toolbuttons.buttonClicked[int].connect(self.tool_clicked)
    # def tool_clicked(self,type:int):
    #     a=type









    def __init__(self):
        super().__init__()


        ## 主窗口布局
        # 图片与标题
        QMainWindow.setWindowIcon(self, QIcon("./picture/icon.png"))
        QMainWindow.setWindowTitle(self, "图片编辑器 by Larry")

        # self.setWindowTitle('CG Demo')

        # 界面大小位置
        # QMainWindow.resize(self,QApplication.desktop().width()*0.9,QApplication.desktop().height()*0.9)
        # QMainWindow.move(self,QApplication.desktop().width()*0.05,QApplication.desktop().height()*0.05)

        self.Menu_init()
        self.Color_init()

        # list widget
        self.Image_window=QDockWidget("图像编辑框")
        self.Image_window.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetFloatable)
        self.Image_window.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.Image_window.setMinimumSize(600,600)

        self.List_window=QDockWidget("图元列表")
        self.List_window.setFeatures(QDockWidget.DockWidgetMovable)
        self.list_widget = QListWidget(self.List_window)
        self.list_widget.setMinimumWidth(200)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self.Image_window)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget
        self.List_window.setWidget(self.list_widget)
        self.Image_window.setWidget(self.canvas_widget)

        self.layout_init()
        self.tool_init()

        #self.hbox_layout = QHBoxLayout()
        #self.hbox_layout.addWidget(self.canvas_widget)
        #self.hbox_layout.addWidget(self.list_widget, stretch=1)
        #self.central_widget = QWidget(self.Image_window)
        #self.central_widget.setLayout(self.hbox_layout)

        #self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)