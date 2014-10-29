import sys
import collections
from PySide.QtGui import *
from PySide.QtCore import *
import helper
import seriesfinder


class MainWidget(QWidget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle("Series Grabber")
        self.setGeometry(300, 250, 400, 300)
        self.my_layout()

    def my_layout(self):
        layout = QHBoxLayout()

        '''left_menu'''
        layout.addWidget(self.left_menu())

        '''Stackedwidget - main'''
        self.stackedwidget = QStackedWidget()
        main_view = QWidget()
        layout_main_view = QVBoxLayout()
        mainlabel = QLabel()
        mainlabel.setText("Main")
        layout_main_view.addWidget(mainlabel)
        main_view.setLayout(layout_main_view)
        sd = helper.series_dict()
        series_dict = collections.OrderedDict(sd)
        self.stackedwidget.addWidget(main_view)

        '''Stackedwidget - series_view'''
        i = 1
        while i < len(series_dict.keys()) + 1:
            serieswidget = QWidget()
            layout_serieswidget = QVBoxLayout()

            #Serienbanner
            pixmap = QPixmap(seriesfinder.get_image(series_dict.keys()[i - 1]))
            lbl = QLabel(self)
            lbl.setPixmap(pixmap)
            layout_serieswidget.addWidget(lbl)

            #Description
            label = QLabel()
            label.setText(seriesfinder.get_description(series_dict.keys()[i - 1]))
            label.setWordWrap(True)
            layout_serieswidget.addWidget(label)

            labelx = QLabel()
            labelx.setText("Mittiges Label")
            label2 = QLabel()
            label2.setText(series_dict.keys()[i - 1])
            layout_serieswidget.addWidget(labelx)
            layout_serieswidget.addWidget(label2)

            serieswidget.setLayout(layout_serieswidget)
            self.stackedwidget.addWidget(serieswidget)
            i += 1

        self.stackedwidget.setCurrentIndex(0)
        layout.addWidget(self.stackedwidget)
        #self.stackedwidget.show()   #?
        self.setLayout(layout)
        return self.stackedwidget

    '''Left menu'''
    def left_menu(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setMaximumWidth(239)

        label = QLabel("<font color=green size= 20><b>Main</b></font>")
        layout.addWidget(label)
        label.setAlignment(Qt.AlignCenter)
        label.show()
        label.mouseReleaseEvent = self.change_stackedwidget_to_main

        main_button = QPushButton("Mainbutton")
        main_button.clicked.connect(lambda: self.display_stacked_widget("main"))
        main_button.setFlat(True)
        layout.addWidget(main_button)
        main_button.show()

        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setMinimumSize(215, 300)
        scroll.setMaximumWidth(215)
        scroll.setWidget(self.series_menu())
        layout.addWidget(scroll)
        scroll.show()

        add_button = QPushButton("Add new series ...")
        layout.addWidget(add_button)
        add_button.move(150, 0)
        add_button.show()

        widget.setLayout(layout)
        return widget

    '''left menu - series_menu'''
    def series_menu(self):
        widget = QWidget()
        widget.setMaximumWidth(200)
        layout = QVBoxLayout()

        sd = helper.series_dict()
        series_dict = collections.OrderedDict(sorted(sd.items()))
        for series in series_dict:
            button = self.add_button(series)
            button.setFlat(True)
            layout.addWidget(button)
            button.show()
        widget.setLayout(layout)
        return widget

    '''Helper'''
    def change_stackedwidget_to_main(self, a):
        self.stackedwidget.setCurrentIndex(0)

    def display_stacked_widget(self, series):
        if series == "main":
            self.stackedwidget.setCurrentIndex(0)
        else:
            sd = helper.series_dict()
            series_dict = collections.OrderedDict(sd)
            self.stackedwidget.setCurrentIndex(series_dict.keys().index(series) + 1)

    def add_button(self, series):
        button = QPushButton(series, self)
        button.clicked.connect(lambda: self.display_stacked_widget(series))
        return button


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
