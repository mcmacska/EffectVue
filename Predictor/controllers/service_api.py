from fastapi import HTTPException

from training.manager import predict

def predict_log_s(smiles: str) -> dict:
    print(smiles)
    if smiles is None or len(smiles) == 0:
        raise HTTPException(status_code=400, detail="No smiles provided")
    try:
        prediction = predict(smiles)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if prediction < -4:
        solubility = "Very poor"
    elif prediction < -2:
        solubility = "Poor"
    elif prediction <= 0:
        solubility = "Moderate"
    else:
        solubility = "Very soluble"

    return {"value": prediction, "solubility": solubility}
