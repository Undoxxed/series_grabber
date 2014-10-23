import sys
from PySide.QtCore import *
from PySide.QtGui import *
import helper
import seriesfinder


qt_app = QApplication(sys.argv)


 
class HelloWorldApp(QWidget):
    ''' A Qt application that displays the text, "Hello, world!" '''
    
    def __init__(self):
        # Initialize the object as a QLabel
        QWidget.__init__(self)
 
        # Salutation
        self.setMinimumSize(400, 185)
        self.setWindowTitle('SeriesGrabber v0.1')
        
        # Layouts
        self.layout = QVBoxLayout()
        self.banner_descr_layout = QFormLayout()
        self.status_rating_layout = QHBoxLayout()
        
        # ComboBox for series in series_dict
        self.series_box = QComboBox(self)
        series_dict = helper.series_dict()  
        for i in range (0, len(series_dict.keys())):
            seriesname = series_dict.keys()[i].replace('.', ' ')
            self.series_box.addItem(seriesname) 
        self.banner_descr_layout.addRow(self.series_box)
  
        # Banner
        self.banner = QLabel(self)
        series = self.series_box.currentText().replace(' ', '.')
        bannerpath = seriesfinder.get_image(series)
        self.banner.setPixmap(bannerpath)
        self.banner_descr_layout.addRow(self.banner)
        
        # Description
        descr_str = seriesfinder.get_description(self.series_box.currentText())
        self.description = QLabel(descr_str, self)
        self.description.setWordWrap(True)
        self.banner_descr_layout.addRow(self.description)
        
        # Connect ComboBox
        self.series_box.currentIndexChanged[str].connect(self.refresh_series)
        
        
        # Add to final layout
        self.layout.addLayout(self.banner_descr_layout)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    
    @Slot()
    def refresh_series(self):
        series = self.series_box.currentText().replace(' ', '.')
        bannerpath = seriesfinder.get_image(series)
        self.banner.setPixmap(bannerpath)
        descr_str = seriesfinder.get_description(self.series_box.currentText())
        self.description.setText(descr_str)
        
    @Slot()    
    def changebanner(self):
        print "Test"
        
        
    def run(self):
        ''' Show the application window and start the main event loop '''
        self.show()
        qt_app.exec_()

app = HelloWorldApp()
app.run()
