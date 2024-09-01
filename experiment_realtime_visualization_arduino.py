import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random, datetime
import os
import time

# make directory
make_dir_path = f"data/interaction/{datetime.datetime.now().strftime('%Y-%m-%d')}"

# detect target directory
if os.path.isdir(make_dir_path):
    pass
else:
    os.makedirs(make_dir_path)

# Open serial port
ser = serial.Serial('COM6', 9600)  
time.sleep(2)
#  ls /dev/tty.*

# Initialize data storage
window_timestamps = []
window_data_values = []

# Initialize data export

save_file_name = f'{datetime.datetime.now()}-height-80mm-action-press-time-test.csv'
save_file_name = save_file_name.replace(":", "-")
save_path = f"{make_dir_path}/{save_file_name}"
with open(save_path, 'a') as f:
    f.write(f"timestamp, voltage\n")
# Initialize plot
N = 50
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, N)  # x range
ax.set_ylim(0, 500)  # y range
ax.set_xlabel('Time')
ax.set_ylabel('Voltage (mV)')
ax.set_title("Realtime Visualization & Record")

def update(frame):
    # Read serial data
    line_data = ser.readline().decode().strip()  # Read and decode serial data
    data, _, _= map(float, line_data.split(','))  # Extract data

    # Adding voltage value to the window list
    window_data_values.append(float(data))

    # Only showing N data points
    window_timestamps = range(0, len(window_data_values))
    
    if len(window_timestamps) > N:
        window_data_values.pop(0)
        window_timestamps = range(0, N)
    
    # Plot data update
    line.set_data(window_timestamps, window_data_values)

    # Export data update
    with open(save_path, 'a') as f:
        f.write(f"{datetime.datetime.now()}, {data}\n")

    # Terminal output
    print(f"Voltage: {data} mV")

    return line,


# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=5)

# Show the plot
plt.show()
