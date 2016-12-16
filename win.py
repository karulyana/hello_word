# -*- coding: utf-8 -*-

import sys
import random
import os
import re
import cmath
import math
from PyQt5 import Qt
import numpy as np
from pprint import pprint
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QFileDialog, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QSizePolicy, QTableWidget,QTableWidgetItem,
                             QVBoxLayout, QTextEdit, QTabWidget,QFormLayout,QGridLayout,
                             )
from PyQt5.QtGui import QColor, QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.pyplot as plt

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


def data_test():
    data_test_13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    -1, -1, -1, -1,
                    1, 1, 1, 1,
                    -1, -1, 1, 1,
                    -1, -1, 1, 1
                    ]
    return data_test_13


def barker_():
    coef_barker = {'n_7': [1, 1, 1, -1, -1, 1, -1],
                   'p_7': [-1, -1, -1, 1, 1, -1, 1],
                   'p_13': [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1],
                   'n_13': [1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, 1]
                   }
    return coef_barker['p_13']

'''
    Результат функции compression:
    кортеж состоящий из двух элементов
    0-элемент - это список данных после сжатия res
    1-эленер - это список модуля res
    '''
data = data_test()
barker = barker_()

def compression(data, barker):
        N_disk_FKM = 210
        N_fil = 1
        N_disk = N_disk_FKM * N_fil

        data_comp = [complex(a, b) for a, b
                     in zip(data[0:-1:2],
                            data[1::2])]

        c = iter(barker)
        i = iter(data_comp)

        res_sgh_comp = []
        n = 0
        N_f = N_fil
        S = complex()

        while N_f:  # 5
            try:
                N_f -= 1
                N_d = 100
                while N_d:  # 210
                    try:
                        f = next(c) * next(i)
                        S += f
                    except StopIteration:
                        n += 1
                        N_d -= 1
                        i = iter(data_comp[n:])
                        c = iter(barker)
                        res_sgh_comp.append(S)
                        S = complex()
                        continue
                    except:
                        break
            except:
                break

        Mod = []
        for i in res_sgh_comp:
            M = abs(i)
            Mod.append(M)
        # print (Mod)

        res_ = []
        for i in res_sgh_comp:
            b = i.real  # b = float.hex(b)
            res_.append(b)
            d = i.imag  # d = float.hex(d)
            res_.append(d)
        # print ('res_ =',res_)

        return res_, Mod

'''
res = compression(data, barker)[0]
mod = compression(data, barker)[1]
#modul res_
Mod_ = [(a ** 2 + b ** 2) ** 0.5 for a, b
                in zip(compression(data,barker)[0:-1:2], compression(data,barker)[1::2])]
'''

class AppWin(QWidget):

    def __init__(self):
        super().__init__()
        self.win()

    def win(self):
        self.setLayout(VBox())
        self.setWindowTitle("%s" %progname)
        self.center()
        self.resize(850,600)
        self.show()

    def center(self):        #прямоугольник точно определяющий форму главного окна
        self.qr = self.frameGeometry()        #форма экрана
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

class open_kn(QPushButton):
    def __init__(self, parent=None):
        super(open_kn, self).__init__(parent)
        self.setText('Open')
        self.resize(self.sizeHint())
        self.clicked.connect(self.showFileDialog)
        #open_kn.setFont(QtGui.QFont('Times New Roman',12))

    def showFileDialog(self, event):
        try:
            self.fileName = QFileDialog.getOpenFileName(self, 'Open file', 'D:\\')[0]
            self.textEdit.setText(self.fileName)
            f = open(self.fileName, 'r')
            data = []
            with f as f:
                for i in f.readlines():
                    # re = int(i[2:6], 16)  # re = int(i)
                    # im = int(i[6:], 16)  # im = int(i)
                    # data.append(re)
                    # data.append(im)
                    data.append(i)
            table = TableWidget(data=data)
        except IOError:
            print('Не могу открыть', self.fileName)
        except ImportError as err:
            print('Error: импортировать файл не удалось!', err)
        except ValueError as err:
            print('Error: не тот формат данных!', err)
        except:
            print('Неожиданная ошибка:', sys.exc_info()[0])
            # return data

class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        #self.setText(name)
        self.resize(self.sizeHint())


class HBox0(QHBoxLayout):
    def __init__(self, parent=None):
        super(HBox0, self).__init__(parent)
        # hBox.addStretch(1)
        lbData = QLabel('________Data:________')
        # lbData.setFont(QtGui.QFont('Times New Roman',12))
        self.addWidget(open_kn())
        self.addWidget(LineEdit())
        self.addWidget(lbData)


class HBox1(QHBoxLayout):
    def __init__(self, parent=None):
        super(HBox1, self).__init__(parent)
        # hBox.addStretch(1)
        offset = QLabel('offset:')
        self.addWidget(offset)
        self.addWidget(LineEdit())
        self.addStretch(1)


