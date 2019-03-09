import numpy as np
import pandas as pd
import scipy.signal as sp
import os

path, dirs, files = next(os.walk("training_data/labels"))
number_of_features = len(files) # 2
features = [None for i in range(number_of_features)]
for i in range(number_of_features):
    features[i] = pd.read_csv("training_data/labels/"+str(i)+".csv").columns[0]
# print(features) # ['question', 'where']

path, dirs, files = next(os.walk("training_data/features/0"))
number_of_instances = len(dirs) # 10
instances = [[None]*number_of_instances for i in range(number_of_features)]

for feature in range(number_of_features):
    for instance in range(number_of_instances):
        acc = pd.read_csv("training_data/features/" + str(feature) + "/instance_" + str(instance) + "/acceleration.csv")
        gyro = pd.read_csv("training_data/features/" + str(feature) + "/instance_" + str(instance) + "/gyroscope.csv")
        orien = pd.read_csv("training_data/features/" + str(feature) + "/instance_" + str(instance) + "/orientation.csv")
        emg = pd.read_csv("training_data/features/" + str(feature) + "/instance_" + str(instance) + "/emg.csv")
        instances[feature][instance] = [
                                        np.array(acc['Acc_X']),     # 0
                                        np.array(acc['Acc_Y']),     # 1
                                        np.array(acc['Acc_Z']),     # 2
                                        np.array(gyro['Gyro_X']),   # 3
                                        np.array(gyro['Gyro_Y']),   # 4
                                        np.array(gyro['Gyro_Z']),   # 5
                                        np.array(orien['Roll']),    # 6
                                        np.array(orien['Pitch']),   # 7
                                        np.array(orien['Yaw']),     # 8
                                        np.array(orien['Orien_X']),     # 9
                                        np.array(orien['Orien_Y']),     # 10
                                        np.array(orien['Orien_Z']),     # 11
                                        np.array(sp.decimate(emg['EMG1'], 4, None, 'fir', -1, True)),   # 12
                                        np.array(sp.decimate(emg['EMG2'], 4, None, 'fir', -1, True)),   # 13
                                        np.array(sp.decimate(emg['EMG3'], 4, None, 'fir', -1, True)),   # 14
                                        np.array(sp.decimate(emg['EMG4'], 4, None, 'fir', -1, True)),   # 15
                                        np.array(sp.decimate(emg['EMG5'], 4, None, 'fir', -1, True)),   # 16
                                        np.array(sp.decimate(emg['EMG6'], 4, None, 'fir', -1, True)),   # 17
                                        np.array(sp.decimate(emg['EMG7'], 4, None, 'fir', -1, True)),   # 18
                                        np.array(sp.decimate(emg['EMG8'], 4, None, 'fir', -1, True))    # 19
                                        ]

# delete the first rows in IMU (IMU length = EMG length) and finding the max length
max_length = 0
for feature in range(number_of_features):
    for instance in range(number_of_instances):
        for column in range(0, 12):
            delete = instances[feature][instance][column].__len__() - instances[feature][instance][12].__len__()
            temp = instances[feature][instance][column]
            instances[feature][instance][column] = temp[delete: temp.__len__()]
        if instances[feature][instance][column].__len__() > max_length:
            max_length = instances[feature][instance][column].__len__()

# zero padding
for feature in range(number_of_features):
    for instance in range(number_of_instances):
        for column in range(0, 19):
            if instances[feature][instance][column].__len__() < max_length:
                zeros = max_length - instances[feature][instance][column].__len__()
                for i in range(zeros):
                    instances[feature][instance][column] = np.append(instances[feature][instance][column], ['0.0'])
