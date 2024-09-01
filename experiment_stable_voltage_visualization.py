import os
import datetime
import serial
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

file_list = ["2024-08-22 15-58-58.952731-80-500N-54mm-voltage-10k-10N-stable-data",
             "2024-08-22 16-03-17.100018-80-500N-54mm-voltage-10k-20N-stable-data",
             "2024-08-22 16-07-22.271746-80-500N-54mm-voltage-10k-50N-stable-data",
             "2024-08-22 16-10-53.662121-80-500N-54mm-voltage-10k-100N-stable-data",
             "2024-08-22 16-14-23.155523-80-500N-54mm-voltage-10k-200N-stable-data",
             "2024-08-22 16-17-28.036107-80-500N-54mm-voltage-10k-250N-stable-data",
             "2024-08-22 16-21-39.266465-80-500N-54mm-voltage-10k-300N-stable-data",
]


fig, ax1 = plt.subplots(figsize=(18, 6))  

for file_name in file_list:
    matches = re.findall(r'-(\d+)N', file_name)
    if matches:
        number_before_last_N = matches[-1]
        label_name = f"{number_before_last_N}N"

    date_name = " ".join(file_name.split("-")[0:3])
    date_list = date_name.split()[0:3]
    date = "-".join(date_list)

    voltage = pd.read_csv(f"data/force_voltage/force-voltage-{date}/{file_name}.csv")
    voltage = voltage.set_index("timestamp").reset_index()
    voltage_voltage = voltage[" voltage"]
    voltage_max = voltage_voltage.max()
    voltage_voltage = voltage_voltage[voltage_max:]
    voltage = voltage[voltage_max:].set_index("timestamp").reset_index()
    ax1.plot(voltage.index, voltage_voltage, label=label_name, alpha=0.7)

ax1.set_xlabel("time")
ax1.set_ylabel("voltage")
ax1.legend(loc='best') 
ax1.title.set_text("Voltage Stability Test")
ax1.grid()
plt.show()

