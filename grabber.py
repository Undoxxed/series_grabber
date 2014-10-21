# encoding=utf8
import requests
import pyperclip
import json
import time
from collections import OrderedDict
from sys import exit
import helper


''' Front page '''


def get_html_fp():
    dict_prefs = helper.prefs_dict()
    if time.time() - dict_prefs['lastchecked'] > \
            (dict_prefs['update_interval_in_minutes'] * 60):
                html = requests.get('http://serienjunkies.org/')
                file = open("data/sj.html", 'w')
                file.write(html.text.encode('utf-8'))
                file.close()
                helper.update_json_time()
                return html.text
    else:
        file = open("data/sj.html", 'r')
        filecontent = file.read()
        file.close()
        return filecontent


def get_episode_from_fp(start_pos):
    html = get_html_fp()
    episode_start = html.find('.S', start_pos)
    after_s = html[episode_start+2:episode_start+3]
    while helper.is_no_number(after_s):
        episode_start += 1
        episode_start = html.find('.S', episode_start)
        after_s = html[episode_start+2:episode_start+3]

    episode_end = html.find('.', episode_start + 1)
    episode = html[episode_start+1:episode_end]
    return episode


def get_release_name_from_fp(series, start_pos):
    html = get_html_fp()
    link_end = html.find('</a>', start_pos)
    release = html[start_pos:link_end]
    return release


def episode_comparison(series, start_pos):
    dict_series = helper.series_dict()
    episode = get_episode_from_fp(start_pos)
    if dict_series[series]["episode"] < episode:
        return True
    return False


''' index dictionary '''


def index_dict():
    in_file = open("data/index.json", 'r')
    index_dict = json.load(in_file)
    in_file.close()
    index_dict = OrderedDict(index_dict)
    return index_dict


def init_index_json(series, start_pos):
    in_file = open("data/index.json", 'r')
    indexfile = json.load(in_file)
    in_file.close()
    html = get_html_fp()
    url = helper.get_last_link_before_pos(start_pos, html)
    release = get_release_name_from_fp(series, start_pos)
    #if series doesn't exist, add series:
    try:
        if indexfile[series] == '':
            indexfile[series] = {}
    except:
            indexfile[series] = {}

    indexfile[series][release] = url

    out_file = open("data/index.json", 'w')
    json.dump(indexfile, out_file, indent=4)
    out_file.close()


def update_index_json(indexfile):
    out_file = open("data/index.json", 'w')
    json.dump(indexfile, out_file, indent=4)
    out_file.close()


def update_series_dict(series):
    dict_series = helper.series_dict()
    dict_index = index_dict()
    largest = ""
    for key in dict_index[series].keys():
        if key > largest:
            largest = key
    largest = helper.get_episode_from_string(0, largest)
    dict_series[series]["episode"] = largest
    out_file = open("data/series.json", 'w')
    json.dump(dict_series, out_file, indent=4)
    out_file.close()


''' Tests '''


def quality_test(series, start_pos):
    dict_series = helper.series_dict()
    release = get_release_name_from_fp(series, start_pos)
    quali = dict_series[series]["quality"]
    if quali == "sd":
        if "720" not in release and "1080" not in release:
            return True
        return False
    elif quali == "720":
        if "720" in release:
            return True
        return False
    elif quali == "1080":
        if "1080" in release:
            return True
        return False
    elif quali == "x264":
        if "720" not in release and "1080" not in release:
            if "x264" in release:
                return True
        return False
    else:
        print "You didn't specify a quality",
        " / The quality you specified doesn't work"


def double_test(series, start_pos):
    dict_index = index_dict()
    episode = get_episode_from_fp(start_pos)
    try:
        i = 0
        found = None
        while i < 100:
            if str(dict_index[series].keys()[i]).find(episode) == -1:
                pass
            else:
                found = True
            i += 1
    except:
        pass
    if found is True:
        return False
    return True


def language_test(series, start_pos):
    release = get_release_name_from_fp(series, start_pos)
    dict_series = helper.series_dict()
    if dict_series[series]["language"] == "en":
        if "GERMAN" in release or "German" in release:
            return False
        return True
    elif dict_series[series]["language"] == "de":
        if "GERMAN" in release or "German" in release:
            return True
        return False
    else:
        return True


''' Search & Update '''


