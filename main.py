import gevent
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide2.QtUiTools import QUiLoader
import childwindow as cw
from PySide2.QtGui import QIcon
import sys
import multiprocessing
from os import getcwd
from hashlib import md5
from time import time


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 从文件中加载ui格式
        self.ui = QUiLoader().load("ui/MainWindow - untitled.ui")
        # 加载图标
        self.ui.setWindowIcon(QIcon("water.ico"))
        # 为按钮添加点击动作
        # self.ui.toth.clicked.connect(self.toth)
        # 设置傅里叶级数
        self.fourier_series = 1000
        self.ui.actionSet_fourier_series.triggered.connect(self.actionSet_fourier_series)
        # 设置解析解运行的CPU核心数
        self.cpu_cores = 1
        self.ui.actionSet_cpu_cores.triggered.connect(self.actionSet_cpu_cores)
        # 设置一维非稳定流的含水层宽度
        self.width = 1
        self.ui.actionSet_width.triggered.connect(self.actionSet_width)
        # 保存为工程文件
        self.ui.save_project.triggered.connect(self.save_project)
        # 打开工程文件
        self.ui.open_project.triggered.connect(self.open_project)
        # 关于本程序
        self.ui.action_about.triggered.connect(self.about)
        # 树状水流模式选择
        self.ui.treeWidget.clicked.connect(self.next)
        # 关于程序与算法的列表选择
        self.ui.listWidget_0.clicked.connect(self.algorithm_information)
        # 解析解的列表选择
        self.ui.listWidget_2.clicked.connect(self.analytic_solutions_information)
        # 关于使用的地下水概念的列表选择
        self.ui.listWidget_1.clicked.connect(self.undergroundwater_information)
        # 可以进行的实验列表选择
        self.ui.listWidget.clicked.connect(self.experiment_information)
        # 实例化具象：设置傅里叶级数
        self.Set_fourier_series_window = cw.Set_fourier_series()
        # 实例化具象：设置解析解运行的cpu核心数
        self.Set_cpu_cores = cw.Set_cpu_cores()
        # 实例化具象：设置含水层宽度
        self.Set_width = cw.Set_width()
        # 实例化具象：对于本程序
        self.About_this_program_window = cw.About_this_program()
        # 实例化具象：承压含水层一维稳定流
        self.one_dimension_confined_aquifer_stable_flow_window = cw.One_dimension_confined_aquifer_stable_flow()
        # 实例化具象：承压含水层一维非稳定流
        self.one_dimension_confined_aquifer_unstable_flow_window = cw.One_dimension_confined_aquifer_unstable_flow()
        self.one_dimension_confined_aquifer_unstable_flow_window.fourier_series = self.fourier_series  # 预设傅里叶级数和CPU运算核心数
        self.one_dimension_confined_aquifer_unstable_flow_window.cpu_cores = self.cpu_cores
        # 实例化具象：潜水含水层一维稳定流
        self.one_dimension_unconfined_aquifer_stable_flow_window = cw.One_dimension_unconfined_aquifer_stable_flow()
        # 实例化具象：潜水含水层一维非稳定流
        self.one_dimension_unconfined_aquifer_unstable_flow_window = cw.One_dimension_unconfined_aquifer_unstable_flow()
        self.one_dimension_unconfined_aquifer_unstable_flow_window.fourier_series = self.fourier_series  # 预设傅里叶级数和CPU运算核心数
        self.one_dimension_unconfined_aquifer_unstable_flow_window.cpu_cores = self.cpu_cores
        # 实例化具象：承压含水层二维稳定流
        self.two_dimension_confined_aquifer_stable_flow_window = cw.Two_dimension_confined_aquifer_stable_flow()
        # 实例化具象：潜水含水层二维稳定流
        self.two_dimension_unconfined_aquifer_stable_flow_window = cw.Two_dimension_unconfined_aquifer_stable_flow()
        # 实例化具象：承压含水层二维非稳定流
        self.two_dimension_confined_aquifer_unstable_flow_window = cw.Two_dimension_confined_aquifer_unstable_flow()
        # 实例化具象：潜水含水层二维非稳定流
        self.two_dimension_unconfined_aquifer_unstable_flow_window = cw.Two_dimension_unconfined_aquifer_unstable_flow()
        # 实例化具象：Tóth复杂盆地
        self.toth_difficult_basin_window = cw.Two_dimension_Toth_difficult_baisn()

    def next(self):  # 该函数用于打开每一种水流模式所对应的主窗口
        item = self.ui.treeWidget.currentItem()
        # 水流模式的条件判断
        if item.whatsThis(0) == "一维流承压含水层稳定流":
            task1 = gevent.spawn(self.one_dimension_confined_aquifer_stable_flow_window.ui.show())  # 创建多进程任务
            task_list.append(task1)  # 把该任务加入到协程列表
        if item.whatsThis(0) == "一维流承压含水层非稳定流":
            task2 = gevent.spawn(self.one_dimension_confined_aquifer_unstable_flow_window.ui.show())
            task_list.append(task2)  # 把该任务加入到协程列表
        if item.whatsThis(0) == "一维流潜水含水层稳定流":
            task3 = gevent.spawn(self.one_dimension_unconfined_aquifer_stable_flow_window.ui.show())
            task_list.append(task3)  # 把该任务加入到协程列表
        if item.whatsThis(0) == "一维流潜水含水层非稳定流":
            task4 = gevent.spawn(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.show())
            task_list.append(task4)  # 把该任务加入到协程列表
        if item.whatsThis(0) == "二维流承压含水层稳定流":
            task5 = gevent.spawn(self.two_dimension_confined_aquifer_stable_flow_window.ui.show())
            task_list.append(task5)  # 把该任务加入到协程列表
        if item.whatsThis(0) == "二维流潜水含水层稳定流":
            task6 = gevent.spawn(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.show())
            task_list.append(task6)  # 把该任务加入到协程列表
        if item.whatsThis(0) == "二维流承压含水层非稳定流":
            task7 = gevent.spawn(self.two_dimension_confined_aquifer_unstable_flow_window.ui.show())
            task_list.append(task7)  # 把该任务加入到协程列表
        if item.whatsThis(0) == "二维流潜水含水层非稳定流":
            task8 = gevent.spawn(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.show())
            task_list.append(task8)  # 把该任务加入到协程列表

    def actionSet_fourier_series(self):
        self.Set_fourier_series_window.ui.show()
        self.Set_fourier_series_window.signal_fourier_series.connect(self.get_fourier_series)

    def get_fourier_series(self, fourier_series):  # 主窗口获得傅里叶级数的槽函数
        self.fourier_series = fourier_series
        self.one_dimension_confined_aquifer_unstable_flow_window.fourier_series = self.fourier_series
        self.one_dimension_unconfined_aquifer_unstable_flow_window.fourier_series = self.fourier_series

    def actionSet_cpu_cores(self):
        self.Set_cpu_cores.ui.show()
        self.Set_cpu_cores.signal_cpu_cores.connect(self.get_cpu_cores)

    def get_cpu_cores(self, cpu_cores):  # 主窗口获得分配CPU核心的槽函数
        self.cpu_cores = cpu_cores
        self.one_dimension_confined_aquifer_unstable_flow_window.cpu_cores = self.cpu_cores
        self.one_dimension_unconfined_aquifer_unstable_flow_window.cpu_cores = self.cpu_cores

    def actionSet_width(self):
        self.Set_width.ui.show()
        self.Set_width.signal_width.connect(self.get_width)

    def get_width(self, width):  # 主窗口获得含水层宽度的槽函数
        self.width = width
        self.one_dimension_confined_aquifer_unstable_flow_window.flow.B = self.width
        self.one_dimension_unconfined_aquifer_unstable_flow_window.flow.B = self.width

    def about(self):  # 打开关于本程序窗口
        self.About_this_program_window.ui.show()

    def algorithm_information(self):
        item = self.ui.listWidget_0.currentItem()
        # 清空文本框
        self.ui.textBrowser_0.clear()
        if item.whatsThis() == '有限差分法':
            self.ui.textBrowser_0.setText('有限差分法(Finite Difference Method)')
            self.ui.textBrowser_0.append(
                '  是求解偏微分方程边值问题和初值问题的一种数值方法，其实质是利用导数的差分近似形式代替偏微分方程形成的差分方程组，通过求解方程组得到离散点的待求变量作为连续场的一种近似结果。')
            self.ui.textBrowser_0.append(
                '  有限差分法中的“有限”，是指网格中的节点、单元或块体数目是有限的。(《地下水运动方程》王旭升等 p99)')
            self.ui.textBrowser_0.append('  在本程序中，使用该方法对地下水含水层的水头进行数值解计算并且绘图。')
        if item.whatsThis() == '差分格式':
            self.ui.textBrowser_0.setText(
                '  在本程序中主要使用向后隐式差分，因为其简单且绝对收敛，该格式的截断误差为o=Δt+Δx^2')
            self.ui.textBrowser_0.append(
                '  在承压含水层一维非稳定流中，还提供了Crank-Nicolson中心差分的方法，也是绝对收敛的，该格式的截断误差为o=Δt^2+Δx^2')
        if item.whatsThis() == '差分步长':
            self.ui.textBrowser_0.setText('  差分步长表示把偏微分方程降级为差分方程组时把x,y,t的偏导数变为Δx,Δy,Δt。')
            self.ui.textBrowser_0.append(
                '  差分步长直接决定了数值计算的精度，一般形况下差分步长越小，数值解计算的精度越高，在本程序中，需要输入时间差分步长和空间差分步长，在输值框中输入整数或者浮点数（小数）')
        if item.whatsThis() == '差分方程组求解':
            self.ui.textBrowser_0.setText(
                '  对于数值法求解偏微分方程而言，如何使用程序求解方程组是一个重要的问题，在线性代数计算中有几种方法可以求解大型线性方程组：\n')
            self.ui.textBrowser_0.append('1.直接法，其中包括：高斯消元法，LU分解法，追赶法')
            self.ui.textBrowser_0.append(
                '2.迭代法：常见的迭代法有：Jacobi迭代法，Gauss-Seidel迭代法，超松弛迭代法，预条件迭代法')
            self.ui.textBrowser_0.append(
                '  在本程序中使用的是LU分解法，由python扩展库numpy.linalg中的solve函数提供，使用上个世纪90年代编写的lapack程序包的_gesv例程。\n')
            self.ui.textBrowser_0.append(
                '注意：本程序在进行大规模矩阵求解运算时会全额占用计算机的CPU和内存，程序页面暂时卡死是正常现象。')
        if item.whatsThis() == '矩阵赋值':
            self.ui.textBrowser_0.setText('  numpy.linalg.solve(a, b)函数的适用方法为aX=b:')
            self.ui.textBrowser_0.append(
                '  其中a为系数矩阵,b为常数矩阵，对solve函数输入上述两个矩阵会返回求解的X矩阵。因此按照对应的差分格式对矩阵a,b进行赋值后即可带入函数进行求解。')
            self.ui.textBrowser_0.append(
                '  根据水流方程以及差分格式来构建合适的差分方程，随后对差分方程组的各个参数的值赋到矩阵a,b中再进行计算。')
            self.ui.textBrowser_0.append(
                '  本程序有两种矩阵赋值方式，第一种以承压含水层水流方程为例，赋值的时候把x,y,t,三个维度的各个水头系数值赋值到一个系数矩阵a中,将三维数组一维化，使用一次solve函数一次完成求解。\n  该方法优点是程序简洁，缺点是该方法无法求解非线性的潜水Boussinesq方程，而且矩阵容易超过程序能够处理的极限70000*70000，且计算缓慢耗时巨大，有时计算时间能达到40分钟以上。')
            self.ui.textBrowser_0.append(
                '  第二种以潜水Boussinesq方程为例，赋值的时候把x,y,两个维度的水头系数值赋值到一个系数矩阵a中，并使用一次solve函数计算这一时刻的水头值，再使用当前计算的值带入到下一时刻的计算中，连续使用多次计算出所有的水头值。\n  该方法优点是在大量计算时运算速度比上一种方法快，可以解更大的矩阵方程，可以求解非线性方程，缺点是逻辑复杂。\n')

    def analytic_solutions_information(self):
        item = self.ui.listWidget_2.currentItem()
        # 清空文本框
        self.ui.textBrowser_2.clear()
        if item.whatsThis() == '一维非稳定流承压含水层':
            self.ui.textBrowser_2.setText(
                '  在边界长度有限的情况下推荐使用分离变量法进行求解，本程序内部解析解由分离变量法得到，使用C++实现，解析解的形态为无穷多项的傅里叶级数，程序在默认情况下取前1000项。')
            self.ui.textBrowser_2.append(
                '  在边界长度无限大的情况下，推荐使用拉普拉斯变换，傅里叶变换进行求解，如果要使用玻尔兹曼变换的化请注意定解方程的初始条件能和无穷远边界条件统一。')
            self.ui.textBrowser_2.append(
                '  如果边界条件不为0，方程需要先变换为齐次方程之后在进行求解。《地下水运动方程》王旭升p37')
            self.ui.textBrowser_2.append('  本程序只有在源汇项为0的时候才可以使用解析解计算！')
        if item.whatsThis() == '一维非稳定流潜水含水层的参考厚度法':
            self.ui.textBrowser_2.setText(
                '  由于潜水含水层的数学方程是非线性的，需要先把方程线性化在进行解析解求解，而数值解不需要线性化，关于Boussinesq方程的线性化技术参考《地下水运动方程》第五章。')
            self.ui.textBrowser_2.append(
                '  在边界长度有限的情况下推荐使用分离变量法进行求解，本程序内部解析解由分离变量法得到，使用C++实现，解析解的形态为无穷多项的傅里叶级数，程序在默认情况下取前1000项。')
            self.ui.textBrowser_2.append(
                '  在边界长度无限大的情况下，推荐使用拉普拉斯变换，傅里叶变换进行求解，如果要使用玻尔兹曼变换的化请注意定解方程的初始条件能和无穷远边界条件统一。')
            self.ui.textBrowser_2.append('  程序解析解来源于《地下水运动方程》王旭升p37。')
        if item.whatsThis() == '一维非稳定流潜水含水层的平方法':
            self.ui.textBrowser_2.setText(
                '  由于潜水含水层的数学方程是非线性的，需要先把方程线性化在进行解析解求解，而数值解不需要线性化，关于Boussinesq方程的线性化技术参考《地下水运动方程》第五章。')
            self.ui.textBrowser_2.setText(
                '  在边界长度有限的情况下推荐使用分离变量法进行求解，本程序内部解析解由分离变量法得到，使用C++实现，解析解的形态为无穷多项的傅里叶级数，程序在默认情况下取前1000项。')
            self.ui.textBrowser_2.append(
                '  在边界长度无限大的情况下，推荐使用拉普拉斯变换，傅里叶变换进行求解，如果要使用玻尔兹曼变换的化请注意定解方程的初始条件能和无穷远边界条件统一。')
            self.ui.textBrowser_2.append(
                '  程序解析解来源于《地下水运动方程》王旭升p37所提供的解析解进行平方变换之后得到的。')
            self.ui.textBrowser_2.append(
                '  通过于参考厚度法解析解和有限差分法数值解对比，可以发现平方法的解一直要略大于参考厚度法的解，并且更加贴合数值解。')

    def undergroundwater_information(self):
        item = self.ui.listWidget_1.currentItem()
        # 清空文本框
        self.ui.textBrowser_1.clear()
        if item.whatsThis() == '渗透系数':
            self.ui.textBrowser_1.setText('渗透系数(hydraulic conductivity)')
            self.ui.textBrowser_1.append(
                '  渗透系数是一个及其重要的水文地质参数，是表征多孔介质透水能力的参数，常用单位为m/d。')
            self.ui.textBrowser_1.append(
                '  渗透系数既与多孔介质的空隙性质有关，也与渗透液体的物理性质有关。(《地下水动力学》陈崇希等 p10,《地下水科学概论》周训等 p44)')
        if item.whatsThis() == '导水系数':
            self.ui.textBrowser_1.setText('导水系数(transmissivity)')
            self.ui.textBrowser_1.append(
                '  虽然渗透系数(K)可以说明岩层的透水能力，但不能单独说明含水层的出水能力。对于承压含水层，由于其厚度(M)是定值，则T=KM也是定值。T称为导水系数，它指的是在水力梯度等于1水流经整个含水层厚度上的单宽流量，常用单位是m2/d。导水系数是表征承压含水层导水能力的参数，只使用于二维流，对于三维流则没有意义。')
        if item.whatsThis() == '源汇项函数':
            self.ui.textBrowser_1.setText('源汇项函数')
            self.ui.textBrowser_1.append(
                '  表明含水层由于外界大气降水，或者相邻含水层的越流等作用对含水层水量的补给。表示在单位时间内，单位含水层柱体所增加或减少的水头，单位为m。')
        if item.whatsThis() == '给水度':
            self.ui.textBrowser_1.setText('给水度(specific_yield)')
            self.ui.textBrowser_1.append('  一定体积的饱水多孔介质在重力作用下释放出的水的体积与多孔介质体积之比。')
        if item.whatsThis() == '贮水系数':
            self.ui.textBrowser_1.setText('贮水系数(storativity)')
            self.ui.textBrowser_1.append(
                '  测压水头下降（或升高）一个单位，从单位水平面积承压含水层柱体中释放（或释水）能力的参数。《地下水科学概论》p32')
        if item.whatsThis() == '参考厚度':
            self.ui.textBrowser_1.setText('参考厚度')
            self.ui.textBrowser_1.append(
                '  潜水含水层的参考厚度，在计算解析解中，默认潜水面的参考厚度等于初始条件，使用参考厚度法或者平方法来线性化Boussinesq方程，若计算解析解必须填入此项，输入整数或者浮点数.')
        if item.whatsThis() == '初始条件':
            self.ui.textBrowser_1.setText('初始条件')
            self.ui.textBrowser_1.append('  非稳定流的初始水头条件，表明在水位开始波动前的含水层水头。')
        if item.whatsThis() == '定水头边界':
            self.ui.textBrowser_1.setText('定水头边界')
            self.ui.textBrowser_1.append(
                '  第一类边界边界条件，这类边界是最常见的是渗流区与地表水体的分界线（面），当边界上水头不随时间改变时，称为定水头边界。')
        if item.whatsThis() == 'Dupuit假设':
            self.ui.textBrowser_1.setText('Dupuit假设')
            self.ui.textBrowser_1.append(
                '  虽然流动的潜水面不是水平的，但是大多数情况下潜水面的坡度很小，渗流的垂直分速度远远小于水平分速度，而可以忽略垂直分速度，即假定等水头面是铅直面。《地下水动力学》陈崇希p44')

    def experiment_information(self):
        item = self.ui.listWidget.currentItem()
        # 清空文本框
        self.ui.textBrowser.clear()
        if item.whatsThis() == '承压含水层一维稳定流抛物线型解':
            self.ui.textBrowser.setText('  选择开始菜单下的打开工程文件，在目录中找到-承压含水层一维稳定流抛物线型解')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append('  点击计算并绘图，查看水头图像，尝试调试一下源汇项的值，看看有什么变化？')
            self.ui.textBrowser.append('  对应的数学描述《地下水运动方程》王旭升p11-p12')
        if item.whatsThis() == '承压含水层一维稳定流对数线性解':
            self.ui.textBrowser.setText('  选择开始菜单下的打开工程文件，在目录中找到-承压含水层一维稳定流对数线性解')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append('  点击计算并绘图，查看水头图像，尝试调试一下有关渗透系数的函数，看看有什么变化？')
            self.ui.textBrowser.append('  对应的数学描述《地下水运动方程》王旭升p13')
        if item.whatsThis() == '潜水含水层一维稳定流分水岭':
            self.ui.textBrowser.setText('  选择开始菜单下的打开工程文件，在目录中找到-潜水含水层一维稳定流分水岭')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append(
                '  点击计算并绘图，查看水头图像，尝试调试一下源汇项的值，左右边界水头的值，看看分水岭怎么移动，水头曲线有什么变化？')
            self.ui.textBrowser.append('  对应的数学描述《地下水运动方程》王旭升p15，《地下水动力学》陈崇希p58-p63')
        if item.whatsThis() == '潜水含水层一维稳定流分水岭':
            self.ui.textBrowser.setText('  选择开始菜单下的打开工程文件，在目录中找到-潜水含水层一维稳定流分水岭')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append(
                '  点击计算并绘图，查看水头图像，尝试调试一下源汇项的值，左右边界水头的值，看看分水岭怎么移动，水头曲线有什么变化？')
            self.ui.textBrowser.append('  对应的数学描述《地下水运动方程》王旭升p15，《地下水动力学》陈崇希p58-p63')
        if item.whatsThis() == '对比承压含水层一维非稳定流的解析解和数值解':
            self.ui.textBrowser.setText(
                '  选择开始菜单下的打开工程文件，在目录中找到-对比承压含水层一维非稳定流-数值解与解析解对比')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append(
                '  分别使用两种数值解计算方式与解析解进行对比，按时刻查看水头图像对比图，分析一下为什么二者的初始条件在左右边界处有较大差异？并且感受一下数值解的离散效果，调试一下导水系数，贮水系数的值，分析一下水头趋于稳定流的速度，同时也可以把参数输入到稳定流水流模型中进行绘图观察。在进行误差比对分析，尝试调试一下差分步长，看看相对误差和均方误差有什么变化？想继续分析误差变化可以选择保存关于误差的excel表格。')
            self.ui.textBrowser.append('  对应的数学描述《地下水运动方程》王旭升p37')
        if item.whatsThis() == '对比潜水含水层一维非稳定流的解析解和数值解':
            self.ui.textBrowser.setText(
                '  选择开始菜单下的打开工程文件，在目录中找到-潜水含水层一维非稳定流-数值解与解析解对比')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append(
                '  分别使用两种解析解计算方式与数值解进行对比，按时刻查看水头图像对比图，尝试调试一下渗透系数，给水度的值，分析一下水头趋于稳定流的速度，同时也可以把参数输入到稳定流水流模型中进行绘图观察。')
            self.ui.textBrowser.append(
                '  对比一下平方法解析解与参考厚度法解析解的大小，调试绘图时刻，参考厚度，看看两种解析解谁更准确一些？提示：导入的工程文件从第二时刻开始观察。')
            self.ui.textBrowser.append('  对应的数学描述《地下水运动方程》王旭升p37')
        if item.whatsThis() == '使用水均衡功能计算和分析边界的流量':
            self.ui.textBrowser.setText(
                '  选择开始菜单下的打开工程文件，在目录中找到承压含水层一维非稳定流-数值解与解析解对比；潜水含水层一维非稳定流-数值解与解析解对比')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append(
                '  进行数值解计算以及解析解计算，选定计算水均衡的时间段，进行水均衡计算观察边界流量以及含水层储存的水量变化。调整初始水位和边界条件在进行计算分析，更改一下空间差分步长和时间差分步长后在计算一下看看结果？')
            self.ui.textBrowser.append('  对应的数学描述即计算方法思想（数值积分）《地下水动力学》薛禹群p66')
        if item.whatsThis() == '体验难以计算解析解的地下水水流模型':
            self.ui.textBrowser.setText(
                '  选择开始菜单下的打开工程文件，在目录中找到-承压含水层二维稳定流与非稳定流对比')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append(
                '  计算并绘图，观察水头图像，尝试调试一下源汇项的值，左右边界水头的值，水头曲线有什么变化？')
            self.ui.textBrowser.append(
                '  同样的，你也可以在一维流计算模型中把渗透系数，源汇项设置成非常难以计算解析解的函数，程序会进行数值求解，可以绘图观察水头模型。')
        if item.whatsThis() == '体验没有解析解的地下水水流模型':
            self.ui.textBrowser.setText(
                '  选择开始菜单下的打开工程文件，在目录中找到-潜水含水层二维稳定流与非稳定流对比')
            self.ui.textBrowser.append('  打开左侧对应的水流模型')
            self.ui.textBrowser.append(
                '  非线性的潜水Boussinesq方程是没有由初等函数构成的解析解，但是索性有有限差分法，有限单元法所求得的数值解我们可以一睹其真容。')
            self.ui.textBrowser.append(
                '  计算并绘图，观察水头图像，尝试调试一下源汇项的函数，左右边界水头的值，水头曲线有什么变化？')
            self.ui.textBrowser.append(
                '  同样的，你也可以在一维非稳定流计算模型中把渗透系数，源汇项设置成非常难以计算解析解的函数，程序会进行数值求解，可以绘图观察水头模型。')

    def toth(self):  # 进入Tóth复杂盆地的部分
        task10 = gevent.spawn(self.toth_difficult_basin_window.ui.show())
        task_list.append(task10)  # 把该任务加入到协程列表

    def write_one_dimension_confined_aquifer_stable_flow(self, filepath):
        file = open(filepath, mode='a', encoding='utf8')  # 打开文件
        file.write('承压含水层一维稳定流\n')
        # 写入参数
        file.write(self.one_dimension_confined_aquifer_stable_flow_window.ui.transmissivity.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_stable_flow_window.ui.source_sink_term.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_stable_flow_window.ui.l_boundary.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_stable_flow_window.ui.r_boundary.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_stable_flow_window.ui.length.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_stable_flow_window.ui.step_length.toPlainText() + '\n')

        file.close()

    def read_one_dimension_confined_aquifer_stable_flow(self, filepath, line_number):
        file = open(filepath, mode='r', encoding='utf8')  # 打开文件
        linelist = file.readlines()  # 读取每一行的数据
        self.one_dimension_confined_aquifer_stable_flow_window.ui.transmissivity.setText(linelist[line_number + 1][:-1])
        self.one_dimension_confined_aquifer_stable_flow_window.ui.source_sink_term.setText(
            linelist[line_number + 2][:-1])
        self.one_dimension_confined_aquifer_stable_flow_window.ui.l_boundary.setText(linelist[line_number + 3][:-1])
        self.one_dimension_confined_aquifer_stable_flow_window.ui.r_boundary.setText(linelist[line_number + 4][:-1])
        self.one_dimension_confined_aquifer_stable_flow_window.ui.length.setText(linelist[line_number + 5][:-1])
        self.one_dimension_confined_aquifer_stable_flow_window.ui.step_length.setText(linelist[line_number + 6][:-1])

        file.close()

    def write_one_dimension_confined_aquifer_unstable_flow(self, filepath):
        file = open(filepath, mode='a', encoding='utf8')
        file.write('承压含水层一维非稳定流\n')
        # 写入参数
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.transmissivity.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.storativity.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.source_sink_term.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.l_boundary.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.r_boundary.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.x_length.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.step_length.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.initial_condition.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.t_length.toPlainText() + '\n')
        file.write(self.one_dimension_confined_aquifer_unstable_flow_window.ui.step_time.toPlainText() + '\n')

        file.close()

    def read_one_dimension_confined_aquifer_unstable_flow(self, filepath, line_number):
        file = open(filepath, mode='r', encoding='utf8')  # 打开文件
        linelist = file.readlines()  # 读取每一行的数据
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.transmissivity.setText(
            linelist[line_number + 1][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.storativity.setText(linelist[line_number + 2][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.source_sink_term.setText(
            linelist[line_number + 3][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.l_boundary.setText(linelist[line_number + 4][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.r_boundary.setText(linelist[line_number + 5][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.x_length.setText(linelist[line_number + 6][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.step_length.setText(linelist[line_number + 7][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.initial_condition.setText(
            linelist[line_number + 8][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.t_length.setText(linelist[line_number + 9][:-1])
        self.one_dimension_confined_aquifer_unstable_flow_window.ui.step_time.setText(linelist[line_number + 10][:-1])

        file.close()

    def write_one_dimension_unconfined_aquifer_stable_flow(self, filepath):
        file = open(filepath, mode='a', encoding='utf8')
        file.write('潜水含水层一维稳定流\n')
        # 写入参数
        file.write(
            self.one_dimension_unconfined_aquifer_stable_flow_window.ui.hydraulic_conductivity.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_stable_flow_window.ui.source_sink_term.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_stable_flow_window.ui.l_boundary.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_stable_flow_window.ui.r_boundary.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_stable_flow_window.ui.length.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_stable_flow_window.ui.step_length.toPlainText() + '\n')

        file.close()

    def read_one_dimension_unconfined_aquifer_stable_flow(self, filepath, line_number):
        file = open(filepath, mode='r', encoding='utf8')
        linelist = file.readlines()  # 读取每一行的数据
        self.one_dimension_unconfined_aquifer_stable_flow_window.ui.hydraulic_conductivity.setText(
            linelist[line_number + 1][:-1])
        self.one_dimension_unconfined_aquifer_stable_flow_window.ui.source_sink_term.setText(
            linelist[line_number + 2][:-1])
        self.one_dimension_unconfined_aquifer_stable_flow_window.ui.l_boundary.setText(linelist[line_number + 3][:-1])
        self.one_dimension_unconfined_aquifer_stable_flow_window.ui.r_boundary.setText(linelist[line_number + 4][:-1])
        self.one_dimension_unconfined_aquifer_stable_flow_window.ui.length.setText(linelist[line_number + 5][:-1])
        self.one_dimension_unconfined_aquifer_stable_flow_window.ui.step_length.setText(linelist[line_number + 6][:-1])

        file.close()

    def write_one_dimension_unconfined_aquifer_unstable_flow(self, filepath):
        file = open(filepath, mode='a', encoding='utf8')
        file.write('潜水含水层一维非稳定流\n')
        # 写入参数
        file.write(
            self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.hydraulic_conductivity.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.source_sink_term.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.l_boundary.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.r_boundary.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.x_length.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.step_length.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.t_length.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.step_time.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.specific_yield.toPlainText() + '\n')
        file.write(
            self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.reference_thickness.toPlainText() + '\n')
        file.write(self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.initial_condition.toPlainText() + '\n')

        file.close()

    def read_one_dimension_unconfined_aquifer_unstable_flow(self, filepath, line_number):
        file = open(filepath, mode='r', encoding='utf8')
        linelist = file.readlines()  # 读取每一行的数据
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.hydraulic_conductivity.setText(
            linelist[line_number + 1][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.source_sink_term.setText(
            linelist[line_number + 2][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.l_boundary.setText(linelist[line_number + 3][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.r_boundary.setText(linelist[line_number + 4][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.x_length.setText(linelist[line_number + 5][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.step_length.setText(
            linelist[line_number + 6][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.t_length.setText(linelist[line_number + 7][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.step_time.setText(linelist[line_number + 8][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.specific_yield.setText(
            linelist[line_number + 9][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.reference_thickness.setText(
            linelist[line_number + 10][:-1])
        self.one_dimension_unconfined_aquifer_unstable_flow_window.ui.initial_condition.setText(
            linelist[line_number + 11][:-1])

        file.close()

    def write_two_dimension_confined_aquifer_stable_flow(self, filepath):
        file = open(filepath, mode='a', encoding='utf8')  # 打开文件
        file.write('承压含水层二维稳定流\n')
        # 写入参数
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.transmissivity.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.source_sink_term.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.t_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.b_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.l_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.r_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.x_length.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.y_length.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_stable_flow_window.ui.step_length.toPlainText() + '\n')

        file.close()

    def read_two_dimension_confined_aquifer_stable_flow(self, filepath, line_number):
        file = open(filepath, mode='r', encoding='utf8')  # 打开文件
        linelist = file.readlines()  # 读取每一行的数据
        self.two_dimension_confined_aquifer_stable_flow_window.ui.transmissivity.setText(linelist[line_number + 1][:-1])
        self.two_dimension_confined_aquifer_stable_flow_window.ui.source_sink_term.setText(
            linelist[line_number + 2][:-1])
        self.two_dimension_confined_aquifer_stable_flow_window.ui.t_boundary.setText(linelist[line_number + 3][:-1])
        self.two_dimension_confined_aquifer_stable_flow_window.ui.b_boundary.setText(linelist[line_number + 4][:-1])
        self.two_dimension_confined_aquifer_stable_flow_window.ui.l_boundary.setText(linelist[line_number + 5][:-1])
        self.two_dimension_confined_aquifer_stable_flow_window.ui.r_boundary.setText(linelist[line_number + 6][:-1])
        self.two_dimension_confined_aquifer_stable_flow_window.ui.x_length.setText(linelist[line_number + 7][:-1])
        self.two_dimension_confined_aquifer_stable_flow_window.ui.y_length.setText(linelist[line_number + 8][:-1])
        self.two_dimension_confined_aquifer_stable_flow_window.ui.step_length.setText(linelist[line_number + 9][:-1])

        file.close()

    def write_two_dimension_confined_aquifer_unstable_flow(self, filepath):
        file = open(filepath, mode='a', encoding='utf8')  # 打开文件
        file.write('承压含水层二维非稳定流\n')
        # 写入参数
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.transmissivity.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.source_sink_term.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.t_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.b_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.l_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.r_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.x_length.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.y_length.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.step_length.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.initial_condition.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.t_length.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.step_time.toPlainText() + '\n')
        file.write(self.two_dimension_confined_aquifer_unstable_flow_window.ui.storativity.toPlainText() + '\n')

        file.close()

    def read_two_dimension_confined_aquifer_unstable_flow(self, filepath, line_number):
        file = open(filepath, mode='r', encoding='utf8')  # 打开文件
        linelist = file.readlines()  # 读取每一行的数据
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.transmissivity.setText(
            linelist[line_number + 1][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.source_sink_term.setText(
            linelist[line_number + 2][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.t_boundary.setText(linelist[line_number + 3][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.b_boundary.setText(linelist[line_number + 4][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.l_boundary.setText(linelist[line_number + 5][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.r_boundary.setText(linelist[line_number + 6][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.x_length.setText(linelist[line_number + 7][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.y_length.setText(linelist[line_number + 8][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.step_length.setText(linelist[line_number + 9][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.initial_condition.setText(
            linelist[line_number + 10][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.t_length.setText(linelist[line_number + 11][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.step_time.setText(linelist[line_number + 12][:-1])
        self.two_dimension_confined_aquifer_unstable_flow_window.ui.storativity.setText(linelist[line_number + 13][:-1])

        file.close()

    def write_two_dimension_unconfined_aquifer_stable_flow(self, filepath):
        file = open(filepath, mode='a', encoding='utf8')
        file.write('潜水含水层二维稳定流\n')
        # 写入参数
        file.write(
            self.two_dimension_unconfined_aquifer_stable_flow_window.ui.hydraulic_conductivity.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.source_sink_term.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.t_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.b_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.l_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.r_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.x_length.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.y_length.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_stable_flow_window.ui.step_length.toPlainText() + '\n')

        file.close()

    def read_two_dimension_unconfined_aquifer_stable_flow(self, filepath, line_number):
        file = open(filepath, mode='r', encoding='utf8')  # 打开文件
        linelist = file.readlines()  # 读取每一行的数据
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.hydraulic_conductivity.setText(
            linelist[line_number + 1][:-1])
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.source_sink_term.setText(
            linelist[line_number + 2][:-1])
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.t_boundary.setText(linelist[line_number + 3][:-1])
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.b_boundary.setText(linelist[line_number + 4][:-1])
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.l_boundary.setText(linelist[line_number + 5][:-1])
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.r_boundary.setText(linelist[line_number + 6][:-1])
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.x_length.setText(linelist[line_number + 7][:-1])
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.y_length.setText(linelist[line_number + 8][:-1])
        self.two_dimension_unconfined_aquifer_stable_flow_window.ui.step_length.setText(linelist[line_number + 9][:-1])

        file.close()

    def write_two_dimension_unconfined_aquifer_unstable_flow(self, filepath):
        file = open(filepath, mode='a', encoding='utf8')
        file.write('潜水含水层二维非稳定流\n')
        # 写入参数
        file.write(
            self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.hydraulic_conductivity.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.source_sink_term.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.t_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.b_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.l_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.r_boundary.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.x_length.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.y_length.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.step_length.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.initial_condition.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.t_length.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.step_time.toPlainText() + '\n')
        file.write(self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.specific_yield.toPlainText() + '\n')

        file.close()

    def read_two_dimension_unconfined_aquifer_unstable_flow(self, filepath, line_number):
        file = open(filepath, mode='r', encoding='utf8')  # 打开文件
        linelist = file.readlines()  # 读取每一行的数据
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.hydraulic_conductivity.setText(
            linelist[line_number + 1][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.source_sink_term.setText(
            linelist[line_number + 2][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.t_boundary.setText(linelist[line_number + 3][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.b_boundary.setText(linelist[line_number + 4][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.l_boundary.setText(linelist[line_number + 5][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.r_boundary.setText(linelist[line_number + 6][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.x_length.setText(linelist[line_number + 7][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.y_length.setText(linelist[line_number + 8][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.step_length.setText(
            linelist[line_number + 9][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.initial_condition.setText(
            linelist[line_number + 10][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.t_length.setText(linelist[line_number + 11][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.step_time.setText(linelist[line_number + 12][:-1])
        self.two_dimension_unconfined_aquifer_unstable_flow_window.ui.specific_yield.setText(
            linelist[line_number + 13][:-1])

        file.close()

    def save_project(self):  # 保存工程文件
        path_exe = getcwd()
        filepath, fileobject = QFileDialog.getSaveFileName(
            self.ui,
            "选择工程文件存储路径",
            path_exe,  # 起始目录
            "文本文件(*.txt)"
        )  # 文件选择路径和名称的打开方法
        file = open(filepath, mode='w', encoding='utf8')  # 创建文件
        file.write('*********1005203115*********\n')
        file.write('******本科毕业设计工程文件******\n')
        time_hash = time()
        file.write(str(time_hash) + '\n')  # 写入时间作为哈希加密的原值
        # 哈希验证码写入
        code = str(time_hash) + '|1005203115'  # 密钥为我的学号
        m = md5()  # 创建哈希对象
        m.update(code.encode())  # 字符串对象encode转换成字节串对象
        resultHex = m.hexdigest()  # 产生哈希值的十六进制表示
        file.write(str(resultHex) + '\n')
        file.close()  # 关闭文件
        # 进行文件写入
        self.write_one_dimension_confined_aquifer_stable_flow(filepath)
        self.write_one_dimension_confined_aquifer_unstable_flow(filepath)
        self.write_one_dimension_unconfined_aquifer_stable_flow(filepath)
        self.write_one_dimension_unconfined_aquifer_unstable_flow(filepath)
        self.write_two_dimension_confined_aquifer_stable_flow(filepath)
        self.write_two_dimension_confined_aquifer_unstable_flow(filepath)
        self.write_two_dimension_unconfined_aquifer_stable_flow(filepath)
        self.write_two_dimension_unconfined_aquifer_unstable_flow(filepath)

    def open_project(self):  # 打开工程文件
        path_exe = getcwd()
        filepath, fileobject = QFileDialog.getOpenFileName(self.ui, '选择工程文件', path_exe, '文本文件(*.txt)')
        file = open(filepath, mode='r', encoding='utf8')
        linelist = file.readlines()  # 读取每一行的数据
        file.close()  # 关闭文件
        # 哈希验证码校对
        time_hash = linelist[2][:-1]  # 读取时需要去除换行符号
        code = str(time_hash) + '|1005203115'
        m = md5()  # 创建哈希对象
        m.update(code.encode())  # 字符串对象encode转换成字节串对象
        resultHex = m.hexdigest()  # 产生哈希值的十六进制表示
        if str(resultHex) == linelist[3][:-1]:  # 读取时需要去除换行符号
            pass
        else:
            QMessageBox.critical(self.ui, '错误', '该文件未通过哈希算法校验，请选择正确的工程文件！')  # 未通过校验即报错
            return 0  # 结束代码
        # 读取文件信息
        line_number = 0  # 记录代码读取到哪一行了
        for line in linelist:
            if line[:-1] == '承压含水层一维稳定流':
                self.read_one_dimension_confined_aquifer_stable_flow(filepath, line_number)
            if line[:-1] == '承压含水层一维非稳定流':
                self.read_one_dimension_confined_aquifer_unstable_flow(filepath, line_number)
            if line[:-1] == '潜水含水层一维稳定流':
                self.read_one_dimension_unconfined_aquifer_stable_flow(filepath, line_number)
            if line[:-1] == '潜水含水层一维非稳定流':
                self.read_one_dimension_unconfined_aquifer_unstable_flow(filepath, line_number)
            if line[:-1] == '承压含水层二维稳定流':
                self.read_two_dimension_confined_aquifer_stable_flow(filepath, line_number)
            if line[:-1] == '承压含水层二维非稳定流':
                self.read_two_dimension_confined_aquifer_unstable_flow(filepath, line_number)
            if line[:-1] == '潜水含水层二维稳定流':
                self.read_two_dimension_unconfined_aquifer_stable_flow(filepath, line_number)
            if line[:-1] == '潜水含水层二维非稳定流':
                self.read_two_dimension_unconfined_aquifer_unstable_flow(filepath, line_number)

            line_number += 1


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    multiprocessing.freeze_support()  # 预防多进程打包后运行出错
    app = QApplication()
    window = MainWindow()
    task_list = []  # 创建协程列表
    task0 = gevent.spawn(window.ui.show())
    task_list.append(task0)
    gevent.joinall(task_list)  # 协程任务启动
    sys.exit(app.exec_())
