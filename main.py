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


class Ship:
    def __init__(self, x, y, angle1, v):
        self.x = x
        self.y = y
        self.angle1 = angle1
        self.v = v


class Torpedo:
    def __init__(self, x, y, angle2, v):
        self.x = x
        self.y = y
        self.angle2 = angle2
        self.v = v


class Simulator1:
    def __init__(self, ship, torpedo, t):
        self.ship = ship
        self.torpedo = torpedo
        self.t = t

    def hit(self, dt):
        n_steps = 140
        time_step = dt / n_steps
        print(self.ship.v)
        dx1 = time_step * self.ship.v * math.cos(math.radians(self.ship.angle1))
        dy1 = time_step * self.ship.v * math.sin(math.radians(self.ship.angle1))
        dx2 = time_step * self.torpedo.v * math.cos(self.torpedo.angle2)
        dy2 = time_step * self.torpedo.v * math.sin(self.torpedo.angle2)
        for i in range(n_steps):
            self.ship.x += dx1
            self.ship.y += dy1
            self.torpedo.x += dx2
            self.torpedo.y += dy2



def get_torpedo_angle(x1, y1, x2, y2, v1, v2, angle1):
    dx = x1 - x2
    dy = y1 - y2
    b = v1 / v2
    if dx > 0:
        if dy > 0:
            angle2 = math.atan(dy/dx) + math.asin(b * math.sin(math.radians(angle1) - math.atan(dy/dx)))
        else:
            angle2 = 2*math.pi + math.atan(dy/dx) + math.asin(b * math.sin(math.radians(angle1) - math.atan(dy/dx)))
    else:
        angle2 = math.pi + math.atan(dy/dx) - math.asin(b * math.sin(math.radians(angle1) - math.atan(dy/dx)))

    return angle2


def visualize(simulator1):
    X1 = [simulator1.ship.x]
    Y1 = [simulator1.ship.y]
    X2 = [simulator1.torpedo.x]
    Y2 = [simulator1.torpedo.y]
    fig = plt.figure()
    ax = plt.subplot(111, aspect='equal')
    line1, = ax.plot(X1, Y1, 'ro')
    line2, = ax.plot(X2, Y2, 'rv')

    plt.xlim(-10, 30)
    plt.ylim(-10, 30)

    def init():
        line1.set_data(X1, Y1)
        line2.set_data(X2, Y2)
        return line1,line2,

    def init2():
        line2.set_data(X2, Y2)
        return line2,

    simulator1.hit(simulator1.t)
    X1 = [simulator1.ship.x]
    Y1 = [simulator1.ship.y]
    X2 = [simulator1.torpedo.x]
    Y2 = [simulator1.torpedo.y]

    def animate(aa):
        # simulator1.hit(simulator1.t)
        # X1 = [simulator1.ship.x]
        # Y1 = [simulator1.ship.y]
        # X2 = [simulator1.torpedo.x]
        # Y2 = [simulator1.torpedo.y]
        # print(X1)
        # line1, = ax.plot(X1, Y1, 'ro')
        # line2, = ax.plot(X2, Y2, 'rv')
        line1.set_data(X1, Y1)
        line2.set_data(X2, Y2)
        return line1,line2,

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   frames=100000000,
                                   init_func=init,
                                   blit=True,
                                   interval=5000
                                   )
    plt.show()


def test_visualize():
    angle1 = random.uniform(0, 360)
    x1 = random.uniform(0, 20)
    y1 = random.uniform(0, 20)
    x2 = random.uniform(0, 20)
    y2 = random.uniform(0, 20)
    v1 = 0.01
    v2 = 0.025
    while math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < 10:
        x2 = random.uniform(0, 20)
        y2 = random.uniform(0, 20)
    # print(x1, y1)
    # print(x2, y2)
    cos1 = math.cos(math.radians(angle1))
    angle2 = get_torpedo_angle(x1, y1, x2, y2, v1, v2, angle1)
    cos2 = math.cos(angle2)
    t = (x1 - x2)/(v2 * cos2 - v1 * cos1)
    print(t)
    ship = Ship(x1, y1, angle1, v1)
    torpedo = Torpedo(x2, y2, angle2, v2)
    simulator = Simulator1(ship, torpedo, t)
    visualize(simulator)


if __name__ == '__main__':
    test_visualize()