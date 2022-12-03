import yaml
import joblib
import copy
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(config: dict) -> pd.DataFrame:
    raw_data = pd.read_csv(config["data_raw"], index_col=0)
    return raw_data

def new_columns(input_data: pd.DataFrame, config: dict) -> pd.DataFrame:
    input_data.columns = config["new_cols"]
    return input_data

def convert_tanggal(input_data: pd.DataFrame, config: dict) -> pd.DataFrame:
    input_data = input_data.copy()
    # Convert to datetime
    input_data[config["datetime_columns"][0]] = pd.to_datetime(
            input_data[config["datetime_columns"][0]],
            unit = "s")
    return input_data

def check_data(input_data: pd.DataFrame, config: dict):
    input_data = copy.deepcopy(input_data)
    config = copy.deepcopy(config)
    # assert input_data.select_dtypes("datetime").columns.to_list() == \
    #     config["datetime_columns"], "an error occurs in datetime column(s)."
    assert input_data.select_dtypes("int").columns.to_list() == \
        config["int_columns"], "an error occurs in int column(s)."
    assert input_data.select_dtypes("float").columns.to_list() == \
        config["float_columns"], "an error occurs in float column(s)."

def split_data(input_data: pd.DataFrame, config: dict):
    # Split predictor and target
    x = input_data[config["predictors"]].copy()
    y = input_data[config["target"]].copy()

    x_train, x_test, \
    y_train, y_test = train_test_split(
        x, y,
        test_size = config["test_size"],
        random_state = 42,
        stratify = y )

    x_valid, x_test, \
    y_valid, y_test = train_test_split(
        x_test, y_test,
        test_size = config["valid_size"],
        random_state = 42,
        stratify = y_test )

    return x_train, x_valid, x_test, y_train, y_valid, y_test




if __name__ == "__main__":
    # 1. config
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # 2. load data
    raw_data = load_data(config)

    # 3. rubah nama kolom
    raw_data = new_columns(raw_data, config)

    # 4. convert tanggal
    raw_data = convert_tanggal(raw_data, config)

    # 5. check data
    check_data(raw_data, config)

    # 6. Splitdata
    x_train, x_valid, x_test, \
        y_train, y_valid, y_test = split_data(raw_data, config)

    # 7. Simpan Data
    joblib.dump(x_train, config["path_train"][0])
    joblib.dump(y_train, config["path_train"][1])

    joblib.dump(x_valid, config["path_valid"][0])
    joblib.dump(y_valid, config["path_valid"][1])

    joblib.dump(x_test, config["path_test"][0])
    joblib.dump(y_test, config["path_test"][1])

    joblib.dump(raw_data, config["data_final"])