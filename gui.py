#Python imports
import sys
import json

#External imports
from PySide.QtCore import *
from PySide.QtGui import *

#Internal imports
import helper
#import serieshelper


class MainWidget(QWidget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        # Main Window
        self.setWindowTitle("Series Grabber")

        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # Initialize layouts
        self.init_left_layout()

         # Set layouts
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

    ''' Left layout '''

    def init_left_layout(self):
        self.init_series_box()


    def init_main_button(self):
        print "x"


    def init_series_box(self):
        # Widgets & Layout
        self.scroll_area = QScrollArea()
        self.series_layout = QVBoxLayout()

        self.scroll_area.setMinimumWidth(250)

        # Open series_dict
        series_dict = helper.series_dict()
        for series in series_dict.keys():
            print series
            # Add push button
            button = QPushButton(series)
            button.setStyleSheet("QPushButton {text-align: left; font-size: 15px}")
            self.series_layout.addWidget(button)

        # Add to layout
        self.scroll_area.setLayout(self.series_layout)
        self.left_layout.addWidget(self.scroll_area)


    def init_add_button(self):
        print "x"









if __name__ == '__main__':
# Exception Handling
    try:
        myApp = QApplication(sys.argv)
        mainWindow = MainWidget()
        mainWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
