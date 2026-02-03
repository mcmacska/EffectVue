from typing import Optional
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time

from controllers.service_api import predict_next
from data.manager import get_data
from core.scheduler import register_jobs, start_scheduler
from training.manager import train_data


# test
data = get_data()
train_data(data)


app = FastAPI()

# register jobs
register_jobs()

# start the scheduler
start_scheduler()

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

@app.get("/predict")
async def predict(interval: Optional[str] = None):
    return predict_next()

@app.get("/historic_data")
async def get_historic_data():
    return {"id": "asd", "name": "asd"}

# @app.get("/users/{user_id}")
# async def get_user(user_id: str):
#     if user_id != "u_123":
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"id": "u_123", "name": "Ada", "email": "ada@example.com"}


# ---- global error handler example ----
@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
