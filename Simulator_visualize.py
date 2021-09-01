
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import math
import numpy as np
"""
导出视频必须下载ffmeg.exe文件，经过路径导入
"""
plt.rcParams['animation.ffmpeg_path'] = r'D:\ffmpeg\bin\ffmpeg.exe'


class Ship1:
    def __init__(self, x, y, angle1, v):
        self.x = x
        self.y = y
        self.angle1 = angle1
        self.v = v


class Torpedo1:
    def __init__(self, x, y, angle2, v):
        self.x = x
        self.y = y
        self.angle2 = angle2
        self.v = v


class Torpedo2:
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v


class Simulator1:
    def __init__(self, ship, torpedo, t):
        self.ship = ship
        self.torpedo = torpedo
        self.t = t


class Simulator2:
    def __init__(self, ship, torpedo):
        self.ship = ship
        self.torpedo = torpedo


def get_torpedo_angle(x1, y1, x2, y2, v1, v2, angle1):
    dx = x1 - x2
    dy = y1 - y2
    b = v1 / v2
    if dx > 0:
        if dy > 0:
            angle2 = math.atan(dy / dx) + math.asin(b * math.sin(math.radians(angle1) - math.atan(dy / dx)))
        else:
            angle2 = 2 * math.pi + math.atan(dy / dx) + math.asin(
                b * math.sin(math.radians(angle1) - math.atan(dy / dx)))
    else:
        angle2 = math.pi + math.atan(dy / dx) - math.asin(b * math.sin(math.radians(angle1) - math.atan(dy / dx)))
    return angle2


def get_position_angle(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    if dx > 0:
        if dy > 0:
            angle = math.atan(dy / dx)
        else:
            angle = 2 * math.pi + math.atan(dy / dx)
    elif dx < 0:
        angle = math.pi + math.atan(dy / dx)
    else:
        if dy > 0:
            angle = 0.5 * math.pi
        else:
            angle = 1.5 * math.pi
    return angle


def get_initial_data():
    x1 = 15
    x2 = random.uniform(0, 30)
    y1 = 15
    y2 = random.uniform(0, 30)
    while y1 == y2:
        y2 = random.uniform(0, 30)
    while x1 == x2:
        x2 = random.uniform(0, 30)
    v1 = 0.01
    v2 = 0.025
    while math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < 10 or math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) > 15:
        x2 = random.uniform(0, 30)
        y2 = random.uniform(0, 30)
    theta = get_position_angle(x1, y1, x2, y2)
    flag = random.randint(0, 3)
    if flag == 0:
        angle1 = random.uniform(math.degrees(theta) + 40, math.degrees(theta) + 65)
    elif flag == 1:
        angle1 = random.uniform(math.degrees(theta) + 65, math.degrees(theta) + 90)
    elif flag == 2:
        angle1 = random.uniform(math.degrees(theta) - 40, math.degrees(theta) - 65)
    else:
        angle1 = random.uniform(math.degrees(theta) - 65, math.degrees(theta) - 90)
    return angle1, x1, y1, x2, y2, v1, v2


def zone_point(x1, y1, angle1):
    """
    传入A点坐标即舰船坐标以及航向角度
    按照B，C，D，E顺序计算
    """
    angle2 = angle1 + 135
    angle3 = angle1 + 225
    angle4 = angle1 + 180
    x2 = x1 + 0.085 * math.sqrt(2) * math.cos(math.radians(angle2))
    y2 = y1 + 0.085 * math.sqrt(2) * math.sin(math.radians(angle2))
    x3 = x1 + 0.085 * math.sqrt(2) * math.cos(math.radians(angle3))
    y3 = y1 + 0.085 * math.sqrt(2) * math.sin(math.radians(angle3))
    x4 = x3 + 1.715 * math.cos(math.radians(angle4))
    y4 = y3 + 1.715 * math.sin(math.radians(angle4))
    x5 = x2 + 1.715 * math.cos(math.radians(angle4))
    y5 = y2 + 1.715 * math.sin(math.radians(angle4))
    poly = [[x2, y2], [x3, y3], [x4, y4], [x5, y5]]
    return poly


