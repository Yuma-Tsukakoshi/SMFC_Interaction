import pandas as pd
import numpy as np
import os


def concat_csv(input_path, save_path):
    """
    Concatenate all csv files in a directory into one csv file.
    """
    files = os.listdir(input_path)
    files = [f for f in files if f.endswith('.csv')]
    df = pd.concat([pd.read_csv(os.path.join(input_path, f)) for f in files])
    df.to_csv(save_path, index=False)
    print("Saved concatenated csv file to: {}".format(save_path))

if __name__ == "__main__":
    concat_csv('./data/', './concatenated_data.csv')