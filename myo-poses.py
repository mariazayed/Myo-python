import myo
from myo.lowlevel import pose_t
from myo.six import print_
import random

myo.init()

"""
There can be a lot of output from certain data like acceleration and orientation.
This parameter controls the percent of times that data is shown.
"""
SHOW_OUTPUT_CHANCE = 0.01

class Listener(myo.DeviceListener):
    # return False from any method to stop the Hub

    def on_connect(self, myo, timestamp):
        print_("Connected to Myo")
        myo.vibrate('short')
        myo.request_rssi()

    # RSSI, is a Received Signal Strength Indicator
    def on_rssi(self, myo, timestamp, rssi):
        print_("RSSI: ", rssi)

    def on_event(self, event):
        """ Called before any of the event callbacks. """

    def on_event_finished(self, event):
        """ Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        print_('Paired')

    def on_disconnect(self, myo, timestamp):
        print_('on_disconnect')

    def on_pose(self, myo, timestamp, pose):
        if pose == pose_t.double_tap:
            print("Double tap")
        elif pose == pose_t.fingers_spread:
            print("Finger spread")
        elif pose == pose_t.fist:
            print("Fist")
        elif pose == pose_t.wave_in:
            print("Wave in")
        elif pose == pose_t.wave_out:
            print("Wave out")
        elif pose == pose_t.rest:
            print("Rest")
        else:
            print("None")


def show_output(message, data):
    if random.random() < SHOW_OUTPUT_CHANCE:
        print_(message + ':' + str(data))

def main():
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)
    hub.run(1000, Listener())

    # Listen to keyboard interrupts and stop the
    # hub in that case.
    try:
        while hub.running:
            myo.time.sleep(0.2)
    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)

if __name__ == '__main__':
    main()