def search_for_new_episodes(series):
    html = get_html_fp()
    if html.find(series):
        start_pos = html.find(series)
        while start_pos != -1:
            if language_test(series, start_pos):
                if quality_test(series, start_pos):
                    if double_test(series, start_pos):
                        if episode_comparison(series, start_pos):
                            init_index_json(series, start_pos)

            start_pos = html.find(series, start_pos + 1)


def check_all():
    dict_series = helper.series_dict()
    for i in dict_series:
        search_for_new_episodes(str(i))


def download_all():
    dict_index = index_dict()
    check_all()
    for series in dict_index:
        download_series(series)


def action():
    check_all()
    print_index()
    user_choice()


def background_action():
    check_all()
    download_all()
    #Jdownloader-Plugin: check if correct
    dict_index = index_dict()
    for series in dict_index:
        update_series_dict(series)
    dict_index = {}
    update_index_json(dict_index)


''' User Interaction & Output '''


def print_index():
    dict_series = helper.series_dict()
    dict_series = OrderedDict(dict_series)
    dict_index = index_dict()
    dict_index = OrderedDict(dict_index)
    print "\n"
    print ("Index" + " "*10 +
           "Series" + " "*15 +
           "Last" + " "*26 +
           "New Episodes")
    print "\n"
    for i in dict_series:
        if i in dict_index:
            pass
        else:
            #long_episodes for cases like S26E01-E03
            long_episodes = len(dict_series[i]["episode"]) - 6
            print ("-" + " "*14 +
                   i + ' ' * (21 - len(i)) +
                   dict_series[i]["episode"] + ' ' * (24 - long_episodes) +
                   "-")
    #print "\n"
    for i in dict_index:
        try:
            exception = dict_index[i]
            long_episodes = len(dict_series[i]["episode"]) - 6
            print dict_index.keys().index(i) + 1,\
                " "*12, i + ' ' * (20 - len(i)),\
                dict_series[i]["episode"], " "*(22 - long_episodes),\
                len(dict_index[i]), "<<"
        except:
            pass
    print "\n"


#ask if one worked if answer is no
def user_choice():
    dict_index = index_dict()
    string = ("Type a index to download all new episodes of that series,\n" +
              "or type 'a' or 'all' to download all found new episodes,\n" +
              "or type 'x' or 'exit' or 'quit' to quit.\n")
    userchoice = raw_input(string)
    if userchoice == "a" or userchoice == "all":
        download_all()
        ask_if_all_downloads_correct()
    elif userchoice == "x" or userchoice == "quit" or userchoice == "exit":
        exit("BahBah :)")
    else:
        try:
            seriesname = dict_index.items()[(int(userchoice) - 1)][0]
            print "Sending", seriesname, "to jDownloader."
            download_series(seriesname)
            ask_if_download_correct(seriesname)

        except:
            if dict_index == {}:
                exit("Nothing new.Bye :)")
            user_choice()


def download_series(series):
    dict_index = index_dict()

    try:
        i = 0
        while i < 100:
            html = requests.get(dict_index[series].values()[i])
            text = html.text
            key_pos = text.find(dict_index[series].keys()[i])
            link = helper.get_hoster_link(key_pos, text)
            pyperclip.copy(link)
            #time.sleep(1)
            i += 1
    except:
        pass


def ask_if_download_correct(series):
    dict_index = index_dict()
    if len(dict_index[series].keys()) == 1:
        episode_string = "episode"
    else:
        episode_string = "episodes"
    question = "Did you successfully download {} {} of {}?",
    "\n'y'/'yes' or 'n'/'no':"
    question = question.format(len(dict_index[series].keys()),
                               episode_string, series)
    try:
        answer = raw_input(question)
    except:
        print "Why did I choose to use a try??'"
    if answer == "y" or answer == "yes":
        print series, "removed from index.json\nHave fun watching! :)"
        update_series_dict(str(series))
        dict_index.pop(series, None)
        update_index_json(dict_index)
        action()
    elif answer == "n" or answer == "no":
        pass
    else:
        print "Wrong input.Please type 'y'/'yes' or 'n'/'no'\n"
        ask_if_download_correct(series)


def ask_if_all_downloads_correct():
    dict_index = index_dict()
    for series in dict_index:
        ask_if_download_correct(series)
