import grabber
import seriesgrabber
import helper
import seriesfinder
import gui_new_layout
from PIL import Image

#grabber.action()
#seriesgrabber.get_last_episode("The.Simpsons")
# profile.run('get_last_episode("The.Simpsons")')
# get_last_episode("Scandal")
#seriesgrabber.get_last_episode("The.Big.Bang.Theory")
#download_dict = helper.download_dict()
#helper.download_series("The.Big.Bang.Theory", download_dict)
#helper.init_json("test")
#grabber.action()
# for series in dict_series:
#     print seriesfinder.get_series_info(series)
#     seriesfinder.get_image(series)
#
# gui.main()
#seriesfinder.search_series()
#print seriesfinder.get_air_date("The.Simpsons", 26, 5)
#string = seriesfinder.print_whole_series("The Big Bang Theory")
#print string
#print "\n"
#seriesfinder.get_image("The.Simpsons")
t = seriesfinder.return_tvdb()
print t["The Simpsons"][1][1].keys()
seriesfinder.get_episode_image_from_tvdb("The Simpsons", 1 ,1)

app = gui_new_layout.SeriesGrabberGUI()
app.run()

