from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("C:\\KiwoomFlash3\\Bin\\NKMiniStarter.exe")

title = "번개3 Login"
dlg = timings.wait_until_passes(20,0.5,lambda : app.window(title=title))

pass_ctrl = dlg.Edit2
pass_ctrl.set_focus()
pass_ctrl.type_keys('kjs8034')

#cert_ctrl = dlg.Edit3
#cert_ctrl.set_focus()
#cert_ctrl.type_keys('yyyy')

btn_ctrl = dlg.Button0
btn_ctrl.click()

time.sleep(50)
os.system("taskkill /im khmini.exe")

#여기서 명령창 실행
#python -m PyQt5.uic.pyuic -x main_window.ui -o main_window.py

