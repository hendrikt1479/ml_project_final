from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import numpy as np
import yaml
import joblib

# import step1 as data_pipeline
# import step2 as preprocessing
# import step3 as modelling

# load config & model
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)
model_data = joblib.load(config["final_model_path"])

class api_data(BaseModel):
    Temperature : int
    Humidity : int
    Pressure : int
    PM1 : int
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
    # data = pd.DataFrame(data).set_index(0).T.reset_index(drop = True)  # type: ignore
    # data.columns = config["predictors"]

    # # Convert dtype
    # data = pd.concat(
    #     [
    #         data[config["predictors"][:4]].astype(np.float64),  # type: ignore
    #         data[config["predictors"][4:]].astype(np.int64)  # type: ignore
    #     ],
    #     axis = 1
    # )

    # # Check range data
    # try:
    #     data_pipeline.check_data(data, config, True)  # type: ignore
    # except AssertionError as ae:
    #     return {"res": [], "error_msg": str(ae)}

    # # Predict data
    # y_pred = model_data.predict(data)

    # if y_pred[0] == 0:
    #     y_pred = "Tidak ada api."
    # else:
    #     y_pred = "Ada api."

    # return {"res" : y_pred, "error_msg": ""}
    return {"res":9999999999999}

if __name__ == "__main__":
    uvicorn.run("api:app", host = "0.0.0.0", port = 8080)