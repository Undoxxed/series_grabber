import sys
from PySide.QtCore import *
from PySide.QtGui import *
import helper
import seriesfinder
import time


grabber_app = QApplication(sys.argv)
        
class SeriesGrabberGUI(QWidget):
    
    def __init__(self):
        # Initialize the object
        QWidget.__init__(self)
        
         # Main Window
        self.setMinimumSize(900, 720)
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
        
        # Info windows while adding
        self.infowindow = QWidget()
        self.infolayout = QVBoxLayout()
        self.infowindow.resize(200, 300)
        self.infolabel = QLabel()
        self.infowindow.setLayout(self.infolayout)
        
        # Set finder layout
        self.finder.setLayout(self.search_layout)
        
        
        ''' MAIN WINDOW '''
        
        # Layouts
        self.layout = QHBoxLayout()
        self.left_side = QVBoxLayout()
        self.right_side = QVBoxLayout()
        
        
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
        
        # Episode layout caption
        self.episode_caption = QHBoxLayout()
        self.caption1 = QLabel()
        self.caption2 = QLabel()
        self.caption3 = QLabel()
        self.caption1.setText("No.")
        self.caption2.setText("Episodename")
        self.caption3.setText("Airdate")
        self.caption1.setFixedWidth(25)
        self.caption2.setFixedWidth(419)
        self.caption3.setFixedWidth(150)
        self.caption1.setFixedHeight(15)
        self.caption2.setFixedHeight(15)
        self.caption3.setFixedHeight(15)
        self.episode_caption.addWidget(self.caption1)
        self.episode_caption.addWidget(self.caption2)
        self.episode_caption.addWidget(self.caption3)
        self.episode_caption.setAlignment(Qt.AlignTop)
        self.right_side.addLayout(self.episode_caption)
        
        # Episode line2
        self.line2 = QLabel()
        self.line2.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        self.line2.setLineWidth(1)
        self.line2.setMaximumHeight(5)
        self.right_side.addWidget(self.line2)
        
        # Episode layout
        self.episode_layout = QHBoxLayout()
        self.episodename = QLabel()
        self.episode_no = QLabel()
        self.episode_airdate = QLabel()
        self.episode_download = QPushButton()
        self.episode_no.setText("01.")
        self.episode_no.setFixedWidth(25)
        self.episodename.setText("This is a placeholder episodename")
        self.episodename.setFixedWidth(419)
        self.episode_airdate.setText("25.06.2014 (aired)")
        self.episode_airdate.setFixedWidth(150)
        self.episode_download.setText("Download now!")
        self.episode_download.setFixedWidth(150)
        self.episode_layout.addWidget(self.episode_no)
        self.episode_layout.addWidget(self.episodename)
        self.episode_layout.addWidget(self.episode_airdate)
        self.episode_layout.addWidget(self.episode_download)
        self.episode_layout.setAlignment(Qt.AlignTop)
        self.right_side.addLayout(self.episode_layout)
        
#         # Bottom layout
#         self.bottom_layout = QHBoxLayout()
#         self.status = QLabel()
#         self.rating = QLabel()
#         self.exit_button = QPushButton() 
#         self.status.setText("Current status: Continuing")
#         self.rating.setText("TVDB Rating: 9.0 / 10.0")
#         self.exit_button.setText("Exit")
#         self.status.setFixedHeight(40)
#         self.rating.setFixedHeight(40)
#         self.exit_button.setFixedHeight(40)
#         self.exit_button.setFixedWidth(150)
#         self.bottom_layout.addWidget(self.status)
#         self.bottom_layout.addWidget(self.rating)
#         self.bottom_layout.addWidget(self.exit_button)
#         self.bottom_layout.setAlignment(Qt.AlignBottom)   
#         self.right_side.addLayout(self.bottom_layout)
        
        # Connect signals
        self.series_list.currentItemChanged.connect(self.change_list_selection)
        self.season_sel.currentIndexChanged.connect(self.change_season_selection)
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
        self.infolabel.setText("Adding series: " + selected_item + "...")
        self.infolayout.addWidget(self.infolabel)
        self.infowindow.show()
        seriesfinder.get_image(selected_item)
        self.infowindow.close()
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
        
    
    @Slot()
    def change_season_selection(self):
        print "Debug"
    
    @Slot()
    def open_finder(self):
        self.finder.show()
    
    def get_current_selection(self):
        current_sel = self.series_list.currentRow()
        print current_sel
        return current_sel
        
    def run(self):
        ''' Show the application window and start the main event loop '''
        self.show()
        grabber_app.exec_()
