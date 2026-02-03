import pandas as pd
import numpy as np
from training.train import train

def train_data(data):
    df = pd.DataFrame(data)

    n_total = len(data)
    n_unique = data['smiles'].nunique()

    print(f"Total molecules: {n_total}")
    print(f"Unique SMILES: {n_unique}")

    # run the training
    train(df)