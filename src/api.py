from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import numpy as np
import yaml

import data_pipeline as data_pipeline
import preprocessing as preprocessing


config = utils.load_config()
model_data = utils.pickle_load(config["production_model_path"])

class api_data(BaseModel):
    Temperature : float
    Humidity : float
    Pressure : float
    PM1 : float
    TVOC : int
    eCO2 : int
    H2 : int
    Ethanol : int

app = FastAPI()

@app.get("/")
def home():
    return "Hello, FastAPI up!"

@app.post("/predict/")
def predict(data: api_data):    
    # Convert data api to dataframe
    data = pd.DataFrame(data).set_index(0).T.reset_index(drop = True)  # type: ignore
    data.columns = config["predictors"]

    # Convert dtype
    data = pd.concat(
        [
            data[config["predictors"][:4]].astype(np.float64),  # type: ignore
            data[config["predictors"][4:]].astype(np.int64)  # type: ignore
        ],
        axis = 1
    )

    # Check range data
    try:
        data_pipeline.check_data(data, config, True)  # type: ignore
    except AssertionError as ae:
        return {"res": [], "error_msg": str(ae)}

    # Predict data
    y_pred = model_data.predict(data)

    if y_pred[0] == 0:
        y_pred = "Tidak ada api."
    else:
        y_pred = "Ada api."
    return {"res" : y_pred, "error_msg": ""}

if __name__ == "__main__":
    uvicorn.run("api:app", host = "0.0.0.0", port = 8080)