def is_in_zone(x, y, px, py, angle1):
    """
    判断鱼雷是否已经进入尾流区域，ture/false
    :x,y 舰船坐标，angle1 舰船航向角度
    :px,py鱼雷坐标
    :poly:[[],[],[],...]
    """
    poly = zone_point(x, y, angle1)
    is_in = False
    for i, corner in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = corner
        x2, y2 = poly[next_i]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:  # if point is on edge
                is_in = True
                break
            elif x > px:  # if point is on left-side of line
                is_in = not is_in
    return is_in


def edge_num(x, y, px, py, angle1):
    """
    判断鱼雷从尾流区域哪条边进入
    :x,y 舰船坐标，angle1 舰船航向角度
    :px,py鱼雷坐标
    :return: 1,2,3,4
    """
    [[x2, y2], [x3, y3], [x4, y4], [x5, y5]] = zone_point(x, y, angle1)
    # 舰船A对鱼雷之角度
    a = get_position_angle(px, py, x, y)
    # A对B,C,D,E之角度
    b1 = get_position_angle(x2, y2, x, y)
    b2 = get_position_angle(x3, y3, x, y)
    b3 = get_position_angle(x4, y4, x, y)
    b4 = get_position_angle(x5, y5, x, y)
    if min(b1, b4) <= a <= max(b1, b4):
        return 1     # AB与AE之间，BE边进入
    elif min(b3, b4) <= a <= max(b3, b4):
        return 2     # AE与AD之间，DE边进入
    elif min(b2, b3) <= a <= max(b2, b3):
        return 3     # AD与AC之间，CD边进入
    else:
        return 4     # AB或AC边进入，几乎不可能


def get_error_data(x1, y1, x2, y2):
    s = math.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)
    # 探测鱼雷位置的误差点在以真实点为圆心，r为半径的圆内，先给r初始化一个值
    if s >= 3.5:
        r = s * 0.3
    elif 0.1 < s < 3.5:
        r = s * 0.025 + 0.05
    else:
        r = s * 0.5
    """
    方向误差，限制条件是方向误差必须与上一个误差圆相交，否则得不到监测数据
    由正态分布生成的误差角必须满足以下条件
    r > s * math.sin(math.radians(error_angle))
    """
    # 生成服从正态分布的误差角，均值为真实值，方差为3.2
    miu = get_position_angle(x2, y2, x1, y1)
    # miu此为弧度，先转为角度，再代入得到监测数据
    monitor_angle = np.random.normal(loc=math.degrees(miu), scale=math.sqrt(3.2))
    # monitor_angle是角度，把miu转为角度，都是角度好判正负，生成error_angle也是角度
    test_angle = math.degrees(math.asin(r/s))
    error_angle = math.fabs(monitor_angle - math.degrees(miu))
    while math.degrees(miu) - test_angle > monitor_angle or monitor_angle > math.degrees(miu) + test_angle:
        monitor_angle = np.random.normal(loc=math.degrees(miu), scale=math.sqrt(3.2))
        error_angle = math.fabs(monitor_angle - math.degrees(miu))
    # 反余弦出来的beta是弧度
    print("monitor_angle=", monitor_angle, "miu=", math.degrees(miu))
    beta = math.acos(s * math.sin(math.radians(error_angle)) / r)
    print("beta=", math.degrees(beta))
    position_angle = get_position_angle(x1, y1, x2, y2)
    if monitor_angle > math.degrees(miu):
        theta_a = position_angle - (0.5 * math.pi - beta - math.radians(error_angle))
        theta_b = position_angle - (0.5 * math.pi - beta - math.radians(error_angle)) - 2 * beta
    else:
        theta_a = position_angle + (0.5 * math.pi - beta - math.radians(error_angle))
        theta_b = position_angle + (0.5 * math.pi - beta - math.radians(error_angle)) + 2 * beta
    x_a = x2 + r * math.cos(theta_a)
    y_a = y2 + r * math.sin(theta_a)
    x_b = x2 + r * math.cos(theta_b)
    y_b = y2 + r * math.sin(theta_b)
    if x_a != x_b:
        # 求截距式直线方程的k和b
        k = (y_b - y_a) / (x_b - x_a)
        b = (x_b * y_a - x_a * y_b)/(x_b - x_a)
        x = random.uniform(min(x_a, x_b), max(x_a, x_b))
        y = k * x + b
    else:
        x = x_a
        y = random.uniform(min(y_a, y_b), max(y_a, y_b))
    return x, y


