#!/bin/bash

CONDA_BASE=`conda info --base`
conda env create --name test --file environment.yml
source "${CONDA_BASE}/etc/profile.d/conda.sh"
conda activate test

export PYTHONPATH=.
python3 src/main/main.py
# pytest --junitxml=junit.xml --cov-report xml:cov.xml --cov-report term --cov-branch --cov
conda deactivate
conda remove --yes -n test --all
