#!/bin/bash

array=(77 78 79 80 81)

for sample in ${array[*]}
do
    mlflow run . --env-manager local -e predict -P example_version=$sample -P port=5001 -P random_state=15
done