import os

import pandas as pd
from sklearn import svm, metrics
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.utils import shuffle
import numpy

main_dir = 'H:\Tutorials\Minor Project\part1\Essentia_data\_training_data'
test_dir = 'H:\Tutorials\Minor Project\part1\Essentia_data\_testing_data'
mood = 'angry'
csv_path = os.path.join(main_dir)

train_data = pd.read_csv(os.path.join(csv_path, mood + '.csv'))
train_data.loc[train_data['label'] == mood, 'label'] = 1
train_data.loc[train_data["label"] == 'not' + mood, "label"] = 0

test_data = pd.read_csv(os.path.join(os.path.join(test_dir), mood + '.csv'))
test_data.loc[test_data['label'] == mood, 'label'] = 1
test_data.loc[test_data["label"] == 'not' + mood, "label"] = 0

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

X = train_data[predictors]
Y = train_data['label'].astype(int)

# Using cross validation to check accuracy of SVM

classifier = svm.SVC(C=718.9740641134905, gamma=8.0)
# scores = []
classifier.decision_function()
sf = StratifiedKFold(n_splits=10)
sf.get_n_splits(X, Y)
score = cross_val_score(classifier, X, Y, cv=sf, scoring='accuracy')
print(score)
# for i in range(10):
#     x, y = shuffle(X, Y, random_state=i)
#     sf = StratifiedKFold(n_splits=10, random_state=i)
#     score = cross_val_score(classifier, x, y, cv=sf, scoring='accuracy')
#     scores.append(score.mean())
#
# score = numpy.array([arr.mean() for arr in scores]).mean()
# print('%.1f' % (score*100))