def straight_running_torpedo(simulator1):
    # 船和鱼雷的初始位置以及创建轨迹数据列表
    X10 = simulator1.ship.x
    Y10 = simulator1.ship.y
    X20 = simulator1.torpedo.x
    Y20 = simulator1.torpedo.y
    X1 = [simulator1.ship.x]
    Y1 = [simulator1.ship.y]
    X2 = [simulator1.torpedo.x]
    Y2 = [simulator1.torpedo.y]
    x_error, y_error = get_error_data(X10, Y10, X20, Y20)
    X_error = [x_error]
    Y_error = [y_error]
    # 设定窗口画布属性
    fig = plt.figure(figsize=(6, 6), facecolor='#000000', edgecolor='#333333')
    fig.canvas.set_window_title('Simulator')
    # 设定窗口绝对位置(600, 626)
    mngr = plt.get_current_fig_manager()
    # geom = mngr.window.geometry()
    # x, y, dx, dy = geom.getRect()
    mngr.window.setGeometry(300, 31, 600, 626)
    # 设置窗口标题
    plt.title('Simulator')
    # 设定子窗口
    ax = plt.subplot(111, aspect='equal')
    # 设定子窗口轨迹动画颜色标志
    line1, = ax.plot(X1, Y1, 'go', markersize=4)
    line2, = ax.plot(X2, Y2, 'ro', markersize=1)
    line3, = ax.plot(X_error, Y_error, '.y', markersize=1.5)

    # 设置子窗口颜色
    ax.set_facecolor('#333333')
    # 设定子窗口坐标轴等属性
    ax.tick_params(axis='x', color='white', labelcolor='white')
    ax.tick_params(axis='y', color='white', labelcolor='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.plot()
    # 设定坐标轴范围
    plt.xlim(0, 30)
    plt.ylim(0, 30)
    # 计算直航情况下每步长后的坐标数据(列表数据)
    n_steps = 140
    time_step = simulator1.t / n_steps
    dx1 = time_step * simulator1.ship.v * math.cos(math.radians(simulator1.ship.angle1))
    dy1 = time_step * simulator1.ship.v * math.sin(math.radians(simulator1.ship.angle1))
    dx2 = time_step * simulator1.torpedo.v * math.cos(simulator1.torpedo.angle2)
    dy2 = time_step * simulator1.torpedo.v * math.sin(simulator1.torpedo.angle2)
    for i in range(n_steps):
        X10 += dx1
        Y10 += dy1
        X20 += dx2
        Y20 += dy2
        x_error, y_error = get_error_data(X10, Y10, X20, Y20)
        X1.append(X10)
        Y1.append(Y10)
        X2.append(X20)
        Y2.append(Y20)
        X_error.append(x_error)
        Y_error.append(y_error)

    def init():
        line1.set_data(X10, Y10)
        line2.set_data(X20, Y20)
        return line1, line2,

    def animate(i):
        line1.set_data(X1[i], Y1[i])
        line2.set_data(X2[i], Y2[i])
        line3.set_data(X_error[i], Y_error[i])
        plt.plot(X1[1:i], Y1[1:i], 'g--', linewidth=0.5)
        plt.plot(X2[1:i], Y2[1:i], 'r--', linewidth=0.5)
        plt.plot(X_error[1:i], Y_error[1:i], '.y', markersize=0.1)
        return line1, line2, line3,

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   frames=140,
                                   # init_func=init,
                                   blit=False,
                                   interval=30)
    # 存gif
    # anim.save("直航.gif", writer='pillow', fps=60)
    # 存视频
    # Writer = animation.FFMpegWriter(fps=20, metadata=dict(artist='Me'))
    # anim.save('h.mp4', writer=Writer)
    plt.show()


