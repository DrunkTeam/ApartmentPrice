import mlflow

# mlflow.set_tracking_uri(uri="http://localhost:5000")

# MLFLOW_TRACKING_URI  environment variable

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# Load the Iris dataset
X, y = datasets.load_iris(return_X_y=True)


# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=0.2, random_state=42
)

# Define the model hyperparameters
params = {
  "solver": "lbfgs",
  "penalty": "l2",
  "random_state": 8888,
}

# Train the model
lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

# Predict on the test set
y_pred = lr.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="macro")
recall = recall_score(y_test, y_pred, average="macro")
f1 = f1_score(y_test, y_pred, average="macro")

print(accuracy, precision, recall, f1)

import mlflow
from mlflow.models import infer_signature
import mlflow.sklearn
import mlflow.exceptions

# Set our tracking server uri for logging
# mlflow.set_tracking_uri(uri = "http://localhost:5000")

experiment_name = "MLflow-experiment-01"

try:
    # Create a new MLflow Experiment
    experiment_id = mlflow.create_experiment(name=experiment_name)
except mlflow.exceptions.MlflowException as e:
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

print(experiment_id)


# Start an MLflow run
with mlflow.start_run(run_name="run-01", experiment_id=experiment_id) as run:

    # Log the hyperparameters
    mlflow.log_params(params=params)

    # Log the performance metrics
    mlflow.log_metric("accuracy", accuracy) # type: ignore
    mlflow.log_metric("f1", f1) # type: ignore
    mlflow.log_metrics({
        "accuracy": accuracy,
        "f1": f1
    })

    # Set a tag that we can use to remind ourselves what this run was for
    mlflow.set_tag("Training Info", "Basic LR model for my data")

    # Infer the model signature
    signature = infer_signature(X_test, y_test)


    # Log the model
    model_info = mlflow.sklearn.log_model(
        sk_model=lr,
        artifact_path="LR_model",
        signature=signature,
        input_example=X_test,
        registered_model_name="first_model"
    )

import pandas as pd

# Load the model back for predictions as a generic Python Function model flavor
loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)

# Run predictions
predictions = loaded_model.predict(X_test)

iris_feature_names = datasets.load_iris().feature_names

# Compare some prediction results
result = pd.DataFrame(X_test, columns=iris_feature_names)
result["actual_class"] = y_test
result["predicted_class"] = predictions

result[:4]