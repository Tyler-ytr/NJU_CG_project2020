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
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QPen,QBitmap,QCursor
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import *
import numpy as np


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

        # self.polygonlist=[]

        self.penColor = Qt.black
        self.penwidth = 2

        self.centerx = 0
        self.centery = 0
        self.firstx = 0
        self.firsty = 0
        self.cur_id=0#用于鼠标选择


        self.rotateangle = 0
    def reset_canvas(self):
        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        pass
        #self.clear_selection()
        #print("herer")
        #
        # self.cur_id=0
        # self.centerx = 0
        # self.centery = 0
        # self.firstx = 0
        # self.firsty = 0
        # self.temp_item = None
        # #
        # self.scene().clear()
        # self.scene().update()
        # self.list_widget.clear()
        #
        #
        #
        # self.item_dict.clear()
        # self.item_dict.update()
        # self.selected_id = ''
        #
        # self.status = ''
        # self.temp_algorithm = ''
        # self.temp_id = ''

        #self.finish_draw()

        #self.temp_id = ''



    def setpenColor(self, c: QColor):
        self.penColor = c

    def setpenWidth(self, w: int):
        self.penwidth = w

    def start_draw_line(self, algorithm, item_id):
        self.finish_draw(1)
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        # self.polygonlist.clear()

    def start_draw_polygon(self, algorithm, item_id):
        self.finish_draw(1)
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        self.finish_draw(1)
        self.status = 'ellipse'
        self.temp_id = item_id

    def start_draw_curve(self, algorithm, item_id):
        self.finish_draw(1)
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_translate(self):
        self.finish_draw(1)
        self.setCursor(Qt.SizeAllCursor)
        self.status = 'translate'

        self.temp_id = self.selected_id
        # print(self.selected_id)

    def start_draw_rotate(self):
        self.finish_draw(1)
        self.status = 'rotate'
        self.temp_id = self.selected_id

    def start_draw_scale(self):
        self.finish_draw(1)
        self.setCursor(Qt.SizeFDiagCursor)
        self.status = 'scale'

        self.temp_id = self.selected_id
    def start_draw_clip(self,algorithm):
        self.finish_draw(1)
        self.status='clip'

        self.temp_id=self.selected_id
        self.temp_algorithm = algorithm
    def start_cursor_selection(self):
        if self.status=='ellipse' or self.status=='polygon' or self.status=='curve':
            if self.temp_item!=None:
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
        self.status='cursor'
        self.finish_draw()
    def start_fill_polygon(self):
        self.finish_draw(1)
        self.status='fill'
        if self.selected_id!='':
            self.temp_id=self.selected_id
            self.temp_item=self.item_dict[self.temp_id]
            if self.temp_item.item_type=='polygon':
                self.temp_item.fill(self.penColor)

            self.finish_draw()
    def start_cut_polygon(self):
        self.finish_draw(1)
        self.status='polygon_cut'
        self.temp_id = self.selected_id
        self.finish_draw()
    def start_x_mirror_draw(self):
        self.finish_draw(1)
        self.status='x_mirror'
        if self.selected_id!='':
            self.temp_id=self.selected_id
            self.temp_item=self.item_dict[self.temp_id]
            self.centerx, self.centery = self.getcenterpoint(self.temp_item)
            self.temp_item.x_mirror(self.centery)

            self.finish_draw()
    def start_y_mirror_draw(self):
        self.finish_draw(1)
        self.status='y_mirror'
        if self.selected_id!='':
            self.temp_id=self.selected_id
            self.temp_item=self.item_dict[self.temp_id]
            self.centerx, self.centery = self.getcenterpoint(self.temp_item)
            self.temp_item.y_mirror(self.centerx)

            self.finish_draw()
    def start_copy_draw(self,item_id):
        self.finish_draw(1)
        self.status='copy'
        self.temp_item=None
        if self.selected_id!='':
            self.temp_id=self.selected_id
            self.temp_item=self.item_dict[self.temp_id]
            self.centerx,self.centery=self.getcenterpoint(self.temp_item)
            self.temp_id=item_id
            cur_item = MyItem(self.temp_item.pen_width, self.temp_item.pen_color, self.temp_id,
                              self.temp_item.item_type, self.temp_item.p_list, self.temp_item.algorithm)
            cur_item.if_polygon_fill=self.temp_item.if_polygon_fill
            cur_item.filled_list=self.temp_item.filled_list
            cur_item.fill_color=self.temp_item.fill_color
            cur_item.fillpen.setColor(cur_item.fill_color)

            self.temp_item=cur_item
            self.scene().addItem(self.temp_item)
            self.finish_draw()
    def start_delete_draw(self):
        self.finish_draw(1)
        self.status='delete'
        if self.selected_id != '':
            self.temp_id=self.selected_id
            self.temp_item=self.item_dict[self.temp_id]
            self.scene().removeItem(self.temp_item)





    def finish_draw(self,a=0):

        if self.status=='line' or self.status=='ellipse' or self.status=='polygon' or self.status=='curve' or self.status=='copy':
            if self.temp_item!=None:
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
        if self.status == 'translate' or self.status == 'rotate' or self.status == 'scale' or self.status=='clip' or self.status=='cursor'or a==1 or self.status=='fill'or self.status=='polygon_cut' or self.status=='x_mirror'or self.status=='y_mirror':
            self.temp_id = self.selected_id
        else:
            self.temp_id = self.main_window.get_id()
        self.temp_item = None
        self.updateScene([self.sceneRect()])
        self.rotateangle = 0
        if self.status=='translate' or self.status=='scale':
            pass
        else:
            self.setCursor(Qt.ArrowCursor)
        if a==1:
            self.setCursor(Qt.ArrowCursor)

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        if selected==-1:
            return
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def polygoncheck(self, x0, y0):
        success = True
        if self.temp_item is None:
            pass
        else:
            p_list = self.temp_item.p_list
            for [x, y] in p_list:
                if (x - x0) * (x - x0) + (y - y0) * (y - y0) < 1:
                    success = False
                    break
        return success

    def getcenterpoint(self, item):
        p_list = item.p_list
        x_list = []
        y_list = []
        for [x0, y0] in p_list:
            x_list.append(x0)
            y_list.append(y0)
        x = min(x_list)
        y = min(y_list)
        w = max(x_list) - x
        h = max(y_list) - y
        #print(x + w / 2, y + h / 2)
        return [x + w / 2, y + h / 2]

    def computerangle(self, x1, y1, x2, y2, x3, y3):  # x2,y2是中心点,返回的值是度(°)
        AB = np.array([x1 - x2, y1 - y2])
        AC = np.array([x3 - x2, y3 - y2])
        LAB = np.sqrt(AB.dot(AB))
        LAC = np.sqrt(AC.dot(AC))
        cos_angle = AB.dot(AC) / (LAB * LAC)
        angle = np.arccos(cos_angle)  # 弧度
        angle2 = angle * 360 / 2 / np.pi
        # print(AB.dot(AC))
        return angle2

    def getscale(self, x1, y1, x2, y2, x3, y3):  # A,B,C 返回AC:AB
        AB = np.array([x1 - x2, y1 - y2])
        AC = np.array([x1 - x3, y1 - y3])
        LAB = np.sqrt(AB.dot(AB))
        LAC = np.sqrt(AC.dot(AC))
        result=float(LAC/LAB)
       # print(result)
        return result

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.penwidth, self.penColor, self.temp_id, self.status, [[x, y], [x, y]],
                                    self.temp_algorithm)
            self.scene().addItem(self.temp_item)

            # self.temp_item=None
        if self.status == 'polygon':
            if self.temp_item is None:
                self.temp_item = MyItem(self.penwidth, self.penColor, self.temp_id, self.status, [[x, y], [x, y]],
                                        self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                if event.button() == Qt.RightButton:
                    # self.item_dict[self.temp_id] = self.temp_item
                    # self.list_widget.addItem(self.temp_id)
                    self.finish_draw()
                    self.temp_item = None
                else:
                    success = self.polygoncheck(x, y)
                    if success:
                        self.temp_item.p_list.append([x, y])
                    else:
                        # self.item_dict[self.temp_id] = self.temp_item
                        # self.list_widget.addItem(self.temp_id)
                        self.finish_draw()
                        self.temp_item = None
        if self.status == 'ellipse':
            self.temp_item = MyItem(self.penwidth, self.penColor, self.temp_id, self.status, [[x, y], [x, y]],
                                    self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        if self.status == 'curve':
            if self.temp_item is None:
                self.temp_item = MyItem(self.penwidth, self.penColor, self.temp_id, self.status, [[x, y], [x, y]],
                                        self.temp_algorithm)
                self.scene().addItem(self.temp_item)
            else:
                if event.button() == Qt.RightButton:
                    # self.item_dict[self.temp_id] = self.temp_item
                    # self.list_widget.addItem(self.temp_id)
                    self.finish_draw()
                    self.temp_item = None
                else:
                    success = self.polygoncheck(x, y)
                    if success:
                        self.temp_item.p_list.append([x, y])
                    else:
                        # self.item_dict[self.temp_id] = self.temp_item
                        # self.list_widget.addItem(self.temp_id)
                        self.finish_draw()
                        self.temp_item = None
        if self.status == 'translate':
            if self.temp_id not in self.item_dict:
                self.status=''
                pass
            elif self.temp_item is None:
                # print(self.selected_id)
                self.temp_item = self.item_dict[self.temp_id]
                self.centerx, self.centery = self.getcenterpoint(self.temp_item)
                # self.scene().addItem(self.temp_item)#可能不需要
        if self.status == 'rotate':
            if self.temp_id not in self.item_dict:
                self.status=''
                pass
            elif self.temp_item is None:
                self.temp_item = self.item_dict[self.temp_id]
                self.centerx, self.centery = self.getcenterpoint(self.temp_item)
                self.firstx = x
                self.firsty = y
        if self.status == 'scale':
            if self.temp_id not in self.item_dict:
                self.status=''
                pass
            elif self.temp_item is None:

                self.temp_item = self.item_dict[self.temp_id]
                self.centerx, self.centery = self.getcenterpoint(self.temp_item)
                self.firstx = x
                self.firsty = y
        if self.status=='clip':
            if self.temp_id not in self.item_dict:
                self.status=''
                pass
            elif self.temp_item is None:
                #print(self.temp_id)
                self.temp_item = self.item_dict[self.temp_id]
                self.firstx=x
                self.firsty=y
                self.drawtemp_item=MyItem(1, Qt.blue,-1, "Rect", [[x, y], [x, y]],
                                        self.temp_algorithm)
                self.scene().addItem(self.drawtemp_item)
        if self.status=='cursor':
            #print("cursor")
            tempx=x
            tempy=y
            temptemp_item=self.itemAt(tempx,tempy)
            select_id=-1
            for k,v in self.item_dict.items():
                if v==temptemp_item:
                    select_id=k
            self.cur_id=select_id

        if self.status=='polygon_cut':
            if self.temp_id not in self.item_dict:
                self.status=''
                pass
            elif self.temp_item is None:
                self.temp_item = self.item_dict[self.temp_id]
                self.firstx=x
                self.firsty=y
                self.drawtemp_item=MyItem(1, Qt.green,-1, "Rect", [[x, y], [x, y]],
                                        self.temp_algorithm)
                self.scene().addItem(self.drawtemp_item)



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
            # self.temp_item.prepareGeometryChange()
            self.updateScene([self.sceneRect()])
        #
        if self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
            self.updateScene([self.sceneRect()])
            # self.temp_item.prepareGeometryChange()
        if self.status == 'translate':
            # self.temp_item.posx=x
            # self.temp_item.posy=y
            self.temp_item.translate(x - self.centerx, y - self.centery)
            self.centerx, self.centery = self.getcenterpoint(self.temp_item)
            self.updateScene([self.sceneRect()])
        if self.status == 'rotate':
            angle = self.computerangle(self.firstx, self.firsty, self.centerx, self.centery, x, y)
            # print(angle)
            angle = 0 - angle
            self.temp_item.rotate(self.centerx, self.centery, angle)
            # self.rotateangle =angle
            self.firstx = x
            self.firsty = y
            self.centerx, self.centery = self.getcenterpoint(self.temp_item)
            self.updateScene([self.sceneRect()])

        if self.status == 'scale':
            scale = self.getscale(self.centerx, self.centery, self.firstx, self.firsty, x, y)
            self.temp_item.scalea(self.centerx,self.centery,scale)
            self.firstx = x
            self.firsty = y
            self.centerx=self.centerx
            self.centery=self.centery
            #self.centerx, self.centery = self.getcenterpoint(self.temp_item)
            self.updateScene([self.sceneRect()])
        if self.status=='clip':
            x0,y0=self.firstx,self.firsty
            xmin=min(x0,x)
            xmax=max(x0,x)
            ymin=min(y0,y)
            ymax=max(y0,y)
            self.drawtemp_item.p_list[0]=[xmin,ymin]
            self.drawtemp_item.p_list[1]=[xmax,ymax]
            self.updateScene([self.sceneRect()])
        if self.status=='polygon_cut':
            x0, y0 = self.firstx, self.firsty
            xmin=min(x0,x)
            xmax=max(x0,x)
            ymin=min(y0,y)
            ymax=max(y0,y)
            self.drawtemp_item.p_list[0]=[xmin,ymin]
            self.drawtemp_item.p_list[1]=[xmax,ymax]
            self.updateScene([self.sceneRect()])



        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        x = min(x, 600)
        y = min(y, 600)
        x = max(0, x)
        y = max(0, y)
        if self.status == 'line':
            # self.item_dict[self.temp_id] = self.temp_item
            # self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        if self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
            self.updateScene([self.sceneRect()])
            # self.item_dict[self.temp_id] = self.temp_item
            # self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        if self.status == 'translate':
            self.item_dict[self.temp_id] = self.temp_item
            self.finish_draw()
        if self.status == 'rotate':
            self.temp_item.rotate_fill()
            self.item_dict[self.temp_id] = self.temp_item

            self.finish_draw()
        if self.status == 'scale':
            self.temp_item.scale_fill()
            self.item_dict[self.temp_id] = self.temp_item
            self.finish_draw()
        if self.status=='clip':
            self.temp_item.clip(self.firstx,self.firsty,x,y,self.temp_algorithm)
            self.scene().removeItem(self.drawtemp_item)
            self.item_dict[self.temp_id] = self.temp_item
            x0,y0=self.temp_item.p_list[0]
            x1,y1=self.temp_item.p_list[1]
            if x0==0 and y0==0 and x1==0 and y1==0:
                self.scene().removeItem(self.temp_item)
                #self.item_dict.pop(self.temp_id)
                self.status=''
                #self.list_widget.removeItemWidget(self.temp_id)

            self.finish_draw()
        if self.status=='cursor':
            #print(self.cur_id)
            self.selection_changed(self.cur_id)

        if self.status=='polygon_cut':
            self.temp_item.polygon_cut(self.firstx,self.firsty,x,y)
            self.scene().removeItem(self.drawtemp_item)
            self.item_dict[self.temp_id] = self.temp_item
            x0,y0=self.temp_item.p_list[0]
            x1,y1=self.temp_item.p_list[1]
            if x0==0 and y0==0 and x1==0 and y1==0:
                self.scene().removeItem(self.temp_item)
                #self.item_dict.pop(self.temp_id)
                self.status=''
                #self.list_widget.removeItemWidget(self.temp_id)

            self.finish_draw()


        #     # self.temp_item.posx=x
        #     # self.temp_item.posy=y
        #     self.temp_item.translate(x-self.centerx,y-self.centery)
        #     self.updateScene([self.sceneRect()])
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
        self.p_list = p_list  # 图元参数,如果是polygon_cut类型,最后两个点是边框(xmin,ymin,xmax,ymax)
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.pen_width = penwidth
        self.pen_color = pencolor
        self.temppen = QPen()
        self.temppen.setWidth(self.pen_width)
        self.temppen.setColor(self.pen_color)
        self.if_polygon_fill=False
        self.filled_list=[]
        self.fill_color=pencolor
        self.fillpen=QPen()
        #self.polygon_cut_list=[]#存储边框


    def translate(self, dx, dy):
        temp_list = alg.translate(self.p_list, dx, dy)
        # temp_list_int = []
        # for [x, y] in temp_list:
        #     temp_list_int.append([round(x), round(y)])
        self.p_list = temp_list
        if self.if_polygon_fill==True:
            temp_list=alg.translate(self.filled_list,dx,dy)
            self.filled_list=temp_list

    def rotate(self, x, y, r):
        if self.item_type!='ellipse':
            temp_list = alg.rotate(self.p_list, x, y, r)
            self.p_list = temp_list
        if self.if_polygon_fill==True:
            temp_list= alg.rotate(self.filled_list, x, y, r)
            self.filled_list=temp_list
    def rotate_fill(self):
        if self.if_polygon_fill==True:
            #print("herer\n")
            temp_list = alg.polifill(self.p_list)
            self.filled_list=temp_list



    def scalea(self, x, y, s):#重名加了一个a
        temp_list = alg.scale(self.p_list, x, y, s)
        self.p_list = temp_list
        if self.if_polygon_fill==True:
            temp_list= alg.scale(self.filled_list, x, y, s)
            self.filled_list=temp_list
    def scale_fill(self):
        if self.if_polygon_fill==True:
            #print("herer\n")
            temp_list = alg.polifill(self.p_list)
            self.filled_list=temp_list

    def clip(self,x1,y1,x2,y2,algorithm):
        if self.item_type=='line':
            xmin=min(x1,x2)
            ymin=min(y1,y2)
            xmax=max(x1,x2)
            ymax=max(y1,y2)
            temp_list=alg.clip(self.p_list,xmin,ymin,xmax,ymax,algorithm)
            self.p_list=temp_list
    def fill(self,fillcolor):

        self.fill_color=fillcolor
        self.if_polygon_fill=True
        self.filled_list=alg.polifill(self.p_list)
        self.fillpen.setColor(self.fill_color)
    def polygon_cut(self,x0,y0,x1,y1):
        xmin,xmax=min(x0,x1),max(x0,x1)
        ymin,ymax=min(y0,y1),max(y0,y1)
        if self.item_type=='polygon':
            self.item_type='polygon_cut'
            self.p_list.append([xmin,ymin])
            self.p_list.append([xmax,ymax])
        elif self.item_type=='polygon_cut':
            length=len(self.p_list)
            self.p_list[length-2]=[xmin,ymin]
            self.p_list[length-1]=[xmax,ymax]
    def x_mirror(self,centery):
        temp_list=alg.x_mirror(self.p_list,centery)
        self.p_list = temp_list
        if self.if_polygon_fill==True:
            temp_list= alg.x_mirror(self.filled_list,centery)
            self.filled_list=temp_list
    def y_mirror(self,centerx):
        temp_list=alg.y_mirror(self.p_list,centerx)
        self.p_list = temp_list
        if self.if_polygon_fill==True:
            temp_list= alg.y_mirror(self.filled_list,centerx)
            self.filled_list=temp_list





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
            if len(self.p_list) >= 2:
                #填充
                if self.if_polygon_fill:
                    painter.setPen(self.fillpen)
                    for p in self.filled_list:
                        painter.drawPoint(*p)
                painter.setPen(self.temppen)
                item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
                for p in item_pixels:
                    painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())


        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x_min = min(x0, x1)
            x_max = max(x0, x1)
            y_min = min(y0, y1)
            y_max = max(y0, y1)
            self.temp_list = []
            self.temp_list.append([x_min, y_max])
            self.temp_list.append([x_max, y_min])

            item_pixels = alg.draw_ellipse(self.temp_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            if len(self.p_list) >= 2:
                item_pixels = alg.draw_curve(self.p_list, self.algorithm)
                for p in item_pixels:
                    painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type=='Rect':
            fake_p_list=[]
            x0,y0=self.p_list[0]
            x1,y1=self.p_list[1]
            fake_p_list.append([x0,y0])
            fake_p_list.append([x0,y1])
            fake_p_list.append([x1,y1])
            fake_p_list.append([x1,y0])
            item_pixels=alg.draw_polygon(fake_p_list,"DDA")
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type=='polygon_cut':
            if len(self.p_list)>=4:
                length=len(self.p_list)
                xmin,ymin=self.p_list[length-2]
                xmax,ymax=self.p_list[length-1]
                temp_list=self.p_list[0:length-2]
                item_pixels=alg.draw_polygon_cut(temp_list,xmin,xmax,ymin,ymax)
                for p in item_pixels:
                    painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())




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
            if len(self.p_list) == 0:
                return QRectF(0, 0, 0, 0)
            if len(self.p_list) < 2:
                x0, y0 = self.p_list[0]
                return QRectF(x0 - 1, y0 - 1, x0 + 1, y0 + 1)
            x_list = []
            y_list = []
            for [x0, y0] in self.p_list:
                x_list.append(x0)
                y_list.append(y0)
            x = min(x_list)
            y = min(y_list)
            w = max(x_list) - x
            h = max(y_list) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            if len(self.p_list) == 0:
                return QRectF(0, 0, 0, 0)
            if len(self.p_list) < 2:
                x0, y0 = self.p_list[0]
                return QRectF(x0 - 1, y0 - 1, x0 + 1, y0 + 1)
            x_list = []
            y_list = []
            for [x0, y0] in self.p_list:
                x_list.append(x0)
                y_list.append(y0)
            x = min(x_list)
            y = min(y_list)
            w = max(x_list) - x
            h = max(y_list) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type=='Rect':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type=='polygon_cut':
            if len(self.p_list) == 0:
                return QRectF(0, 0, 0, 0)
            if len(self.p_list) < 2:
                x0, y0 = self.p_list[0]
                return QRectF(x0 - 1, y0 - 1, x0 + 1, y0 + 1)
            x_list = []
            y_list = []
            for [x0, y0] in self.p_list[0:(len(self.p_list))-2]:
                x_list.append(x0)
                y_list.append(y0)
            x = min(x_list)
            y = min(y_list)
            w = max(x_list) - x
            h = max(y_list) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
