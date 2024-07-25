Check that your entry points are running successfully without errors.
mlflow run . -e validate
mlflow run . -e transform
mlflow run . -e extract

```bash
python src/validate.py --model-name gradient_boosting_regressor --data-version 1 --validate-all
```