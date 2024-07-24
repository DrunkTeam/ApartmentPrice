import os
import shutil
import argparse
import mlflow
import pandas as pd
from model import load_features
from hydra import compose, initialize

def evaluate(model_name, data_version, model_alias = "champion") -> None:
    X, y = load_features(name="features_target", version=data_version)

    model_uri = f"models:/{model_name}@{model_alias}"
    loaded_model = mlflow.sklearn.load_model(model_uri=model_uri)

    experiment_name = model_name + "_eval" 

    try:
        # Create a new MLflow Experiment
        experiment_id = mlflow.create_experiment(name=experiment_name)
    except mlflow.exceptions.MlflowException as e:
        experiment_id = mlflow.get_experiment_by_name(name=experiment_name).experiment_id  # type: ignore

    with mlflow.start_run(run_name=f"{model_name}_{model_alias}_{data_version}_eval", experiment_id=experiment_id) as run:
        mlflow.set_tag("model_name", model_name)
        mlflow.set_tag("model_alias", model_alias)
        mlflow.set_tag("data_version", data_version)

        # Log parameters
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("model_alias", model_alias)
        mlflow.log_param("data_version", data_version)
        mlflow.log_param("model_uri", model_uri)

        predictions = loaded_model.predict(X)

        eval_data = pd.DataFrame(y)
        eval_data.columns = ["label"]
        eval_data["predictions"] = predictions

        eval_data.to_csv("eval_data.csv", index=False)
        mlflow.log_artifact("eval_data.csv")
        os.remove("eval_data.csv")
        mlflow.sklearn.save_model(loaded_model, "model")
        mlflow.log_artifact("model")
        shutil.rmtree("model")

        results = mlflow.evaluate(
            data=eval_data,
            model_type="regressor",  # Correct model type for regression
            targets="label",
            predictions="predictions",
            evaluators=["default"],
        )
        mlflow.log_metrics(results.metrics)


def main():
    with initialize(config_path="../configs",version_base=None):
        parser = argparse.ArgumentParser()
        parser.add_argument("--model-name", type=str, default="decision_tree_regressor", help="Model name (decision_tree_regressor//gradient_boosting_regressor)")
        parser.add_argument("--model-alias", type=str, default="champion", help="Model alias (champion or challenger<i>)")
        parser.add_argument("--data-version", type=str, default="1", help="Dataset version")
        args = parser.parse_args()
        evaluate(args.model_name, args.data_version, args.model_alias)


if __name__ == "__main__":
    main()


# import argparse
# from collections import defaultdict
# import os
# import shutil

# import mlflow
# import numpy as np
# import pandas as pd
# import sklearn
# import hydra
# from omegaconf import DictConfig
# from model import load_features
# from hydra import compose, initialize

# def evaluate_model(model, X_test, y_test, metrics_fns):
#     predictions = model.predict(X_test)
#     metrics = {}
#     for metric_name, metric_fn in metrics_fns.items():
#         metrics[metric_name] = metric_fn(y_test, predictions)
    
#     return metrics

# def evaluate(cfg, data_version, model_name, model_alias = "champion") -> None:
#     model_uri = f"models:/{model_name}@{model_alias}"
#     model = mlflow.sklearn.load_model(model_uri=model_uri)

#     experiment_name = model_name + "_eval"
#     print(f"Evaluating model {model_name}@{model_alias} on data sample {data_version}")

#     X_test, y_test = load_features(name="features_target", version=data_version, target_col=cfg.datasets.target_col)

#     metrics_fns = {
#         "MAE": sklearn.metrics.mean_absolute_error,
#         "MSE": sklearn.metrics.mean_squared_error,
#         "RMSE": lambda y_true, y_pred: np.sqrt(sklearn.metrics.mean_squared_error(y_true, y_pred)),
#     }

#     test_metrics = evaluate_model(model, X_test, y_test, metrics_fns)
    
#     for metric_name, value in test_metrics.items():
#         print(f'{metric_name}: {value:.5f}')
    
#     experiment_name = model_name + "_evaluate" 

#     try:
#         # Create a new MLflow Experiment
#         experiment_id = mlflow.create_experiment(name=experiment_name)
#     except mlflow.exceptions.MlflowException as e:
#         experiment_id = mlflow.get_experiment_by_name(name=experiment_name).experiment_id  # type: ignore

#     with mlflow.start_run(run_name=f"{model_name}_{model_alias}_{data_version}_evaluate", 
#                           experiment_id=experiment_id) as run:
#         mlflow.set_tag("model_name", model_name)
#         mlflow.set_tag("model_alias", model_alias)
#         mlflow.set_tag("data_version", data_version)

#         mlflow.log_param("model_name", model_name)
#         mlflow.log_param("model_alias", model_alias)
#         mlflow.log_param("data_version", data_version)

#         for metric_name, value in test_metrics.items():
#             mlflow.log_metric(metric_name, value)

# def main():
#     with initialize(config_path="../configs", job_name="evaluate", version_base=None):
#         cfg = compose(config_name="main")
#         parser = argparse.ArgumentParser()
#         parser.add_argument("--model-name", type=str, default="decision_tree_regressor", help="Model name (decision_tree_regressor//gradient_boosting_regressor)")
#         parser.add_argument("--model-alias", type=str, default="champion", help="Model alias (champion or challenger<i>)")
#         parser.add_argument("--data-version", type=str, default="1", help="Dataset version")
#         args = parser.parse_args()
#         evaluate(cfg, args.data_version, args.model_name, args.model_alias)


# if __name__ == "__main__":
#     main()