class HBox2(QHBoxLayout):
    def __init__(self, parent=None):
        super(HBox2, self).__init__(parent)
        # hBox.addStretch(1)
        stride = QLabel('stride:')
        self.addWidget(stride)
        self.addWidget(LineEdit())
        self.addStretch(1)


class HBox3(QHBoxLayout):
    def __init__(self, parent=None):
        super(HBox3, self).__init__(parent)
        # hBox.addStretch(1)
        count = QLabel('count:')
        self.addWidget(count)
        self.addWidget(LineEdit())
        self.addStretch(1)


class TabDemo(QTabWidget):

    def __init__(self, parent=None):
        super(TabDemo, self).__init__(parent)
        #m = PlotCanvas(self, width=8, height=5)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        layout = QFormLayout()
        self.setTabText(0, "Data")
        m = PlotWidgetD()
        layout.addRow(m)
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        self.setTabText(1, "Res")
        m = PlotWidgetR()
        layout.addRow(m)
        self.tab2.setLayout(layout)


class HBox4(QGridLayout):
    def __init__(self, parent=None):
        super(HBox4, self).__init__(parent)
        table = TableWidget()
        self.addWidget(table, *(0,0))
        self.addWidget(TabDemo(), *(0,1)) #таблица
        #self.addStretch(1)


class VBox(QVBoxLayout):
    def __init__(self, parent=None):
        super(VBox, self).__init__(parent)
        self.addLayout(HBox0())
        self.addLayout(HBox1())
        self.addLayout(HBox2())
        self.addLayout(HBox3())

        self.addStretch(1)
        self.addLayout(HBox4())


class TableWidget(QTableWidget):
    def __init__(self, parent=None, data=None):
        super(TableWidget, self).__init__(parent)
        self.setColumnCount(1)
        self.setRowCount(len(data_test()))
        for i, entry in enumerate(data_test(), start=1):
            self.setRowCount(i)
            item = QTableWidgetItem()
            item.setText(str(entry))
            self.setItem(0, i - 1, item)


class PlotWidgetD(QWidget):
    def __init__( self, parent = None ):
        QWidget.__init__( self, parent )
        self.canvas = PlotCanvasData() #create canvas that will hold our plot
        self.navi_toolbar = NavigationToolbar(self.canvas, self) #createa navigation toolbar for our plot canvas

        self.vbl = QVBoxLayout()
        self.vbl.addWidget( self.canvas )
        self.vbl.addWidget(self.navi_toolbar)
        self.setLayout( self.vbl )


class PlotCanvasData(FigureCanvas):

    def __init__(self):
        fig = Figure()
        #self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        fig.set_facecolor('black')
        #self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot_data()

    def plot_data(self):
        offset = 0
        stride = 2
        count = 100
        data_re = data[offset:count:stride]
        data_im = data[3:100:2]
        ax = self.figure.add_subplot(111, frameon=True)
        ax.plot(data_re, 'b-', data_im, 'r-')
        ax.set_title('data')
        ax.patch.set_facecolor('black')
        ax.grid(True, color='w')
        xlabels = ax.xaxis.get_ticklabels()
        xlines = ax.xaxis.get_ticklines()
        for label in xlines:
            label.set_color('white')
        for label in xlabels:
            label.set_color('white')
        ylabels = ax.yaxis.get_ticklabels()
        ylines = ax.yaxis.get_ticklines()
        for label in ylines:
            label.set_color('white')
        for label in ylabels:
            label.set_color('white')
        self.draw()


class PlotWidgetR(QWidget):
    def __init__( self, parent = None ):
        QWidget.__init__( self, parent )
        self.canvas = PlotCanvasRes() #create canvas that will hold our plot
        self.navi_toolbar = NavigationToolbar(self.canvas, self) #createa navigation toolbar for our plot canvas

        self.vbl = QVBoxLayout()
        self.vbl.addWidget( self.canvas )
        self.vbl.addWidget(self.navi_toolbar)
        self.setLayout( self.vbl )


class PlotCanvasRes(FigureCanvas):

    def __init__(self):
        fig = Figure()
        # self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        fig.set_facecolor('black')
        # self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot_res()

    def plot_res(self):
        offset = 0
        stride = 2
        count = 100
        res_d_g = compression(data,barker)[0][offset:count:stride]
        mod_d_g = compression(data,barker)[1][0:50:1]
        ax = self.figure.add_subplot(111)
        ax.plot(res_d_g, 'r-')
        ax.plot(mod_d_g, 'g-')
        ax.set_title('res')
        ax.grid(True, color='w')
        ax.patch.set_facecolor('black')
        xlabels = ax.xaxis.get_ticklabels()
        xlines = ax.xaxis.get_ticklines()
        for label in xlines:
            label.set_color('white')
        for label in xlabels:
            label.set_color('white')
        ylabels = ax.yaxis.get_ticklabels()
        ylines = ax.yaxis.get_ticklines()
        for label in ylines:
            label.set_color('white')
        for label in ylabels:
            label.set_color('white')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppWin()
    sys.exit(app.exec_())