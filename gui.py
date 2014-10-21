#!/usr/bin/env python

import sys
import helper
import seriesfinder
import grabber
import seriesgrabber
import os
import platform
import PySide

from ui_untitled import Ui_Dialog

from PySide.QtGui import QApplication, QMainWindow, QTextEdit,\
                         QPushButton,  QMessageBox

from PySide import QtGui, QtCore

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
#         hbox = QtGui.QHBoxLayout(PySide.QtGui.QWidget)      
#         series_dict = helper.series_dict()
#         count = 0
#         for series in series_dict:
#             print series
#             path = seriesfinder.get_image(series)
#             pixmap = QtGui.QPixmap(path) 
#             lbl = QtGui.QLabel(self)
#             lbl.setPixmap(pixmap)
#             hbox.addWidget(lbl)
#             count+=1
#         self.setLayout(hbox)
#         self.setWindowTitle('Image viewer')
#         self.show()  
              
        self.img_fold = r"data/pictures"

        self.widget_layout = QtGui.QGridLayout(self)
        self.scrollarea = QtGui.QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.widget_layout.addWidget(self.scrollarea)
        self.widget = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout(self.widget)
        self.scrollarea.setWidget(self.widget)

        self.layout.setAlignment(QtCore.Qt.AlignLeft)

        for img in os.listdir(self.img_fold):
            img_path = os.path.join(self.img_fold, img)
            pixmap = QtGui.QPixmap(img_path)
            lbl = QtGui.QLabel(self)
            lbl.setPixmap(pixmap)
            self.layout.addWidget(lbl)
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('Image viewer')
        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()