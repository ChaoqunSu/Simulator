# 直航情况下

# Ship
# ##### 初始位置在中心点->便于模拟鱼雷从周围任何一方向发射而来以及划定周围10公里范围
# ##### 初始方向360度随机(float),初始方向既定以后就一直保持此方向航行(直航情况下，目前暂不考虑其发现鱼雷后做出的航向改变)
# ##### 匀速10m/s,ship和torpedo的速度以及二者的距离需要统一比例尺(根据窗口大小换算)

# Torpedo
# ##### 于10公里外的随机某处向ship发射，注意这里的10公里换算的比例尺
# ##### 匀速25m/s
# ##### 要想在直航情况下打中，需将ship的运动量考虑在内(这里不考虑ship发现鱼雷后做出航向上的改变)

# 记录下鱼雷轨迹140个点（x,y）
# 3.5公里外30%误差  以内2.5%误差  （3.5km 开始主动？）


from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random
import math


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
    else:
        angle = math.pi + math.atan(dy / dx)
    return angle


def get_initial_data():
    angle1 = random.uniform(0, 360)
    x1 = random.uniform(0, 20)
    y1 = random.uniform(0, 20)
    x2 = random.uniform(0, 20)
    y2 = random.uniform(0, 20)
    v1 = 0.01
    v2 = 0.025
    while math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < 10:
        x2 = random.uniform(0, 20)
        y2 = random.uniform(0, 20)
    return angle1, x1, y1, x2, y2, v1, v2


def visualize1(simulator1):
    # 船和鱼雷的初始位置以及创建轨迹数据列表
    X10 = simulator1.ship.x
    Y10 = simulator1.ship.y
    X20 = simulator1.torpedo.x
    Y20 = simulator1.torpedo.y
    X1 = [simulator1.ship.x]
    Y1 = [simulator1.ship.y]
    X2 = [simulator1.torpedo.x]
    Y2 = [simulator1.torpedo.y]
    # 设定窗口画布属性
    fig = plt.figure(figsize=(8, 8), facecolor='#000000', edgecolor='#333333')
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
    line1, = ax.plot(X1, Y1, 'go', markersize=7)
    line2, = ax.plot(X2, Y2, 'r>', markersize=3)
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
    plt.xlim(-15, 30)
    plt.ylim(-15, 30)
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
        X1.append(X10)
        Y1.append(Y10)
        X2.append(X20)
        Y2.append(Y20)

    def init():
        line1.set_data(X10, Y10)
        line2.set_data(X20, Y20)
        return line1, line2,

    def animate(i):
        line1.set_data(X1[i], Y1[i])
        line2.set_data(X2[i], Y2[i])
        plt.plot(X1[1:i], Y1[1:i], 'g--', linewidth=1.2)
        plt.plot(X2[1:i], Y2[1:i], 'r--', linewidth=1.0)
        return line1, line2,

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   frames=140,
                                   # init_func=init,
                                   blit=False,
                                   interval=60)

    # anim.save("直航.gif", writer='pillow', fps=60)
    plt.show()
    plt.pause(0)


def visualize2(simulator):
    # 线导(按距离调整变向)
    X10 = simulator.ship.x
    Y10 = simulator.ship.y
    X20 = simulator.torpedo.x
    Y20 = simulator.torpedo.y
    X1 = [simulator.ship.x]
    Y1 = [simulator.ship.y]
    X2 = [simulator.torpedo.x]
    Y2 = [simulator.torpedo.y]
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
    line1, = ax.plot(X1, Y1, 'go', markersize=7)
    line2, = ax.plot(X2, Y2, 'r>', markersize=3)
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
    plt.xlim(-15, 30)
    plt.ylim(-15, 30)
    # 鱼雷初始角度是对船方向，在绝大多数情况下与船的行驶方向不一致
    # 鱼雷需要每隔一段时间调整一次方向，直到鱼雷-船的距离在2km以内
    S0 = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    S = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    angle = get_position_angle(X10, Y10, X20, Y20)
    T = 0.000000000000
    nums = 0
    while S > 2:
        S = 0.3 * S
        t = S / simulator.torpedo.v
        n_steps = int(150*S/S0)
        # n_steps = 5*a
        time_step = t / n_steps
        dx1 = time_step * simulator.ship.v * math.cos(math.radians(simulator.ship.angle1))
        dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
        dx2 = time_step * simulator.torpedo.v * math.cos(angle)
        dy2 = time_step * simulator.torpedo.v * math.sin(angle)
        for i in range(n_steps):
            X10 += dx1
            Y10 += dy1
            X20 += dx2
            Y20 += dy2
            X1.append(X10)
            Y1.append(Y10)
            X2.append(X20)
            Y2.append(Y20)
        T += t
        nums += n_steps
        S = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
        angle = get_position_angle(X10, Y10, X20, Y20)
    # print(nums)
    # 自导(直线)
    cos1 = math.cos(math.radians(simulator.ship.angle1))
    angle2 = get_torpedo_angle(X10, Y10, X20, Y20, simulator.ship.v, simulator.torpedo.v, simulator.ship.angle1)
    cos2 = math.cos(angle2)
    t2 = (X10 - X20)/(simulator.torpedo.v * cos2 - simulator.ship.v * cos1)
    n_steps = 30
    time_step = t2 / n_steps
    dx1 = time_step * simulator.ship.v * cos1
    dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
    dx2 = time_step * simulator.torpedo.v * cos2
    dy2 = time_step * simulator.torpedo.v * math.sin(angle2)
    for i in range(n_steps):
        X10 += dx1
        Y10 += dy1
        X20 += dx2
        Y20 += dy2
        X1.append(X10)
        Y1.append(Y10)
        X2.append(X20)
        Y2.append(Y20)

    def animate(i):
        line1.set_data(X1[i], Y1[i])
        line2.set_data(X2[i], Y2[i])
        plt.plot(X1[0:i], Y1[0:i], 'g--', linewidth=1.2)
        plt.plot(X2[0:i], Y2[0:i], 'r--', linewidth=1.2)
        return line1, line2,

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   frames=nums + n_steps,
                                   # init_func=init,
                                   blit=False,
                                   interval=50)
    # anim.save("线导.gif", writer='pillow', fps=60)
    plt.show()
    plt.pause(0)


