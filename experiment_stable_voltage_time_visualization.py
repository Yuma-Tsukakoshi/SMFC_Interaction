INITIAL_VOLTAGE = 35

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

fig, ax1 = plt.subplots(figsize=(18, 8))

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

    force = pd.read_csv(f"force_logger/force-logger-{date}/{force_file_name}.csv", skiprows=5)
    force = force.set_index("番号").reset_index()
    force_force = force["荷重"]

    force_return_zero_idx = force_force[(force_force == 0) & (force_force.index > force_force.idxmax())].idxmin()
    voltage_initial_idx = voltage_voltage[voltage_voltage == INITIAL_VOLTAGE].idxmin()
    voltage_initial_time = force_return_zero_idx-voltage_initial_idx

    ax1.bar(i, voltage_initial_time, label=label_name, alpha=0.6)
    ax1.text(i, voltage_initial_time, f"{voltage_initial_time} [s]", ha='center', va='bottom')

ax1.set_xlabel("Test Case")
ax1.set_ylabel("Time to Return to Initial Voltage [s]")
ax1.legend(title="Force")
plt.suptitle("Voltage and Force Stability Test")
plt.show()
