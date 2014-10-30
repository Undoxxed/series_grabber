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