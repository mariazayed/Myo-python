import myo
from myo.lowlevel import stream_emg
from myo.six import print_
from time import sleep
import numpy as np
import os
import csv

myo.init()

timeout = 4
counter = 9
pose_id = 1
pose_name = ['where']

feature_dir = 'training_data/features/' + str(pose_id) + '/instance_' + str(counter)
label_dir = 'training_data/labels/'
label_path = label_dir + str(pose_id) + '.csv'

# flags to label the headers of CSV files
acc_flag = False
orien_flag = False
gyro_flag = False
emg_flag = False

# headers for CSV files
acc_header = ['Acc_X', 'Acc_Y', 'Acc_Z']
gyro_header = ['Gyro_X', 'Gyro_Y', 'Gyro_Z']
orien_header = ['Roll', 'Pitch', 'Yaw', 'Orien_X', 'Orien_Y', 'Orien_Z']
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
    feature_path = feature_dir + '/' + sensor + '.csv'

    # create the directory if it doesn't exist
    if not os.path.isdir(feature_dir):
        os.makedirs(feature_dir)
        acc_flag = True
        orien_flag = True
        gyro_flag = True
        emg_flag = True

    if not os.path.isdir(label_dir):
        os.makedirs(label_dir)

    if not os.path.isfile(label_path):
        with open(label_path, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(pose_name)
        csvFile.close()

    with open(feature_path, 'a', newline='') as csvFile:

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
            raw_data = [roll, pitch, yaw, data[0], data[1], data[2]]
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
    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)


if __name__ == '__main__':
    main()
