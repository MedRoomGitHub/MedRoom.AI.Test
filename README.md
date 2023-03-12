# Natural Language Processing - Models Similariting Words

[![Documentation](https://img.shields.io/badge/docs-0.0.8-orange.svg?style=flat-square)](https://google.com)
[![Python required version: 3.8](https://img.shields.io/badge/python-3.8-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-370)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Model of a library for Natural Language Processing and Machine Learning applied to Computational Linguistics.

[Inner-Source](https://en.wikipedia.org/wiki/Inner_source) project. Please feel free to fix bugs, add new functionalities and tools. If you do so, please add your name to the list of contributors down below.

## ⚠️ Attention!

This project needed to install docker and docker-compose to run
If there is any update on this lib, the version must be updated on this file :)

Please follow that steps: [docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) to install.

Thanks 😄

## Usage

```shell
$docker-compose --env-file config/local/.env build
$docker-compose --env-file config/local/.env up -d **to up container** # A local jupyter server is now
             # available at localhost:8081
$docker-compose --env-file config/local/.env down **if you want off container**

```

## Install Libraries from Whl

```shell
* In terminal
python3 setup.py bdist_wheel

```

## Black Formatter

[Comand Line Black Option](https://github.com/psf/black#command-line-options)

> Ignore the formatter black in code row or function

```python

# fmt: off
def func(x, b):
    return x * b

```

## Current functionalities:

Natural Language Extractor:

* Cleaner

Natural Language Transformer:

* Word2Vec

Natural Language Model:

* t-SNE

## Main Contributors (until mar/2023- please join us!)

* Eneas Rodrigues de Souza Junior - eneas.rodrigues25@gmail.com
