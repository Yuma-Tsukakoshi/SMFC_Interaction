import os
import datetime
import serial
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

file_list = ["2024-08-22 14-40-18.227579-80-500N-94mm-voltage-10k-data",
            #  "2024-08-22 14-44-47.262451-80-500N-94mm-voltage-10k-data",
            #  "2024-08-22 15-35-48.530461-80-500N-94mm-voltage-10k-data",
            #  "2024-08-22 15-41-24.219176-80-500N-54mm-voltage-10k-data",
            #  "2024-08-22 15-45-46.032379-80-500N-54mm-voltage-10k-data",
            #  "2024-08-22 15-53-56.003033-80-500N-54mm-voltage-10k-data",
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

    voltage = pd.read_csv(f"force_voltage/force-voltage-{date}/{file_name}.csv")
    voltage = voltage.set_index("timestamp").reset_index()
    voltage_voltage = voltage[" voltage"]
    ax1.plot(voltage.index, voltage_voltage, label=label_name, alpha=0.7)


ax1.set_xlabel("time")
ax1.set_ylabel("voltage")
ax1.legend(loc='best') 
ax1.title.set_text("Voltage Stability Test")
ax1.grid()
plt.show()


