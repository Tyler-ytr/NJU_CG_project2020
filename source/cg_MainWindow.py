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
    QMenu,
    QFileDialog,

)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QIcon, QPalette,QPixmap,QImage
from cg_PaintWidget import MyCanvas, MyItem
from PyQt5.QtCore import *
from PIL import Image
import numpy as np


class CusToolButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPopupMode(QToolButton.MenuButtonPopup)
        self.triggered.connect(self.setDefaultAction)


class MainWindow(QMainWindow):
    def reset_canvas_action(self):
        self.item_cnt=0
        self.canvas_widget.reset_canvas()
    def save_canvas_action(self):
        #pixMap = view->grab(view->sceneRect().toRect());
        # QString
        # fileName = QFileDialog::getSaveFileName(this, "Save image",
        #                                         QCoreApplication::applicationDirPath(), "BMP Files (*.bmp);;JPEG (*.JPEG);;PNG (*.png)" );
        #filename=QFileDialog.getSaveFileName("Save image",QCoreApplication.applicationDirPath(),"BMP Files (*.bmp);;JPEG (*.JPEG);;PNG (*.png)")
        filename , ok2 = QFileDialog.getSaveFileName(self,
                                    "Save Image",
                                    QDir.currentPath(),
                                    "BMP Files (*.bmp);;JPEG (*.JPEG);;PNG (*.png)")

        #
        pixmap=QPixmap()
        pixmap=self.canvas_widget.grab(self.canvas_widget.sceneRect().toRect())
        pixmap.save(filename)

    def Menu_init(self):
        menubar = self.menuBar()
        # 菜单栏
        mfile = menubar.addMenu("文件")
        # 重置
        reset_canvas_act = QAction(QIcon("./icon/file.png"), "重置画布", self)

        reset_canvas_act.triggered.connect(self.reset_canvas_action) #To be done

        #保存
        save_canvas_act=QAction(QIcon("./icon/save.png"),"保存画布",self)
        save_canvas_act.triggered.connect(self.save_canvas_action)

        # 将action添加到file上面
        mfile.addAction(reset_canvas_act)
        mfile.addAction(save_canvas_act)
        # 工具栏
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        toolbar.addAction(reset_canvas_act)
        toolbar.addAction(save_canvas_act)

    def pen_width(self):
        w = self.spinbox_penwidth.text()
        w = int(w)
        # print("w:" + w)
        self.canvas_widget.setpenWidth(w)
        self.statusBar().showMessage('宽度为%d' % (w))

    def pen_color(self):
        c = QColorDialog.getColor()
        self.frame_color.setPalette(QPalette(c))
        # assert(0)
        self.frame_color.setStyleSheet("QWidget { background-color: %s }" % c.name())
        # self.frame_color.setStyleSheet("QFrame{background-color: rgba("+c.red()+","+c.green()+","+c.blue()+",1);border:none}")
        # print(c.red())
        # 参考了https://www.cnblogs.com/icat-510/p/10166882.html
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

        # 布局
        color_layout = QHBoxLayout()
        color_layout.setAlignment(Qt.AlignLeft)

        color_layout.addWidget(label_penwidth)
        color_layout.addWidget(self.spinbox_penwidth)
        color_layout.addWidget(self.color_botton)
        color_layout.addWidget(self.frame_color)

        color_widget = QWidget()
        color_widget.setLayout(color_layout)
        colorbar.addWidget(color_widget)

    def layout_init(self):
        # p=self.takeCentralWidget()
        self.setDockNestingEnabled(True)  # 允许嵌套

        self.Tool_window = QDockWidget("工具栏")

        self.setCentralWidget(self.Image_window)
        self.addDockWidget(Qt.TopDockWidgetArea, self.Tool_window)
        self.addDockWidget(Qt.RightDockWidgetArea, self.List_window)

    def line_action(self, algorithm):
        self.canvas_widget.start_draw_line(algorithm, self.get_id())
        self.statusBar().showMessage(algorithm + '算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def DDA_line_draw_action(self):
        self.line_action('DDA')

    def Bresenham_line_draw_action(self):
        self.line_action('Bresenham')

    def polygon_action(self, algorithm):
        self.canvas_widget.start_draw_polygon(algorithm, self.get_id())
        self.statusBar().showMessage(algorithm + '算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def DDA_polygon_draw_action(self):
        self.polygon_action('DDA')

    def Bresenham_polygon_draw_action(self):
        self.polygon_action('Bresenham')

    def ellipse_draw_action(self):
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('中心圆算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_draw_action(self, algorithm):
        self.canvas_widget.start_draw_curve(algorithm, self.get_id())
        self.statusBar().showMessage(algorithm + '算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def Bezier_curve_draw_action(self):
        self.curve_draw_action('Bezier')

    def B_spline_curve_draw_action(self):
        self.curve_draw_action('B-spline')

    def translate_draw_action(self):
        self.canvas_widget.start_draw_translate()
        self.statusBar().showMessage('平移图元')
        # self.list_widget.clearSelection()
        # self.canvas_widget.clear_selection()

    def rotate_draw_action(self):
        self.canvas_widget.start_draw_rotate()
        self.statusBar().showMessage('旋转图元')

    def scale_draw_action(self):
        self.canvas_widget.start_draw_scale()
        self.statusBar().showMessage('缩放图元')

    def clip_draw_action(self,algorithm):
        self.canvas_widget.start_draw_clip(algorithm)
        self.statusBar().showMessage(algorithm+'裁剪线段')

    def Cohen_Sutherland_clip_draw_action(self):
        self.clip_draw_action("Cohen-Sutherland")
    def Liang_Barsky_clip_draw_action(self):
        self.clip_draw_action("Liang_Barsky")

    def tool_init(self):
        # line相关,使用的https://www.walletfox.com/course/customqtoolbutton.php做的可选算法button
        self.line_action_1 = QAction("DDA line")
        self.line_action_2 = QAction("Bresenham line")
        self.line_action_1.setIcon(QIcon("./icon/line.png"))
        self.line_action_2.setIcon(QIcon("./icon/line.png"))
        self.line_action_1.triggered.connect(self.DDA_line_draw_action)
        self.line_action_2.triggered.connect(self.Bresenham_line_draw_action)
        self.line_menu = QMenu()
        self.line_menu.addAction(self.line_action_1)
        self.line_menu.addAction(self.line_action_2)
        self.line_tool_button = CusToolButton()
        self.line_tool_button.setMenu(self.line_menu)
        self.line_tool_button.setDefaultAction(self.line_action_1)
        self.line_tool_bar = QToolBar(self)
        self.line_tool_bar.addWidget(self.line_tool_button)

        # polygon相关
        self.polygon_action_1 = QAction("DDA polygon")
        self.polygon_action_2 = QAction("Bresenham polygon")
        self.polygon_action_1.setIcon(QIcon("./icon/polygon.png"))
        self.polygon_action_2.setIcon(QIcon("./icon/polygon.png"))
        self.polygon_action_1.triggered.connect(self.DDA_polygon_draw_action)
        self.polygon_action_2.triggered.connect(self.Bresenham_polygon_draw_action)
        self.polygon_menu = QMenu()
        self.polygon_menu.addAction(self.polygon_action_1)
        self.polygon_menu.addAction(self.polygon_action_2)
        self.polygon_tool_button = CusToolButton()
        self.polygon_tool_button.setMenu(self.polygon_menu)
        self.polygon_tool_button.setDefaultAction(self.polygon_action_1)
        self.polygon_tool_bar = QToolBar(self)
        self.polygon_tool_bar.addWidget(self.polygon_tool_button)

        # ellipse相关
        self.ellipse_action = QAction("Ellipse")
        self.ellipse_action.setIcon(QIcon("./icon/ellipse.png"))
        self.ellipse_action.triggered.connect(self.ellipse_draw_action)

        self.ellipse_tool_bar = QToolBar(self)
        self.ellipse_tool_bar.addAction(self.ellipse_action)

        # curve相关
        self.curve_action_1 = QAction("Bezier Curve")
        self.curve_action_1.setIcon(QIcon("./icon/curve.png"))
        self.curve_action_2 = QAction("B-spline Curve")
        self.curve_action_2.setIcon(QIcon("./icon/curve.png"))
        self.curve_action_1.triggered.connect(self.Bezier_curve_draw_action)
        self.curve_action_2.triggered.connect(self.B_spline_curve_draw_action)
        self.curve_menu = QMenu()
        self.curve_menu.addAction(self.curve_action_1)
        self.curve_menu.addAction(self.curve_action_2)
        self.curve_tool_button = CusToolButton()
        self.curve_tool_button.setMenu(self.curve_menu)
        self.curve_tool_button.setDefaultAction(self.curve_action_1)

        self.curve_tool_bar = QToolBar(self)
        self.curve_tool_bar.addWidget(self.curve_tool_button)

        # translate相关(平移)
        self.translate_action = QAction("Translate")
        self.translate_action.setIcon(QIcon("./icon/move.png"))
        self.translate_action.triggered.connect(self.translate_draw_action)

        self.translate_tool_bar = QToolBar(self)
        self.translate_tool_bar.addAction(self.translate_action)

        # rotate相关 旋转
        self.rotate_action = QAction("Rotate")
        self.rotate_action.setIcon(QIcon("./icon/rotate.png"))
        self.rotate_action.triggered.connect(self.rotate_draw_action)

        self.rotate_tool_bar = QToolBar(self)
        self.rotate_tool_bar.addAction(self.rotate_action)
        # scale相关,缩放;
        self.scale_action = QAction("Scale")
        self.scale_action.setIcon(QIcon("./icon/scale.png"))
        self.scale_action.triggered.connect(self.scale_draw_action)

        self.scale_tool_bar = QToolBar(self)
        self.scale_tool_bar.addAction(self.scale_action)
        # clip 裁剪
        self.clip_action_1 = QAction("Cohen-Sutherland Clip")
        self.clip_action_2 = QAction("Liang-Barsky Clip")

        self.clip_action_1.setIcon(QIcon("./icon/crop.png"))
        self.clip_action_2.setIcon(QIcon("./icon/crop.png"))
        self.clip_action_1.triggered.connect(self.Cohen_Sutherland_clip_draw_action)
        self.clip_action_2.triggered.connect(self.Liang_Barsky_clip_draw_action)


        self.clip_menu=QMenu()
        self.clip_menu.addAction(self.clip_action_1)
        self.clip_menu.addAction(self.clip_action_2)
        self.clip_tool_button=CusToolButton()
        self.clip_tool_button.setMenu(self.clip_menu)
        self.clip_tool_button.setDefaultAction(self.clip_action_1)

        self.clip_tool_bar = QToolBar(self)
        self.clip_tool_bar.addWidget(self.clip_tool_button)

        #     #布局
        tools_layout = QGridLayout()
        tools_layout.setAlignment(Qt.AlignLeft)
        tools_layout.addWidget(self.line_tool_bar, 0, 0)
        tools_layout.addWidget(self.polygon_tool_bar, 0, 1)
        tools_layout.addWidget(self.ellipse_tool_bar, 0, 2)
        tools_layout.addWidget(self.curve_tool_bar, 0, 3)
        tools_layout.addWidget(self.translate_tool_bar, 0, 4)
        tools_layout.addWidget(self.rotate_tool_bar, 0, 5)
        tools_layout.addWidget(self.scale_tool_bar, 0, 6)
        tools_layout.addWidget(self.clip_tool_bar, 0, 7)
        # 加入tool_window
        tools_widget = QWidget(self.Tool_window)
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
        self.item_cnt = 0

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
        self.Image_window = QDockWidget("图像编辑框")
        self.Image_window.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.Image_window.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.Image_window.setMinimumSize(602, 602)

        self.List_window = QDockWidget("图元列表")
        self.List_window.setFeatures(QDockWidget.DockWidgetMovable)
        self.list_widget = QListWidget(self.List_window)
        self.list_widget.setMinimumWidth(200)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self.Image_window)

        self.canvas_widget.setFixedSize(602, 602)#这样就没有滑动条了
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        self.List_window.setWidget(self.list_widget)
        self.Image_window.setWidget(self.canvas_widget)

        # 槽函数
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        self.layout_init()
        self.tool_init()

        # self.hbox_layout = QHBoxLayout()
        # self.hbox_layout.addWidget(self.canvas_widget)
        # self.hbox_layout.addWidget(self.list_widget, stretch=1)
        # self.central_widget = QWidget(self.Image_window)
        # self.central_widget.setLayout(self.hbox_layout)

        # self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id
