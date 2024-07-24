
# src/validate.py

from data import extract_data  # custom module
from transform_data import transform_data  # custom module
from model import retrieve_model_with_alias  # custom module
from utils import init_hydra  # custom module
import giskard
import mlflow

def validate():
    cfg = init_hydra()

    version = cfg.test_data_version

    df, version = extract_data(version=version, cfg=cfg)

    TARGET_COLUMN = cfg.data.target_cols[0]
    CATEGORICAL_COLUMNS = list(cfg.data.cat_cols) + list(cfg.data.bin_cols)
    dataset_name = cfg.data.dataset_name

    giskard_dataset = giskard.Dataset(
        df=df,
        target=TARGET_COLUMN,
        name=dataset_name,
        cat_columns=CATEGORICAL_COLUMNS
    )

    client = mlflow.MlflowClient()

    challenger1 = retrieve_model_with_alias('model_name', 'challenger1')
    challenger2 = retrieve_model_with_alias('model_name', 'challenger2')

    mv1 = client.get_model_version_by_alias(name='model_name', alias='challenger1')
    mv2 = client.get_model_version_by_alias(name='model_name', alias='challenger2')

    model_version1 = mv1.version
    model_version2 = mv2.version

    transformer_version = cfg.data_transformer_version

    def predict_challenger1(raw_df):
        X = transform_data(
            df=raw_df,
            version=version,
            cfg=cfg,
            return_df=False,
            only_transform=True,
            transformer_version=transformer_version,
            only_X=True
        )
        return challenger1.predict(X)

    def predict_challenger2(raw_df):
        X = transform_data(
            df=raw_df,
            version=version,
            cfg=cfg,
            return_df=False,
            only_transform=True,
            transformer_version=transformer_version,
            only_X=True
        )
        return challenger2.predict(X)

    giskard_model1 = giskard.Model(
        model=predict_challenger1,
        model_type="classification",
        classification_labels=list(cfg.data.labels),
        feature_names=df.columns,
        name='challenger1'
    )

    giskard_model2 = giskard.Model(
        model=predict_challenger2,
        model_type="classification",
        classification_labels=list(cfg.data.labels),
        feature_names=df.columns,
        name='challenger2'
    )

    scan_results1 = giskard.scan(giskard_model1, giskard_dataset)
    scan_results_path1 = f"reports/test_suite_challenger1_{model_version1}_{dataset_name}_{version}.html"
    scan_results1.to_html(scan_results_path1)

    scan_results2 = giskard.scan(giskard_model2, giskard_dataset)
    scan_results_path2 = f"reports/test_suite_challenger2_{model_version2}_{dataset_name}_{version}.html"
    scan_results2.to_html(scan_results_path2)

    test_suite1 = giskard.Suite(name=f"test_suite_challenger1_{model_version1}_{dataset_name}_{version}")
    test1 = giskard.testing.test_f1(model=giskard_model1, dataset=giskard_dataset, threshold=cfg.model.f1_threshold)
    test_suite1.add_test(test1)

    test_suite2 = giskard.Suite(name=f"test_suite_challenger2_{model_version2}_{dataset_name}_{version}")
    test2 = giskard.testing.test_f1(model=giskard_model2, dataset=giskard_dataset, threshold=cfg.model.f1_threshold)
    test_suite2.add_test(test2)

    test_results1 = test_suite1.run()
    test_results2 = test_suite2.run()

    if test_results1.passed and test_results1.num_issues < test_results2.num_issues:
        selected_model = 'challenger1'
        selected_model_version = model_version1
    else:
        selected_model = 'challenger2'
        selected_model_version = model_version2

    print(f"Selected model: {selected_model} (version: {selected_model_version})")

if __name__ == "__main__":
    validate()