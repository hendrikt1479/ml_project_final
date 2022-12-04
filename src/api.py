from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import numpy as np
import yaml
import joblib

# load config & model
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)
model_data = joblib.load(config["final_model_path"])

class api_data(BaseModel):
    temperature : float
    humidity : float
    tvoc : int
    eco2 : int
    raw_h2 : int
    raw_ethanol : int
    pressure : float
    pm10 : float

app = FastAPI()

@app.get("/")
def home():
    return "Hello, FastAPI up! ... berhasilll"

@app.post("/predict/")
def predict(data: api_data):    
    # Convert data api to dataframe
    data = pd.DataFrame(data).set_index(0).T.reset_index(drop = True)  # type: ignore
    data.columns = config["predictors"]

    # Predict data
    y_pred = model_data.predict(data)

    return str(y_pred)

if __name__ == "__main__":
    uvicorn.run("api:app", host = "0.0.0.0", port = 8080)