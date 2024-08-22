import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

# Get data from serial port
serial_port = '/dev/cu.usbmodem144101'
baud_rate = 9600
ser = serial.Serial(serial_port, baudrate=baud_rate, timeout=5)
# Data container initialization
timestamps = []
data_values = []

# Random data for testing
data = [[300,1],[0, 0]]

# Initialize a figure
fig, ax = plt.subplots()

# Heatmap object initialization
heatmap = ax.imshow(data, cmap='viridis')

# Color bar
plt.colorbar(heatmap)

# Update
def update(frame): 
    data = str(ser.readline().decode('utf-8').strip())
    data_list = np.array([float(i) for i in data.split(',')])
    print(data_list)
    data_list = np.array([[data_list[3], data_list[2]], [data_list[1], data_list[0]]])
    # new_data = np.random.rand(3, 1)  # 生成新的随机数据
    # print(new_data)
    # print(np.array(data_list))
    heatmap.set_array(data_list)
    return heatmap,

# Add animation
ani = animation.FuncAnimation(fig, update, frames=range(50), interval=100)

# Display animation
plt.show()
