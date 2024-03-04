import os
import warnings

from pandas.errors import SettingWithCopyWarning

warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

import numpy as np
import pandas as pd

from catboost import CatBoostRegressor, metrics
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split, GridSearchCV

from person_info import PersonInfo
from product_info import ProductInfo


class RegressorSettings:
    def __init__(self, iterations: int, learning_rate: float, depth: int):
        self.iterations = iterations
        self.learning_rate = learning_rate
        self.depth = depth


class RegressorTuner:
    def __init__(self, model: CatBoostRegressor, X_train: pd.DataFrame, y_train: np.ndarray, cat_features: list):
        self.params = {
            "iterations": [100, 200, 300, 400],
            "learning_rate": [0.1, 0.3, 0.6, 1],
            "depth": [6, 7, 8, 9]
        }

        self.grid_search = GridSearchCV(model, param_grid=self.params, cv=5)
        self.grid_search.fit(X_train, y_train, cat_features=cat_features)

    def get_settings(self) -> RegressorSettings:
        iterations = self.grid_search.best_params_["iterations"]
        learning_rate = self.grid_search.best_params_["learning_rate"]
        depth = self.grid_search.best_params_["depth"]
        return RegressorSettings(iterations, learning_rate, depth)


class Regressor:
    def __init__(self, data: pd.DataFrame):
        self.model = CatBoostRegressor(iterations=10000,
                                       depth=8,
                                       loss_function=metrics.MAPE(),
                                       random_state=408,
                                       learning_rate=0.1)
        self.target_column = "daily_dose"
        self.X = data.loc[:, data.columns != self.target_column]
        self.X.drop(self.X.columns[1], axis=1, inplace=True)
        self.Y = data.loc[:, self.target_column]
        self.cat_features = [1, 4, 5]

        self.model_path = "../data/model/model.cbm"
        self.tuned_model_path = "../data/model/model_tuned.cbm"

    def tune_parameters(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=408)
        regressor_tuner = RegressorTuner(self.model, X_train, y_train, self.cat_features)

        settings = regressor_tuner.get_settings()
        self.model = CatBoostRegressor(iterations=settings.iterations,
                                       depth=settings.depth,
                                       loss_function=metrics.MAPE(),
                                       random_state=408,
                                       learning_rate=settings.learning_rate)

    def train(self, tune_parameters: bool):
        if tune_parameters:
            self.tune_parameters()
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=408)
        self.model.fit(X_train, y_train,
                       cat_features=self.cat_features,
                       eval_set=(X_test, y_test),
                       logging_level="Verbose")

        y_predicted = self.model.predict(X_test)
        r2 = r2_score(y_test, y_predicted)
        print(f'r2 = {r2}')
        self.save_model(self.model_path)

    def prepare_model(self, tune_parameters: bool = False):
        if os.path.exists(self.model_path):
            self.load_model(self.model_path, tune_parameters)
        else:
            self.train(tune_parameters)

    def load_model(self, path, tune_parameters: bool = False):
        if tune_parameters:
            self.model.load_model(self.tuned_model_path)
        else:
            self.model.load_model(path)

    def save_model(self, path: str):
        self.model.save_model(path)

    def predict(self, person_info: PersonInfo, product_info: ProductInfo):
        request = [person_info.age,
                   person_info.gender,
                   person_info.height,
                   person_info.weight,
                   person_info.activity_level,
                   person_info.goal,

                   product_info.protein,
                   product_info.fats,
                   product_info.carbo]

        calories = product_info.protein * 4 + product_info.fats * 9 + product_info.carbo * 4
        result = "{:.2f}".format(self.model.predict(request, verbose=True) / calories * 100)
        print(f"Рекомендуемое количество продукта: {result} грамм")
