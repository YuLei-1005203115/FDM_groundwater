# 地下水流随机方程的数值模拟求解尝试
import random
from scipy.fftpack import fft, ifft

import numpy as np
from numpy import sin, cos, tan
import numpy.linalg as nla
from sympy import symbols
import sympy as sy
import matplotlib

matplotlib.use('QtAgg')
import matplotlib.pyplot as plt


class Random_flow:
    def __init__(self):
        self.ic = None
        self.tl = None
        self.st = None
        self.name_chinese = "非稳定随机一维流"
        self.xl = None
        self.sl = None
        self.h_r = []
        self.h_l = []
        self.B = 1  # 默认一维流的宽度为1个单位

    def l_boundary(self, h_l, Dirichlet=False, Neumann=False, Robin=False):  # 左边界
        if Dirichlet:
            self.h_l = [1, float(h_l)]
        elif Neumann:
            self.h_l = [2, float(h_l)]

    def r_boundary(self, h_r, Dirichlet=False, Neumann=False, Robin=False):  # 右边界
        if Dirichlet:
            self.h_r = [1, float(h_r)]
        elif Neumann:
            self.h_r = [2, float(h_r)]

    def step_length(self, sl):  # X轴差分步长
        self.sl = float(sl)

    def step_time(self, st):  # 时间轴差分步长
        self.st = float(st)

    def x_length(self, xl):  # X轴轴长
        self.xl = float(xl)

    def t_length(self, tl):  # 时间轴轴长，原则上单位为天
        self.tl = float(tl)

    def initial_condition(self, ic: str):  # 初始条件的水头设定
        self.ic = str(ic)

    def width(self, B):  # 含水层宽度的设定
        self.B = float(B)

    def draw(self, H_ALL: np.ndarray, time=0, title=''):  # 按给定的时刻绘制水头曲线
        # X轴单元格的数目
        m = int(self.xl / self.sl) + 1
        # X轴
        X = np.linspace(0, self.xl, m)
        # 可以plt绘图过程中中文无法显示的问题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决负号为方块的问题
        plt.rcParams['axes.unicode_minus'] = False
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot()
        ax.plot(X, H_ALL[time], linewidth=1, antialiased=True)

        def maxH_y(h_all):
            hy = 0
            for i in h_all:
                if i > hy:
                    hy = i
            return hy

        def minH_y(h_all):
            hy = 0
            for i in h_all:
                if i < hy:
                    hy = i
            return hy

        ax.set_ylim(minH_y(H_ALL[time]), maxH_y(H_ALL[time]))
        ax.set(ylabel='水头（m）', xlabel='X轴（m）')
        plt.suptitle(self.name_chinese)
        if title == '':
            plt.title("差分数值解，当前为第{0}时刻(差分空间步长{1}，时间步长{2})".format(time, self.sl, self.st))
        else:
            plt.title(title)
        plt.show()

    def draw_location(self, H_ALL: np.ndarray, location=0, title=''):  # 按给定的时刻绘制水头曲线
        # T轴单元格的数目
        m = int(self.tl / self.st) + 1
        # T轴
        T = np.linspace(0, self.tl, m)
        # 水头轴
        H = []
        for i in H_ALL:
            H.append(i[location])
        # 可以plt绘图过程中中文无法显示的问题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决负号为方块的问题
        plt.rcParams['axes.unicode_minus'] = False
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot()
        ax.plot(T, H, linewidth=1, antialiased=True)
        ax.set_ylim(min(H) - 1, max(H) + 1)
        ax.set(ylabel='水头（m）', xlabel='时间轴（d）')
        plt.suptitle(self.name_chinese)
        if title == '':
            plt.title("差分数值解，当前为第{0}位置(差分空间步长{1}，时间步长{2})".format(location, self.sl, self.st))
        else:
            plt.title(title)
        plt.show()

    def draw_surface(self, H_ALL: np.ndarray, title=''):  # 绘制表面图
        # X轴单元格的数目
        m = int(self.xl / self.sl) + 1
        # 时间轴单元格数目
        n = int(self.tl / self.st) + 1
        # X轴
        X = np.linspace(0, self.xl, m)
        # 时间轴
        T = np.linspace(0, self.tl, n)
        # 定义初值
        X, T = np.meshgrid(X, T)
        # 可以plt绘图过程中中文无法显示的问题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决负号为方块的问题
        plt.rcParams['axes.unicode_minus'] = False
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(projection='3d')

        def maxH_z(h_all):
            hz = 0
            for i in h_all:
                for j in i:
                    if j > hz:
                        hz = j
            return hz

        def minH_z(h_all):
            hz = 0
            for i in h_all:
                for j in i:
                    if j < hz:
                        hz = j
            return hz

        ax.set_zlim(minH_z(H_ALL), maxH_z(H_ALL))
        ax.plot_surface(X, T, H_ALL, linewidth=0, antialiased=True, cmap=plt.get_cmap('rainbow'))
        ax.set(zlabel='水头（m）', ylabel='时间轴（d）', xlabel='X轴（m）')
        plt.suptitle(self.name_chinese)
        if title == '':
            plt.title("差分数值解(差分空间步长{0}，时间步长{1})".format(self.sl, self.st))
        else:
            plt.title(title)
        plt.show()


