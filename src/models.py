import torch
from torch import nn
import torch.nn.functional as F
import random
import numpy as np
import pandas as pd
from skorch import NeuralNetRegressor


class SimpleNet(nn.Module):
    def __init__(
            self,
            input_size,
            hidden_layer_1,
            hidden_layer_2,
            hidden_layer_3,
            output_size,
            seed,
    ):
        random.seed(int(seed))
        np.random.seed(int(seed))
        torch.manual_seed(int(seed))
        super(SimpleNet, self).__init__()

        self.hidden1 = nn.Sequential(
            nn.Linear(int(input_size), int(hidden_layer_1)),
            nn.ReLU(),
        )
        self.hidden2 = nn.Sequential(
            nn.Linear(int(hidden_layer_1), int(hidden_layer_2)),
            nn.ReLU(),
        )
        self.hidden3 = nn.Sequential(
            nn.Linear(int(hidden_layer_2), int(hidden_layer_3)),
            nn.ReLU(),
        )
        self.output = nn.Linear(int(hidden_layer_3), int(output_size))

    def forward(self, x):
        x = self.hidden1(x)
        x = self.hidden2(x)
        x = self.hidden3(x)
        x = self.output(x)
        return x


class RegressionNet(nn.Module):
    def __init__(
            self,
            input_size,
            hidden_layer_1,
            hidden_layer_2,
            hidden_layer_3,
            output_size,
            seed):
        super(RegressionNet, self).__init__()
        self._set_seed(int(seed))

        # Define layers
        self.hidden1 = nn.Linear(int(input_size), int(hidden_layer_1))
        self.hidden2 = nn.Linear(int(hidden_layer_1), int(hidden_layer_2))
        self.hidden3 = nn.Linear(int(hidden_layer_2), int(hidden_layer_3))
        self.output = nn.Linear(int(hidden_layer_3), int(output_size))

        # Define dropout and activation functions
        self.dropout = nn.Dropout(p=0.5)
        self.leaky_relu = nn.LeakyReLU(negative_slope=0.01)

    def _set_seed(self, seed):
        seed = int(seed)
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

    def forward(self, x):
        x = self.leaky_relu(self.hidden1(x))
        x = self.dropout(x)
        x = self.leaky_relu(self.hidden2(x))
        x = self.dropout(x)
        x = self.leaky_relu(self.hidden3(x))
        x = self.dropout(x)
        x = self.output(x)
        return x


class WrapperNN(NeuralNetRegressor):
    def __init__(self, *args, **kwargs):
        super(WrapperNN, self).__init__(*args, **kwargs)

    def prepare_data(self, X):
        if isinstance(X, pd.DataFrame):
            return X.values.astype(np.float32)
        return X

    def prepare_target(self, y):
        if isinstance(y, pd.Series):
            return y.values.astype(np.float32).reshape(-1, 1)
        return y

    def fit(self, X, y, **fit_params):
        X = self.prepare_data(X)
        y = self.prepare_target(y)
        return super(WrapperNN, self).fit(X, y, **fit_params)

    def predict(self, X):
        X = self.prepare_data(X)
        return super(WrapperNN, self).predict(X)

    def score(self, X, y):
        X = self.prepare_data(X)
        y = self.prepare_target(y)
        return super(WrapperNN, self).score(X, y)


class RMSELoss(nn.Module):
    def __init__(self):
        super(RMSELoss, self).__init__()

    def forward(self, yhat, y):
        criterion = nn.MSELoss()
        loss = torch.sqrt(criterion(yhat, y) + 1e-6)
        return loss
