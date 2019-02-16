import myo
from myo.lowlevel import stream_emg
from myo.six import print_
from time import sleep, time
import numpy as np
import csv

myo.init()


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
        myo.set_stream_emg(1)
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

    def on_emg(self, myo, timestamp, emg):
        save_record('emg', emg)


def save_record(sensor, data):
    record_id = 1
    path = 'training_data/pose1/record'+str(record_id)+'/'+sensor+str(record_id)+'.csv'
    with open(path, 'a') as csvFile:
        writer = csv.writer(csvFile)
        if sensor == 'orientation':
            # calculate orientation Euler
            x = data[0]
            y = data[1]
            z = data[2]
            w = data[3]

            roll = np.arctan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
            pitch = np.arcsin(max(-1.0, min(1.0, 2.0 * (w * y - z * x))))
            yaw = np.arctan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))

            raw_data = [roll, pitch, yaw]
            writer.writerow(raw_data)
        elif sensor == 'acceleration':
            print('acceleration')
            writer.writerow(data)
        elif sensor == 'gyroscope':
            print('gyroscope')
            writer.writerow(data)
        elif sensor == 'emg':
            print('emg')
            writer.writerow(data)
    csvFile.close()


def main():
    # timeOut = 2
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)
    hub.run(1000, Listener())
    # while timeOut > 0:
    #     sleep(1)
    #     timeOut -= 1
    #     print('************************** ' + str(timeOut) + '\n')
    # if timeOut == 0:
    #     hub.stop(True)

    # try:
    #     while hub.running:
    #         myo.time.sleep(10)
    # except KeyboardInterrupt:
    #     print_("Quitting ...")
    #     hub.stop(True)


if __name__ == '__main__':
    main()

