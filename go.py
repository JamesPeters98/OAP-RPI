from PyQt4 import QtGui,QtCore
import sys
import ui_main
import numpy as np
import pylab
import time
import pyqtgraph
import requests
from envirophat import motion

class AccelerationGraph(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    
    global points, X, Y_ax, Y_ay, Y_az, Y_r, a, inactivity_time, inactive
    
    points=100 #number of data points
    #Array of points
    X=np.arange(points)
    Y_ax = np.zeros(points)
    Y_ay = np.zeros(points)
    Y_az = np.zeros(points)
    Y_r = np.zeros(points)
    
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(AccelerationGraph, self).__init__(parent)
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.update)
        self.grPlot.plotItem.showGrid(True, True, 0.7)
        self.chkMore.checked = True

    def update(self):
        #acceleration in each dimension
        ax,ay,az =  motion.accelerometer()
        #resultant acceleration
        a = np.sqrt(ax*ax+ay*ay+az*az)
        
        if(a<0.15):
            print("falling detected")
            print(a)
            inactivity_time = time.time()+1
            
        if((inactivity_time < time.time())&&((time.time()-inactivity_time)<=5):
            if((a <= 1.1)&&(a >= 0.9):
               inactive = true
            else
               inactive = false
               
        if((inactivity_time < time.time())&&((time.time()-inactivity_time)>5):
           if inactive:
                r = requests.post("https://maker.ifttt.com/trigger/raspberry_pi/with/key/cy_OmR1__iqa_mYUIMAdzY")
                print(r.text)
            
        
        #print(" ")
        #print(np.around(ax,2),np.around(ay,2),np.around(az,2),"r:",a)
        
        for i in range(points):
            if(i > 0):
                Y_ax[i-1] = Y_ax[i]
                Y_ay[i-1] = Y_ay[i]
                Y_az[i-1] = Y_az[i]
                Y_r[i-1] = Y_r[i]
            Y_ax[i] = ax
            Y_ay[i] = ay
            Y_az[i] = az
            Y_r[i] = a
            
        C=pyqtgraph.hsvColor(0,alpha=.75)
        pen=pyqtgraph.mkPen(color=C,width=2.5)
        C2=pyqtgraph.hsvColor(0.5,alpha=.75)        
        pen2=pyqtgraph.mkPen(color=C2,width=2.5)
        C3=pyqtgraph.hsvColor(0.8,alpha=.75)        
        pen3=pyqtgraph.mkPen(color=C3,width=2.5)
        C4=pyqtgraph.hsvColor(1,alpha=.75)        
        pen4=pyqtgraph.mkPen(color=C4,width=2.5)  
        
        #self.grPlot.plot(X,Y_ax,pen=pen,clear=True)
        #self.grPlot.plot(X,Y_ay,pen=pen2,clear=False) 
        #self.grPlot.plot(X,Y_az,pen=pen3,clear=False)
        self.grPlot.plot(X,Y_r,pen=pen4,clear=True)                

        #print("update took %.02f ms"%((time.clock()-t1)*1000))
        if self.chkMore.isChecked():
            QtCore.QTimer.singleShot(50, self.update) # QUICKLY repeat

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = AccelerationGraph()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")