import csv
from collections import defaultdict
from urllib.request import urlopen

import musicbrainzngs
import json
import os


def create_tag_track_list():
    tag_track_matrix = defaultdict(list)
    file_path = '../lastfm_train/lastfm_train/{0}/{1}/{2}/{3}.json'

    with open('complimentary_tag_track_matrix.csv', 'r', newline='') as in_file:
        csv_reader = csv.DictReader(in_file)
        i = 0
        for dictionary in csv_reader:

            for key, value in dictionary.items():

                filename = ''
                if value.split():
                    filename = value.split()[0]
                if filename:
                    filename = file_path.format(filename[2], filename[3], filename[4], filename)
                    try:
                        file_ob = open(filename, 'r', encoding='UTF-8')
                        if file_ob:
                            json_dic = json.load(file_ob)
                            title = json_dic['title']
                            artist = json_dic['artist']
                            tid = json_dic['track_id']
                            track_mat = dict([('title', title), ('artist', artist), ('tid', tid)])
                            tag_track_matrix[key].append(track_mat)
                    except Exception as e:
                        print(e)

    with open('complimentary_track_list.json', 'w', encoding='UTF-8') as fp:
        json.dump(tag_track_matrix, fp, ensure_ascii=False)


def search_for_MBID(search_dict):
    track_list = search_dict['recording-list']
    for dicts in track_list:
        t_title = dicts['title']
        t_artist = dicts['artist-credit'][0]['artist']['name']
        t_mbid = dicts['id']
        if artist == t_artist and t_title == title:
            return t_mbid
    return ''


def start_getting_track_list():
    track_matrix = {}
    create_tag_track_list
    musicbrainzngs.set_useragent(app='IDEProject', version='0.1', contact='shivam.srivastava31093@gmail.com')

    print('-------------------------------------------------------------------------------------------------------')

    with open('complimentary_track_list.json', 'r+', encoding='utf-8') as fp:
        song = 0
        track_matrix = json.load(fp)
        for k, v in track_matrix.items():
            for track_details in v:
                artist = track_details['artist']
                title = track_details['title']
                tid = track_details['tid']
                print('Getting MBID for track no ', song, ':', str(title).encode(encoding='utf-8'))
                try:
                    search = musicbrainzngs.search_recordings(title)
                except Exception as e:
                    print(e)
                    track_details['mbid'] = ''
                else:
                    mbid = search_for_MBID(search)
                    print('MBID fir this track is: %s' % str(mbid).encode(encoding='utf-8'))
                    track_details['mbid'] = mbid

                finally:
                    song += 1
            fp.seek(0)
            json.dump(track_matrix, fp, indent=4)

    print('-------------------------------------------------------------------------------------------------------')
    print('process finished')
    print('-------------------------------------------------------------------------------------------------------')


def get_json(url):
    return urlopen(url, timeout=6000).readall().decode('utf8')


def create_path_from_trackid(trackid, folder):
    main_dir = 'H:\Tutorials\Minor Project\part1\Essentia_data'
    path = os.path.join(main_dir, folder)
    if not os.path.exists(path):
        os.mkdir(path)
    t_p = trackid
    path = os.path.join(path, t_p)
    return path


def get_data_from_acoustic_brainz(mbid):
    try:
        url = 'https://acousticbrainz.org/api/v1/' + mbid + '/low-level'
        data = get_json(url=url)
        if len(data) == 1:
            return {}
        return data
    except Exception as e:
        print(e)
        return {}


def get_json_files_from_essentia():
    song_dic = {}
    with open('complimentary_track_list.json', 'r', encoding='utf-8') as fp:
        song_dic = json.load(fp)

    for k, v in song_dic.items():
        for track in v:
            trackid = track['tid']
            mbid = track['mbid']
            try:
                path = create_path_from_trackid(trackid, k)

                low_level_data = get_data_from_acoustic_brainz(mbid)
                if not low_level_data:
                    print('json empty!')
                    continue
                if not os.path.exists(path):
                    os.makedirs(path)
                t_p = path + os.sep + trackid + '.json'
                with open(t_p, 'w', encoding='utf-8') as fp:
                    json.dump(low_level_data, fp, ensure_ascii=False)

            except Exception as e:
                print(e)
                if os.path.exists(path):
                    os.rmdir(path)


get_json_files_from_essentia()

