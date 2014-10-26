import sys
from PySide.QtCore import *
from PySide.QtGui import *
import helper
import seriesfinder
import time
from types import NoneType


grabber_app = QApplication(sys.argv)
        
class SeriesGrabberGUI(QWidget):
    
    def __init__(self):
        # Initialize the object
        QWidget.__init__(self)
        
         # Main Window
        self.setMinimumSize(1000, 720)
        self.setWindowTitle('SeriesGrabber v0.1')
        
        ''' ADD SERIES WINDOW '''
        
        # Layout for finder window
        self.search_layout = QVBoxLayout()
        
        # Main Finder Window
        self.finder = QWidget()
        self.finder.resize(400, 400)
        self.finder.setWindowTitle('Add a series to your library')
        
        # Add line edit, buttons & search result list
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
        
        
        ''' MAIN WINDOW '''
        
        # Layouts
        self.layout = QHBoxLayout()
        self.left_side = QVBoxLayout()
        self.right_side = QVBoxLayout()
        self.episode_list_Layout = QHBoxLayout()
        
        
        ''' Left side of main window '''
        
#         # Label for list widget
#         self.list_caption = QLabel(self)
#         self.list_caption.setText("Choose series:")
#         self.left_side.addWidget(self.list_caption)
        
        # List widget for series selection
        self.series_list = QListWidget(self)
        dict_series = helper.series_dict()
        items = dict_series.keys()
        self.series_list.addItems(items)
        self.series_list.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.series_list.setLineWidth(2)
        self.series_list.setFixedWidth(200)
        self.left_side.addWidget(self.series_list)
        
        # Button to add new series to library
        self.add_button = QPushButton("Add series", self)
        self.add_button.setMinimumHeight(40)
        self.add_button.clicked.connect(self.open_finder)
        self.left_side.addWidget(self.add_button)
        
        ''' Right side of main window '''
        
        # Label for list widget
        self.banner = QLabel(self)
        self.banner.setAlignment(Qt.AlignTop)
        self.banner.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.banner.setLineWidth(2)
        self.banner.setMaximumHeight(140)
        self.right_side.addWidget(self.banner)
        
        # Label for description
        self.description = QLabel(self)
        self.description.setText("This is a description, This is a description, This is a description, This is a description, This is a description, This is a description, This is a description, ")
        self.description.setAlignment(Qt.AlignTop)
        self.description.setWordWrap(True)
        self.right_side.addWidget(self.description)
        
        # line1
        self.line1 = QLabel()
        self.line1.setFrameStyle(QFrame.HLine | QFrame.Plain)
        self.line1.setLineWidth(1)
        self.line1.setMaximumHeight(10)
        self.right_side.addWidget(self.line1)
        
        # ComboBox for season selection
        self.season_box = QHBoxLayout()
        self.season_capt = QLabel()
        self.season_capt.setText("Choose season:")
        self.season_capt.setFixedWidth(80)
        self.season_sel = QComboBox()
        self.season_box.addWidget(self.season_capt)
        self.season_box.addWidget(self.season_sel)
        self.right_side.addLayout(self.season_box)
        
        
        # Episode line2
        self.line2 = QLabel()
        self.line2.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        self.line2.setLineWidth(1)
        self.line2.setMaximumHeight(5)
        self.right_side.addWidget(self.line2)
        
        
        # Episode layout
        self.episode_list = QListWidget()
        self.episode_list_info = QVBoxLayout()
        self.episode_name = QLabel()
        self.episode_info_text = QLabel()
        self.episode_rating = QLabel()
        self.episode_airdate = QLabel()
        self.episode_banner = QLabel()
        self.hline_episode_info = QLabel()
        self.episode_download = QPushButton()
        self.episode_download.setText("Download now!")
        self.episode_info_text.setWordWrap(True)
        self.episode_banner.setText("(No episode selected)")
        self.episode_name.setText("Name: No episode selected")
        self.episode_info_text.setText("Description: No episode selected")
        self.episode_rating.setText("TVDB-Rating: No episode selected")
        self.episode_airdate.setText("Originally aired: No episode selected")
        self.hline_episode_info.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.hline_episode_info.setLineWidth(1)
        self.hline_episode_info.setFixedHeight(5)
        fixedWidth = 400
        self.episode_banner.setFixedWidth(fixedWidth)
        self.episode_name.setFixedWidth(fixedWidth)
        self.episode_rating.setFixedWidth(fixedWidth)
        self.episode_info_text.setFixedWidth(fixedWidth)
        self.episode_airdate.setFixedWidth(fixedWidth)
        self.episode_list_info.addWidget(self.episode_banner)
        self.episode_list_info.addWidget(self.episode_name)
        self.episode_list_info.addWidget(self.hline_episode_info)
        self.episode_list_info.addWidget(self.episode_rating)
        self.episode_list_info.addWidget(self.episode_airdate)
        self.episode_list_info.addWidget(self.episode_info_text)
        self.episode_list_info.addWidget(self.episode_download)
        self.episode_list_info.setAlignment(Qt.AlignTop)
        self.episode_list_Layout.addWidget(self.episode_list)
        self.episode_list_Layout.addLayout(self.episode_list_info)
        self.right_side.addLayout(self.episode_list_Layout)
        
        
        # Bottom layout
        self.bottom_layout = QHBoxLayout()
        self.status = QLabel()
        self.rating = QLabel()
        self.exit_button = QPushButton() 
        self.status.setText("Current status: Continuing")
        self.rating.setText("TVDB Rating: 9.0 / 10.0")
        self.status.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.rating.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.status.setAlignment(Qt.AlignCenter)
        self.rating.setAlignment(Qt.AlignCenter)
        self.exit_button.setText("Quit")
        self.status.setFixedHeight(40)
        self.rating.setFixedHeight(40)
        self.exit_button.setFixedHeight(40)
        self.exit_button.setFixedWidth(150)
        self.bottom_layout.addWidget(self.status)
        self.bottom_layout.addWidget(self.rating)
        self.bottom_layout.addWidget(self.exit_button)
        self.bottom_layout.setAlignment(Qt.AlignBottom)   
        self.right_side.addLayout(self.bottom_layout)
        
        # Connect signals
        self.series_list.currentItemChanged.connect(self.change_list_selection)
        self.season_sel.currentIndexChanged.connect(self.change_season_selection)
        self.episode_list.currentItemChanged.connect(self.change_episode_selection)
        self.exit_button.clicked.connect(self.exit_app)
       
        # Add layouts to main window
        self.right_side.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.left_side)
        self.layout.addLayout(self.right_side)
        
        
        # Set main layout
        self.setLayout(self.layout)
        
    @Slot()
    def search_series(self):
        searchstring = self.search_line.text()
        if searchstring == "":
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Error!")
            self.msg.setText("You did not enter anything in the search line!")
            self.msg.exec_()
        else:
            self.search_result_list.clear()
            results = seriesfinder.get_search_results(searchstring)
            self.search_result_list.addItems(results)   
    
    @Slot()
    def add_series(self):
        selected_item = self.search_result_list.currentItem().text()
        series_dict = helper.series_dict()
        print selected_item
        series_dict[selected_item] = ""
        items = series_dict.keys()
        self.series_list.clear()
        self.series_list.addItems(items)
        helper.update_series_dict(series_dict)
        self.finder.close()
    
    @Slot()
    def change_list_selection(self):
        current_sel = self.series_list.currentItem().text()
        self.banner.setPixmap(seriesfinder.get_image(current_sel))
        self.description.setText(seriesfinder.get_description(current_sel))
        
        seasons = seriesfinder.get_seasons(current_sel)
        self.season_sel.clear()
        for key in seasons:
            item = str(key)
            self.season_sel.addItem(item)
        
        current_season = int(self.season_sel.currentText())
        episodes = seriesfinder.get_episodes(current_sel, current_season)
        self.episode_list.clear()
        for episode in episodes:
            episodename = seriesfinder.get_episode_name(current_sel, current_season, episode)
            if episode < 10:
                episode_no = "0" + str(episode)
            else:
                episode_no = str(episode)
            self.episode_list.addItem(episode_no + " " + episodename)
            
    @Slot()
    def change_season_selection(self):
        current_sel = self.series_list.currentItem().text()
        current_season = self.season_sel.currentText()
        if current_season == '':
            current_season = 1
        else:
            current_season = int(current_season)
        episodes = seriesfinder.get_episodes(current_sel, current_season)
        self.episode_list.clear()
        for episode in episodes:
            episodename = seriesfinder.get_episode_name(current_sel, current_season, episode)
            if episode < 10:
                episode_no = "0" + str(episode)
            else:
                episode_no = str(episode)
            self.episode_list.addItem(episode_no + " " + episodename)
        
    @Slot()
    def change_episode_selection(self):
        current_series = self.series_list.currentItem().text()
        current_season = self.season_sel.currentText()
        if current_season == '':
            current_season = 1
        else:
            current_season = int(current_season) 
        try:
            current_episode = int(self.episode_list.currentItem().text()[:2])
        except:
            current_episode = 1
        # Name
        self.episode_name.setText(seriesfinder.get_episode_name(current_series, current_season, current_episode))
        
        # Description
        description = seriesfinder.get_episode_info(current_series, current_season, current_episode)
        if description == None:
            description = "No description available."
        self.episode_info_text.setText("Description: " + description)
        
        # Air date
        air_date = seriesfinder.get_air_date(current_series, current_season, current_episode)
        if air_date == None:
            self.episode_airdate.setText("Originally aired: unknown")
        else:
            self.episode_airdate.setText("Originally aired: " + air_date)
        
        # Rating
        rating = seriesfinder.get_episode_rating(current_series, current_season, current_episode)
        if rating == None:
            rating = "TVDB-Rating: No rating available for this episode"
            self.episode_rating.setText(rating)
        else: 
            self.episode_rating.setText("TVDB-Rating: " + rating)    
        
        # Banner
        try:
            banner = seriesfinder.get_episode_image(current_series, current_season, current_episode)
            self.episode_banner.setPixmap(banner)
        except:
            self.episode_banner.setText("(No banner available)")
    
    @Slot()
    def exit_app(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            grabber_app.quit()
       
        
    @Slot()
    def open_finder(self):
        self.finder.show()
    
    def get_current_selection(self):
        current_sel = self.series_list.currentRow()
        return current_sel
        
    def run(self):
        ''' Show the application window and start the main event loop '''
        self.show()
        grabber_app.exec_()
