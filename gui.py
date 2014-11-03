#Python imports
import sys
from functools import partial
import operator

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
        self.setMinimumSize(900, 600)

        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # Initialize layouts
        self.init_left_layout()
        self.init_right_layout()

        # Global variables
        self.current_series = ""
        self.current_season = -1
        self.current_episode = -1


        # Set layouts
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

    ''' Left layout '''

    def init_left_layout(self):
        self.init_series_box()
        self.init_add_button()

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
        self.add_button = QPushButton("Add series...")
        self.add_button.setMinimumHeight(30)
        self.add_button.setStyleSheet("font-size: 15px")
        self.add_button.clicked.connect(self.add_button_click)
        self.left_layout.addWidget(self.add_button)


#   Slots
    def series_button(self, action):
        self.current_series = action
        self.change_banner_pixmap()
        self.change_description()
        self.change_status_and_rating()
        self.change_season_buttons()
        self.change_episode_grid()

    def season_button(self, action):
        self.current_season = action
        episodes = self.get_no_of_episodes_to_season()
        self.episode_grid_scroll.ensureVisible(0, 100000)
        step = 100 + 31 * episodes + 40 * (action-1)
        self.episode_grid_scroll.ensureVisible(0, step)

    def add_button_click(self):
        # TODO
        pass


    ''' Right layout '''

    def init_right_layout(self):
        self.right_layout.setAlignment(Qt.AlignTop)
        self.init_banner()
        self.right_layout.addWidget(self.banner)
        self.init_description()
        self.right_layout.addWidget(self.description_scroll)
        self.init_status_and_rating()
        self.right_layout.addLayout(self.status_rating_layout)
        self.init_season_buttons()
        self.right_layout.addLayout(self.season_button_layout)
        self.init_episode_box()
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
        self.description.setIndent(5)
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
        self.status.setIndent(5)
        self.rating = QLabel()
        self.status.setMinimumHeight(30)
        self.rating.setMinimumHeight(30)
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
        self.season_button_layout = QHBoxLayout()
        self.change_season_buttons


    def change_season_buttons(self):
        self.clearLayout(self.season_button_layout)
        series_dict = helper.series_dict()
        start_season = int(min(series_dict[self.current_series]['seasons'].keys()))
        end_season = len(series_dict[self.current_series]['seasons'].keys())
        for season in range(start_season, end_season):
            season_button = QPushButton(str(season))
            season_button.clicked.connect(partial(self.season_button, action=int(season)))
            self.season_button_layout.addWidget(season_button)

    def init_episode_box(self):
        # Init main layout
        self.episode_box = QHBoxLayout()

        # Init episode list
        self.episode_widget = QWidget()
        self.episode_grid = QGridLayout(self.episode_widget)
        self.episode_grid_scroll = QScrollArea()
        self.episode_grid_scroll.setWidgetResizable(True)
        self.episode_grid_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.episode_grid_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.episode_grid_scroll.setWidget(self.episode_widget)
        self.episode_box.addWidget(self.episode_grid_scroll)

        # Init episode infobox
        self.infobox_widget = QWidget()
        self.episode_infobox = QVBoxLayout(self.infobox_widget)
        self.infobox_episode = QLabel("No episode selected")
        self.hline = QLabel()
        self.hline.setFrameStyle(QFrame.HLine | QFrame.Plain)
        self.hline.setLineWidth(1)
        self.infobox_episodename = QLabel()
        self.infobox_episodename.setWordWrap(True)
        self.infobox_airdate = QLabel()
        self.infobox_rating = QLabel()
        self.infobox_description = QLabel()
        self.infobox_description.setWordWrap(True)
        self.episode_infobox.addWidget(self.infobox_episode)
        self.episode_infobox.addWidget(self.hline)
        self.episode_infobox.addWidget(self.infobox_episodename)
        self.episode_infobox.addWidget(self.infobox_airdate)
        self.episode_infobox.addWidget(self.infobox_rating)
        self.episode_infobox.addWidget(self.infobox_description)
        self.infobox_widget.setFixedWidth(250)
        self.episode_infobox.setAlignment(Qt.AlignTop)
        self.episode_box.addWidget(self.infobox_widget)


    def change_episode_grid(self):
        try:
            self.clearLayout(self.episode_grid)
            series_dict = helper.series_dict()
            row = 0
            start_season = int(min(series_dict[self.current_series]['seasons'].keys()))
            end_season = len(series_dict[self.current_series]['seasons'].keys())
            for season in range(start_season, end_season):

                if season != end_season:
                    season_seperator = QLabel()
                    season_seperator.setFrameStyle(QFrame.HLine | QFrame.Sunken)
                    season_seperator.setLineWidth(2)
                    s_label = QLabel(str(season))
                    s_label.setFrameStyle(QFrame.Panel | QFrame.Raised)
                    s_label.setLineWidth(2)
                    s_label.setMinimumHeight(35)
                    s_label.setAlignment(Qt.AlignCenter)
                    s_label.setStyleSheet("font: bold 15px")
                    #season_no = QLabel(str(season))
                    #season_no.setStyleSheet("font-size: 20px")
                    self.episode_grid.addWidget(s_label, row, 0, 1, 2)
                    #self.episode_grid.addWidget(season_no, row, 1)
                    self.episode_grid.addWidget(season_seperator, row, 2, 1, 3)
                    row += 1

                start_episode = int(min(series_dict[self.current_series]['seasons'][str(season)].keys()))
                end_episode = len(series_dict[self.current_series]['seasons'][str(season)].keys())
                for episode in range(start_episode, end_episode):
                    #print "S" + str(season) + "E" + str(episode)
                    if str(episode) != "season_link_sj":
                        season_label = QLabel(str(season))
                        season_label.setMaximumWidth(25)
                        season_label.setFixedHeight(25)
                        episode_label = QLabel(str(episode))
                        episode_label.setMaximumWidth(25)
                        episodename = series_dict[self.current_series]['seasons'][str(season)][str(episode)]['episodename']
                        episodename_label = QLabel(episodename)
                        download_button = QPushButton("DL")
                        download_button.setMaximumWidth(50)
                        info_button = QPushButton(">>>")
                        info_button.clicked.connect(partial(self.change_episode_infobox, action=info_button))
                        info_button.setMaximumWidth(50)
                        episodename_label.setWordWrap(True)
                        season_label.setAlignment(Qt.AlignCenter)
                        episode_label.setAlignment(Qt.AlignCenter)
                        self.episode_grid.addWidget(season_label, row, 0)
                        self.episode_grid.addWidget(episode_label, row, 1)
                        self.episode_grid.addWidget(episodename_label, row, 2)
                        self.episode_grid.addWidget(download_button, row, 3)
                        self.episode_grid.addWidget(info_button, row, 4)
                        row += 1

        except:
            print "Exception (" + str(sys.exc_info()[0]) + ") in method 'change_episode_grid'"
            pass

    def change_episode_infobox(self):
        pass

    def change_episode_infobox(self, action):
        series_dict = helper.series_dict()
        row = self.episode_grid.indexOf(action)/5
        episode = int(self.episode_grid.itemAtPosition(row, 1).widget().text())
        season = int(self.episode_grid.itemAtPosition(row, 0).widget().text())
        print episode
        print season
        self.infobox_episode.setText("Season " + str(season) +  ", Episode " + str(episode))
        episodename = series_dict[self.current_series]['seasons'][str(season)][str(episode)]['episodename']
        if episodename == None:
            episodename = "unknown"
        self.infobox_episodename.setText("Name: " + episodename)
        air_date = series_dict[self.current_series]['seasons'][str(season)][str(episode)]['air_date']
        if air_date == None:
            air_date = "unknown"
        self.infobox_airdate.setText("Air date: " + air_date )
        rating = series_dict[self.current_series]['seasons'][str(season)][str(episode)]['rating']
        if rating == None:
            rating = "not rated"
        self.infobox_rating.setText("TVDB-Rating: " + rating)
        description = series_dict[self.current_series]['seasons'][str(season)][str(episode)]['description']
        if description == None:
            description = "not available"
        self.infobox_description.setText("Description: " + description)

    def get_no_of_episodes_to_season(self):
        series_dict = helper.series_dict()
        start_season = int(min(series_dict[self.current_series]['seasons'].keys()))
        end_season = self.current_season
        count = 0
        for season in range(start_season, end_season):
            start_episode = int(min(series_dict[self.current_series]['seasons'][str(season)].keys()))
            end_episode = len(series_dict[self.current_series]['seasons'][str(season)].keys())
            for episode in range(start_episode, end_episode):
                count += 1
        return count


    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())













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
