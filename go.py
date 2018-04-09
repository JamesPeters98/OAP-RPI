from PyQt4 import QtGui,QtCore
import sys
import ui_main
import numpy as np
import pylab
import time
import pyqtgraph
import win32api

class AccelerationGraph(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    
    global points, X, Y, Y2, Y3, x0, y0, x1, y1, prevDist, dist, t0, t, vx0, vx1, vy0, vy1,a
    
    points=100 #number of data points
    X=np.arange(points)
    Y=np.zeros(points)
    Y2 = np.zeros(points)
    Y3 = np.zeros(points)
    x0, y0 = win32api.GetCursorPos()
    x1, y1 = 0, 0
    t0, t1 = 0, 0
    vx0, vx1 = 0, 0
    vy0, vy1 = 0, 0
    
    
    
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(AccelerationGraph, self).__init__(parent)
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.update)
        self.grPlot.plotItem.showGrid(True, True, 0.7)
        self.chkMore.checked = True
        

    def update(self):
        global x0,y0,t0,vx0,vx1,vy0,vy1,ax,ay
                
        x1, y1 = win32api.GetCursorPos()   
        x,y = (x1-x0),(y1-y0)
        dist = np.sqrt((x*x)+(y*y))
        t = (time.time()-t0)
        t0 = time.time()
        
        vx0,vy0 = vx1,vy1
        vx1,vy1 = x/t, y/t
        
        ax,ay = (vx1-vx0)/t, (vy1-vy0)/t
        
        x0,y0 = x1,y1
        
        a = np.sqrt(ax*ax+ay*ay)
        
        print(" ")
        print(vx1,vy1)
        print(ax,ay)
        
        
       
        for i in range(points):
            if(i > 0):
                Y[i-1] = Y[i]
                Y2[i-1] = Y2[i]
                Y3[i-1] = Y3[i]
            Y[i] = ax
            Y2[i] = ay
            Y3[i] = a
            
        C=pyqtgraph.hsvColor(0,alpha=.75)
        pen=pyqtgraph.mkPen(color=C,width=2.5)
        C2=pyqtgraph.hsvColor(0.5,alpha=.75)        
        pen2=pyqtgraph.mkPen(color=C2,width=2.5)
        C3=pyqtgraph.hsvColor(0.8,alpha=.75)        
        pen3=pyqtgraph.mkPen(color=C3,width=2.5)        
        
        self.grPlot.plot(X,Y,pen=pen,clear=True)
        self.grPlot.plot(X,Y2,pen=pen2,clear=False) 
        self.grPlot.plot(X,Y3,pen=pen3,clear=False)                
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