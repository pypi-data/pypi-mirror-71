```
[![PyPi Shield](https://img.shields.io/pypi/v/DataSynthesizer.svg)](https://pypi.python.org/pypi/DataSynthesizer)
[![Travis CI Shield](https://img.shields.io/travis/DataResponsibly/DataSynthesizer.svg?branch=master)](https://travis-ci.com/DataResponsibly/DataSynthesizer)
```

# DataSynthesizer

Generate synthetic data that simulate a given dataset.

### Usage

DataSynthesizer can generate a synthetic dataset from a sensitive one for release to public. It is developed in Python 3 and requires some third-party modules, such as numpy, pandas, and python-dateutil.

Its usage is presented in the following Jupyter Notebooks:

- `./notebooks/DataSynthesizer in random mode.ipynb`
- `./notebooks/DataSynthesizer in independent attribute mode.ipynb`
- `./notebooks/DataSynthesizer in correlated attribute mode.ipynb`

### Assumptions for Input Dataset

1. The input dataset is a table in first normal form (1NF).
2. When implementing differential privacy,  DataSynthesizer injects noises into the statistics within **active domain** that are the values presented in the table.

### Install DataSynthesizer

```bash
pip install DataSynthesizer
```

### Run webUI

DataSynthesizer can be executed by a web-based UI.

```bash
cd DataSynthesizer/webUI/
python manage.py runserver
```

Visit http://127.0.0.1:8000/synthesizer/
