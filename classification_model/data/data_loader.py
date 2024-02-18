from classification_model.data import TITANIC_DATA
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


def load_dataset() -> pd.DataFrame:
    dataframe = pd.read_csv(TITANIC_DATA)
    assert isinstance(dataframe, pd.DataFrame)
    dataframe = dataframe.replace("?", np.nan)
    #
    dataframe["fare"] = dataframe["fare"].astype("float")
    dataframe["age"] = dataframe["age"].astype("float")
    #
    dataframe["cabin"] = dataframe["cabin"].apply(get_first_cabin)
    dataframe["title"] = dataframe["name"].apply(get_title)
    dataframe.drop(labels=["name", "ticket", "boat", "body", "home.dest"], axis=1, inplace=True)
    return dataframe


if __name__ == "__main__":
    load_dataset()
