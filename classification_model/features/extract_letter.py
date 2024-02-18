import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ExtractLetterTransformer(BaseEstimator, TransformerMixin):
    # Extract fist letter of variable

    def __init__(self, features):
        if not isinstance(features, list):
            raise ValueError('Features should be a list')

        self.features = features

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.features:
            X[feature] = [value[0] if isinstance(value, str) else np.nan for value in X[feature]]
        return X
