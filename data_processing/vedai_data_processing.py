# 1- Read the Data 
# 2- Convert and Process the data
# 3- Output the Final Format


import os
import pandas as pd

path = "./data_annotation/vedai/"

def update_annotations(filename):
    with open(filename, 'r') as file:
        data = file.read()

        text = '\n'.join(' '.join(line.split()) for line in data.split('\n'))
        text.replace('\t', ' ')

        # print(text)
        output = open(filename, 'w')
        output.write(text)
        output.close()

        data = pd.read_csv(filename, sep=' ', index_col=None, header=None, names=['x_center', 'y_center', 'orientation', 'class', 'is_contained', 'is_occluded', 'corner1_x', 'corner2_x', 'corner3_x', 'corner4_x', 'corner1_y', 'corner2_y', 'corner3_y', 'corner4_y'])

        data['class'].replace(11, 3, inplace=True)
        data['class'].replace(23, 6, inplace=True)
        data['class'].replace(201, 11, inplace=True)
        data['class'].replace(31, 12, inplace=True)

        data['class'] = data['class'] - 1
        data['x_center_ratio'] = data['x_center'].astype(float) / 1024.
        data['y_center_ratio'] = data['y_center'].astype(float) / 1024.
        data['width_ratio'] = (data[['corner1_x', 'corner2_x', 'corner3_x', 'corner4_x']].max(axis=1) - data[['corner1_x', 'corner2_x', 'corner3_x', 'corner4_x']].min(axis=1)) / 1024.
        data['height_ratio'] = (data[['corner1_y', 'corner2_y', 'corner3_y', 'corner4_y']].max(axis=1) - data[['corner1_y', 'corner2_y', 'corner3_y', 'corner4_y']].min(axis=1)) / 1024.

        res = data.drop(['x_center', 'y_center', 'corner1_x', 'corner2_x', 'corner3_x', 'corner4_x', 'orientation', 'corner1_y', 'corner2_y', 'corner3_y', 'corner4_y', 'is_contained', 'is_occluded'], axis=1)
        # print(res)
        res.to_csv(filename, sep=' ', index=False, header=None)

list = os.listdir(path)
for filename in list:
    if filename.find(".txt")!= -1 and filename[:2] == "00":
        print(filename)
        update_annotations(path + filename)