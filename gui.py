import sys
from PySide.QtCore import *
from PySide.QtGui import *
import helper
import seriesfinder
import time


qt_app = QApplication(sys.argv)


 
class HelloWorldApp(QWidget):
    ''' A Qt application that displays the text, "Hello, world!" '''
    
    def __init__(self):
        # Initialize the object as a QLabel
        QWidget.__init__(self)
 
        # Main Window
        self.setMinimumSize(400, 185)
        self.setWindowTitle('SeriesGrabber v0.1')
        
        # Layouts
        self.layout = QVBoxLayout()
        self.banner_descr_layout = QFormLayout()
        self.status_rating_layout = QHBoxLayout()
        self.episode_list = QFormLayout()
#       self.season_buttons_layout = QHBoxLayout()
        
        # ComboBox for series in series_dict
        self.series_box = QComboBox(self)
        series_dict = helper.series_dict()  
        for i in range (0, len(series_dict.keys())):
            seriesname = series_dict.keys()[i].replace('.', ' ')
            self.series_box.addItem(seriesname) 
        self.banner_descr_layout.addRow(self.series_box)
        
        # Season ComboBox (until Signal-emitting of button works)
        self.season_box = QComboBox(self)
        current_sel = self.series_box.currentText()
        seasons = seriesfinder.get_seasons(current_sel)
        for key in seasons:
            if key != 0:
                self.season_box.addItem(str(key))
        self.banner_descr_layout.addRow("=> Choose season:", self.season_box)
        
        
        # Status & Rating
        self.status = QLabel(self)
        self.rating = QLabel(self)
        current_sel = self.series_box.currentText()
        status_str = "Current Status: " + seriesfinder.get_status(current_sel)
        self.status.setText(status_str)
        self.status.setAlignment(Qt.AlignLeft)
        rating_str = "TVDB Rating: " + seriesfinder.get_rating(current_sel)
        self.rating.setText(rating_str)
        self.rating.setAlignment(Qt.AlignRight)
        self.status_rating_layout.addWidget(self.status)
        self.status_rating_layout.addWidget(self.rating)
        self.banner_descr_layout.addRow(self.status_rating_layout)
        
        
        # Banner
        self.banner = QLabel(self)
        series = self.series_box.currentText().replace(' ', '.')
        bannerpath = seriesfinder.get_image(series)
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setPixmap(bannerpath)
        self.banner_descr_layout.addRow(self.banner)
              
        # Visual Divider
        self.divider3 = QLabel(self)
        self.divider3.setText("_"*125)
        self.banner_descr_layout.addRow(self.divider3)
        
        # Description
        descr_str = seriesfinder.get_description(self.series_box.currentText())
        self.description = QLabel(descr_str, self)
        self.description.setWordWrap(True)
        self.banner_descr_layout.addRow(self.description)
        
        
        # Visual Divider
        self.divider4 = QLabel(self)
        self.divider4.setText("~"*100)
        self.divider4.setAlignment(Qt.AlignCenter)
        self.banner_descr_layout.addRow(self.divider4)
        
#         # Season Buttons
#         current_sel = self.series_box.currentText()
#         seasons = seriesfinder.get_seasons(current_sel)
#         string_signal = Signal(str)
#         for key in seasons:
#                 self.season_button = QPushButton(self)
#                 self.season_button.setText(str(key))
#                 self.season_button.setFixedWidth(25)
#                 self.season_button.setFixedHeight(25)
#                 self.season_button.clicked.connect(self.change_season)
#                 self.season_buttons_layout.addWidget(self.season_button)
        
      
        # Episode list
        current_series = self.series_box.currentText()
        current_season = self.season_box.currentText()
        episodes = seriesfinder.get_episodes(current_series, int(current_season))
        self.overview_label = QLabel(self)
        self.overview_label.setText("No.\t\tEpisodename\n" + "_"*125)
        self.episode_list.addRow(self.overview_label)
        #for key in seasons:
        for i in range(1, len(episodes)):
            self.episode_info = QLabel(self)
            episodename = seriesfinder.get_episode_info(current_series, int(current_season), i)
            if i < 10:
                i = "0" + str(i)
            else:
                i = str(i)
            info = i + "\t\t" + episodename
            self.episode_info.setText(info)
            self.episode_list.addRow(self.episode_info)
        
                
        # Connect Signals
        self.series_box.currentIndexChanged.connect(self.refresh_series)
        self.season_box.activated.connect(self.change_season)
        
        # Add to final layout
        self.layout.addLayout(self.banner_descr_layout)
#        self.layout.addLayout(self.status_rating_layout)
#        self.layout.addWidget(self.season_box)
        self.layout.addLayout(self.episode_list)
#       self.layout.addLayout(self.season_buttons_layout)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
        self.resize(775, 340 + 19*len(episodes))
    
    @Slot()
    def refresh_series(self):
        
         # Refresh season ComboBox
        self.season_box.clear()
        current_sel = self.series_box.currentText()
        seasons = seriesfinder.get_seasons(current_sel)
        for key in seasons:
            if key != 0:
                    self.season_box.addItem(str(key))
                
        # Refresh episodes
        self.change_season()
                     
        # Convert series string
        series = self.series_box.currentText().replace(' ', '.')
        
        # Refresh banner
        bannerpath = seriesfinder.get_image(series)
        self.banner.setPixmap(bannerpath)
        
        # Refresh description
        descr_str = seriesfinder.get_description(self.series_box.currentText())
        self.description.setText(descr_str)
        
        # Refresh status & rating
        current_sel = self.series_box.currentText()
        status_str = "Current Status: " + seriesfinder.get_status(current_sel)
        self.status.setText(status_str)
        rating_str = "TVDB Rating: " + seriesfinder.get_rating(current_sel)
        self.rating.setText(rating_str)


    @Slot()
    def change_season(self):  
        #self.layout.removeItem(self.episode_list)            
        current_series = self.series_box.currentText()
        current_season = self.season_box.currentText()
        episodes = len(seriesfinder.get_episodes(current_series, int(current_season)))
        self.overview_label = QLabel(self)
        self.overview_label.setText("No.\t\tEpisodename\n" + "_"*125)
        self.clearLayout(self.episode_list)
        self.episode_list.addRow(self.overview_label)
        for i in range(1, episodes):
            self.episode_info = QLabel(self)
            episodename = seriesfinder.get_episode_info(current_series, int(current_season), i)
            if i < 10:
                i = "0" + str(i)
            else:
                i = str(i)
            info = i + "\t\t" + episodename
            self.episode_info.setText(info)
            self.episode_list.addRow(self.episode_info) 
        self.resize(775, 340 + 19*episodes)
    @Slot()    
    def changebanner(self):
        print "Test"
     
   
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())
    
    def run(self):
        ''' Show the application window and start the main event loop '''
        self.show()
        qt_app.exec_()

app = HelloWorldApp()
app.run()
