import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from pywinauto import application
from pywinauto import timings
import time
import os


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 550, 750)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        self.btn1 = QPushButton("Login", self)
        self.btn1.move(20, 20)
        self.btn1.clicked.connect(self.btn1_clicked)

        self.btn2 = QPushButton("Check state", self)
        self.btn2.move(120, 20)
        self.btn2.clicked.connect(self.btn2_clicked)

        label = QLabel('종목코드: ', self)
        label.move(20, 120)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(80, 120)
        self.code_edit.setText("039490")

        self.btn3 = QPushButton("조회", self)
        self.btn3.move(190, 120)
        self.btn3.clicked.connect(self.btn3_clicked)

        self.btn4 = QPushButton("계좌 얻기",self)
        self.btn4.move(20,70)
        self.btn4.clicked.connect(self.btn4_clicked)

        self.btn5 = QPushButton("종목코드 얻기",self)
        self.btn5.move(20,500)
        self.btn5.clicked.connect(self.btn5_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 170, 280, 150)
        self.text_edit.setEnabled(False)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10,350,170,130)

        self.kiwoom.OnEventConnect.connect(self.event_connect)
        # OpenAPI+ Event
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")
        print(ret)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")

    def btn3_clicked(self):
        code = self.code_edit.text()
        self.text_edit.append("종목코드: "+code)
        # SetInputValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)","종목코드",code)

        # CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString,QString,int,QString)","opt10001_req","opt10001",0,"0101")

    def btn4_clicked(self):
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)",["ACCNO"])
        self.text_edit.append("계좌번호: "+account_num.rstrip(';'))

    def btn5_clicked(self):
        ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)",["0"])
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []

        for x in kospi_code_list:
            name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)",[x])
            kospi_code_name_list.append(x + " : " + name)

        self.listWidget.addItems(kospi_code_name_list)

    def receive_trdata(self,screen_no,rqname,trcode,recordname,prev_next,data_len,err_code,msg1,msg2):
        if rqname == "opt10001_req":
            name = self.kiwoom.dynamicCall("CommGetData(QString,QString,QString,int,QString)",trcode,"",rqname,0,"종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString,QString,QString,int,QString)",trcode,"",rqname,0,"거래량")
            self.text_edit.append("종목명: "+name.strip())
            self.text_edit.append("거래량: "+volume.strip())

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
