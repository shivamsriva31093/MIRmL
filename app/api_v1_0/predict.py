import json
import os

import pandas
from flask import request, jsonify
from app import app

from modules.mir_sklearn.predict import Predict
from . import api
from ..model.models import Temp


@api.route('/predict/')
def predict():
    track = request.args.get('track')
    artist = request.args.get('artist')

    ''' Search the temp_info table in the database to check if
        the searched track and artist name is present. If present, get the trackId
        and post the json containing the predicted mood of the song. '''

    try:

        track_details = Temp.query.filter_by(track=track, artist=artist).first()
        app.logger.info(track_details)
        if track_details is None:
            return jsonify({'message': 'Unable to fetch record for the track.'})
        file_path = os.path.abspath(track_details.path)
        with open(file_path, mode='r', encoding='utf-8') as fp:
            lowlevel_dic = json.load(fp)
        zcr = lowlevel_dic['lowlevel']['zerocrossingrate']
        td = pandas.DataFrame.from_dict([zcr], orient='columns')
        ob = Predict(td)
        app.logger.info(ob.predict())
        return jsonify({'stats':ob.predict(), 'mood_tag':track_details.label})

    except:
        from app.api_v1_0.errors import InvalidURLParameters
        raise InvalidURLParameters('invalid parameters in URL', status_code=400)
