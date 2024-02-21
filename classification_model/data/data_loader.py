from classification_model.data import TITANIC_DATA
from classification_model.config.core import init_config
import pandas as pd
import numpy as np
import re


def get_first_cabin(row):
    try:
        return row.split()[0]
    except AttributeError:
        return np.nan


def get_title(passenger):
    line = passenger
    if re.search("Mrs", line):
        return "Mrs"
    elif re.search("Mr", line):
        return "Mr"
    elif re.search("Miss", line):
        return "Miss"
    elif re.search("Master", line):
        return "Master"
    else:
        return "Other"


def load_dataset(dataframe: pd.DataFrame = None) -> pd.DataFrame:
    if dataframe is None:
        dataframe = pd.read_csv(TITANIC_DATA)
    dataframe.rename(columns={"home.dest": "homedest"}, inplace=True)
    dataframe = dataframe.replace("?", np.nan)
    #
    dataframe["fare"] = dataframe["fare"].astype("float")
    dataframe["age"] = dataframe["age"].astype("float")
    #
    dataframe["cabin"] = dataframe["cabin"].apply(get_first_cabin)
    dataframe["title"] = dataframe["name"].apply(get_title)
    dataframe.drop(labels=init_config().lr_model_config.dropped_features, axis=1, inplace=True)
    return dataframe


if __name__ == "__main__":
    load_dataset()
