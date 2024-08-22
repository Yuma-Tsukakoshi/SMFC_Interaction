import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random, datetime
# Open serial port
ser = serial.Serial('COM7', 38400)
#  ls /dev/tty.*

# Initialize data storage
window_timestamps = []
window_data_values = []

# Initialize data export
save_path = f'{datetime.datetime.now()}-80-500N-54mm-voltage-10k-300N-stable-data.csv'
save_path = save_path.replace(":", "-")
with open(save_path, 'a') as f:
    f.write(f"timestamp, voltage\n")
# Initialize plot
N = 50
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, N)  # x range
ax.set_ylim(50, 170)  # y range
ax.set_xlabel('Time')
ax.set_ylabel('Voltage (mV)')
ax.set_title("Realtime Visualization & Record")

# Update function
def update(frame):
    # Read serial data
    res = str(ser.read(15))[10:15]
    # data = ser.readline().decode('utf-8').strip()
    data = int(res)

    # Adding voltage value to the window list
    window_data_values.append(float(data))
    # Only showing N data points
    window_timestamps = range(0,len(window_data_values))
    # print(timestamps)
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
