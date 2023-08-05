<p align="center">
  <a href="https://github.com/guaifish/ccpp"><img src="./img/ccpp.png" alt="ccpp"></a>
</p>
<p align="center">
    <em>Cookiecutter template for Python package</em>
</p>
<p align="center">
<a href="https://pypi.org/project/ccpp" target="_blank">
    <img src="https://badge.fury.io/py/ccpp.svg" alt="Package version">
</a>
<a href="https://github.com/guaifish/ccpp/blob/master/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/guaifish/ccpp" alt="GitHub LICNESE">
</a>
<a href="https://github.com/guaifish/ccpp/stargazers" target="_blank">
    <img src="https://img.shields.io/github/stars/guaifish/ccpp?logo=github" alt="GitHub Stars">
</a>
<a href="https://github.com/guaifish/ccpp/network/members" target="_blank">
    <img src="https://img.shields.io/github/forks/guaifish/ccpp?logo=github" alt="GitHub Forks">
</a>
</p>

---

## Requirements

* Python 3.6+

* [cookiecutter](https://github.com/cookiecutter/cookiecutter) - template engine
* [poetry](https://github.com/python-poetry/poetry) - dependency management
* [python-fire](https://github.com/google/python-fire) - command line tool

## Installation

```console
$ pip install ccpp
```

## Usage

### Create a new package

```console
$ ccpp new hello-world && cd hello-world
```

### test the package at the first time

```console
$ pytest tests
```

## License

Copyright © 2020 [guaifish](https://github.com/guaifish).
This project is [MIT](https://github.com/guaifish/ccpp/blob/master/LICENSE) license.