def wire_guided_torpedo(simulator):
    # 线导(按时间调整变向)
    # 船以及鱼雷的位置
    X10 = simulator.ship.x
    Y10 = simulator.ship.y
    X20 = simulator.torpedo.x
    Y20 = simulator.torpedo.y
    # 潜艇位置(鱼雷初始位置)
    X30 = simulator.torpedo.x
    Y30 = simulator.torpedo.y
    # 船位置数据列表以及鱼雷数据列表
    X1 = [simulator.ship.x]
    Y1 = [simulator.ship.y]
    X2 = [simulator.torpedo.x]
    Y2= [simulator.torpedo.y]
    x_error, y_error = get_error_data(X10, Y10, X20, Y20)
    X_error = [x_error]
    Y_error = [y_error]
    # 设定窗口画布属性
    fig = plt.figure(figsize=(6, 6), facecolor='#000000', edgecolor='#333333')
    fig.canvas.set_window_title('Simulator')
    # 设定窗口绝对位置(600, 626)
    mngr = plt.get_current_fig_manager()
    # geom = mngr.window.geometry()
    # x, y, dx, dy = geom.getRect()
    mngr.window.setGeometry(300, 31, 600, 626)
    # 设置窗口标题
    plt.title('Simulator')
    # 设定子窗口
    ax = plt.subplot(111, aspect='equal')
    # 设定子窗口轨迹动画颜色标志
    line1, = ax.plot(X1, Y1, 'go', markersize=4)
    line2, = ax.plot(X2, Y2, 'ro', markersize=1)
    line3, = ax.plot(X_error, Y_error, '.y', markersize=1.5)
    # 设置子窗口颜色
    ax.set_facecolor('#333333')
    # 设定子窗口坐标轴等属性
    ax.tick_params(axis='x', color='white', labelcolor='white')
    ax.tick_params(axis='y', color='white', labelcolor='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.plot()
    # 设定坐标轴范围
    plt.xlim(0, 30)
    plt.ylim(0, 30)
    # 鱼雷初始位置就是潜艇位置，鱼雷初始角度是潜艇对船方向，角度更新时以
    # 鱼雷需要每隔一段时间调整一次方向，直到鱼雷-船的距离在2km以内
    # angle3是鱼雷的速度方向
    # angle3 = get_position_angle(X10, Y10, X30, Y30) + math.radians(random.uniform(10.0, 15.0))
    angle3 = get_position_angle(X10, Y10, X30, Y30)
    print(angle3)
    s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    # nums = n_steps
    # print(X20)
    nums1 = 0
    while s > 2:
        time_step = 4.0
        n_steps = 8
        dx1 = time_step * simulator.ship.v * math.cos(math.radians(simulator.ship.angle1))
        dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
        dx2 = time_step * simulator.torpedo.v * math.cos(angle3)
        dy2 = time_step * simulator.torpedo.v * math.sin(angle3)
        for i in range(n_steps):
            X10 += dx1
            Y10 += dy1
            X20 += dx2
            Y20 += dy2
            X1.append(X10)
            Y1.append(Y10)
            X2.append(X20)
            Y2.append(Y20)
            x_error, y_error = get_error_data(X10, Y10, X20, Y20)
            X_error.append(x_error)
            Y_error.append(y_error)
            # 隔点调整角度，让转弯更顺滑
            if i % 2 == 0:
                angle2 = get_position_angle(X10, Y10, X30, Y30)
                angle4 = get_position_angle(X20, Y20, X30, Y30)
                a = math.fabs(angle3 - angle2)
                if angle2 > angle4:
                    angle3 = angle2 + 0.4*0.5 * 0.5 * (math.pi - a)
                else:
                    angle3 = angle2 - 0.4*0.5 * 0.5 * (math.pi - a)
        # angle2 = get_position_angle(X10, Y10, X30, Y30)
        # angle4 = get_position_angle(X20, Y20, X30, Y30)
        # a = math.fabs(angle3 - angle2)
        # if angle2 > angle4:
        #     angle3 = angle2 + 0.5*0.5 * (math.pi - a)
        # else:
        #     angle3 = angle2 - 0.5*0.5 * (math.pi - a)
        nums1 += n_steps
        s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    print(nums1)
    # 声呐自导(考虑声呐在水中的传导速度)
    angle = get_position_angle(X10, Y10, X20, Y20)
    nums2 = 0
    s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    while s > 0.01:
        time_step = 2
        dx1 = time_step * simulator.ship.v * math.cos(math.radians(simulator.ship.angle1))
        dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
        dx2 = time_step * simulator.torpedo.v * math.cos(angle)
        dy2 = time_step * simulator.torpedo.v * math.sin(angle)
        X10 += dx1
        Y10 += dy1
        X20 += dx2
        Y20 += dy2
        X1.append(X10)
        Y1.append(Y10)
        X2.append(X20)
        Y2.append(Y20)
        x_error, y_error = get_error_data(X10, Y10, X20, Y20)
        X_error.append(x_error)
        Y_error.append(y_error)
        nums2 += 1
        s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
        angle = get_position_angle(X10, Y10, X20, Y20)
    iter1 = nums1 + nums2
    print(iter1)

    def animate(i):
        line1.set_data(X1[i], Y1[i])
        line2.set_data(X2[i], Y2[i])
        line3.set_data(X_error[i], Y_error[i])
        plt.plot(X1[0:i], Y1[0:i], 'g--', linewidth=0.5)
        plt.plot(X2[0:i], Y2[0:i], 'r--', linewidth=0.5)
        plt.plot(X_error[1:i], Y_error[1:i], '.y', markersize=0.1)
        return line1, line2, line3,

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   frames=iter1,
                                   # init_func=init,
                                   blit=False,
                                   interval=30)

    # 存gif图
    # anim.save("线导.gif", writer='pillow', fps=60)
    # 存视频
    # Writer = animation.FFMpegWriter(fps=20, metadata=dict(artist='Me'))
    # anim.save('h.mp4', writer=Writer)
    plt.show()


