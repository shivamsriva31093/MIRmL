import json
import os
import threading
from time import sleep

import itertools
import numpy
import sys
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import shuffle
from config import data_dir
import pandas as pd
import pickle

mood_list = ['angry', 'calm', 'happy', 'sad']


class Train_from_moods:
    __training_data_dir = os.path.join(data_dir, '_training_data')
    __train_data = None

    def __init__(self, mood):
        self.__create_dataset(mood)

    def get_training_data(self):
        return self.__train_data

    def __create_dataset(self, mood):
        self.__train_data = pd.read_csv(os.path.join(self.__training_data_dir, mood + '.csv'))
        self.__train_data.loc[self.__train_data['label'] == mood, 'label'] = 1
        self.__train_data.loc[self.__train_data["label"] == 'not' + mood, "label"] = 0

    def find_suitable_parameters(self):
        predictors = ["dvar",
                      "median",
                      "min",
                      "max",
                      "mean",
                      "var",
                      "dvar2",
                      "dmean2",
                      "dmean"
                      ]
        return predictors

    def tune_parameters_GridSearchCV(self, classifier, x, y, param_grid):
        mean_list = []
        print("Tuning parameter for classifier : ")
        self.__printProgress(iteration=0, total=100, prefix='Progress', suffix='Complete', barLength=50)
        for i in range(10):
            x1, y1 = shuffle(x, y, random_state=i)
            sf = StratifiedKFold(n_splits=10, random_state=i)
            sf.get_n_splits(x1, y1)
            grid = GridSearchCV(classifier, param_grid, scoring='accuracy', cv=sf)
            grid.fit(x1, y1)
            self.__printProgress(iteration=10 * (i + 1), total=100, prefix='Progress', suffix='Complete',
                                 barLength=50)
            mean_list.append(dict(params=grid.best_params_, score=grid.best_score_))

        '''You can find the maximum score and the best parameters for your classifier'''

        best_param = max(mean_list, key=lambda d: d['score'])
        return best_param

    def __printProgress(self, iteration, total, prefix='', suffix='', decimals=1, barLength=100):
        formatStr = "{0:." + str(decimals) + "f}"
        percent = formatStr.format(100 * (iteration / float(total)))
        filledLength = int(round(barLength * iteration / float(total)))
        bar = '█' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix))
        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()


'''We are using SVM as our classifier'''


def save_classifiers():
    print('Classifying and storing the classifiers...')
    # Tuning C and gamma for SVM RBF
    c_range = numpy.logspace(start=-15, stop=15, endpoint=True, base=2, num=100)
    g_range = numpy.logspace(start=-15, stop=3, endpoint=True, base=2, num=100)
    param_grids = dict(C=c_range, gamma=g_range)

    for mood in mood_list:
        print("classifying for mood %s:" % mood)
        data_ob = Train_from_moods(mood)
        train_set = data_ob.get_training_data()
        predictors = data_ob.find_suitable_parameters()
        best_params = data_ob.tune_parameters_GridSearchCV(classifier=svm.SVC(kernel='rbf'), x=train_set[predictors],
                                                           y=train_set['label'].astype(int), param_grid=param_grids)
        file = os.path.join(data_dir, '_classifier_serialized')
        with open(file + os.sep + mood + '.json', 'w') as fp:
            json.dump(best_params, fp)
        c = best_params['params']['C']
        gamma = best_params['params']['gamma']
        clf = svm.SVC(kernel='rbf', C=c, gamma=gamma, probability=True)
        fit_data_and_save(train_set[predictors], train_set['label'].astype(int), clf, mood)

    print('Process finished.')


def fit_data_and_save(X, y, classifier, mood):
    classifier.fit(X, y)
    print("persisting the current classifier")
    with open(os.path.join(data_dir, '_classifier_serialized' + os.sep + mood + '.pkl'), mode='wb') as file:
        pickle.dump(classifier, file)
    print("data stored for %s classifier" % mood)

save_classifiers()