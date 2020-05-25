#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x0 > x1:
            x1, x0 = x0, x1
            y1, y0 = y0, y1
        dx = x1 - x0
        dy = y1 - y0
        k = 999999999
        k_inf = 0
        if dx == 0:
            k_inf = 1
        else:
            k = dy / dx
        x = round(x0)
        y = round(y0)
        '''起始点'''
        if k > -1 and k < 1:
            while True:
                if x > x1:
                    break
                result.append((round(x), round(y)))
                x = x + 1
                y = y + k
        elif k >= 1:
            '''Y最大位移'''
            while True:
                if y > y1:
                    break
                result.append((round(x), round(y)))
                y = y + 1
                if k_inf == 0:
                    x = x + 1 / k
                else:
                    x = x
        else:
            while True:
                if y < y1:
                    break
                result.append((round(x), round(y)))
                y = y - 1
                if k_inf == 0:
                    x = x - 1 / k
                else:
                    x = x

        '''pass'''
        '''参考:https://www.youtube.com/watch?v=W5P8GlaEOSI
        https://blog.csdn.net/u010429424/article/details/77834046
        '''
    elif algorithm == 'Bresenham':
        if x0 > x1:
            x1, x0 = x0, x1
            y1, y0 = y0, y1
        dx = x1 - x0
        dy = y1 - y0
        f = 0

        if 0 <= dy <= dx:
            x = x0
            y = y0
            while x <= x1:
                result.append((round(x), round(y)))
                if f + dy + f + dy - dx < 0:
                    f = f + dy
                else:
                    f = f + dy - dx
                    y = 1 + y
                x = x + 1
        elif dy >= 0 and dy > dx:
            x = x0
            y = y0
            while y <= y1:
                result.append((round(x), round(y)))
                if f - dx + f - dx + dy > 0:
                    f = f - dx
                else:
                    f = f - dx + dy
                    x = x + 1
                y = y + 1
        elif dy <= 0 and -dy <= dx:
            x = x0
            y = y0
            while x <= x1:
                result.append((round(x), round(y)))
                if f + dy + f + dy + dx > 0:
                    f = f + dy
                else:
                    f = f + dy + dx
                    y = y - 1
                x = x + 1
        elif dy <= 0 and -dy > dx:
            x = x0
            y = y0
            while y >= y1:
                result.append((round(x), round(y)))
                if f + dx + f + dx + dy < 0:
                    f = f + dx
                else:
                    f = f + dx + dy
                    x = x + 1
                y = y - 1

        ''' pass'''
        '''参考:https://www.youtube.com/watch?v=RGB-wlatStc&t=415s
        https://segmentfault.com/a/1190000002700500'''
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]

    rx = abs(x1 - x0) / 2
    ry = abs(y1 - y0) / 2
    xc = x0 + rx
    yc = y0 + ry
    p = ry * ry - rx * rx * ry + (rx * rx / 4)

    tx = 0
    ty = ry
    packet = []
    packet.append((round(tx), round(ry)))
    # print("begin",rx,ry,xc,yc)
    while 2 * ry * ry * tx < 2 * rx * rx * ty:
        #   print(tx,ty)
        #  print("left",2 * ry * ry * tx," right",2 * rx * ty)

        if p < 0:
            tx = tx + 1
            p = p + 2 * ry * ry * tx + ry * ry
        elif p >= 0:
            tx = tx + 1
            ty = ty - 1
            p = p + 2 * ry * ry * tx - 2 * rx * rx * ty + ry * ry
        # print("herer")
        packet.append((round(tx), round(ty)))
    # print("out left", 2 * ry * ry * tx, " right", 2 * rx * ty)
    p2 = ry * ry * (tx + 0.5) * (tx + 0.5) + rx * rx * (ty - 1) * (ty - 1) - rx * rx * ry * ry
    # print("next")
    while True:
        #   print(tx, ty)
        if tx >= rx and ty <= 0:
            '''循环到(rx,0)'''
            break
        if p2 > 0:
            ty = ty - 1
            p2 = p2 - 2 * rx * rx * ty + rx * rx
        else:
            tx = tx + 1
            ty = ty - 1
            p2 = p2 + 2 * ry * ry * tx - 2 * rx * rx * ty + rx * rx

        packet.append((round(tx), round(ty)))

    for k in range(len(packet)):
        tempx, tempy = packet[k]
        result.append((round(xc + tempx), round(yc + tempy)))
        result.append((round(xc + tempx), round(yc - tempy)))
        result.append((round(xc - tempx), round(yc + tempy)))
        result.append((round(xc - tempx), round(yc - tempy)))

    return result