def wake_homing_torpedo(simulator):
    """
    线导直至尾流区域，尾流自导
    :param simulator: 包括ship,torpedo等类
    :return: 无
    """
    # 船以及鱼雷的位置
    X10 = simulator.ship.x
    Y10 = simulator.ship.y
    X20 = simulator.torpedo.x
    Y20 = simulator.torpedo.y
    # 潜艇位置(鱼雷初始位置)
    X30 = simulator.torpedo.x
    Y30 = simulator.torpedo.y
    # 船位置数据列表以及鱼雷数据列表
    X1 = [simulator.ship.x]
    Y1 = [simulator.ship.y]
    X2 = [simulator.torpedo.x]
    Y2 = [simulator.torpedo.y]
    x_error, y_error = get_error_data(X10, Y10, X20, Y20)
    X_error = [x_error]
    Y_error = [y_error]
    # 设定窗口画布属性
    fig = plt.figure(figsize=(6, 6), facecolor='#000000', edgecolor='#333333')
    fig.canvas.set_window_title('Simulator')
    # 设定窗口绝对位置(600, 626)
    mngr = plt.get_current_fig_manager()
    # geom = mngr.window.geometry()
    # x, y, dx, dy = geom.getRect()
    mngr.window.setGeometry(300, 31, 600, 626)
    # 设置窗口标题
    plt.title('Simulator')
    # 设定子窗口
    ax = plt.subplot(111, aspect='equal')
    # 设定子窗口轨迹动画颜色标志
    line1, = ax.plot(X1, Y1, 'go', markersize=4)
    line2, = ax.plot(X2, Y2, 'ro', markersize=1)
    line3, = ax.plot(X_error, Y_error, '.y', markersize=1.5)
    # 设置子窗口颜色
    ax.set_facecolor('#333333')
    # 设定子窗口坐标轴等属性
    ax.tick_params(axis='x', color='white', labelcolor='white')
    ax.tick_params(axis='y', color='white', labelcolor='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.plot()
    # 设定坐标轴范围
    plt.xlim(0, 30)
    plt.ylim(0, 30)
    """
    鱼雷初始位置就是潜艇位置，鱼雷初始角度是潜艇对船方向，线导过程中鱼雷需要每隔一段时间调整一次方向
    直到鱼雷进入船的尾流区域内
    angle3是鱼雷的速度方向
    模拟鱼雷进尾流时，鱼雷目标点应该是尾流中心点而不是舰船
    angle3 = get_position_angle(X10, Y10, X30, Y30) + math.radians(random.uniform(10.0, 15.0))
    """
    # 获取尾流区域各顶点
    [[x2, y2], [x3, y3], [x4, y4], [x5, y5]] = zone_point(X10, Y10, simulator.ship.angle1)
    print(math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2))
    # 计算得到尾流区域中心点
    x_center = 0.5 * (x2 + x4)
    y_center = 0.5 * (y2 + y4)
    # angle3 = get_position_angle(X10, Y10, X30, Y30)
    angle3 = get_position_angle(x_center, y_center, X30, Y30)
    nums1 = 0
    nums2 = 0
    nums3 = 0
    while not is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1):
        time_step = 6.0
        n_steps = 25
        dx1 = time_step * simulator.ship.v * math.cos(math.radians(simulator.ship.angle1))
        dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
        # dx2 = time_step * simulator.torpedo.v * math.cos(angle3)
        # dy2 = time_step * simulator.torpedo.v * math.sin(angle3)
        for i in range(n_steps):
            dx2 = time_step * simulator.torpedo.v * math.cos(angle3)
            dy2 = time_step * simulator.torpedo.v * math.sin(angle3)
            X10 += dx1
            Y10 += dy1
            X20 += dx2
            Y20 += dy2
            x_center += dx1
            y_center += dy1
            X1.append(X10)
            Y1.append(Y10)
            X2.append(X20)
            Y2.append(Y20)
            x_error, y_error = get_error_data(X10, Y10, X20, Y20)
            X_error.append(x_error)
            Y_error.append(y_error)
            nums1 += 1
            [[x2, y2], [x3, y3], [x4, y4], [x5, y5]] = zone_point(X10, Y10, simulator.ship.angle1)
            # 计算得到尾流区域中心点
            x_center = 0.5 * (x2 + x4)
            y_center = 0.5 * (y2 + y4)

            if i % 2 == 0:
                angle2 = get_position_angle(x_center, y_center, X30, Y30)
                angle4 = get_position_angle(X20, Y20, X30, Y30)
                a = math.fabs(angle3 - angle2)
                if angle2 > angle4:
                    angle3 = angle2 + 0.4*0.5 * 0.5 * (math.pi - a)
                else:
                    angle3 = angle2 - 0.4*0.5 * 0.5 * (math.pi - a)

            # angle2 = get_position_angle(x_center, y_center, X30, Y30)
            # # angle2 = get_position_angle(X10, Y10, X30, Y30)
            # angle4 = get_position_angle(X20, Y20, X30, Y30)
            # a = math.fabs(angle3 - angle2)
            # if angle2 > angle4:
            #     angle3 = angle2 + 0.5 * 0.5 * (math.pi - a)
            # else:
            #     angle3 = angle2 - 0.5 * 0.5 * (math.pi - a)
            if is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1):
                break
        if is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1):
            break

    print(nums1)
    """
    上一阶段结束条件即进入尾流
    尾流自导
    """
    # 尾流区域各顶点位置数据列表(AC、D、E、BA)
    [[x2, y2], [x3, y3], [x4, y4], [x5, y5]] = zone_point(X10, Y10, simulator.ship.angle1)
    X3 = [x3]
    Y3 = [y3]
    X4 = [x4]
    Y4 = [y4]
    X5 = [x5]
    Y5 = [y5]
    X6 = [x2]
    Y6 = [y2]

    s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    print(s)
    # print(is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1))
    while s >= 0.15:
        # 进入尾流之后先直航
        while is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1):
            time_step = 0.4
            dx1 = time_step * simulator.ship.v * math.cos(math.radians(simulator.ship.angle1))
            dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
            dx2 = time_step * simulator.torpedo.v * math.cos(angle3)
            dy2 = time_step * simulator.torpedo.v * math.sin(angle3)
            X10 += dx1
            x2 += dx1
            x3 += dx1
            x4 += dx1
            x5 += dx1
            Y10 += dy1
            y2 += dy1
            y3 += dy1
            y4 += dy1
            y5 += dy1
            X20 += dx2
            Y20 += dy2
            X1.append(X10)
            Y1.append(Y10)
            X2.append(X20)
            Y2.append(Y20)
            X3.append(x3)
            Y3.append(y3)
            X4.append(x4)
            Y4.append(y4)
            X5.append(x5)
            Y5.append(y5)
            X6.append(x2)
            Y6.append(y2)
            if nums2 % 5 == 0:
                x_error, y_error = get_error_data(X10, Y10, X20, Y20)
                X_error.append(x_error)
                Y_error.append(y_error)
                nums3 += 1
            nums2 += 1
            s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
            if s < 0.15:
                break
        if s < 0.15:
            break
        print("直航出尾流")
        """
        直航出来之后，打圆弧轨迹
        """
        # 鱼雷速度方向与舰船方向角度差
        alpha = math.fabs(simulator.ship.angle1 - angle3)
        # 定义角速度
        w = 0.05 * math.pi
        total_time = 2 * alpha / w
        # 每一时间步长的角度变化
        time_step = 0.4
        delta_theta = w * time_step
        # print(delta_theta)
        # 比较鱼雷与舰船角度的flag，用于驱动鱼雷的整体方向往舰船方向趋近
        a = simulator.ship.angle1 - math.degrees(angle3)
        # print("a=", a)
        dx1 = time_step * simulator.ship.v * math.cos(math.radians(simulator.ship.angle1))
        dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
        while not is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1):
            dx2 = time_step * simulator.torpedo.v * math.cos(angle3)
            dy2 = time_step * simulator.torpedo.v * math.sin(angle3)
            X10 += dx1
            x2 += dx1
            x3 += dx1
            x4 += dx1
            x5 += dx1
            Y10 += dy1
            y2 += dy1
            y3 += dy1
            y4 += dy1
            y5 += dy1
            X20 += dx2
            Y20 += dy2
            X1.append(X10)
            Y1.append(Y10)
            X2.append(X20)
            Y2.append(Y20)
            X3.append(x3)
            Y3.append(y3)
            X4.append(x4)
            Y4.append(y4)
            X5.append(x5)
            Y5.append(y5)
            X6.append(x2)
            Y6.append(y2)
            if nums2 % 5 == 0:
                x_error, y_error = get_error_data(X10, Y10, X20, Y20)
                X_error.append(x_error)
                Y_error.append(y_error)
                nums3 += 1
            if a > 0:
                angle3 = angle3 + delta_theta
                print("1  angle3=", math.degrees(angle3))
                print("1 angle1=", simulator.ship.angle1)
            else:
                angle3 = angle3 - delta_theta
                print("2  angle3=", math.degrees(angle3))
                print("2  angle1=", simulator.ship.angle1)
            nums2 += 1
            s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
            if s < 0.15:
                break
        if s < 0.15:
            break
        # 每次完成圆周运动进入尾流时对angle3进行修正
        if simulator.ship.angle1 - math.degrees(angle3) > 0:
            angle3 = angle3 + 2 * delta_theta
        else:
            angle3 = angle3 - 2 * delta_theta
        print("打出圆弧")
    if s < 0.15:
        torpedo_angle = get_torpedo_angle(X10, Y10, X20, Y20, simulator.ship.v, simulator.torpedo.v,
                                          simulator.ship.angle1)
        cos1 = math.cos(math.radians(simulator.ship.angle1))
        cos2 = math.cos(torpedo_angle)
        t = (X10 - X20) / (simulator.torpedo.v * cos2 - simulator.ship.v * cos1)
        time_step = 0.4
        n_steps = int(t/0.4)
        dx1 = time_step * simulator.ship.v * math.cos(math.radians(simulator.ship.angle1))
        dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
        dx2 = time_step * simulator.torpedo.v * math.cos(torpedo_angle)
        dy2 = time_step * simulator.torpedo.v * math.sin(torpedo_angle)
        for i in range(n_steps):
            X10 += dx1
            x2 += dx1
            x3 += dx1
            x4 += dx1
            x5 += dx1
            Y10 += dy1
            y2 += dy1
            y3 += dy1
            y4 += dy1
            y5 += dy1
            X20 += dx2
            Y20 += dy2
            X1.append(X10)
            Y1.append(Y10)
            X2.append(X20)
            Y2.append(Y20)
            X3.append(x3)
            Y3.append(y3)
            X4.append(x4)
            Y4.append(y4)
            X5.append(x5)
            Y5.append(y5)
            X6.append(x2)
            Y6.append(y2)
            if nums2 % 5 == 0:
                x_error, y_error = get_error_data(X10, Y10, X20, Y20)
                X_error.append(x_error)
                Y_error.append(y_error)
                nums3 += 1
            nums2 += 1
    iter1 = nums1 + nums2
    print(nums2)

    # 尾流区域各顶点数据
    point_x = [[1]]*nums2
    point_y = [[1]]*nums2
    for j in range(nums2):
        point_x[j] = [[X1[nums1+j], X3[j]], [X3[j], X4[j]], [X4[j], X5[j]], [X5[j], X6[j]], [X6[j], X1[nums1+j]]]
        point_y[j] = [[Y1[nums1+j], Y3[j]], [Y3[j], Y4[j]], [Y4[j], Y5[j]], [Y5[j], Y6[j]], [Y6[j], Y1[nums1+j]]]

    # line3, = ax.plot(X3, Y3, 'ro', markersize=0.2)
    # line4, = ax.plot(X4, Y4, 'ro', markersize=0.2)

    def animate(i):
        if i <= nums1:
            line1.set_data(X1[i], Y1[i])
            line2.set_data(X2[i], Y2[i])
            plt.plot(X1[0:i], Y1[0:i], 'g--', linewidth=0.3)
            plt.plot(X2[0:i], Y2[0:i], 'r--', linewidth=0.3)
            line3.set_data(X_error[i], Y_error[i])
            plt.plot(X_error[1:i], Y_error[1:i], '.y', markersize=0.1)
        elif i > nums1:
            plt.xlim(min(X1[nums1], X1[iter1], X2[nums1], X2[iter1])-2, max(X1[nums1], X1[iter1], X2[nums1], X2[iter1])+2)
            plt.ylim(min(Y1[nums1], Y1[iter1], Y2[nums1], Y2[iter1])-2, max(Y1[nums1], Y1[iter1], Y2[nums1], Y2[iter1])+2)
            line1.set_data(X1[i], Y1[i])
            line2.set_data(X2[i], Y2[i])
            plt.plot(X1[0:i], Y1[0:i], 'g--', linewidth=0.3)
            plt.plot(X2[0:i], Y2[0:i], 'r--', linewidth=0.3)
            data_i = int((i-nums1) / 5)
            line3.set_data(X_error[nums1+data_i], Y_error[nums1+data_i])
            plt.plot(X_error[1:nums1+data_i], Y_error[1:nums1+data_i], '.y', markersize=0.1)
            # line3.set_data(X3[i-nums1], Y3[i-nums1])
            # line4.set_data(X4[i-nums1], Y4[i-nums1])
            # plt.plot([X3[i-nums1], X4[i-nums1]], [Y3[i-nums1], Y4[i-nums1]])
            for j in range(5):
                plt.plot(point_x[i-nums1][j], point_y[i-nums1][j], 'w--', linewidth=0.03)

        return line1, line2, line3,

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   frames=iter1,
                                   # init_func=init,
                                   blit=False,
                                   interval=20)

    # anim.save("尾流.gif", writer='pillow', fps=60)
    # Writer = animation.FFMpegWriter(fps=20, metadata=dict(artist='Me'))
    # anim.save('h.mp4', writer=Writer)
    plt.show()


