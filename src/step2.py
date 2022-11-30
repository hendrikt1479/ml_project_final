import yaml
import joblib
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

def load_data(config_data: dict):
    x_train = joblib.load(config_data["path_train"][0])
    y_train = joblib.load(config_data["path_train"][1])

    x_valid = joblib.load(config_data["path_valid"][0])
    y_valid = joblib.load(config_data["path_valid"][1])

    x_test = joblib.load(config_data["path_test"][0])
    y_test = joblib.load(config_data["path_test"][1])

    train = pd.concat([x_train, y_train], axis = 1)
    valid = pd.concat([x_valid, y_valid], axis = 1)
    test = pd.concat([x_test, y_test], axis = 1)

    return train, valid, test

def remove_outliers(train):
    train = train.copy()
    train_remoutl = pd.DataFrame()

    for col_name in train.columns[:-1]:
        q1 = train[col_name].quantile(0.25)
        q3 = train[col_name].quantile(0.75)
        iqr = q3 - q1
        bt_atas = q3 + (1.5*iqr)
        bt_bawah = q1 - (1.5*iqr)
        train_remoutl_col = train[(train[col_name]>=bt_bawah) & (train[col_name]<=bt_atas)].copy()
        train_remoutl = pd.concat([train_remoutl, train_remoutl_col], axis=0)
    index_count = train_remoutl.index.value_counts()
    ss = index_count[index_count == (train.shape[1]-1)].index
    train_remoutl = train_remoutl.loc[ss].drop_duplicates()
    
    return train_remoutl

def balancing_data(train_remoutl, config):
    sm = SMOTE(random_state = 112)
    x_train_remoutl_sm, y_train_remoutl_sm = sm.fit_resample(train_remoutl.drop(config["target"], axis = 1), train_remoutl[config["target"]])
    train_remoutl_sm = pd.concat([x_train_remoutl_sm, y_train_remoutl_sm], axis = 1)

    return train_remoutl_sm



if __name__ == "__main__":
    # 1. config
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # 2. Load data
    train, valid, test = load_data(config)
    
    # 3. Remove outliers
    train_remoutl = remove_outliers(train)

    # 4. SMOTE
    train_remoutl_sm = balancing_data(train_remoutl, config)

    # 5. Simpan Data
    joblib.dump(train_remoutl_sm[config["predictors"]], config["path_train_feat"][0])
    joblib.dump(train_remoutl_sm[config["target"]], config["path_train_feat"][1])
    
    joblib.dump(test[config["predictors"]], config["path_test_feat"][0])
    joblib.dump(test[config["target"]], config["path_test_feat"][1])
    
    joblib.dump(valid[config["predictors"]], config["path_valid_feat"][0])
    joblib.dump(valid[config["target"]], config["path_valid_feat"][1])