from training.manager import predict

def predict_next(smiles: str) -> dict:
    prediction = predict(smiles)

    if prediction < -4:
        solubility = "Very poor"
    elif prediction < -2:
        solubility = "Poor"
    elif prediction <= 0:
        solubility = "Moderate"
    else:
        solubility = "Very soluble"

    return {"value": prediction, "solubility": solubility}
