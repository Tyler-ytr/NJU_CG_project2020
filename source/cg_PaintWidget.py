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
    QStyleOptionGraphicsItem
)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QPen
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import *

class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        #self.polygonlist=[]

        self.penColor = Qt.black
        self.penwidth = 2

    def setpenColor(self, c: QColor):
        self.penColor = c

    def setpenWidth(self, w: int):
        self.penwidth = w

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        #self.polygonlist.clear()
    def start_draw_polygon(self,algorithm,item_id):
        self.status='polygon'
        self.temp_algorithm=algorithm
        self.temp_id=item_id
        #self.polygonlist.clear()
        #self.statusBar().showMessage(algorithm+'sdsdsd')

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()
        self.temp_item=None

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])
    def polygoncheck(self,x0,y0):
        success=True
        if self.temp_item is None:
            pass
        else:
            p_list=self.temp_item.p_list
            for [x,y] in p_list:
                if (x-x0)*(x-x0)+(y-y0)*(y-y0)<1:
                    success=False
                    break
        return success

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.penwidth, self.penColor, self.temp_id, self.status, [[x, y], [x, y]],
                                    self.temp_algorithm)
            self.scene().addItem(self.temp_item)
            #self.temp_item=None
        if self.status=='polygon':
            if self.temp_item is None:
                self.temp_item=MyItem(self.penwidth,self.penColor,self.temp_id,self.status,[[x, y], [x, y]],self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                if event.button()==Qt.RightButton:
                    self.item_dict[self.temp_id] = self.temp_item
                    self.list_widget.addItem(self.temp_id)
                    self.finish_draw()
                    self.temp_item = None
                else:
                    success= self.polygoncheck(x,y)
                    if success:
                        self.temp_item.p_list.append([x,y])
                    else:
                        self.item_dict[self.temp_id] = self.temp_item
                        self.list_widget.addItem(self.temp_id)
                        self.finish_draw()
                        self.temp_item = None
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)
    # def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    #     if self.status=='polygon':
    #         self.item_dict[self.temp_id] = self.temp_item
    #         self.list_widget.addItem(self.temp_id)
    #         #self.polygonlist.clear()
    #         self.finish_draw()
    #         self.temp_item = None
    #     super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        # if self.status == 'polygon':
        #     self.item_dict[self.temp_id] = self.temp_item
        #     #self.list_widget.addItem(self.temp_id)
        #     #self.finish_draw()
        #     # self.item_dict[self.temp_id] = self.temp_item
        #     #self.list_widget.addItem(self.temp_id)

        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(self, penwidth: int, pencolor: QColor, item_id: str, item_type: str, p_list: list, algorithm: str = '',
                 parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id  # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list  # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.pen_width = penwidth
        self.pen_color = pencolor
        self.temppen=QPen()
        self.temppen.setWidth(self.pen_width)
        self.temppen.setColor(self.pen_color)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.temppen)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            if len(self.p_list)>=2:
                item_pixels=alg.draw_polygon(self.p_list,self.algorithm)
                for p in item_pixels:
                    painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            pass
        elif self.item_type == 'curve':
            pass

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            if len(self.p_list)==0:
                return QRectF(0,0,0,0)
            if len(self.p_list)<2:
                x0, y0 = self.p_list[0]
                return QRectF(x0-1,y0-1,x0+1,y0+1)
            x_list=[]
            y_list=[]
            for [x0,y0] in self.p_list:
                x_list.append(x0)
                y_list.append(y0)
            x = min(x_list)
            y = min(y_list)
            w = max(x_list) - x
            h = max(y_list) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'ellipse':
            pass
        elif self.item_type == 'curve':
            pass
