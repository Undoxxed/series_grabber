import json
import time

''' .json methods '''


#   Initiates empty .json file '''
def init_json(name):
    in_file = open("data/" + name + ".json", 'r')
    try:
        json_file = json.load(in_file)
    except IOError:
        json_file = {}
    in_file.close()
    out_file = open("data/" + name + ".json", 'w')
    json.dump(json_file, out_file, indent=4)
    out_file.close()


#   Returns series.json as dictionary
def series_dict():
    in_file = open("data/series.json", 'r')
    series_dict = json.load(in_file)
    in_file.close()
    return series_dict


#   Updates series.json with given dictionary
def update_series_dict(series_dict):
    out_file = open("data/series.json", 'w')
    json.dump(series_dict, out_file, indent=4)
    out_file.close()


#   Returns prefs.json as dictionary
def prefs_dict():
    in_file = open("data/prefs.json", 'r')
    prefs_dict = json.load(in_file)
    in_file.close()
    return prefs_dict


#   Updates prefs.json with given dictionary
def update_prefs_dict(series_dict):
    out_file = open("data/prefs.json", 'w')
    json.dump(series_dict, out_file, indent=4)
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


#   Returns download.json as dictionary
def download_dict():
    in_file = open("data/download.json", 'r')
    download_dict = json.load(in_file)
    in_file.close()
    return download_dict


#   Updates download.json with given dictionary
def update_download_dict(series_dict):
    out_file = open("data/download.json", 'w')
    json.dump(series_dict, out_file, indent=4)
    out_file.close()


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


def is_link(link):
    if link == "javascript:void(0);":
        return False
    else:
        return True


def get_last_link_before_pos(pos, html):
    index_of_a_href = html.rfind('<a href=', 0, pos)
    start_quote = html.find('"', index_of_a_href)
    end_quote = html.find('"', start_quote + 1)
    url = html[start_quote + 1:end_quote]
    return url
