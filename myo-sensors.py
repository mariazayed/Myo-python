import myo
from myo.lowlevel import stream_emg
from myo.six import print_
from time import sleep
import numpy as np
import pandas as pd
import scipy.signal as sp
import send2trash
import os
import csv

myo.init()

timeout = 4
file_id = 0
pose_id = 0
pose_name = ['where']

training_dir = 'training_data/'

# to store the data temporary
temp_dir = 'training_data/temp/'
emg_file = temp_dir + 'emg.csv'
orien_file = temp_dir + 'orientation.csv'
acc_file = temp_dir + 'acceleration.csv'
gyro_file = temp_dir + 'gyroscope.csv'

# for storing sensor's data
feature_dir = 'training_data/features/'
feature_path = feature_dir + str(file_id) + '.csv'

# for saving the label corresponding to each feature data file
label_dir = 'training_data/labels/'
label_path = label_dir + str(file_id) + '.csv'


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
        save_data_to_temp('orientation', orientation)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        save_data_to_temp('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        save_data_to_temp('gyroscope', gyroscope)

    def on_emg(self, myo, timestamp, emg,):
        save_data_to_temp('emg', emg)


# saving the sensors readings to a separates CSV files
def save_data_to_temp(sensor, data):

    # create the directory if it doesn't exist
    if not os.path.isdir(temp_dir):
        os.makedirs(temp_dir)

    if not os.path.isdir(training_dir):
        os.makedirs(training_dir)

    if not os.path.isdir(feature_dir):
        os.makedirs(feature_dir)

    if not os.path.isdir(label_dir):
        os.makedirs(label_dir)

    if sensor == 'orientation':
        with open(orien_file, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            # Calculate Euler angles (roll, pitch, and yaw) from the unit quaternion in radians
            x = data[0]
            y = data[1]
            z = data[2]
            w = data[3]
            # angles calculations
            roll = np.arctan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
            pitch = np.arcsin(max(-1.0, min(1.0, 2.0 * (w * y - z * x))))
            yaw = np.arctan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
            # data vector
            orien_data = [roll, pitch, yaw]
            writer.writerow(orien_data)
        csvFile.close()

    if sensor == 'acceleration':
        with open(acc_file, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(data)
        csvFile.close()

    if sensor == 'gyroscope':
        with open(gyro_file, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(data)
        csvFile.close()

    if sensor == 'emg':
        with open(emg_file, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(data)
        csvFile.close()


def to_csv():
    emg_data = pd.read_csv(emg_file)
    orien_data = pd.read_csv(orien_file)
    acc_data = pd.read_csv(acc_file)
    gyro_data = pd.read_csv(gyro_file)

    # saving each EMG column in separate variable
    # all the EMG data columns has the same length
    emg1 = down_sampling(emg_data[emg_data.columns[0]])
    emg2 = down_sampling(emg_data[emg_data.columns[1]])
    emg3 = down_sampling(emg_data[emg_data.columns[2]])
    emg4 = down_sampling(emg_data[emg_data.columns[3]])
    emg5 = down_sampling(emg_data[emg_data.columns[4]])
    emg6 = down_sampling(emg_data[emg_data.columns[5]])
    emg7 = down_sampling(emg_data[emg_data.columns[6]])
    emg8 = down_sampling(emg_data[emg_data.columns[7]])

    # saving each orientation column in separate variable
    # all the orientation data has the same length
    roll = orien_data[orien_data.columns[0]]
    pitch = orien_data[orien_data.columns[1]]
    yaw = orien_data[orien_data.columns[2]]

    # saving each acceleration column in separate variable
    # all the acceleration data has the same length
    acc_x = acc_data[acc_data.columns[0]]
    acc_y = acc_data[acc_data.columns[1]]
    acc_z = acc_data[acc_data.columns[2]]

    # saving each gyroscope column in separate variable
    # all the gyroscope data has the same length
    gyr_x = gyro_data[gyro_data.columns[0]]
    gyr_y = gyro_data[gyro_data.columns[1]]
    gyr_z = gyro_data[gyro_data.columns[2]]

    max_len = max(emg1.__len__(), roll.__len__(), acc_x.__len__(), gyr_x.__len__())
    min_len = min(emg1.__len__(), roll.__len__(), acc_x.__len__(), gyr_x.__len__())

    # unification of length
    if emg1.__len__() == max_len:
        emg1 = emg1[max_len - min_len: max_len].reset_index(drop=True)
        emg2 = emg2[max_len - min_len: max_len].reset_index(drop=True)
        emg3 = emg3[max_len - min_len: max_len].reset_index(drop=True)
        emg4 = emg4[max_len - min_len: max_len].reset_index(drop=True)
        emg5 = emg5[max_len - min_len: max_len].reset_index(drop=True)
        emg6 = emg6[max_len - min_len: max_len].reset_index(drop=True)
        emg7 = emg7[max_len - min_len: max_len].reset_index(drop=True)
        emg8 = emg8[max_len - min_len: max_len].reset_index(drop=True)

    if roll.__len__() == max_len:
        roll = roll[max_len - min_len: max_len].reset_index(drop=True)
        pitch = pitch[max_len - min_len: max_len].reset_index(drop=True)
        yaw = yaw[max_len - min_len: max_len].reset_index(drop=True)

    if acc_x.__len__() == max_len:
        acc_x = acc_x[max_len - min_len: max_len].reset_index(drop=True)
        acc_y = acc_y[max_len - min_len: max_len].reset_index(drop=True)
        acc_z = acc_z[max_len - min_len: max_len].reset_index(drop=True)

    if gyr_x.__len__() == max_len:
        gyr_x = gyr_x[max_len - min_len: max_len].reset_index(drop=True)
        gyr_y = gyr_y[max_len - min_len: max_len].reset_index(drop=True)
        gyr_z = gyr_z[max_len - min_len: max_len].reset_index(drop=True)

    # collecting ALL the data to one csv file
    for i in range(0, min_len):
        temp_series = pd.Series([float(emg1[i]), float(emg2[i]), float(emg3[i]), float(emg4[i]),
                                 float(emg5[i]), float(emg6[i]), float(emg7[i]), float(emg8[i]),
                                 roll[i], pitch[i], yaw[i],
                                 acc_x[i], acc_y[i], acc_z[i],
                                 gyr_x[i], gyr_y[i], gyr_z[i]])
        pd.DataFrame(temp_series).T.to_csv(feature_path, mode='a',  header=False, index=False)

    # add the corresponding label to this feature file
    with open(label_path, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(str(pose_id))
        csvFile.close()

    # remove the "temp" directory
    send2trash.send2trash(temp_dir)


def down_sampling(signal):
    return sp.decimate(signal, 4, None, 'fir', -1, True)


def main():

    global timeout

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
                    to_csv()
    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)


if __name__ == '__main__':
    main()
