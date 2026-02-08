from data.manager import get_data
from training.manager import train_data


data = get_data()
train_data(data)