class Random_one_dimension_boussinesq(Random_flow):
    def __init__(self):
        super().__init__()
        self.we = None
        self.Sy = None
        self.K = None
        self.w = None
        self.a = None
        self.a_as = None
        self.ha = None
        self.name_chinese = '潜水含水层随机非稳定一维流'

    def reference_thickness(self, ha):  # 潜水含水层的参考厚度，解析解求解中使用参考厚度法线性化偏微分方程
        self.ha = float(ha)

    def pressure_diffusion_coefficient(self, a):  # 潜水含水层压力扩散系数的设定。等于渗透系数乘初始水头常数除给水度Kh0/Sy
        self.a = float(a)

    def source_sink_expectation(self, we):  # 源汇项期望值的设定
        self.we = float(we)

    def source_sink_term(self, w: str):  # 潜水含水层源汇项的设定，可以为一个常数也可以为函数,如sin(x) + cos(t)
        self.w = w

    def fft_source_sink_term(self):  # 对源汇项做快速傅里叶变换
        # 时间轴单元格数目
        n = int(self.tl / self.st) + 1
        # 时间轴
        t = np.linspace(0, self.tl, n)
        fft_w = fft(eval(self.w))
        return fft_w

    @staticmethod
    def fft_location(H_ALL: np.ndarray, location=0):  # 对一个位置的不同时刻水头做快速傅里叶变换
        # 同一位置不同时刻的离散水头
        H = []
        for i in H_ALL:
            H.append(i[location])
        fft_H = fft(H)
        return fft_H

    def hydraulic_conductivity(self, K):  # 潜水含水层渗透系数的设定
        self.K = float(K)

    def specific_yield(self, Sy):  # 潜水含水层储水系数（重力给水度）的设定
        self.Sy = float(Sy)

    def random_w(self):
        # 随机振幅生成
        amplitude = random.uniform(0, self.we)
        # 随机周期生成
        while True:
            cycle = self.tl / int(random.uniform(1, 50))  # 依据香农采样定理采样频率必须大于信号频率的两倍
            if cycle >= 3 * self.st:  # 所以信号周期的随机生成必须大于采样周期的两倍，本程序取三倍
                break
        # 随机频率
        frequency = 1 / cycle
        return amplitude, cycle, frequency

    def solve(self):
        # 如果未设定压力扩散系数
        if self.a is None or self.a == "":
            self.a = self.K / self.Sy
        # 对于潜水含水层一维非稳定流，定义两个参数 x t
        x = symbols("x")
        t = symbols("t")
        # X轴差分点的数目
        m = int(self.xl / self.sl) + 1
        # 时间轴差分点的数目
        n = int(self.tl / self.st) + 1

        # 对函数W(x, t)定义为源汇项函数除以渗透系数K
        def W(x, t):
            return eval(self.w) / self.K

        # 函数IC定义为初始水头分布曲线
        def IC(x):
            return eval(self.ic)

        # 创建一个全部值为0的矩阵，用于存放各个差分位置的水头值
        H_ALL = np.zeros((n, m))
        # 常数b矩阵
        H_b = np.zeros((m * n, 1))
        # 系数a矩阵
        H_a = np.zeros((m * n, m * n))
        # 定义系数a矩阵的行数

        # 矩阵赋值
        for k in range(0, n):  # 对行(时间轴)进行扫描
            iteration_times = 0  # 迭代运算次数计数
            H_previous_iteration = np.zeros((1, m))
            # 迭代运算开始
            while True:
                H_a = np.zeros((m, m))
                l_a = 0
                H_b = np.zeros((m, 1))

                if iteration_times == 0 and k != 0:
                    H_previous_iteration = H_ALL[k - 1]  # 前次迭代的当前时刻水头数值,此处未开始计算，使用上一时刻的水头值进行近似

                for i in range(0, m):  # 对列(X轴)进行扫描
                    # 时间边界赋值(初始条件）
                    if k == 0:
                        H_a[l_a, l_a] = 1
                        H_b[l_a] = IC(i * self.sl)

                    # 左边界赋值
                    elif (i - 1) < 0 and self.h_l[0] == 1:  # 一类边界判断
                        H_a[l_a, l_a] = 1
                        H_b[l_a] = self.h_l[1]
                    elif (i - 1) < 0 and self.h_l[0] == 2:  # 二类边界判断
                        # 源汇项赋值
                        H_b[l_a] = - W(i * self.sl, k * self.st) - self.Sy / (self.K * self.st) * H_ALL[
                            k - 1, i] - 2 * self.sl * self.h_l[1] * (
                                           H_previous_iteration[i] + self.h_l[1] * 0.5 * self.sl) / (
                                           self.sl * self.sl)
                        # 给位置为(i, k)处的水头赋上系数值
                        H_a[l_a, l_a] = -(H_previous_iteration[i + 1] + H_previous_iteration[i]) / (
                                2 * self.sl * self.sl) - (H_previous_iteration[i] + self.h_l[1] * 0.5 * self.sl) / (
                                                self.sl * self.sl) - self.Sy / (self.K * self.st)
                        # 给位置为(i+1, k)处的水头赋上系数值
                        H_a[l_a, l_a + 1] = (H_previous_iteration[i + 1] + H_previous_iteration[i]) / (
                                2 * self.sl * self.sl) + (H_previous_iteration[i] + self.h_l[1] * 0.5 * self.sl) / (
                                                    self.sl * self.sl)

                    # 右边界赋值
                    elif (i + 1) == m and self.h_r[0] == 1:
                        H_a[l_a, l_a] = 1
                        H_b[l_a] = self.h_r[1]
                    elif (i + 1) == m and self.h_r[0] == 2:
                        # 源汇项赋值
                        H_b[l_a] = - W(i * self.sl, k * self.st) - self.Sy / (self.K * self.st) * H_ALL[
                            k - 1, i] + 2 * self.sl * self.h_r[1] * (
                                           H_previous_iteration[i] + self.h_r[1] * 0.5 * self.sl) / (
                                           self.sl * self.sl)
                        # 给位置为(i, k)处的水头赋上系数值
                        H_a[l_a, l_a] = - (H_previous_iteration[i] + self.h_r[1] * 0.5 * self.sl) / (
                                self.sl * self.sl) - (H_previous_iteration[i] + H_previous_iteration[i - 1]) / (
                                                2 * self.sl * self.sl) - self.Sy / (self.K * self.st)
                        # 给位置为(i-1, k)处的水头赋上系数值
                        H_a[l_a, l_a - 1] = (H_previous_iteration[i] + H_previous_iteration[i - 1]) / (
                                2 * self.sl * self.sl) + (H_previous_iteration[i] + self.h_r[1] * 0.5 * self.sl) / (
                                                    self.sl * self.sl)
                    else:  # 非边界部分赋值
                        # 源汇项赋值
                        H_b[l_a] = - W(i * self.sl, k * self.st) - self.Sy / (self.K * self.st) * H_ALL[
                            k - 1, i]
                        # 给位置为(i, k)处的水头赋上系数值
                        H_a[l_a, l_a] = -(H_previous_iteration[i + 1] + H_previous_iteration[i]) / (
                                2 * self.sl * self.sl) - (H_previous_iteration[i] + H_previous_iteration[i - 1]) / (
                                                2 * self.sl * self.sl) - self.Sy / (self.K * self.st)
                        # 给位置为(i-1，k)处的水头赋上系数值
                        H_a[l_a, l_a - 1] = (H_previous_iteration[i] + H_previous_iteration[i - 1]) / (
                                2 * self.sl * self.sl)
                        # 给位置为(i+1, k)处的水头赋上系数值
                        H_a[l_a, l_a + 1] = (H_previous_iteration[i + 1] + H_previous_iteration[i]) / (
                                2 * self.sl * self.sl)
                    l_a += 1

                H = nla.solve(H_a, H_b)  # 进行当前时刻的水头计算结果
                if k == 0:  # 第零时刻不参与迭代计算
                    break

                # 判断是否满足精度需求
                precision = 0
                for u in range(0, m):
                    if abs(H_previous_iteration[u] - H[u]) > 0.01:
                        precision = 1
                if precision != 1:
                    break
                else:
                    iteration_times += 1
                    H_previous_iteration = H

                if iteration_times > 100:
                    break
            for o in range(0, m):  # 对空间进行扫描，整合成所有适合的计算水头
                H_ALL[k, o] = H[o]
        return H_ALL


if __name__ == "__main__":
    flow = Random_one_dimension_boussinesq()
    flow.sl = 10
    flow.st = 5
    flow.ic = '60 + x * np.tan(3.1415/120) + 5 * np.sin(x/60)'
    flow.tl = 365
    flow.xl = 2000
    flow.h_r = [2, 0]
    flow.h_l = [1, 60]
    flow.Sy = 0.08
    flow.K = 10
    flow.we = 0.4
    # flow.w = '0'
    flow.w = '0.4/36 + 0.1/36 * sin(3.1415*t/200) + 0.05/36 * sin(3.1415*t/10)'
    d = flow.fft_source_sink_term()
    h = flow.solve()
    # flow.draw(H_ALL=h, time=0)
    a, b, c = flow.random_w()
    # print(a)
    # print(b)
    # print(c)

    print(len(d))

    flow.draw_surface(H_ALL=h)
