
from matplotlib import pyplot as plt
import random
import math
import numpy as np
import pandas as pd


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
    while 15 < math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) or math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < 10:
        x2 = random.uniform(0, 30)
        y2 = random.uniform(0, 30)
    print(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
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
    ??????A??????????????????????????????????????????
    ??????B???C???D???E????????????
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
    ?????????????????????????????????????????????ture/false
    :x,y ???????????????angle1 ??????????????????
    :px,py????????????
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
    ??????????????????????????????????????????
    :x,y ???????????????angle1 ??????????????????
    :px,py????????????
    :return: 1,2,3,4
    """
    [[x2, y2], [x3, y3], [x4, y4], [x5, y5]] = zone_point(x, y, angle1)
    # ??????A??????????????????
    a = get_position_angle(px, py, x, y)
    # A???B,C,D,E?????????
    b1 = get_position_angle(x2, y2, x, y)
    b2 = get_position_angle(x3, y3, x, y)
    b3 = get_position_angle(x4, y4, x, y)
    b4 = get_position_angle(x5, y5, x, y)
    if min(b1, b4) <= a <= max(b1, b4):
        return 1     # AB???AE?????????BE?????????
    elif min(b3, b4) <= a <= max(b3, b4):
        return 2     # AE???AD?????????DE?????????
    elif min(b2, b3) <= a <= max(b2, b3):
        return 3     # AD???AC?????????CD?????????
    else:
        return 4     # AB???AC???????????????????????????


def get_error_data(x1, y1, x2, y2):
    s = math.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)
    # ?????????????????????????????????????????????????????????r???????????????????????????r??????????????????
    if s >= 3.5:
        r = s * 0.3
    elif 0.1 < s < 3.5:
        r = s * 0.025 + 0.05
    else:
        r = s * 0.5
    """
    ?????????????????????????????????????????????????????????????????????????????????????????????????????????
    ?????????????????????????????????????????????????????????
    r > s * math.sin(math.radians(error_angle))
    """
    # ?????????????????????????????????????????????????????????????????????3.2
    miu = get_position_angle(x2, y2, x1, y1)
    # miu????????????????????????????????????????????????????????????
    monitor_angle = np.random.normal(loc=math.degrees(miu), scale=math.sqrt(3.2))
    # monitor_angle???????????????miu????????????????????????????????????????????????error_angle????????????
    test_angle = math.degrees(math.asin(r/s))
    error_angle = math.fabs(monitor_angle - math.degrees(miu))
    while math.degrees(miu) - test_angle > monitor_angle or monitor_angle > math.degrees(miu) + test_angle:
        monitor_angle = np.random.normal(loc=math.degrees(miu), scale=math.sqrt(3.2))
        error_angle = math.fabs(monitor_angle - math.degrees(miu))
    # ??????????????????beta?????????
    # print("monitor_angle=", monitor_angle, "miu=", math.degrees(miu))
    beta = math.acos(s * math.sin(math.radians(error_angle)) / r)
    # print("beta=", math.degrees(beta))
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
        # ???????????????????????????k???b
        k = (y_b - y_a) / (x_b - x_a)
        b = (x_b * y_a - x_a * y_b)/(x_b - x_a)
        x = random.uniform(min(x_a, x_b), max(x_a, x_b))
        y = k * x + b
    else:
        x = x_a
        y = random.uniform(min(y_a, y_b), max(y_a, y_b))
    return x, y


"""
??????????????????????????????????????????????????????????????????????????????2???
sample_time = 2
"""


def visualize1(simulator1):
    # ?????????????????????????????????????????????????????????
    sample_time = 2
    X10 = simulator1.ship.x
    Y10 = simulator1.ship.y
    X20 = simulator1.torpedo.x
    Y20 = simulator1.torpedo.y
    X1 = [round(simulator1.ship.x, 6)]
    Y1 = [simulator1.ship.y]
    X2 = [simulator1.torpedo.x]
    Y2 = [simulator1.torpedo.y]
    x_error, y_error = get_error_data(X10, Y10, X20, Y20)
    X_error = [x_error]
    Y_error = [y_error]
    # data = [[x_error, y_error]]
    # ????????????????????????????????????????????????(????????????)
    n_steps = int(simulator1.t/sample_time)
    dx1 = sample_time * simulator1.ship.v * math.cos(math.radians(simulator1.ship.angle1))
    dy1 = sample_time * simulator1.ship.v * math.sin(math.radians(simulator1.ship.angle1))
    dx2 = sample_time * simulator1.torpedo.v * math.cos(simulator1.torpedo.angle2)
    dy2 = sample_time * simulator1.torpedo.v * math.sin(simulator1.torpedo.angle2)
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
        # data.append([x_error, y_error])
        X_error.append(x_error)
        Y_error.append(y_error)
    print(n_steps)
    head = ['X', 'Y']
    out_list = [X_error, Y_error]
    # list_change = numpy.transpose(out_list)
    test = pd.DataFrame(data=out_list)
    test.to_csv('add.csv', mode='a', header=False, index=False)


def visualize2(simulator):
    # ??????(?????????????????????)
    # ????????????????????????
    X10 = simulator.ship.x
    Y10 = simulator.ship.y
    X20 = simulator.torpedo.x
    Y20 = simulator.torpedo.y
    data_x1 = simulator.ship.x
    data_y1 = simulator.ship.y
    data_x2 = simulator.torpedo.x
    data_y2 = simulator.torpedo.y
    # ????????????(??????????????????)
    X30 = simulator.torpedo.x
    Y30 = simulator.torpedo.y
    # ?????????????????????????????????????????????
    X1 = [simulator.ship.x]
    Y1 = [simulator.ship.y]
    X2 = [simulator.torpedo.x]
    Y2= [simulator.torpedo.y]
    x_error, y_error = get_error_data(X10, Y10, X20, Y20)
    X_error = [x_error]
    Y_error = [y_error]
    # ???????????????????????????????????????????????????????????????????????????????????????????????????
    # ???????????????????????????????????????????????????????????????-???????????????2km??????
    # angle3????????????????????????
    # angle3 = get_position_angle(X10, Y10, X30, Y30) + math.radians(random.uniform(10.0, 15.0))
    angle3 = get_position_angle(X10, Y10, X30, Y30)
    s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
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
            for j in range(2):
                data_x1 += 0.5 * dx1
                data_y1 += 0.5 * dy1
                data_x2 += 0.5 * dx2
                data_y2 += 0.5 * dy2
                x_error, y_error = get_error_data(data_x1, data_y1, data_x2, data_y2)
                X_error.append(x_error)
                Y_error.append(y_error)
            # ???????????????????????????????????????
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

        # angle3 = 2 * angle2 - angle3
        # if angle2 > angle4:
        #     angle3 = 2 * angle2 - angle3

        nums1 += 2 * n_steps
        s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    # ????????????(????????????????????????????????????)
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
    out_list = [X_error, Y_error]
    # list_change = numpy.transpose(out_list)
    test = pd.DataFrame(data=out_list)
    test.to_csv('add.csv', mode='a', header=False, index=False)


def visualize3(simulator):
    """
    ???????????????????????????????????????
    :param simulator: ??????ship,torpedo??????
    :return: ???
    """
    # ????????????????????????
    X10 = simulator.ship.x
    Y10 = simulator.ship.y
    X20 = simulator.torpedo.x
    Y20 = simulator.torpedo.y
    data_x1 = simulator.ship.x
    data_y1 = simulator.ship.y
    data_x2 = simulator.torpedo.x
    data_y2 = simulator.torpedo.y
    # ????????????(??????????????????)
    X30 = simulator.torpedo.x
    Y30 = simulator.torpedo.y
    # ?????????????????????????????????????????????
    X1 = [simulator.ship.x]
    Y1 = [simulator.ship.y]
    X2 = [simulator.torpedo.x]
    Y2 = [simulator.torpedo.y]
    x_error, y_error = get_error_data(X10, Y10, X20, Y20)
    X_error = [x_error]
    Y_error = [y_error]
    """
    ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
    ???????????????????????????????????????
    angle3????????????????????????
    ?????????????????????????????????????????????????????????????????????????????????
    angle3 = get_position_angle(X10, Y10, X30, Y30) + math.radians(random.uniform(10.0, 15.0))
    """
    # ???????????????????????????
    [[x2, y2], [x3, y3], [x4, y4], [x5, y5]] = zone_point(X10, Y10, simulator.ship.angle1)
    print(math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2))
    # ?????????????????????????????????
    x_center = 0.5 * (x2 + x4)
    y_center = 0.5 * (y2 + y4)
    # angle3 = get_position_angle(X10, Y10, X30, Y30)
    angle3 = get_position_angle(x_center, y_center, X30, Y30)
    nums1 = 0
    nums3 = 0
    while not is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1):
        time_step = 6
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
            for j in range(3):
                data_x1 += 1/3 * dx1
                data_y1 += 1/3 * dy1
                data_x2 += 1/3 * dx2
                data_y2 += 1/3 * dy2
                x_error, y_error = get_error_data(data_x1, data_y1, data_x2, data_y2)
                X_error.append(x_error)
                Y_error.append(y_error)
                nums3 += 1
            X1.append(X10)
            Y1.append(Y10)
            X2.append(X20)
            Y2.append(Y20)
            nums1 += 1
            [[x2, y2], [x3, y3], [x4, y4], [x5, y5]] = zone_point(X10, Y10, simulator.ship.angle1)
            # ?????????????????????????????????
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
            if is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1):
                break
        if is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1):
            break
        # angle2 = get_position_angle(x_center, y_center, X30, Y30)
        # angle4 = get_position_angle(X20, Y20, X30, Y30)
        # a = math.fabs(angle3 - angle2)
        # if angle2 > angle4:
        #     angle3 = angle2 + 0.5 * 0.5 * (math.pi - a)
        # else:
        #     angle3 = angle2 - 0.5 * 0.5 * (math.pi - a)

    # print(nums1)
    """
    ???????????????????????????????????????
    ????????????
    """
    # ???????????????????????????????????????(AC???D???E???BA)
    [[x2, y2], [x3, y3], [x4, y4], [x5, y5]] = zone_point(X10, Y10, simulator.ship.angle1)
    X3 = [x3]
    Y3 = [y3]
    X4 = [x4]
    Y4 = [y4]
    X5 = [x5]
    Y5 = [y5]
    X6 = [x2]
    Y6 = [y2]
    nums2 = 0
    s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
    # print(s)
    # print(is_in_zone(X10, Y10, X20, Y20, simulator.ship.angle1))
    while s >= 0.15:
        # ???????????????????????????
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
        print("???????????????")
        """
        ????????????????????????????????????
        """
        # ??????????????????????????????????????????
        alpha = math.fabs(simulator.ship.angle1 - angle3)
        # ???????????????
        w = 0.05 * math.pi
        total_time = 2 * alpha / w
        # ?????????????????????????????????
        time_step = 0.4
        delta_theta = w * time_step
        # print(delta_theta)
        # ??????????????????????????????flag?????????????????????????????????????????????????????????
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
                # print("1  angle3=", math.degrees(angle3))
                # print("1 angle1=", simulator.ship.angle1)
            else:
                angle3 = angle3 - delta_theta
                # print("2  angle3=", math.degrees(angle3))
                # print("2  angle1=", simulator.ship.angle1)
            nums2 += 1
            s = math.sqrt((X10 - X20) ** 2 + (Y10 - Y20) ** 2)
            if s < 0.15:
                break
        if s < 0.15:
            break
        # ??????????????????????????????????????????angle3????????????
        if simulator.ship.angle1 - math.degrees(angle3) > 0:
            angle3 = angle3 + 2 * delta_theta
        else:
            angle3 = angle3 - 2 * delta_theta
        print("????????????")
    if s < 0.15:
        torpedo_angle = get_torpedo_angle(X10, Y10, X20, Y20, simulator.ship.v, simulator.torpedo.v,
                                          simulator.ship.angle1)
        cos1 = math.cos(math.radians(simulator.ship.angle1))
        cos2 = math.cos(torpedo_angle)
        t = (X10 - X20) / (simulator.torpedo.v * cos2 - simulator.ship.v * cos1)
        time_step = 0.4
        n_steps = int(t / 0.4)
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
    print(nums3)
    out_list = [X_error, Y_error]
    # list_change = numpy.transpose(out_list)
    test = pd.DataFrame(data=out_list)
    test.to_csv('add.csv', mode='a', header=False, index=False)


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
    for i in range(300):
        # test_visualize1()
        # test_visualize2()
        test_visualize3()