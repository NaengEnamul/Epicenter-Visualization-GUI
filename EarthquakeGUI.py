# NaengEnamul #
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import folium
import io
import os

#절대 경로 찾는 함수
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
Ui_MainWindow, QtBaseClass = uic.loadUiType(BASE_DIR + r'\GUI.ui')

Icon_DIR = os.path.dirname(os.path.abspath(__file__))


#test에 바로 실행시킬 파일명을 입력하면 됨
y_l=[] #위도
x_l=[] #경도
pst_l=[]
p_l=[]
s_l=[]
colorlist = ['#ff0000', '#ffa500', '#ffff00', '#00ff00', '#0000ff', '#00008b']
stacka=0
d=0
m=folium.Map(location=[36.84671094764842, 178.29490427750144], zoom_start=3)

class MainWindow(QMainWindow,QWidget,Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.initUI()
        self.show()

    def initUI(self):
        global data, m
        self.setupUi(self)
        self.setWindowTitle("Epicenter Visualization GUI")
        self.setWindowIcon(QIcon(Icon_DIR + r'\quake.ico'))
        # self.pushButton_3.clicked.connect(self.ViewStart)
        # self.pushButton_2.clicked.connect(self.Del)
        # self.pushButton.clicked.connect(self.New)
        
    def ViewStart(self):  #시작 버튼
        global data
        self.webEngineView.setHtml(data.getvalue().decode())#html속성으로 디코드

    def Restart(self): #삭제버튼
        global x_l, y_l, pst_l, p_l, s_l, stacka, data, m
        self.setupUi(self)
        stacka=0
        x_l.clear()
        y_l.clear()
        pst_l.clear()
        p_l.clear()
        s_l.clear()
        m=folium.Map(location=[36.84671094764842, 178.29490427750144], zoom_start=3)
        data=io.BytesIO()   #웹 크롤링 함수
        m.save(data, close_file=False) #folium함수에 넣을 파일 저장
        self.webEngineView.setHtml(data.getvalue().decode())
        
    def New(self):  #확인 버튼 
        global stacka, data
        # self.text = self.X_textedit.toPlainText()
        # self.ps_t_textedit.setText(self.text)
        # self.ps_t_textedit.setText("") 공백으로 바꾸는 코드
        self.listWidget.addItem(QListWidgetItem("--------------------------------%d--------------------------------" %(stacka+1)))
        self.listWidget.addItem(QListWidgetItem("Latitude : %s" %(self.Y_textedit.toPlainText())))
        self.listWidget.addItem(QListWidgetItem("Longitude : %s" %(self.X_textedit.toPlainText())))
        self.listWidget.addItem(QListWidgetItem("P-Wave-Speed : %skm/s" %(self.P_textedit.toPlainText())))
        self.listWidget.addItem(QListWidgetItem("S-Wave-Speed : %skm/s" %(self.S_textedit.toPlainText())))
        self.listWidget.addItem(QListWidgetItem("PS-Time : %sseconds" %(self.ps_t_textedit.toPlainText())))
        y_l.append(float(self.Y_textedit.toPlainText()))
        x_l.append(float(self.X_textedit.toPlainText()))
        pst_l.append(float(self.ps_t_textedit.toPlainText()))
        p_l.append(float(self.P_textedit.toPlainText()))
        s_l.append(float(self.S_textedit.toPlainText()))
        d = (p_l[stacka]*s_l[stacka])/(p_l[stacka]-s_l[stacka])*pst_l[stacka]
        folium.Circle([y_l[stacka],x_l[stacka]], radius=d*1000,color=colorlist[stacka],fill_color=colorlist[stacka], popup=stacka+1).add_to(m)
        folium.Marker([y_l[stacka],x_l[stacka]], popup=stacka+1, icon=folium.Icon('red', icon='star'),).add_to(m)
        self.X_textedit.setText("")
        self.Y_textedit.setText("")
        self.ps_t_textedit.setText("")
        stacka = stacka+1
        data=io.BytesIO()   #웹 크롤링 함수
        m.save(data, close_file=False) #folium함수에 넣을 파일 저장

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