def visualize3(simulator):
    # 线导(按时间调整变向)
    X10 = simulator.ship.x
    Y10 = simulator.ship.y
    X20 = simulator.torpedo.x
    Y20 = simulator.torpedo.y
    X1 = [simulator.ship.x]
    Y1 = [simulator.ship.y]
    X2 = [simulator.torpedo.x]
    Y2 = [simulator.torpedo.y]
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
    line1, = ax.plot(X1, Y1, 'go', markersize=7)
    line2, = ax.plot(X2, Y2, 'r>', markersize=3)
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
    plt.xlim(-15, 30)
    plt.ylim(-15, 30)
    # 鱼雷初始角度是对船方向，在绝大多数情况下与船的行驶方向不一致
    # 鱼雷需要每隔一段时间调整一次方向，直到鱼雷-船的距离在2km以内
    S0 = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    S = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    angle = get_position_angle(X10, Y10, X20, Y20)
    T = 0.000000000000
    nums = 0
    while S > 2:
        t = 100
        n_steps = 25
        time_step = t / n_steps
        dx1 = time_step * simulator.ship.v * math.cos(math.radians(simulator.ship.angle1))
        dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
        dx2 = time_step * simulator.torpedo.v * math.cos(angle)
        dy2 = time_step * simulator.torpedo.v * math.sin(angle)
        for i in range(n_steps):
            X10 += dx1
            Y10 += dy1
            X20 += dx2
            Y20 += dy2
            X1.append(X10)
            Y1.append(Y10)
            X2.append(X20)
            Y2.append(Y20)
        T += t
        nums += n_steps
        S = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
        angle = get_position_angle(X10, Y10, X20, Y20)
    # print(nums)
    # 自导(直线)
    cos1 = math.cos(math.radians(simulator.ship.angle1))
    angle2 = get_torpedo_angle(X10, Y10, X20, Y20, simulator.ship.v, simulator.torpedo.v, simulator.ship.angle1)
    cos2 = math.cos(angle2)
    t2 = (X10 - X20) / (simulator.torpedo.v * cos2 - simulator.ship.v * cos1)
    n_steps = 30
    iter1 = n_steps + nums
    time_step = t2 / n_steps
    dx1 = time_step * simulator.ship.v * cos1
    dy1 = time_step * simulator.ship.v * math.sin(math.radians(simulator.ship.angle1))
    dx2 = time_step * simulator.torpedo.v * cos2
    dy2 = time_step * simulator.torpedo.v * math.sin(angle2)
    for i in range(n_steps):
        X10 += dx1
        Y10 += dy1
        X20 += dx2
        Y20 += dy2
        X1.append(X10)
        Y1.append(Y10)
        X2.append(X20)
        Y2.append(Y20)

    def animate(i):
        line1.set_data(X1[i], Y1[i])
        line2.set_data(X2[i], Y2[i])
        plt.plot(X1[0:i], Y1[0:i], 'g--', linewidth=1.2)
        plt.plot(X2[0:i], Y2[0:i], 'r--', linewidth=1.0)
        return line1, line2,

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   frames=iter1,
                                   # init_func=init,
                                   blit=False,
                                   interval=50)

    anim.save("线导.gif", writer='pillow', fps=60)
    plt.show()
    plt.pause(0)


def test_visualize1():
    angle1, x1, y1, x2, y2, v1, v2 = get_initial_data()
    cos1 = math.cos(math.radians(angle1))
    angle2 = get_torpedo_angle(x1, y1, x2, y2, v1, v2, angle1)
    cos2 = math.cos(angle2)
    t = (x1 - x2) / (v2 * cos2 - v1 * cos1)
    ship = Ship1(x1, y1, angle1, v1)
    torpedo = Torpedo1(x2, y2, angle2, v2)
    simulator1 = Simulator1(ship, torpedo, t)
    visualize1(simulator1)


def test_visualize2():
    angle1, x1, y1, x2, y2, v1, v2 = get_initial_data()
    ship = Ship1(x1, y1, angle1, v1)
    torpedo = Torpedo2(x2, y2, v2)
    simulator2 = Simulator2(ship, torpedo)
    visualize2(simulator2)


def test_visualize3():
    angle1, x1, y1, x2, y2, v1, v2 = get_initial_data()
    ship = Ship1(x1, y1, angle1, v1)
    torpedo = Torpedo2(x2, y2, v2)
    simulator2 = Simulator2(ship, torpedo)
    visualize3(simulator2)


if __name__ == '__main__':
    # test_visualize1()
    test_visualize2()
    # test_visualize3()