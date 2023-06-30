import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

TR_REQ_TIME_INTERVAL = 1

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        self.timer2 = QTimer(self)
        self.timer2.start(1000 * 10)
        self.timer2.timeout.connect(self.timeout2)

        self.load_attract_list()

    def load_attract_list(self):
        f = open("attract_list.txt", 'rt')
        self.attract_list = f.readlines()
        f.close()

        row_count = len(self.attract_list)
        self.tableWidget.setRowCount(row_count)

        # attract list
        for j in range(len(self.attract_list)):
            row_data = self.attract_list[j]
            split_row_data = row_data.split(';')

            for i in range(len(split_row_data)):
                item = QTableWidgetItem(split_row_data[i].rstrip())
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.tableWidget.setItem(j, i, item)

        self.tableWidget.resizeRowsToContents()

    def timeout(self):
        current_time = QTime.currentTime()

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        self.statusbar.showMessage(state_msg + " | " + time_msg)

        #df = web.DataReader(code, "yahoo")
        #df['MA20'] = df['Adj Close'].rolling(window=20).mean()
        #df['MA60'] = df['Adj Close'].rolling(window=60).mean()

        #ax = self.fig.add_subplot(111)
        #ax.plot(df.index, df['Adj Close'], label='Adj Close')
        #ax.plot(df.index, df['MA20'], label='MA20')
        #ax.plot(df.index, df['MA60'], label='MA60')
        #ax.legend(loc='upper right')
        #ax.grid()

        #self.canvas.draw()

    def timeout2(self):
        self.set_stock_data()

    def set_stock_data(self):
        # Item list
        item_count = len(self.kiwoom.opt10081_output)
        if item_count > 0:
            self.tableWidget_2.setRowCount(item_count)
            for j in range(item_count):
                col = self.kiwoom.opt10081_output[j]
                print(col)
                for i in range(len(col)):
                    item = QTableWidgetItem(col[i])
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.tableWidget_2.setItem(j, i, item)

            self.tableWidget_2.resizeRowsToContents()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1722, 1161)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 9, 231, 891))
        self.groupBox.setObjectName("groupBox")

        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(QtCore.QRect(0, 20, 221, 861))
        self.tableWidget.setRowCount(1)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)


        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(250, 10, 630, 441))
        self.groupBox_2.setObjectName("groupBox_2")

        self.btn1 = QPushButton("action", self.groupBox_2)
        self.btn1.move(20, 20)
        self.btn1.clicked.connect(self.btn_clicked)

        self.tableWidget_2 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 60, 610, 361))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(6)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, item)



        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(250, 460, 630, 441))
        self.groupBox_3.setObjectName("groupBox_3")

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        chartLayout = QVBoxLayout()
        chartLayout.addWidget(self.canvas)

        self.groupBox_3.setLayout(chartLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1722, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyTrader v0.4"))
        self.groupBox.setTitle(_translate("MainWindow", "관심종목"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "종목명"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "종목코드"))
        self.groupBox_2.setTitle(_translate("MainWindow", "종목현황"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "일자"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "시가"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "고가"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "저가"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "현재가"))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "거래량"))
        self.groupBox_3.setTitle(_translate("MainWindow", "종목 현황"))

    def btn_clicked(self):
        print("check execute !! ")
        self.kiwoom.reset_opt10081_output()
        for j in range(len(self.attract_list)):
            row_data = self.attract_list[j]
            split_row_data = row_data.split(';')
            if j == 0:
                for i in range(len(split_row_data)):
                    if i == 1:
                        time.sleep(TR_REQ_TIME_INTERVAL)
                        code = split_row_data[i].rstrip()
                        print("################### code : " + code + " ######################")
                        # opt10081 TR 요청
                        self.kiwoom.set_input_value("종목코드", code)
                        self.kiwoom.set_input_value("기준일자", "20230628")
                        self.kiwoom.set_input_value("수정주가구분", 1)
                        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
                        while self.kiwoom.remained_data:
                            self.kiwoom.set_input_value("종목코드", code)
                            self.kiwoom.set_input_value("기준일자", "20230628")
                            self.kiwoom.set_input_value("수정주가구분", 1)
                            self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()