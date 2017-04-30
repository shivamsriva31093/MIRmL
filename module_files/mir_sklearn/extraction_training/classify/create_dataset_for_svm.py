import os
from sklearn import metrics

import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

main_dir = 'H:\Tutorials\Minor Project\part1\Essentia_data\_training_data'
mood = 'calm'
csv_path = os.path.join(main_dir)

test_dir = 'H:\Tutorials\Minor Project\part1\Essentia_data\_testing_data'

data = pd.read_csv(os.path.join(csv_path, mood + '.csv'))
data.loc[data['label'] == mood, 'label'] = 1
data.loc[data['label'] == 'not'+mood, "label"] = 0

test_data = pd.read_csv(os.path.join(os.path.join(test_dir), mood+ '.csv'))
test_data.loc[test_data['label'] == mood, 'label'] = 1
test_data.loc[test_data["label"] == 'not'+mood, "label"] = 0


predictors = ['mean']

print(data[predictors].shape)
from sklearn.ensemble import RandomForestClassifier

# Initialize our algorithm with the default paramters
# n_estimators is the number of trees we want to make
# min_samples_split is the minimum number of rows we need to make a split
# min_samples_leaf is the minimum number of samples we can have at the place where a tree branch ends (the bottom points of the tree)

alg = RandomForestClassifier(random_state=1, n_estimators=100, min_samples_split=10, min_samples_leaf=1)
# # Compute the accuracy score for all the cross validation folds.  (much simpler than what we did before!)
kf = KFold(n_splits=10, random_state=1)
kf.get_n_splits(data)
scores = cross_val_score(alg, data[predictors], data['label'].astype(int), cv=kf)
print(scores.mean())


alg.fit(data[predictors], data['label'].astype(int))
y = alg.predict(test_data[predictors])
accuracy_score = metrics.accuracy_score(test_data['label'].astype(int), y)
print(accuracy_score)


