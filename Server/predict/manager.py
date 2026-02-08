import joblib
import numpy as np
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


def predict(smiles):
    # convert smiles string to morgan fingerprints
    fp = smiles_to_fingerprint(smiles)
    if fp is None:
        raise ValueError("Invalid SMILES string")

    if fp.sum() < 5:
        print("Warning: Molecule may be outside predict domain")

    fp = fp.reshape(1, -1)  # scikit-learn expects 2D

    # load model
    model = joblib.load(MODEL_PATH)

    # predict
    prediction = model.predict(fp)[0]

    print(f"Prediction: {prediction}")
    return prediction