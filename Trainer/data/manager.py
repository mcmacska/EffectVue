import time
from datetime import timedelta
from data.read_data import read_data
import pandas as pd

dataset_path = "delaney-processed.csv"

def get_data() -> list[dict]:
    # read the data
    data = read_data(dataset_path)

    return data