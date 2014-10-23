import requests
import helper
import tvdb_api
from tvdb_api import Season
from PIL import Image
import urllib
import os.path
from mhlib import PATH

def get_series_html():
    link = "http://serienjunkies.org/?cat=0&showall"
    html = requests.get(link)
    return html.text


def print_whole_series(series):
    print "TEST"
    t = tvdb_api.Tvdb(banners = True)
    t.apikey = getAPI()
    
    for i in range(1, len(t[series].keys())):
        series_info = "*" * 100 + "\n"
        series_info += t[series]['seriesname'] + " Season " + str(i) + " overview:\n"
        series_info += "*" * 100 + "\n"
        for o in range (1, len(t[series][int(i)].keys())):
            series_info += str(o) + "." + t[series][int(i)][int(o)]['episodename']+"\n"
        print series_info
        ## Print "None" at the end
    
    
def search_series():
    html_text = get_series_html()
    startpos = html_text.find("<h2>Serien")
    string = "Which series would you like to add to the library?\n"
    userchoice = raw_input(string)
    userchoice = userchoice.title()
    seriespos = html_text.find(userchoice, startpos)
    link = helper.get_last_link_before_pos(seriespos, html_text)
    if check_link(link):
        print "Series available under the following link: " + link
        series_dict = helper.series_dict()
        series = userchoice.replace(' ', '.')
        if series not in series_dict.keys():
            series_dict[series] = {}    
        series_dict[series]["link"] = link
        helper.update_series_dict(series_dict)
        print series
    else:
        print "Series not found! Try again"
        search_series()


def add_links_to_json():
    series_dict = helper.series_dict()
    for series in series_dict:
        get_and_save_link(series)


def get_and_save_link(series):
    html_text = get_series_html()
    startpos = html_text.find("<h2>Serien")
    searchstring = series.replace('.', '-').lower()
    seriespos = html_text.find(searchstring, startpos)
    link = helper.get_last_link_before_pos(seriespos, html_text)

    if check_link(link):
        series_dict = helper.series_dict()
        series_dict[series]["link"] = link
        helper.update_series_dict(series_dict)
    else:
        print "Link not found."


def check_link(link):
    if link == "javascript:void(0);":
        return False
    else:
        return True


def getAPI():
    return "5F3B75C374E7D098"


def test_tvdb():
    t = tvdb_api.Tvdb(banners = True)
    t.apikey = getAPI()
    dict_series = helper.series_dict()

    for series in dict_series:
        try:
            series = series.replace('.', ' ').lower()
            test = t[series]
#             keys = t[series]['_banners']['series']['graphical'].keys()
#             banners = t[series]['_banners']['series']['graphical'][keys[0]]['bannerpath']
#             path = "http://thetvdb.com/banners/" + banners
#             urllib.urlretrieve(path, "data/pictures/" + key + ".jpg")
#             Image.open("data/pictures/" + key + ".jpg").show()
            print test
        except:
            print "Series not found on TVDB"
            continue
#      keys = t[series]['_banners']['series']['graphical'].keys()
#      for key in keys:
#          banners = t['scrubs']['_banners']['series']['graphical'][key]['bannerpath']
#          path = "http://thetvdb.com/banners/" + banners
#          urllib.urlretrieve(path, "data/pictures/" + key + ".jpg")
#          Image.open("data/pictures/" + key + ".jpg").show()


def get_series_info(series):
    string = series.replace('.', ' ').title() + " (Status: " + get_status(series) + ")\n"
    seasons = get_seasons(series)
    if seasons == 1:
        string += str(seasons) + " Season,"
    else:
        string += str(seasons) + " Seasons,"
    string += " TVDB Rating: " + str(get_rating(series)) + "\n"
    string += "~" * 100
    return string


def get_description(series):
    t = tvdb_api.Tvdb(banners = True)
    t.apikey = getAPI()
    series = series.replace('.', ' ').lower()
    description = t[series]['overview']
    return description


def get_rating(series):
    t = tvdb_api.Tvdb(banners=True)
    t.apikey = getAPI()
    series = series.replace('.', ' ').lower()
    rating = t[series]['rating']
    return rating


def get_status(series):
    t = tvdb_api.Tvdb(banners=True)
    t.apikey = getAPI()
    series = series.replace('.', ' ').lower()
    status = t[series]['status']
    return status


def get_seasons(series):
    t = tvdb_api.Tvdb(banners=True)
    t.apikey = getAPI()
    series = series.replace('.', ' ').lower()
    seasons = t[series].keys()
    return seasons


def get_no_of_episodes(series, season):
    t = tvdb_api.Tvdb(banners=True)
    t.apikey = getAPI()
    series = series.replace('.', ' ').lower()
    episodes = len(t[series][season].keys())
    return episodes

def get_episode_info(series, season, episode):
    t = tvdb_api.Tvdb(banners=True)
    t.apikey = getAPI()
    episodeinfo = t[series][season][episode]['episodename']
    return episodeinfo


def get_image(series):
    path = "data/pictures/" + series.replace('.', '').lower() + ".jpg"
    if os.path.exists(path):
        return path
    else:
        path = get_image_from_tvdb(series)
        return path


def get_air_date(series, season, episode):
    t = tvdb_api.Tvdb(banners = True)
    t.apikey = getAPI()
    series = series.replace('.', ' ').lower()
    air_date = t[series][season][episode]['firstaired']
    return air_date


def get_search_results(searchstring):
    t = tvdb_api.Tvdb(interactive = True, select_first=False)
    t.apikey = getAPI()
    search_results = t.search(searchstring)
    print "Search results for <" + searchstring + ">:"
    search_result = ""
    for i in range(0,len(search_results)):
        search_result += str(i+1) + ". " + search_results[i]['seriesname'] + "\n"
    return search_result


def get_image_from_tvdb(series):
    t = tvdb_api.Tvdb(banners = True)
    t.apikey = getAPI()
    series = series.replace('.', ' ').lower()
    keys = t[series]['_banners']['series']['graphical'].keys()
    banner = t[series]['_banners']['series']['graphical'][keys[0]]['bannerpath']
    link = "http://thetvdb.com/banners/" + banner
    path = "data/pictures/" + series.replace(' ', '') + ".jpg"
    urllib.urlretrieve(link, path)
    return path