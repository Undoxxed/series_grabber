#Python imports
import sys
import json
from functools import partial

#External imports
from PySide.QtCore import *
from PySide.QtGui import *

#Internal imports
import helper
import serieshelper


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
        self.init_right_layout()

        # Global variables
        self.current_series = ""


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
            button = QPushButton("{action}".format(action=series), self)
            button.setStyleSheet("QPushButton {text-align: left; font-size: 15px}")
            button.clicked.connect(partial(self.series_button, action=series))
            self.series_layout.addWidget(button)

        # Add to layout
        self.series_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setLayout(self.series_layout)
        self.left_layout.addWidget(self.scroll_area)

    def init_add_button(self):
        print "x"


#   Slots
    def series_button(self, action):
        self.current_series = action
        self.change_banner_pixmap()
        self.change_description()
        self.change_status_and_rating()
        self.change_episode_grid()

    ''' Right layout '''

    def init_right_layout(self):
        self.right_layout.setAlignment(Qt.AlignTop)
        self.init_banner()
        self.right_layout.addWidget(self.banner)
        self.init_description()
        self.right_layout.addWidget(self.description_scroll)
        self.init_status_and_rating()
        self.right_layout.addLayout(self.status_rating_layout)
        self.init_episode_grid()
        #self.right_layout.addLayout(self.episode_grid_layout)
        self.right_layout.addLayout(self.episode_box)

    def init_banner(self):
        self.banner = QLabel()
        self.banner.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.banner.setLineWidth(1)
        self.banner.setFixedSize(758, 140)
        self.change_banner_pixmap()

    def change_banner_pixmap(self):
        try:
            path = serieshelper.get_image(self.current_series)
            self.banner.setPixmap(path)
        except:
            pass

    def init_description(self):
        self.description_scroll = QScrollArea()
        self.description = QLabel()
        self.description.setWordWrap(True)
        self.change_description()
        self.description_scroll.setWidgetResizable(True)
        self.description_scroll.setMaximumHeight(50)
        self.description_scroll.setWidget(self.description)

    def change_description(self):
        try:
            dict_series = helper.series_dict()
            self.description.setText(dict_series[self.current_series]['description'])
        except:
            pass

    def init_status_and_rating(self):
        self.status_rating_layout = QHBoxLayout()
        self.status = QLabel()
        self.rating = QLabel()
        self.change_status_and_rating()
        self.status_rating_layout.setAlignment(Qt.AlignLeft)
        self.status_rating_layout.addWidget(self.status)
        self.status_rating_layout.addWidget(self.rating)

    def change_status_and_rating(self):
        try:
            series_dict = helper.series_dict()
            self.status.setText("Current Status: " + series_dict[self.current_series]['status'])
            self.rating.setText(" |   TVDB-Rating: " + series_dict[self.current_series]['rating'])
        except:
            pass

    def init_series_prefs(self):
        pass

    def init_season_buttons(self):
        pass

    def init_episode_grid(self):
        self.episode_grid_scroll = QScrollArea()
        self.episode_grid_layout = QGridLayout()
        self.episode_box = QHBoxLayout()
        self.episode_grid = QWidget()
        self.testlabel = QLabel()
        self.testlabel.setText("GRSDJSFSOEFSDES")
        self.episode_grid.setLayout(self.episode_grid_layout)
        self.change_episode_grid()
        self.episode_grid_layout.setAlignment(Qt.AlignLeft)
        self.episode_grid_scroll.setWidgetResizable(True)
        self.episode_grid_scroll.setWidget(self.episode_grid)
        self.episode_box.addWidget(self.episode_grid_scroll)
        self.episode_box.addWidget(self.testlabel)



    def change_episode_grid(self):
        try:
            series_dict = helper.series_dict()
            row = 0
            for season in series_dict[self.current_series]['seasons'].keys():
                for episode in series_dict[self.current_series]['seasons'][season].keys():
                    print "S" + str(season) + "E" + str(episode)
                    if episode != "season_link_sj":
                        season_Label = QLabel()
                        episode_label = QLabel()
                        episodename_label = QLabel()
                        season_Label.setText(str(season))
                        episode_label.setText(str(episode))
                        print series_dict[self.current_series]['seasons'][season][episode]['episodename']
                        episodename_label.setText(series_dict[self.current_series]['seasons'][season][episode]['episodename'])
                        self.episode_grid_layout.addWidget(episodename_label, row, 3)
                        self.episode_grid_layout.addWidget(season_Label, row, 1)
                        self.episode_grid_layout.addWidget(episode_label, row, 2)
                        row += 1
        except:
            pass

    def episode_infobox(self):
        pass













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
