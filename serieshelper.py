# Python imports
import os
import urllib

# External imports
import tvdb_api

# Internal imports
import helper


''' TVDB - Methods '''

# General

def getAPI():
    return "5F3B75C374E7D098"


def get_search_results(searchstring):
    t = tvdb_api.Tvdb(interactive = True, select_first=False)
    t.apikey = getAPI()
    search_results = t.search(searchstring)
    search_result = []
    for i in range(0,len(search_results)):
         search_result.append(search_results[i]['seriesname'])
    return search_result


# Get info from TVDB

def get_description(series):
    t = tvdb_api.Tvdb()
    t.apikey = getAPI()
    description = t[series]['overview']
    return description


def get_episode_description(series, season, episode):
    t = tvdb_api.Tvdb()
    t.apikey = getAPI()
    episodeinfo = t[series][season][episode]['overview']
    return episodeinfo


def get_status(series):
    t = tvdb_api.Tvdb()
    t.apikey = getAPI()
    status = t[series]['status']
    return status


def get_rating(series):
    t = tvdb_api.Tvdb()
    t.apikey = getAPI()
    rating = t[series]['rating']
    return rating


def get_episode_rating(series, season, episode):
    t = tvdb_api.Tvdb()
    t.apikey = getAPI()
    rating = t[series][season][episode]['rating']
    return rating


def get_air_date(series, season, episode):
    t = tvdb_api.Tvdb()
    t.apikey = getAPI()
    air_date = t[series][season][episode]['firstaired']
    return air_date


def add_series_to_json(series):
    t = tvdb_api.Tvdb()
    t.apikey = getAPI()

    # Open series.json in dictionary
    dict_series = helper.series_dict()
    dict_series[series] = {}

    # Get general series info / add empty values to dictionary
    dict_series[series]['description'] = get_description(series)
    dict_series[series]['rating'] = get_rating(series)
    dict_series[series]['status'] = get_status(series)
    dict_series[series]['userstatus'] = ""
    dict_series[series]['language'] = ""
    dict_series[series]['quality'] = ""
    dict_series[series]['sj_link'] = ""
    dict_series[series]['last_episode'] = ""

    # Loop through seasons and save in dict
    dict_series[series]['seasons'] = {}
    for season in t[series].keys():
        dict_series[series]['seasons'][season] = {}
        dict_series[series]['seasons'][season]['season_link_sj'] = ""
        for episode in t[series][season].keys():
            dict_series[series]['seasons'][season][episode] = {}
            dict_series[series]['seasons'][season][episode]['episodename'] = t[series][season][episode]['episodename']
            dict_series[series]['seasons'][season][episode]['air_date'] = get_air_date(series, season, episode)
            dict_series[series]['seasons'][season][episode]['rating'] = get_episode_rating(series, season, episode)
            dict_series[series]['seasons'][season][episode]['description'] = get_episode_description(series, season, episode)

    # Save dictionary in series.json
    helper.update_series_dict(dict_series)


# Images

def get_image(series):
    directory = "data/pictures/" + series.replace(' ', '').lower()
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + "/main.jpg"
    if os.path.exists(path):
        return path
    else:
        path = get_image_from_tvdb(series)
        return path

def get_image_from_tvdb(series):
    t = tvdb_api.Tvdb(banners=True)
    t.apikey = getAPI()
    banner_id = get_highest_rated_banner_id(series)
    if banner_id != -1:
        url = t[series]['_banners']['series']['graphical'][banner_id]['_bannerpath']
        path = "data/pictures/" + series.replace(' ', '').lower() + "/main.jpg"
        urllib.urlretrieve(url, path)
        return path
    else:
        return "data/pictures/error.jpg"


def get_highest_rated_banner_id(series):
    t = tvdb_api.Tvdb(banners=True)
    t.apikey = getAPI()
    keys = t[series]['_banners']['series']['graphical'].keys()
    value = 0
    returnkey = 0
    for key in keys:
        try:
            key_rating = float(t[series]['_banners']['series']['graphical'][key]['rating'])
            key_rating_count = float(t[series]['_banners']['series']['graphical'][key]['ratingcount'])
            key_value = key_rating * key_rating_count
            if key_value > value:
                value = key_value
                return key
        except KeyError:
            pass

    if value == 0:
        series_dict = helper.series_dict()
        lan_pref = series_dict[series]['language']
        for key in keys:
            try:
                lan = t[series]['_banners']['series']['graphical'][key]['language']
                if lan == lan_pref:
                    return key
            except KeyError:
                pass

        for key in keys:
            try:
                lan = t[series]['_banners']['series']['graphical'][key]['language']
                if lan == "en":
                    return key
            except KeyError:
                pass

    return -1

def get_episode_image(series, season, episode):
    directory = "data/pictures/" + series.replace(' ', '').lower()
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + "/S" + season + "E" + episode + ".jpg"
    if os.path.exists(path):
        return path
    else:
        path = get_episode_image_from_tvdb(series, season, episode)
        return path

def get_episode_image_from_tvdb(series, season, episode):
    t = tvdb_api.Tvdb(banners=True)
    t.apikey = getAPI()
    try:
        url = t[series][int(season)][int(episode)]['filename']
        path = "data/pictures/" + series.replace(' ', '').lower() + "/S" + str(season) + "E" + str(episode) + ".jpg"
        urllib.urlretrieve(url, path)
        return path
    except KeyError:
        return "data/pictures/episode_error.jpg"


def get_images_for_all_episodes(series):
    dict_series = helper.series_dict()
    for season in dict_series[series]["seasons"].keys():
        for episode in dict_series[series]["seasons"][season].keys():
            if episode != "season_link_sj":
                print "S" + season + "E" + episode
                get_episode_image(series, season, episode)



#add_series_to_json("The Simpsons")
#add_series_to_json("Scrubs")
get_images_for_all_episodes("Scrubs")
#get_images_for_all_episodes("The Simpsons")

