import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from rdkit import Chem
from rdkit.Chem import AllChem
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator


def smiles_to_fingerprints(smiles,n_bits=2048, radius=2):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    generator = GetMorganGenerator(radius=radius, fpSize=n_bits)
    fp = generator.GetFingerprint(mol)
    arr = np.zeros(n_bits, dtype=int)
    Chem.DataStructs.ConvertToNumpyArray(fp, arr)
    return arr

def train(df: DataFrame):
    # generate fingerprints
    fingerprints = df['smiles'].apply(smiles_to_fingerprints)

    # remove invalid molecules
    fingerprints = fingerprints[fingerprints.notnull()]

    # stack into a 2D array
    X = np.vstack(fingerprints.values)

    # target variable
    y = df.loc[fingerprints.index, 'measured log solubility in mols per litre']

    # train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    model = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)

    # fit
    model.fit(X_train, y_train)



    # evaluate prediction
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mse = mean_absolute_error(y_test, y_pred)

    print("R2:", r2)
    print("Mean Absolute Error:", mse)


    # # is model better than naive baseline
    # if rmse >= baseline_rmse:
    #     print("Bad model")
    # else:
    #     print("Good model")

    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
    plt.xlabel("Actual logS")
    plt.ylabel("Predicted logS")
    plt.title("Predicted vs Actual Solubility")
    plt.show()


