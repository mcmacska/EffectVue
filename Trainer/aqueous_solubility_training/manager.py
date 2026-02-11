import joblib
import pandas as pd
import numpy as np
from aqueous_solubility_training.train import train
from rdkit import Chem
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

MODEL_PATH = "aqueous_solubility.joblib"
SMILES_COLUMN_NAME = "SMILES"
LOG_S_COLUMN_NAME = "logS"

def is_valid_molecule(smiles, allowed_elements=None):
    if allowed_elements is None:
        allowed_elements = {'H', 'C', 'O', 'N', 'S', 'F', 'Cl', 'Br'}
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in allowed_elements:
            return False
    return True



def smiles_to_fingerprint(smiles: str, n_bits=2048, radius=2):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    generator = GetMorganGenerator(radius=radius, fpSize=n_bits)
    fp = generator.GetFingerprint(mol)
    arr = np.zeros(n_bits, dtype=int)
    Chem.DataStructs.ConvertToNumpyArray(fp, arr)
    return arr

def train_data(data):
    # convert
    df = pd.DataFrame(data)

    n_total = len(data)
    n_unique = data[SMILES_COLUMN_NAME].nunique()

    print(f"Total molecules: {n_total}")
    print(f"Unique SMILES: {n_unique}")

    # convert smiles string to morgan fingerprints
    fingerprints = df[SMILES_COLUMN_NAME].apply(smiles_to_fingerprint)

    # remove invalid molecules
    fingerprints = fingerprints[fingerprints.notnull()]

    # stack into a 2D array
    X = np.vstack(fingerprints.values)

    # target variable
    y = df.loc[fingerprints.index, LOG_S_COLUMN_NAME]

    # run the aqueous_solubility_training
    model = train(X, y)

    # save the model
    joblib.dump(model, filename=MODEL_PATH)
