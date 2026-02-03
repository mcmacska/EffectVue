import time
from datetime import timedelta
from data.read_data import read_data
import pandas as pd


def get_data() -> list[dict]:
    start = time.perf_counter()

    # read the data
    data = read_data()


    # # calculate average frequency using timestamps
    # all_diff_ts = sum(
    #     next_["timestamp"] - curr["timestamp"]
    #     for curr, next_ in zip(historic_price_data, historic_price_data[1:])
    # )
    #
    # average_diff_seconds = all_diff_ts / (len(historic_price_data) - 1)
    # average_frequency = timedelta(milliseconds=average_diff_seconds)
    #
    # end = time.perf_counter()
    # print(f"getting data: {end - start:0.5f} seconds")
    #
    # print("Average candle frequency:", average_frequency)
    # print("Size:", len(historic_price_data))
    return data