import helper
import requests


''' Checks '''


def check_next_episode(episode, html, pos):
    currentepisode = int(episode[4:])
    nextepisode = currentepisode + 1
    if nextepisode < 10:
        nextepisode = '0' + str(nextepisode)
    else:
        nextepisode = str(nextepisode)
    print "Searching next episode..."
    pos = html.find(episode[:4]+nextepisode, pos)
    print "Found next episode!"
    if pos != -1:
        return True
    else:
        return False


''' Tests '''


def quality_test(series, html_text, pos):
    dict_series = helper.series_dict()
    pos1 = html_text.find(".", pos)
    pos2 = html_text.find(".", pos1 + 1)
    quali_episode = html_text[pos1+1:pos2]
    quali = dict_series[series]["quality"]
    if quali == "sd":
        if "720" not in quali_episode and "1080" not in quali_episode:
            return True
        return False
    elif quali == "720":
        if "720" in quali_episode:
            return True
        return False
    elif quali == "1080":
        if "1080" in quali_episode:
            return True
        return False
    elif quali == "x264":
        if "720" not in quali_episode and "1080" not in quali_episode:
            if "x264" in quali_episode:
                return True
        return False
    else:
        print "You didn't specify a quality",
        " / The quality you specified doesn't work"


def double_test(series, rel_name):
    download_dict = helper.download_dict()
    try:
        while True:
            if rel_name in download_dict[series]:
                return False
            else:
                return True
    except:
        pass
    return True


''' Getter '''


def get_season_link(series):
    dict_series = helper.series_dict()
    print "Searching for " + series.replace('.', ' ') + "..."
    name = "http://serienjunkies.org/" + series.replace('.', '-').lower()
    html = requests.get(name)
    season = dict_series[series]["episode"]
    season = season[1:3]
    if season[0] == "0":
        season = season[1]
    searchstring = "; Season " + season
    if searchstring in html.text:
        pos = html.text.find(searchstring)
    else:
        print "Error"
    link = helper.get_last_link_before_pos(pos, html.text)
    return link


def get_episode(series, episode, html, pos):
    if quality_test(series, html, pos):
        rel_name = get_release_name_from_series(html, pos)
        if double_test(series, rel_name):
            print series.replace(".", " ") + " " + episode + " added!"
            hoster_link = helper.get_hoster_link(pos, html)
            helper.init_download_list(series, hoster_link, rel_name)


def get_last_episode(series):
    link = get_season_link(series)
    html = requests.get(link)
    dict_series = helper.series_dict()
    #dict_index = index_dict()
    episode = dict_series[series]["episode"]
    # episode = str(episode)
    if episode[4:] == "00":
        episode = episode[:4] + "01"
        pos = html.text.find("." + episode) + 1
        get_episode(series, episode, html.text, pos)

    pos = html.text.find("." + episode) + 1
    while True:
        if check_next_episode(episode, html.text, pos):
            currentepisode = int(episode[4:])
            nextepisode = currentepisode + 1
            if nextepisode < 10:
                nextepisode = '0' + str(nextepisode)
            else:
                nextepisode = str(nextepisode)
            episode = episode[:4]+nextepisode
            pos = html.text.find(episode, pos)
            get_episode(series, episode, html.text, pos)
            continue
        else:
            break
    print "Done"


def get_release_name_from_series(html, start_pos):
    name_start = html.rfind(">", 0, start_pos)
    name_end = html.find("<", name_start)
    release = html[name_start+1:name_end]
    return release
