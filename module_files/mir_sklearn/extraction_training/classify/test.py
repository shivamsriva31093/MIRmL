import json
import os
import pandas as pd
from pandas.io.json import json_normalize

main_dir = 'H:\Tutorials\Minor Project\part1\Essentia_data\_testing_data'
mood = 'sad'
path = os.path.join(main_dir, mood)
csv_path = os.path.join(main_dir)
data_frame = pd.DataFrame()


def add_to_dataframe(data_path, label):
    with open(os.path.join(data_path), 'r', encoding='utf-8') as fp:
        json_dic = json.load(fp)
        json_dic = json_dic['lowlevel']['zerocrossingrate']
        data = pd.Series(json_dic)
        data['label'] = label
        global data_frame
        df = data_frame.append(data, ignore_index=True)
        data_frame = df

for data_type in os.listdir(path):
    path1 = os.path.join(path, data_type)
    label = ''
    if data_type == 'negative':
        label = 'not'+ mood
    else:
        label = mood
    for folder in os.listdir(path1):
        print(folder)
        path2 = os.path.join(path1, folder)
        for files in os.listdir(path2):
            path3 = os.path.join(path2, files)
            add_to_dataframe(path3, label)

data_frame.to_csv(os.path.join(csv_path, mood+'.csv'))



