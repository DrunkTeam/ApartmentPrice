# import random
# import json
# import requests
# import hydra
# from model import load_features
# import zenml
# from hydra.core.global_hydra import GlobalHydra
# from hydra import compose, initialize

# from data import preprocess_data

# # @hydra.main(config_path="../configs", config_name="main", version_base=None) # type: ignore
# def predict(cfg = None):    
#     cfg = compose(config_name="main")


#     X, y = load_features(name = "features_target", 
#                         version = 1, 
#                         )

#     random.seed(cfg.data.random_state)
#     idx = random.randint(0, y.shape[0] - 1)
#     example = X.iloc[idx,:]
#     example_target = y.iloc[idx]   

#     example = json.dumps(   
#         {"inputs" : example.to_dict()}
#     )

#     response = requests.post(
#         url=f"http://localhost:{5001}/predict",
#         data=example,
#         headers={"Content-Type": "application/json"},
#     )       

#     print(response.json())
#     print("actual price: ", example_target)


# if __name__=="__main__":
#     predict()

import numpy as np
import requests
# import sklearn.metrics
# import torch
# import zenml
import hydra
from model import load_features
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig
from omegaconf import open_dict
# import sklearn
import json

def predict(cfg):
    X_test, y_test = load_features(
        name="features_target",
        version=cfg.example_version,
        # target_col=cfg.datasets.target_col
    )

    inputs = X_test[[0], :]
    # inputs = inputs[:, np.newaxis]
    inputs = inputs.tolist()

    input_data = {
        "inputs": inputs
    }
    y_true = y_test[0]

    response = requests.post(
        url=f"http://localhost:5001/invocations",
        data=json.dumps(input_data),
        headers={"Content-Type": "application/json"},
    )

    print(response)
    print(response.json())
    print("y_true", y_true)

@hydra.main(config_path="../configs", config_name="main", version_base=None)
def main(cfg: DictConfig):
    predict(cfg)

if __name__ == "__main__":
    main()