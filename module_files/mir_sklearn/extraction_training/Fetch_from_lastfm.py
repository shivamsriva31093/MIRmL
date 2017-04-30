import json
from collections import defaultdict
from urllib.parse import urlencode
from urllib.request import urlopen


def get_json(url):
    return urlopen(url, timeout=6000).readall().decode('utf8')


class SetUpLastFm:
    api_key = ""
    url = ""
    methods = {}
    params = {}

    def __init__(self, api_key=""):
        self.api_key = api_key
        self.url = "http://ws.audioscrobbler.com/2.0/?"
        self.methods = {
            'getInfo': 'tag.getinfo',
            'getSimilar': 'tag.getsimilar',
            'getTopTracks': 'tag.gettoptracks',
            'getTopTags': 'track.gettoptags',
            'getTrackInfo': 'track.getinfo',
        }
        self.params = {
            'api_key': api_key,
            'format': 'json'
        }

    def create_url(self, params):
        getUrl = self.url
        return getUrl + urlencode(params)

    def get_similar_tags(self, tag=''):
        params = self.params
        params['method'] = self.methods['getSimilar']
        params['tag'] = tag
        url = self.create_url(params)
        return get_json(url)

    def get_top_tracks(self, tag=''):
        params = self.params
        params['method'] = self.methods['getTopTracks']
        params['tag'] = tag

        url = self.create_url(params)
        return get_json(url)

    def get_top_tags(self, mbid, artist, track):
        params = self.params
        params['method'] = self.methods['getTopTags']
        if mbid is not None:
            params['track'] = track
            params['artist'] = artist
        else:
            params['mbid'] = mbid

        url = self.create_url(params)
        return get_json(url)


class FetchData:
    lastFm = None

    def __init__(self):
        self.lastFm = SetUpLastFm('ba92613bbd5220636c51359dd355e3a0')

    def populate_data(self, mood):
        print('-------------------------------------------------------------------------------------------------------')
        print('getting tracks where the tag %s is applied more than 50 times to maintain data consistency' % mood)
        print('-------------------------------------------------------------------------------------------------------')
        top_tracks_for_tag = self.__get_top_tracks(mood)
        return self.__get_consistent_tracks(top_tracks_for_tag, mood)

    def __get_top_tracks(self, mood):
        json_response = self.lastFm.get_top_tracks(mood)
        json_dict = json.loads(json_response, encoding='utf8')
        return json_dict['tracks']['track']

    def __get_consistent_tracks(self, data, mood):
        ret_dictionary = []
        try:
            flag = 0
            for tracks in data:
                temp_dict = dict()
                if self.__check_track_consistency(tracks['mbid'], tracks['artist']['name'], tracks['name'], mood):
                    flag += 1
                    temp_dict['mbid'] = tracks['mbid']
                    temp_dict['artist'] = tracks['artist']['name']
                    temp_dict['track'] = tracks['name']
                    ret_dictionary.append(temp_dict)
            print('---------------------------------------------------------------------------------------------------')
            print('%s tracks added to file' % flag)
            print('---------------------------------------------------------------------------------------------------')
        except Exception as e:
            print(e)
        return ret_dictionary

    def __check_track_consistency(self, mbid, artist_name, track_name, mood):
        print("__check_track_consistency: checking track for consistency")
        response = self.lastFm.get_top_tags(mbid, artist_name, track_name)
        top_tags = json.loads(response, encoding='utf8')
        for tags in top_tags['toptags']['tag']:
            if (tags['name'] == mood) and (tags['count'] >= 50.0):
                print('track %s consistent')
                return True
        return False

    def __write_to_file(self, mbid, artist, track):
        pass