def test_straight():
    angle1, x1, y1, x2, y2, v1, v2 = get_initial_data()
    cos1 = math.cos(math.radians(angle1))
    angle2 = get_torpedo_angle(x1, y1, x2, y2, v1, v2, angle1)
    cos2 = math.cos(angle2)
    t = (x1 - x2) / (v2 * cos2 - v1 * cos1)
    ship = Ship1(x1, y1, angle1, v1)
    torpedo = Torpedo1(x2, y2, angle2, v2)
    simulator1 = Simulator1(ship, torpedo, t)
    straight_running_torpedo(simulator1)


def test_wire_guided():
    angle1, x1, y1, x2, y2, v1, v2 = get_initial_data()
    ship = Ship1(x1, y1, angle1, v1)
    torpedo = Torpedo2(x2, y2, v2)
    simulator2 = Simulator2(ship, torpedo)
    wire_guided_torpedo(simulator2)


def test_wake_homing():
    angle1, x1, y1, x2, y2, v1, v2 = get_initial_data()
    ship = Ship1(x1, y1, angle1, v1)
    torpedo = Torpedo2(x2, y2, v2)
    simulator2 = Simulator2(ship, torpedo)
    wake_homing_torpedo(simulator2)


if __name__ == '__main__':
    # test_straight()
    # test_wire_guided()
    test_wake_homing()