##B 样条曲线的辅助函数
def getLambda(i, r, t, u):
    if abs(u[i + 4 - r] - u[i]) <= 1e-7:
        return 0
    else:
        return (t - u[i]) / (u[i + 4 - r] - u[i])


def deBoorCox_X(i, r, t, p_list, u):
    tempx, tempy = p_list[i]
    # if t==2:
    #    print("r:",r)
    if r == 0:
        return tempx
    else:
        return getLambda(i, r, t, u) * deBoorCox_X(i, r - 1, t, p_list, u) + (1 - getLambda(i, r, t, u)) * deBoorCox_X(
            i - 1, r - 1, t, p_list, u)


def deBoorCox_Y(i, r, t, p_list, u):
    tempx, tempy = p_list[i]
    if r == 0:
        return tempy
    else:
        return getLambda(i, r, t, u) * deBoorCox_Y(i, r - 1, t, p_list, u) + (1 - getLambda(i, r, t, u)) * deBoorCox_Y(
            i - 1, r - 1, t, p_list, u)


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    q_list = []
    # print("here")
    if algorithm == 'Bezier':
        # 使用了De Casteljau’s Algorithm
        n = len(p_list)  # 次数
        # print(n)
        qy = []
        qx = []
        for i in range(len(p_list)):
            tempx, tempy = p_list[i]
            # print(tempx, tempy)
            qx.append(tempx)
            qy.append(tempy)
            # q_list.append([tempx, tempy])

        xarray = [0 for _ in range(n)]
        yarray = [0 for _ in range(n)]

        x = qx[0]
        y = qy[0]
        # print("n:",n)
        for tt in range(0, 1000 * n + 1, 1):
            t = (tt / 1000) / n
            # print(t)
            for i in range(1, n, 1):  # 迭代的次数
                for j in range(0, n - i, 1):

                    if i == 1:
                        xarray[j] = qx[j] * (1 - t) + qx[j + 1] * t
                        yarray[j] = qy[j] * (1 - t) + qy[j + 1] * t
                        continue
                    else:
                        xarray[j] = xarray[j] * (1 - t) + xarray[j + 1] * t
                        yarray[j] = yarray[j] * (1 - t) + yarray[j + 1] * t

            q_list.append([x, y])
            x = xarray[0]
            y = yarray[0]

        for i in range(0, len(q_list) - 1):
            line = draw_line([q_list[i], q_list[i + 1]], 'DDA')
            result += line
        # pass
    elif algorithm == 'B-spline':
        k = 4
        n = len(p_list) - 1
        q_list = []
        u = [0 for _ in range(n + k + 2)]
        for i in range(0, n + k + 1 + 1, 1):
            # print(n,i)
            u[i] = i

        step = 0.01
        for j in range(k - 1, n + 1, 1):
            t = u[j]
            # print("j:t",j,t)
            while t <= u[j + 1]:
                # print(t)
                x = deBoorCox_X(j, k - 1, t, p_list, u)
                y = deBoorCox_Y(j, k - 1, t, p_list, u)
                q_list.append([x, y])
                t = t + step
        for i in range(0, len(q_list) - 1):
            line = draw_line([q_list[i], q_list[i + 1]], 'DDA')
            result += line

    # 参考: Bezier: https://www.bilibili.com/video/av33675067?p=15
    # https://www.bilibili.com/video/av66548502?p=11
    # https://blog.csdn.net/Fioman/article/details/2578895
    # B样条
    # https://www.bilibili.com/video/av33675067?t=4&p=22
    # http://www.whudj.cn/?p=535
    # https://blog.csdn.net/qingcaichongchong/article/details/52797854
    # pass
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for [i, j] in p_list:
        #  print(i,j)
        tempx = i + dx
        tempy = j + dy
        result.append([tempx, tempy])
    return result

    # pass


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # print(math.pi);
    Pi = math.pi
    Theta = -r * Pi / 180
    result = []
    for [i, j] in p_list:
        x0 = i
        y0 = j
        tempx = x + (x0 - x) * math.cos(Theta) - (y0 - y) * math.sin(Theta)
        tempy = y + (x0 - x) * math.sin(Theta) + (y0 - y) * math.cos(Theta)
        result.append([tempx, tempy])
    return result


