# Myo-python
The `myo-python` is a Python wrapping for windows myo SDK for Python developers to allow them to interact with Myo armband hardaware easily. Its compatible with Python 2 and 3

# Getting Started
* Download the Myo SDK for windows from [here](https://drive.google.com/open?id=1W9d6LjeIR_TAojWxxZov8X5kI3qDDEh4)
* Add the Myo SDK to your path
    1. Open the installed myo SDK folder
    2. 	Open the "bin" folder and copy the path
    3. 	Go to Control Panel --> System and Security --> System
    4. 	Click on "Advanced system settings" a new window will popped up
    5. 	Click on "Environment Valiables"
    6. 	Double click on the "Path" under the System variables a new window will popped up
    7. 	Click on "New" and paste the copied path
* Run the project<br><br>
The `myo-poses` file detects the 5 built-in gestures (wave in, wave out, fist, finger spread, and double tap) in addition to the "rest" pose
The `myo-sensors` file reads the EMG and IMU sensors
