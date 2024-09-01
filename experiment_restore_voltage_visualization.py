# 0N ~ 200N ~ 0Nの電圧を測定する (VWC: 50, 70, 90で実施予定)
# voltageとindexの関係を示すのみ(200Nのmax時を合わせる感じで行う)
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

fig, ax1 = plt.subplots(figsize=(18, 8))


def get_resampling_data(data, move_idx):
    if move_idx == 0:
        return data
    else:
        return pd.concat([pd.Series([data.min()] * move_idx), data], ignore_index=True)


def date_name_to_date(file_name):
    date_name = " ".join(file_name.split("-")[0:3])
    date_list = date_name.split()[0:3]
    return "-".join(date_list)

max_idx_list = []
for i, voltage_file_name in enumerate(voltage_list):
    date = date_name_to_date(voltage_file_name)
    voltage = pd.read_csv(f"data/force_voltage/force-voltage-{date}/{voltage_file_name}.csv")
    voltage = voltage.set_index("timestamp").reset_index()
    voltage_voltage = voltage[" voltage"]
    max_idx_list.append(voltage_voltage.idxmax())

max_voltage_idx = max(max_idx_list)

move_idx_list = [] 
for max_idx in max_idx_list:
    move_idx = abs(max_idx - max_voltage_idx)
    move_idx_list.append(move_idx)

for i, (voltage_file_name, move_idx) in enumerate(zip(voltage_list, move_idx_list)):
    date = date_name_to_date(voltage_file_name)
    voltage = pd.read_csv(f"data/force_voltage/force-voltage-{date}/{voltage_file_name}.csv")
    voltage = voltage.set_index("timestamp").reset_index()
    voltage_voltage = voltage[" voltage"]
    voltage_voltage = get_resampling_data(voltage_voltage, move_idx)
    ax1.plot(voltage_voltage.index, voltage_voltage, label=f"Voltage Test {i+1}", alpha=0.6)

ax1.set_xlabel("time")
ax1.set_ylabel("voltage")
ax1.legend(loc='best') 
ax1.title.set_text("Restore Voltage Visualization")
ax1.grid()
plt.show()
