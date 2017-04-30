import os
import pickle

import pandas

from config import data_dir


class Predict:
    __classifiers = dict()
    __test_data = dict()

    def __init__(self, test_data):
        self.__load_classifiers()
        self.__test_data = test_data

    def __load_classifiers(self):
        folder = os.path.join(data_dir, '_classifier_serialized')
        classifiers = {}
        moods = ['angry', 'calm', 'happy', 'sad']
        for mood in moods:
            file = folder + os.sep + mood + '.pkl'
            try:
                with open(file, mode='rb') as fp:
                    classifiers[mood] = pickle.load(fp)
            except FileNotFoundError as e:
                print(mood + '.pkl does not exist!')
        self.__classifiers = classifiers

    def predict(self):
        prediction = {}
        for k,v in self.__classifiers.items():
            mood_class = v.predict(self.__test_data)
            if mood_class == 0:
                mood_class = 'not '+k
            else:
                mood_class = k
            prediction[k] = {
                'mood': k,
                'class': mood_class,
                'probabiity': v.predict_proba(self.__test_data).tolist()
            }
        return prediction


# if __name__ == '__main__':
#     dic = {
#         "dmean": 0.0139594515786,
#         "median": 0.064453125,
#         "dmean2": 0.0160617846996,
#         "dvar2": 0.000231879690546,
#         "min": 0.001953125,
#         "var": 0.00233350670896,
#         "dvar": 0.000180437418749,
#         "max": 0.51611328125,
#         "mean": 0.0707667768002
#     }
#     td = pandas.DataFrame.from_dict([dic], orient='columns')
#     ob = Predict(td)
#     print(ob.predict())