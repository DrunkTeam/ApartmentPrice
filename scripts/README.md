## Installing dependencies

To install environments and requirements, use the following script:
```bash
conda create -n mlops python=3.11.9 
conda activate mlops
pip install poetry==1.8.1
poetry install

poetry run ... write command (example, python src/data.py)
```

To automate taking data and validation you can use test_data.sh
```bash
./scripts/test_data.sh <path_to_csv> <tag_name> <branch of git>
```
