Check that your entry points are running successfully without errors.
mlflow run . -e validate
mlflow run . -e transform
mlflow run . -e extract

```bash
python src/validate.py --model-name decision_tree_regressor --data-version 1 --validate-all
```