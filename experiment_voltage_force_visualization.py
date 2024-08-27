import os
import datetime
import serial
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

voltage_list = [
    "2024-08-22 15-41-24.219176-80VWC-500N-54mm-voltage-10k-data",
    "2024-08-22 15-45-46.032379-80VWC-500N-54mm-voltage-10k-data",
    "2024-08-22 15-53-56.003033-80VWC-500N-54mm-voltage-10k-data"
]

force_list = [
    "2024-08-22 15-41-24.219176-80-500N-54mm-force-10k-data",
    "2024-08-22 15-45-46.032379-80-500N-54mm-force-10k-data",
    "2024-08-22 15-53-56.003033-80-500N-54mm-force-10k-data",
]

fig, axs = plt.subplots(len(voltage_list), figsize=(18, 8 * len(voltage_list)))

for i, (voltage_file_name, force_file_name) in enumerate(zip(voltage_list, force_list)):
    matches = re.findall(r'-(\d+)N', voltage_file_name)
    if matches:
        number_before_last_N = matches[-1]
        label_name = f"{number_before_last_N}N"

    date_name = " ".join(voltage_file_name.split("-")[0:3])
    date_list = date_name.split()[0:3]
    date = "-".join(date_list)

    voltage = pd.read_csv(f"force_voltage/force-voltage-{date}/{voltage_file_name}.csv")
    voltage = voltage.set_index("timestamp").reset_index()
    voltage_voltage = voltage[" voltage"]
    ax1 = axs[i] 
    ax2 = ax1.twinx() 
    force = pd.read_csv(f"force_logger/force-logger-{date}/{force_file_name}.csv", skiprows=5)
    force = force.set_index("番号").reset_index()
    force_force = force["荷重"]

    max_voltage_idx = voltage_voltage.idxmax()
    max_force_idx = force_force.idxmax()
    if max_voltage_idx >= max_force_idx:
        flag = "voltage"
    elif max_voltage_idx < max_force_idx:
        flag = "force"
    move_idx = abs(max_voltage_idx - max_force_idx)
    max_idx = max(max_voltage_idx, max_force_idx)
    # max_idxの大きい方にデータのindexを増やし、移動させた分は0で埋める　そして、データのindexを再構成してほしい
    if flag == "voltage":
        force_force = pd.concat([pd.Series([force_force.min()] * move_idx), force_force], ignore_index=True)
        force_force = force_force[:len(voltage_voltage)]
    elif flag == "force":
        voltage_voltage = pd.concat([pd.Series([voltage_voltage.min()] * move_idx), voltage_voltage], ignore_index=True)
        voltage_voltage = voltage_voltage[:len(force_force)]

    ax1.plot(voltage_voltage.index, voltage_voltage, label=f"Voltage Test {i+1}", color="blue", alpha=0.6)
    ax2.plot(force_force.index, force_force, label=f"Force Test {i+1}", color="green", alpha=0.6)

    ax1.set_xlabel("time")
    ax1.set_ylabel("voltage", color="blue")
    ax2.set_ylabel("force", color="green")
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.grid()

plt.suptitle("Voltage and Force Stability Test")
plt.show()