# 参考：https://blog.csdn.net/LearnLHC/article/details/93623031
# pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for [i, j] in p_list:
        x0 = x - i
        y0 = y - j
        tempx = x0 * s + x
        tempy = y0 * s + y
        result.append([tempx, tempy])
    return result
    # pass


def Checklocation(x, y, x_min, y_min, x_max, y_max) -> int:
    result = 0
    INSIDE = 0  # 0000
    LEFT = 1  # 0001
    RIGHT = 2  # 0010
    BOTTOM = 4  # 0100
    TOP = 8  # 1000

    result = INSIDE

    if x < x_min:
        result = result | LEFT
    elif x > x_max:
        result = result | RIGHT
    if y < y_min:
        result = result | BOTTOM
    elif y > y_max:
        result = result | TOP
    return result


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """

    # Cohen-Sutherland 算法
    # 参考:https://www.jianshu.com/p/d512116bbbf3
    # https://www.omegaxyz.com/2018/10/29/cohen-sutherland/
    if algorithm == 'Cohen-Sutherland':
        INSIDE = 0  # 0000
        LEFT = 1  # 0001
        RIGHT = 2  # 0010
        BOTTOM = 4  # 0100
        TOP = 8  # 1000
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]
        outcode0 = Checklocation(x0, y0, x_min, y_min, x_max, y_max)
        outcode1 = Checklocation(x1, y1, x_min, y_min, x_max, y_max)
        # print(x0, y0)
        # print(x1, y1)
        # print(x_max, y_max, x_min, y_min)
        pass
        # success = False
        while (1):
            # print(x1, y1, x0, y0)
            # print(outcode0, outcode1)
            if bool((outcode0 | outcode1)) == 0:
                success = True  # 在区域里面
                break
            elif bool(outcode0 & outcode1) == 1:  # 注意这里是位运算应该用Bool类型
                success = False  # 不在区域里面
                break
            else:
                # 找到界外的点
                x = 0
                y = 0
                if outcode0 == 0:
                    outcode = outcode1
                else:
                    outcode = outcode0
                # 找到和边界相交的点 点斜式:y-b=k(x-a)
                # y=y0+k*(x-x0) x=x0+(1/k)*(y-y0)

                if outcode & TOP:
                    rk = (x1 - x0) / (y1 - y0)
                    y = y_max
                    x = x0 + rk * (y - y0)
                elif outcode & BOTTOM:
                    rk = (x1 - x0) / (y1 - y0)
                    y = y_min
                    x = x0 + rk * (y - y0)
                elif outcode & RIGHT:
                    k = (y1 - y0) / (x1 - x0)
                    x = x_max
                    y = y0 + k * (x - x0)
                elif outcode & LEFT:
                    k = (y1 - y0) / (x1 - x0)
                    x = x_min
                    y = y0 + k * (x - x0)
                if outcode == outcode1:
                    x1 = x
                    y1 = y
                    outcode1 = Checklocation(x1, y1, x_min, y_min, x_max, y_max)
                else:
                    x0 = x
                    y0 = y
                    outcode0 = Checklocation(x0, y0, x_min, y_min, x_max, y_max)
        if success == True:
            result = [[x0, y0], [x1, y1]]
        else:
            result = [[0, 0], [0, 0]]
        return result
    elif algorithm == 'Liang-Barsky':
        # 参考：https://blog.csdn.net/soulmeetliang/article/details/79185603
        result = []
        # p_list, x_min, y_min, x_max, y_max, algorithm
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]
        dx = x1 - x0
        dy = y1 - y0
        p = [0 for _ in range(5)]
        q = [0 for _ in range(5)]
        p[1] = -dx
        p[2] = dx
        p[3] = -dy
        p[4] = dy
        q[1] = x0 - x_min
        q[2] = x_max - x0
        q[3] = y0 - y_min
        q[4] = y_max - y0
        success = 1
        # 初始状态:
        u1 = 0
        u2 = 1
        for i in range(1, 5, 1):
            if p[i] < 0:
                u1 = max(u1, q[i] / p[i])
            elif p[i] > 0:
                u2 = min(u2, q[i] / p[i])
            elif p[i] == 0 and q[i] < 0:
                success = 0
            if u1 > u2:
                success = 0

        if success == 0:
            result = [[0, 0], [0, 0]]
        else:
            x00 = x0 + u1 * dx
            y00 = y0 + u1 * dy
            x11 = x0 + u2 * dx
            y11 = y0 + u2 * dy
            result = [[x00, y00], [x11, y11]]

        return result

    # pass