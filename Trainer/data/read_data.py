import pandas as pd
import requests

import os

def read_data(path: str):

    # get the folder where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, path)
    data = pd.read_csv(csv_path)

    # look at the first few rows
    print(data.head())

    return data
