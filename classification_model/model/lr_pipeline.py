from feature_engine.imputation import CategoricalImputer, AddMissingIndicator, MeanMedianImputer
from feature_engine.encoding import RareLabelEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from classification_model import __version__ as _version
from classification_model.features.extract_letter import ExtractLetterTransformer
from classification_model.config.core import init_config, TRAINED_MODEL_DIR
from classification_model.data.data_loader import load_dataset
from classification_model.data.data_validator import validate_data
from typing import Union
import pandas as pd
import os
import joblib


class LRPipeline:

    def __init__(self, pipeline: Pipeline = None, config: Union[dict, str] = None):
        if config is None:
            self.config = init_config()
        else:
            self.config = init_config(parsed_config=config)
        if pipeline is not None:
            self.pipeline = pipeline
        else:
            self.__initialize_pipeline()

    def __initialize_pipeline(self):
        self.pipeline = Pipeline([
            # ===== IMPUTATION =====
            # impute categorical variables with string missing
            ('categorical_imputation', CategoricalImputer(imputation_method='missing',
                                                          variables=self.config.lr_model_config.categorical_variables)),

            # add missing indicator to numerical variables
            ('missing_indicator', AddMissingIndicator(variables=self.config.lr_model_config.numerical_variables)),

            # impute numerical variables with the median
            ('median_imputation', MeanMedianImputer(imputation_method='median',
                                                    variables=self.config.lr_model_config.numerical_variables)),

            # Extract letter from cabin
            ('extract_letter', ExtractLetterTransformer(features=self.config.lr_model_config.cabin)),

            # == CATEGORICAL ENCODING ======
            # remove categories present in less than 5% of the observations (0.05)
            # group them in one category called 'Rare'
            ('rare_label_encoder', RareLabelEncoder(tol=0.05, n_categories=1,
                                                    variables=self.config.lr_model_config.categorical_variables)),

            # encode categorical variables using one hot encoding into k-1 variables
            ('categorical_encoder', OneHotEncoder(drop_last=True,
                                                  variables=self.config.lr_model_config.categorical_variables)),

            # scale
            ('scaler', StandardScaler()),

            # classifier
            ('Logit', LogisticRegression(C=self.config.lr_model_config.C,
                                         random_state=self.config.lr_model_config.random_state)),
        ])
        return self

    def save_pipeline(self, pipeline_name: str = None):
        if pipeline_name is not None:
            if pipeline_name.endswith(".pkl"):
                pipeline_path = os.path.join(TRAINED_MODEL_DIR, pipeline_name)
            else:
                pipeline_path = os.path.join(TRAINED_MODEL_DIR, pipeline_name, ".pkl")
                print(Warning(f"AAlthough given pipeline name doesn't end with '.pkl', "
                              f"pipeline will be saved as pickle format."))
        else:
            pipeline_path = os.path.join(TRAINED_MODEL_DIR, self.config.app_config.pipeline_save_file, _version, ".pkl")
            print(f"Using the default trained pipeline name")

        joblib.dump(self.pipeline, pipeline_path)

    def load_pipeline(self, pipeline_name: str):
        pipeline_path = os.path.join(TRAINED_MODEL_DIR, pipeline_name)
        if os.path.isfile(pipeline_path):
            self.pipeline = joblib.load(pipeline_path)
        else:
            raise FileNotFoundError(f"Trained pipeline is not found on {pipeline_path}")

    @staticmethod
    def delete_pipeline(pipeline_name: str):
        pipeline_path = os.path.join(TRAINED_MODEL_DIR, pipeline_name)
        if os.path.isfile(pipeline_path):
            os.remove(pipeline_path)
        else:
            raise FileNotFoundError(f"Trained pipeline is not found on {pipeline_path}")

    def train(self, is_saved: bool = False, saved_pipeline_name: str = None):
        data = load_dataset()
        X_train, X_test, y_train, y_test = train_test_split(data[self.config.lr_model_config.features],
                                                            data[self.config.lr_model_config.label],
                                                            test_size=self.config.lr_model_config.test_size,
                                                            random_state=self.config.lr_model_config.random_state)

        self.pipeline.fit(X_train, y_train)

        predicted_class = self.pipeline.predict(X_train)
        predicted_proba = self.pipeline.predict_proba(X_train)[:, 1]

        print('TRAINING ROC-AUC: {}'.format(roc_auc_score(y_train, predicted_proba)))
        print('TRAINING ACCURACY: {}'.format(accuracy_score(y_train, predicted_class)))

        if is_saved:
            if saved_pipeline_name is None:
                self.save_pipeline()
            else:
                self.save_pipeline(pipeline_name=saved_pipeline_name)

        return self

    def predict(self, data: Union[pd.DataFrame, dict]) -> dict:
        validated_data, validation_errors = validate_data(input_data=pd.DataFrame(data))
        predictions = None
        if not validation_errors:
            predictions = self.pipeline.predict(X=validated_data[self.config.lr_model_config.features])
        response = {"predictions": predictions, "version": _version, "errors": validation_errors}
        return response
