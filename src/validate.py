# Wrap your raw dataset

from data import extract_data  # custom module
from transform_data import transform_data  # custom module
from model import retrieve_model_with_alias  # custom module
from utils import init_hydra  # custom module
import giskard
import hydra
import mlflow

cfg = init_hydra()

version = cfg.test_data_version

df, version = extract_data(version=version, cfg=cfg)

# Specify categorical columns and target column
TARGET_COLUMN = cfg.data.target_cols[0]

CATEGORICAL_COLUMNS = list(cfg.data.cat_cols) + list(cfg.data.bin_cols)

dataset_name = cfg.data.dataset_name

# Wrap your Pandas DataFrame with giskard.Dataset (validation or test set)
giskard_dataset = giskard.Dataset(
    df=df,  # A pandas.DataFrame containing raw data (before pre-processing) and including ground truth variable.
    target=TARGET_COLUMN,  # Ground truth variable
    name=dataset_name,  # Optional: Give a name to your dataset
    cat_columns=CATEGORICAL_COLUMNS
    # List of categorical columns. Optional, but improves quality of results if available.
)

# Wrap your model
model_name = cfg.model.best_model_name

# You can sweep over challenger aliases using Hydra
model_alias = cfg.model.best_model_alias

model: mlflow.pyfunc.PyFuncModel = retrieve_model_with_alias(model_name, model_alias=model_alias)

client = mlflow.MlflowClient()

mv = client.get_model_version_by_alias(name=model_name, alias=model_alias)
challenger1 = retrieve_model_with_alias('model_name', 'challenger1')
challenger2 = retrieve_model_with_alias('model_name', 'challenger2')

model_version = mv.version

# Define custom predict function

transformer_version = cfg.data_transformer_version


def predict(raw_df):
    X = transform_data(
        df=raw_df,
        version=version,
        cfg=cfg,
        return_df=False,
        only_transform=True,
        transformer_version=transformer_version,
        only_X=True
    )

    return model.predict(X)


predictions = predict(df[df.columns].head())
print(predictions)

# Create Giskard model

# giskard_model = giskard.Model(
#     model=predict,
#     model_type="regression",
#     classification_labels=list(cfg.data.labels),
#     # The order MUST be identical to the prediction_function's output order
#     feature_names=df.columns,  # By default all columns of the passed dataframe
#     name=model_name,  # Optional: give it a name to identify it in metadata
#     # classification_threshold=0.5, # Optional: Default: 0.5
# )

giskard_model1 = giskard.Model(
    model=challenger1,
    model_type="regression",
    classification_labels=list(cfg.data.labels),
    feature_names=df.columns,
    name='challenger1'
)

giskard_model2 = giskard.Model(
    model=challenger2,
    model_type="regression",
    classification_labels=list(cfg.data.labels),
    feature_names=df.columns,
    name='challenger2'
)


# Scan your model

# scan_results = giskard.scan(giskard_model, giskard_dataset)
#
# # Save the results in `html` file
# scan_results_path = f"reports/validation_results_{model_name}_{model_version}_{dataset_name}_{version}.html"
# scan_results.to_html(scan_results_path)
#
# # Create a test suite
# suite_name = f"test_suite_{model_name}_{model_version}_{dataset_name}_{version}"
# test_suite = giskard.Suite(name=suite_name)

# We can also generate a test suite from the scan results
# test_suite = scan_results.generate_test_suite(suite_name)
# We will not do this for simplicity

scan_results1 = giskard.scan(giskard_model1, giskard_dataset)
scan_results_path1 = f"reports/test_suite_{model_name}_1_{dataset_name}_{version}.html"
scan_results1.to_html(scan_results_path1)

scan_results2 = giskard.scan(giskard_model2, giskard_dataset)
scan_results_path2 = f"reports/test_suite_{model_name}_2_{dataset_name}_{version}.html"
scan_results2.to_html(scan_results_path2)


# # Add performance tests
# test1 = giskard.testing.test_f1(model=giskard_model,
#                                 dataset=giskard_dataset,
#                                 threshold=cfg.model.f1_threshold)
#
# test_suite.add_test(test1)

test_suite1 = giskard.Suite(name=f"test_suite_challenger1_{model_version}_{dataset_name}_{version}")
test1 = giskard.testing.test_f1(model=giskard_model1, dataset=giskard_dataset, threshold=0.6)
test_suite1.add_test(test1)

test_suite2 = giskard.Suite(name=f"test_suite_challenger2_{model_version}_{dataset_name}_{version}")
test2 = giskard.testing.test_f1(model=giskard_model2, dataset=giskard_dataset, threshold=0.6)
test_suite2.add_test(test2)


# test
test_results1 = test_suite1.run()
test_results2 = test_suite2.run()

if test_results1.passed and test_results1.num_issues < test_results2.num_issues:
    selected_model = 'challenger1'
else:
    selected_model = 'challenger2'

