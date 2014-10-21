import json
import time
import pyperclip
import time

''' .json methods '''


#   Initiates empty .json file '''
def init_json(name):
    in_file = open("data/" + name + ".json", 'r')
    try:
        json_file = json.load(in_file)
    except:
        json_file = {}
    in_file.close()
    out_file = open("data/" + name + ".json", 'w')
    json.dump(json_file, out_file, indent=4)
    out_file.close()


#   Updates lastchecked time in prefs.json
def update_json_time():
    in_file = open("data/prefs.json", 'r')
    datefile = json.load(in_file)
    in_file.close()
    datefile['lastchecked'] = time.time()
    out_file = open("data/prefs.json", 'w')
    json.dump(datefile, out_file, indent=4)
    out_file.close()


#   Initiates download.json with given series, hosterlink, release name
def init_download_list(series, hosterlink, rel_name):
    in_file = open("data/download.json", 'r')
    download_dic = json.load(in_file)
    in_file.close()
    try:
        if download_dic[series] == '':
            download_dic[series] = {}
    except:
        download_dic[series] = {}
    download_dic[series][rel_name] = hosterlink
    out_file = open("data/download.json", 'w')
    json.dump(download_dic, out_file, indent=4)
    out_file.close()


#   Returns series.json as dictionary
def series_dict():
    in_file = open("data/series.json", 'r')
    series_dict = json.load(in_file)
    in_file.close()
    return series_dict


#   Returns prefs.json as dictionary
def prefs_dict():
    in_file = open("data/prefs.json", 'r')
    prefs_dict = json.load(in_file)
    in_file.close()
    return prefs_dict


#   Returns download.json as dictionary
def download_dict():
    in_file = open("data/download.json", 'r')
    download_dict = json.load(in_file)
    in_file.close()
    return download_dict


'''Series methods'''


def get_episode_from_string(start_pos, string):
    episode_start = string.find('.S', start_pos)
    after_s = string[episode_start+2:episode_start+3]
    while is_no_number(after_s):
        episode_start += 1
        episode_start = string.find('.S', episode_start)
        after_s = string[episode_start+2:episode_start+3]
    episode_end = string.find('.', episode_start + 1)
    episode = string[episode_start+1:episode_end]
    return episode


def get_hoster_link(key_pos, html):
    dict_prefs = prefs_dict()
    hoster = dict_prefs['hoster']
    hosterlinkindex = html.find(hoster, key_pos)
    hosterlink = get_last_link_before_pos(hosterlinkindex, html)
    return hosterlink


def download_series(series, dict_input):
    try:
        i = 0
        while i < 100:
            key = dict_input[series].values()[i]
            pyperclip.copy(key)
            print key
            time.sleep(1)
            i += 1
    except:
        pass


'''Helper methods'''


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


def is_no_number(s):
    try:
        float(s)
        return False
    except ValueError:
        return True


def get_last_link_before_pos(pos, html):
    index_of_a_href = html.rfind('<a href=', 0, pos)
    start_quote = html.find('"', index_of_a_href)
    end_quote = html.find('"', start_quote + 1)
    url = html[start_quote + 1:end_quote]
    return url
