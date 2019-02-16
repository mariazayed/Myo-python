import myo
from myo.lowlevel import stream_emg
from myo.six import print_
from time import sleep
import numpy as np
import csv
import os

myo.init()

record_id = 1
pose_name = 'test'

# flags to label the headers of CSV files
acc_flag = False
orien_flag = False
gyro_flag = False
emg_flag = False


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
        print_("Connected to Myo")
        myo.vibrate('short')
        myo.request_rssi()

    def on_disconnect(self, myo, timestamp):
        """
        Called when a Myo is disconnected.
        """

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
        save_record('orientation', orientation)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        save_record('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        save_record('gyroscope', gyroscope)

    def on_emg(self, myo, timestamp, emg,):
        save_record('emg', emg)


# saving the sensors readings to a CSV files
def save_record(sensor, data):

    global acc_flag, orien_flag, gyro_flag, emg_flag

    path = 'training_data/'+pose_name+'/record'+str(record_id)+'/'+sensor+str(record_id)+'.csv'
    dir = 'training_data/'+pose_name+'/record'+str(record_id)

    # create the directory if it doesn't exist
    if not os.path.isdir(dir):
        os.makedirs(dir)
        acc_flag = True
        orien_flag = True
        gyro_flag = True
        emg_flag = True

    print(sensor, acc_flag, orien_flag, gyro_flag, emg_flag)

    with open(path, 'a', newline='') as csvFile:

        writer = csv.writer(csvFile)

        if sensor == 'orientation':
            # calculate orientation Euler
            x = data[0]
            y = data[1]
            z = data[2]
            w = data[3]
            # angles calculations
            roll = np.arctan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
            pitch = np.arcsin(max(-1.0, min(1.0, 2.0 * (w * y - z * x))))
            yaw = np.arctan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
            # data vector
            raw_data = [roll, pitch, yaw]
            # add the CSV header if the file is created
            if orien_flag:
                writer.writerow(['Roll', 'Pitch', 'Yaw'])
                orien_flag = False
            writer.writerow(raw_data)

        elif sensor == 'acceleration':
            # add the CSV header if the file is created
            if acc_flag:
                writer.writerow(['X', 'Y', 'Z'])
                acc_flag = False
            writer.writerow(data)

        elif sensor == 'gyroscope':
            # add the CSV header if the file is created
            if gyro_flag:
                writer.writerow(['X', 'Y', 'Z'])
                gyro_flag = False
            writer.writerow(data)

        elif sensor == 'emg':
            # add the CSV header if the file is created
            if emg_flag:
                writer.writerow(['EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8'])
                emg_flag = False
            writer.writerow(data)

    csvFile.close()


def main():
    timeout = 1
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

