from typing import Optional
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time

from controllers.service_api import predict_log_s


app = FastAPI()

# # register jobs
# register_jobs()
#
# # start the scheduler
# start_scheduler()

# ---- "middleware" (like app.use) ----
@app.middleware("http")
async def logger(request: Request, call_next):
    start = time.time()
    resp: Response = await call_next(request)
    ms = (time.time() - start) * 1000
    print(f"{request.method} {request.url.path} -> {resp.status_code} ({ms:.1f}ms)")
    return resp

# ---- types / validation (kinda like TS interfaces) ----
class CreateUserBody(BaseModel):
    name: str
    email: str


# ---- routes (like app.get/app.post) ----
@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/predict_aqueous_solubility/")
async def predict_aqueous_solubility(smiles: str):
    return predict_log_s(smiles)



# ---- global error handler example ----
@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
