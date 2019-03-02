import myo
from myo.lowlevel import stream_emg
from myo.six import print_
from time import sleep
import pandas as pd
import scipy.signal as sp
import numpy as np
import os
import csv
import send2trash

myo.init()

pose_id = 1
pose_name = ['welcome']

feature_path = 'training_data/' + str(pose_id) + '.csv'

emg_data = []
gyro_data = []
acc_data = []
orien_data = []

# flags to label the headers of CSV files
acc_flag = False
orien_flag = False
gyro_flag = False
emg_flag = False

# headers
acc_header = ['Acc_X', 'Acc_Y', 'Acc_Z']
gyro_header = ['Gyro_X', 'Gyro_Y', 'Gyro_Z']
orien_header = ['Roll', 'Pitch', 'Yaw']
emg_header = ['EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8']


class Listener(myo.DeviceListener):
    """
    Listener implementation. Return False from any function to
    stop the Hub.
    """

    interval = 0.02  # Output only 0.02 seconds

    def __init__(self):
        super(Listener, self).__init__()
        self.orientation = None
        self.gyroscope = None
        self.acceleration = None
        self.emg = None
        self.rssi = None

    def on_connect(self, myo, timestamp):
        print("Hello, Myo!")
        myo.vibrate('short')
        myo.request_rssi()

    def on_disconnect(self, myo, timestamp):
        print("Goodbye, Myo!")

    def on_rssi(self, myo, timestamp, rssi):
        self.rssi = rssi

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        """
        Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub.
        """

    def on_lock(self, myo, timestamp):
        self.locked = True

    def on_unlock(self, myo, timestamp):
        self.locked = False

    def on_pair(self, myo, timestamp):
        myo.set_stream_emg(stream_emg.enabled)
        print_('Paired')

    def on_unpair(self, myo, timestamp):
        """
        Called when a Myo armband is unpaired.
        """

    def on_arm_sync(self, myo, timestamp, arm, x_direction, rotation, warmup_state):
        """
        Called when a Myo armband and an arm is synced.
        """

    def on_arm_unsync(self, myo, timestamp):
        """
        Called when a Myo armband and an arm is unsynced.
        """

    def on_warmup_completed(self, myo, timestamp, warmup_result):
        """
        Called when the warm up completed.
        """

    def on_orientation_data(self, myo, timestamp, orientation):
        save_to_separate_csv('orientation', orientation)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        save_to_separate_csv('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        save_to_separate_csv('gyroscope', gyroscope)

    def on_emg(self, myo, timestamp, emg,):
        save_to_separate_csv('emg', emg)


# saving the sensors readings to a separates CSV files
def save_to_separate_csv(sensor, data):

    global orien_flag, acc_flag, gyro_flag, emg_flag
    # to store the sign's feature
    path = 'training_data/temp'+'/'+sensor+'.csv'
    path_dir = 'training_data/temp'
    # to store the sign's label
    label = 'labels/'+str(pose_id)+'.csv'
    label_dir = 'labels'

    # create the directory if it doesn't exist
    if not os.path.isdir(path_dir):
        os.makedirs(path_dir)
        acc_flag = True
        orien_flag = True
        gyro_flag = True
        emg_flag = True

    if not os.path.isdir(label_dir):
        os.makedirs(label_dir)

    if not os.path.isfile(label):
        with open(label, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(pose_name)
        csvFile.close()

    with open(path, 'a', newline='') as csvFile:

        writer = csv.writer(csvFile)

        if sensor == 'orientation':
            # Calculate Euler angles (roll, pitch, and yaw) from the unit quaternion in radians
            x = data[0]
            y = data[1]
            z = data[2]
            w = data[3]
            # angles calculations
            roll = np.arctan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
            pitch = np.arcsin(max(-1.0, min(1.0, 2.0 * (w * y - z * x))))
            yaw = np.arctan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))

            if orien_flag:
                writer.writerow(orien_header)
                orien_flag = False

            # data vector
            raw_data = [roll, pitch, yaw]
            writer.writerow(raw_data)

        elif sensor == 'acceleration':
            if acc_flag:
                writer.writerow(acc_header)
                acc_flag = False
            writer.writerow(data)

        elif sensor == 'gyroscope':
            if gyro_flag:
                writer.writerow(gyro_header)
                gyro_flag = False
            writer.writerow(data)

        elif sensor == 'emg':
            if emg_flag:
                writer.writerow(emg_header)
                emg_flag = False
            writer.writerow(data)

    csvFile.close()


def to_csv():

    headers = emg_header + orien_header + acc_header + gyro_header

    # add the csv headers if the file is newly created
    if not os.path.isfile(feature_path):
        with open(feature_path, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(headers)
        csvFile.close()

    emg_file = pd.read_csv('training_data/temp/emg.csv')
    orien_file = pd.read_csv('training_data/temp/orientation.csv')
    acc_file = pd.read_csv('training_data/temp/acceleration.csv')
    gyro_file = pd.read_csv('training_data/temp/gyroscope.csv')

    emg1 = emg_downsampling(emg_file[headers[0]])
    emg2 = emg_downsampling(emg_file[headers[1]])
    emg3 = emg_downsampling(emg_file[headers[2]])
    emg4 = emg_downsampling(emg_file[headers[3]])
    emg5 = emg_downsampling(emg_file[headers[4]])
    emg6 = emg_downsampling(emg_file[headers[5]])
    emg7 = emg_downsampling(emg_file[headers[6]])
    emg8 = emg_downsampling(emg_file[headers[7]])

    roll = orien_file[headers[8]]
    pitch = orien_file[headers[9]]
    yaw = orien_file[headers[10]]

    acc_x = acc_file[headers[11]]
    acc_y = acc_file[headers[12]]
    acc_z = acc_file[headers[13]]

    gyr_x = gyro_file[headers[14]]
    gyr_y = gyro_file[headers[15]]
    gyr_z = gyro_file[headers[16]]

    for i in range(0, emg1.__len__()):
        temp_series = pd.Series([float(emg1[i]), float(emg2[i]), float(emg3[i]), float(emg4[i]),
                                 float(emg5[i]), float(emg6[i]), float(emg7[i]), float(emg8[i]),
                                 roll[i], pitch[i], yaw[i],
                                 acc_x[i], acc_y[i], acc_z[i],
                                 gyr_x[i], gyr_y[i], gyr_z[i]])
        pd.DataFrame(temp_series).T.to_csv(feature_path, mode='a',  header=False, index=False)

    # remove the "temp" directory
    send2trash.send2trash('training_data/temp')


# to change the EMG sampling rate from 200Hz to 50Hz
def emg_downsampling(column):
    return sp.decimate(column, 4, None, 'fir', -1, True)


def main():

    timeout = 2
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)
    hub.run(1000, Listener())

    try:
        while hub.running:
            while timeout > 0:
                sleep(1)
                timeout -= 1
                if timeout == 0:
                    hub.stop(True)
    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)

    to_csv()


if __name__ == '__main__':
    main()
