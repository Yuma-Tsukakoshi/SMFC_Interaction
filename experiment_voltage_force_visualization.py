import os
import datetime
import serial
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 前提: 各々データの名前を識別できるようにする 保存名はforce_loggerとforce_voltageで同じ名前とする

file_name = ""
# 2024-12-31-50VWC-45mm-10k-50N-stable-grasp-test
date_name = file_name.split("-")[0]

# force_logger ディレクトリからinputで取得した名前のcsvファイルを探索してforceとtimestampを取得する
force = pd.read_csv(f"force_logger/force-logger-{date_name}/{file_name}.csv")
force_timestamp = force["No."]
force_force = force["Force"]

# force_voltage ディレクトリからinputで取得した名前のcsvファイルを探索してvoltageとtimestampを取得する
voltage = pd.read_csv(f"force_voltage/foce-voltage-{date_name}/{file_name}.csv")
voltage_timestamp = voltage["timestamp"]
voltage_voltage = voltage["voltage"]

# それぞれのデータを結合してグラフを描画する 2軸グラフで左軸にforce, 右軸にvoltageを表示する　x軸はtimestampとする
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(force_timestamp, force_force, color="green")
ax2.plot(voltage_timestamp, voltage_voltage, color="blue")
ax1.set_xlabel("timestamp")
ax1.set_ylabel("force", color="blue")
ax2.set_ylabel("voltage", color="red")
plt.show()

# グラフの描画後imgディレクトリを作成してその中に日付のディレクトリを作成してその中にグラフの画像を保存する　保存名はcsvファイルと同じ名前とする
os.makedirs("img", exist_ok=True)
os.makedirs(f"img/{datetime.datetime.now().strftime('%Y-%m-%d')}", exist_ok=True)
plt.savefig(f"img/{datetime.datetime.now().strftime('%Y-%m-%d')}/{file_name}.png")
