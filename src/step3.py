import yaml
import joblib

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report


def load_data_feat(config: dict):
    x_train = joblib.load(config["path_train_feat"][0])
    y_train = joblib.load(config["path_train_feat"][1])

    x_valid = joblib.load(config["path_valid_feat"][0])
    y_valid = joblib.load(config["path_valid_feat"][1])

    x_test = joblib.load(config["path_test_feat"][0])
    y_test = joblib.load(config["path_test_feat"][1])

    return x_train, y_train, x_valid, y_valid, x_test, y_test

def train_model(x_train, y_train, x_valid, y_valid):
    dtc = DecisionTreeClassifier()
    dtc.fit(x_train, y_train)

    y_pred = dtc.predict(x_valid)
    print(classification_report(y_valid, y_pred))

    return dtc


if __name__ == "__main__":
    # 1. config
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # 2. Load data feat
    x_train, y_train, x_valid, y_valid, x_test, y_test = load_data_feat(config)

    # 3. Train model
    dtc = train_model(x_train, y_train, x_valid, y_valid)

    # 4. Simpan model
    joblib.dump(dtc, config["final_model_path"])