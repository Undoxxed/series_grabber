#Python imports
import sys
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
        self.setWindowTitle("SeriesGrabber v0.1")
        self.setMinimumSize(900, 650)
        pixmap_window = QPixmap("data/icons/window.png")
        icon_window = QIcon(pixmap_window)
        self.setWindowIcon(icon_window)
        #self.setPalette(self.getPalette("gw"))

        # Initialize stacked widgets
        self.left_widget = QWidget()
        self.right_widget = QStackedWidget()

        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # Initialize layouts
        self.init_left_layout()
        self.init_right_layout()
        self.init_main_page_layout()


        # Global variables
        self.current_series = ""
        self.current_season = -1
        self.current_episode = -1


        # Set layouts
        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.right_widget)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

    ''' Left layout '''

    def init_left_layout(self):
        self.init_main_button()
        self.init_series_box()
        self.init_add_button()
        self.left_layout.setSpacing(15)
        self.left_widget.setLayout(self.left_layout)

    def init_main_button(self):
        self.main_button = QPushButton()
        self.main_button.setFixedHeight(75)
        main_pixmap = QPixmap("data/icons/main.png")
        main_icon = QIcon(main_pixmap)
        self.main_button.setIcon(main_icon)
        self.main_button.setIconSize(QSize(65, 65))
        stylesheet_hover = "QPushButton:hover {background-color: lightgreen; border-width: 3px}"
        stylesheet_normal = "QPushButton {background-color: lightgrey; border-color: black; border-style: outset; border-width: 2px; border-radius: 5px}"
        self.main_button.setStyleSheet(stylesheet_normal + stylesheet_hover)
        self.main_button.clicked.connect(self.main_button_click)
        self.left_layout.addWidget(self.main_button)

    def init_series_box(self):

        # Widgets & Layout
        self.scroll_area = QScrollArea()
        self.series_layout = QVBoxLayout()
        self.scroll_area.setMinimumWidth(200)

        # Open series_dict
        series_dict = helper.series_dict()
        for series in series_dict.keys():
            # Add push button
            button = QPushButton("{action}".format(action=series), self)
            stylesheet_hover = "QPushButton:hover {text-align: center; background-color: lightgreen; border-style: outset; border-width: 2px}"
            stylesheet_normal = "QPushButton {text-align: left; font: bold 12px; background-color: lightgrey; border-color: black; border-width: 0px; border-radius: 5px}"
            button.setMinimumHeight(30)
            button.setStyleSheet(stylesheet_normal + stylesheet_hover)
            button.clicked.connect(partial(self.series_button, action=series))
            self.series_layout.addWidget(button)

        # Add to layout
        self.series_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setLayout(self.series_layout)
        scroll_area_stylesheet = "background-color: lightgrey; border-color: black; border-style: outset; border-width: 2px; border-radius: 5px"
        self.scroll_area.setStyleSheet(scroll_area_stylesheet)
        self.left_layout.addWidget(self.scroll_area)

    def init_add_button(self):
        self.add_button = QPushButton()
        self.add_button.setMinimumHeight(40)
        stylesheet_hover = "QPushButton:hover {background-color: lightgreen; border-width: 3px}"
        stylesheet_normal = "QPushButton {text-align: center; font: bold 12px; background-color: lightgrey; border-color: black; border-style: outset; border-width: 2px; border-radius: 5px}"
        pixmap_add = QPixmap("data/icons/add.png")
        icon_add = QIcon(pixmap_add)
        self.add_button.setIcon(icon_add)
        self.add_button.setIconSize(QSize(30, 30))
        self.add_button.setToolTip("Add new series to library...")
        self.add_button.setStyleSheet(stylesheet_hover + stylesheet_normal)
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
        self.right_widget.setCurrentWidget(self.right_episode_widget)


    def season_button(self, action):
        self.current_season = action
        if self.current_season == 0:
            self.episode_grid_scroll.ensureVisible(0, 0)
        else:
            episodes = self.get_no_of_episodes_to_season()
            step = 100 + 31 * episodes + 40 * (action-1)
            self.episode_grid_scroll.ensureVisible(0, 100000)
            self.episode_grid_scroll.ensureVisible(0, step)

    def add_button_click(self):
        self.init_add_series_widget()
        self.finder.show()

    def main_button_click(self):
        self.right_widget.setCurrentWidget(self.main_page_widget)


    def download_click(self, action):
        row = self.episode_grid.indexOf(action)/5
        episode = int(self.episode_grid.itemAtPosition(row, 1).widget().text())
        season = int(self.episode_grid.itemAtPosition(row, 0).widget().text())
        print serieshelper.get_download_link(self.current_series, season, episode)

    ''' Right layout '''

    def init_right_layout(self):
        self.right_episode_widget = QWidget()
        self.right_layout.setAlignment(Qt.AlignTop)
        self.init_banner()
        self.right_layout.addWidget(self.banner)
        self.init_description()
        self.right_layout.addWidget(self.description_scroll)
        self.init_status_and_rating()
        self.right_layout.addWidget(self.status_rating_scroll)
        self.init_season_buttons()
        self.right_layout.addLayout(self.season_button_layout)
        self.init_episode_box()
        self.right_layout.addLayout(self.episode_box)
        self.init_bottom_box()
        self.right_layout.addWidget(self.bottom_box)
        self.right_layout.setSpacing(15)
        self.right_episode_widget.setLayout(self.right_layout)
        self.right_widget.addWidget(self.right_episode_widget)

    def init_banner(self):
        self.banner = QLabel()
        self.banner.setFixedSize(758, 140)
        self.change_banner_pixmap()
        stylesheet_banner = "background-color: lightgrey; border-color: black; border-style: outset; border-width: 2px; border-radius: 3px"
        self.banner.setStyleSheet(stylesheet_banner)

    def change_banner_pixmap(self):
        try:
            path = serieshelper.get_image(self.current_series)
            pixmap = QPixmap(path)
            self.banner.setPixmap(pixmap)
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
        stylesheet_descr = "background-color: lightgrey; border-color: black; border-style: solid; border-width: 1px; border-radius: 3px"
        self.description_scroll.setStyleSheet(stylesheet_descr)
        self.description_scroll.verticalScrollBar().setStyleSheet("QScrollBar {width: 0px;}")
        self.description_scroll.setWidget(self.description)

    def change_description(self):
        try:
            dict_series = helper.series_dict()
            self.description.setText(dict_series[self.current_series]['description'])
        except:
            pass

    def init_status_and_rating(self):
        self.status_rating_scroll = QScrollArea()
        self.status_rating_scroll.setWidgetResizable(True)
        self.status_rating_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.status_rating_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.status_rating_widget = QWidget()
        self.status_rating_widget.setMaximumHeight(40)
        self.status_rating_layout = QHBoxLayout(self.status_rating_widget)
        self.status = QLabel()
        self.rating = QLabel()
        self.vline = QLabel()
        self.vline.setFrameStyle(QFrame.VLine | QFrame.Plain)
        self.vline.setLineWidth(1)
        self.vline.setAlignment(Qt.AlignCenter)
        self.status.setAlignment(Qt.AlignCenter)
        self.rating.setAlignment(Qt.AlignCenter)
        self.vline.setMaximumWidth(5)
        self.status.setFixedWidth(200)
        self.rating.setFixedWidth(200)
        self.change_status_and_rating()
        self.status_rating_layout.addWidget(self.status)
        self.status_rating_layout.addWidget(self.vline)
        self.status_rating_layout.addWidget(self.rating)
        self.status_rating_layout.setSpacing(0)
        self.status_rating_widget.setLayout(self.status_rating_layout)
        stylesheet_widget = "background-color: lightgrey"
        self.status_rating_widget.setStyleSheet(stylesheet_widget)
        stylesheet_scroll = "QScrollArea {text-align: center; background-color: lightgrey; border-color: black; border-style: solid; border-width: 2px; border-radius: 3px}"
        self.status_rating_scroll.setStyleSheet(stylesheet_scroll)
        self.status_rating_scroll.setMaximumHeight(40)
        self.status_rating_scroll.setWidget(self.status_rating_widget)

    def change_status_and_rating(self):
        try:
            series_dict = helper.series_dict()
            self.status.setText("Current Status: " + series_dict[self.current_series]['status'])
            self.rating.setText("TVDB-Rating: " + series_dict[self.current_series]['rating'])
        except:
            pass

    def init_series_prefs(self):
        # TODO
        pass

    def init_season_buttons(self):
        self.season_button_layout = QHBoxLayout()
        self.season_button_layout.setAlignment(Qt.AlignLeft)
        self.season_button_layout.setSpacing(5)
        self.change_season_buttons


    def change_season_buttons(self):
        self.clearLayout(self.season_button_layout)
        series_dict = helper.series_dict()
        start_season = int(min(series_dict[self.current_series]['seasons'].keys()))
        end_season = len(series_dict[self.current_series]['seasons'].keys())
        stylesheet_normal = "QPushButton {font: bold 15px; background-color: lightgrey; border-color: black; border-style: solid; border-width: 2px; border-radius: 18px}"
        stylesheet_hover = "QPushButton:hover {border-color: white; background-color: black; color: white; border-width: 3px}"
        for season in range(start_season, end_season):
            season_button = QPushButton(str(season))
            season_button.setFixedWidth(36)
            season_button.setFixedHeight(36)
            season_button.setStyleSheet(stylesheet_normal + stylesheet_hover)
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
        stylesheet = "QScrollArea {text-align: center; background-color: lightgrey; border-color: black; border-style: solid; border-width: 2px; border-radius: 3px}"
        stylesheet_episode_widget = "background-color: lightgrey"
        self.episode_grid_scroll.setStyleSheet(stylesheet)
        self.episode_widget.setStyleSheet(stylesheet_episode_widget)
        self.episode_grid_scroll.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        self.episode_box.addWidget(self.episode_grid_scroll)

        # Init episode infobox
        self.infobox_widget = QWidget()
        self.episode_infobox_scroll = QScrollArea()
        self.episode_infobox_scroll.setWidgetResizable(True)
        self.episode_grid_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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
        self.episode_infobox.setAlignment(Qt.AlignTop)
        self.episode_infobox_scroll.setWidget(self.infobox_widget)
        self.episode_infobox_scroll.setMaximumWidth(250)
        stylesheet_scroll = "QScrollArea {text-align: center; background-color: lightgrey; border-color: black; border-style: solid; border-width: 2px; border-radius: 3px}"
        stylesheet_infobox ="background-color: lightgrey"
        self.infobox_widget.setStyleSheet(stylesheet_infobox)
        self.episode_infobox_scroll.setStyleSheet(stylesheet_scroll)
        self.episode_infobox_scroll.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        self.episode_box.addWidget(self.episode_infobox_scroll)


    def change_episode_grid(self):
        try:
            self.clearLayout(self.episode_grid)
            series_dict = helper.series_dict()
            row = 0
            start_season = int(min(series_dict[self.current_series]['seasons'].keys()))
            end_season = len(series_dict[self.current_series]['seasons'].keys())
            dl_pixmap = QPixmap("data/icons/download.png")
            dl_icon = QIcon(dl_pixmap)
            info_pixmap = QPixmap("data/icons/info.png")
            info_icon = QIcon(info_pixmap)
            for season in range(start_season, end_season):

                if season != end_season:
                    season_seperator = QLabel()
                    season_seperator.setFrameStyle(QFrame.HLine | QFrame.Plain)
                    season_seperator.setLineWidth(1)
                    s_label = QLabel(str(season))
                    stylesheet_label = "font: bold 15px; background-color: lightgrey; border-style: outset; border-width: 1px; border-radius: 5px"
                    s_label.setStyleSheet(stylesheet_label)
                    s_label.setMinimumHeight(35)
                    s_label.setAlignment(Qt.AlignCenter)
                    #season_no = QLabel(str(season))
                    #season_no.setStyleSheet("font-size: 20px")
                    self.episode_grid.addWidget(s_label, row, 0, 1, 2)
                    #self.episode_grid.addWidget(season_no, row, 1)
                    self.episode_grid.addWidget(season_seperator, row, 2, 1, 3)
                    row += 1

                start_episode = int(min(series_dict[self.current_series]['seasons'][str(season)].keys()))
                end_episode = len(series_dict[self.current_series]['seasons'][str(season)].keys())
                stylesheet_buttons_normal = "QPushButton {border-style: inset; border-width: 1px; border-radius: 5px}"
                stylesheet_buttons_hover = "QPushButton:hover {border-style: outset; background-color: lightgreen;}"
                for episode in range(start_episode, end_episode):
                    #print "S" + str(season) + "E" + str(episode)
                    if str(episode) != "season_link_sj":
                        try:
                            season_label = QLabel(str(season))
                            season_label.setMaximumWidth(25)
                            season_label.setFixedHeight(25)
                            episode_label = QLabel(str(episode))
                            episode_label.setMaximumWidth(25)
                            episodename = series_dict[self.current_series]['seasons'][str(season)][str(episode)]['episodename']
                            episodename_label = QLabel(episodename)
                            download_button = QPushButton()
                            download_button.setIcon(dl_icon)
                            download_button.clicked.connect(partial(self.download_click, action=download_button))
                            download_button.setMaximumWidth(50)
                            download_button.setFixedHeight(25)
                            download_button.setStyleSheet(stylesheet_buttons_normal + stylesheet_buttons_hover)
                            info_button = QPushButton()
                            info_button.setIcon(info_icon)
                            info_button.clicked.connect(partial(self.change_episode_infobox, action=info_button))
                            info_button.setMaximumWidth(50)
                            info_button.setFixedHeight(25)
                            info_button.setStyleSheet(stylesheet_buttons_normal + stylesheet_buttons_hover)
                            episodename_label.setWordWrap(True)
                            season_label.setAlignment(Qt.AlignCenter)
                            episode_label.setAlignment(Qt.AlignCenter)
                            self.episode_grid.addWidget(season_label, row, 0)
                            self.episode_grid.addWidget(episode_label, row, 1)
                            self.episode_grid.addWidget(episodename_label, row, 2)
                            self.episode_grid.addWidget(download_button, row, 3)
                            self.episode_grid.addWidget(info_button, row, 4)
                            row += 1
                        except KeyError:
                            continue

        except:
            print "Exception (" + str(sys.exc_info()[0]) + ") in method 'change_episode_grid'"
            pass

    def change_episode_infobox(self, action):
        series_dict = helper.series_dict()
        row = self.episode_grid.indexOf(action)/5
        episode = int(self.episode_grid.itemAtPosition(row, 1).widget().text())
        season = int(self.episode_grid.itemAtPosition(row, 0).widget().text())
        self.infobox_episode.setText("Season " + str(season) + ", Episode " + str(episode))
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

    def init_bottom_box(self):
        self.bottom_box = QLabel()
        self.bottom_box.setText("Placeholder")
        stylesheet = "font: bold 12px; background-color: lightgrey; border-color: black; border-style: outset; border-width: 2px; border-radius: 5px"
        self.bottom_box.setStyleSheet(stylesheet)
        self.bottom_box.setAlignment(Qt.AlignCenter)
        self.bottom_box.setMinimumHeight(40)

    ''' Main page layout '''

    def init_main_page_layout(self):
        self.main_page_widget = QWidget()
        self.main_page_layout = QVBoxLayout()
        self.main_page_widget.setLayout(self.main_page_layout)
        self.main_page_widget.setFixedSize(758, 650)
        self.right_widget.addWidget(self.main_page_widget)

    ''' Add series Widget '''

    def init_add_series_widget(self):
        # Layout for finder window
        self.search_layout = QVBoxLayout()

        # Main Finder Window
        self.finder = QWidget()
        self.finder.resize(400, 400)
        self.finder.setWindowTitle('Add a series to your library')

        # Add line edit, buttons & search result list
        self.search_label = QLabel()
        self.search_label.setText("Search TVDB for the series you want to add:")
        self.search_layout.addWidget(self.search_label)
        self.search_line = QLineEdit()
        self.search_layout.addWidget(self.search_line)
        self.search_layout.setAlignment(Qt.AlignTop)
        self.search_button = QPushButton()
        self.search_button.setText("Search")
        self.search_button.clicked.connect(self.search_series)
        self.search_layout.addWidget(self.search_button)
        self.search_result_list = QListWidget()
        self.search_layout.addWidget(self.search_result_list)
        self.choose_selection = QPushButton()
        self.choose_selection.setText("Choose selected series")
        self.choose_selection.clicked.connect(self.add_series)
        self.search_layout.addWidget(self.choose_selection)

        # Set finder layout
        self.finder.setLayout(self.search_layout)

    def add_series(self):
        selected_item = self.search_result_list.currentItem().text()
        serieshelper.add_series_to_json(selected_item)
        self.clearLayout(self.left_layout)
        self.init_left_layout()
        self.finder.close()

    def search_series(self):
        searchstring = self.search_line.text()
        if searchstring == "":
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Error!")
            self.msg.setText("You did not enter anything in the search line!")
            self.msg.exec_()
        else:
            self.search_result_list.clear()
            results = serieshelper.get_search_results(searchstring)
            self.search_result_list.addItems(results)

# Helper methods for GUI

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def getPalette(self, background):
        path = "data/patterns/"
        if background == "bm":
            file = "black_maze.png"
        elif background == "gf":
            file = "green_fibers.png"
        elif background == "gt":
            file = "grey_triangles.png"
        elif background == "gw":
            file = "grey_washed.png"
        elif background == "wh":
            file = "white_husk.png"
        else:
            file = "black_maze.png"
        pixmap = QPixmap(path + file)
        palette = QPalette()
        palette.setBrush(QPalette.Background, pixmap)
        return palette

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
