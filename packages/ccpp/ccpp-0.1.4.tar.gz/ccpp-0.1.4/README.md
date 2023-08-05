<p align="center">
  <a href="https://github.com/guaifish/ccpp"><img src="https://github.com/guaifish/ccpp/blob/master/img/ccpp-logo.png" alt="ccpp"></a>
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

### Test the package at the first time

```console
$ pytest tests
```

### Building package

```console
$ poetry build

Building hello-world (0.1.0)
 - Building sdist
 - Built hello-world-0.1.0.tar.gz

 - Building wheel
 - Built hello-world-0.1.0-py3-none-any.whl
```

### Publishing package to PyPI

```console
$ poetry publish

Publishing hello-world (0.1.0) to PyPI
Username: guaifish
Password:
 - Uploading hello-world-0.1.0-py3-none-any.whl 0%
 - Uploading hello-world-0.1.0-py3-none-any.whl 65%
 - Uploading hello-world-0.1.0-py3-none-any.whl 100%
 - Uploading hello-world-0.1.0-py3-none-any.whl 100%
 - Uploading hello-world-0.1.0.tar.gz 0%
 - Uploading hello-world-0.1.0.tar.gz 83%
 - Uploading hello-world-0.1.0.tar.gz 100%
 - Uploading hello-world-0.1.0.tar.gz 100%
```

## License

Copyright © 2020 [guaifish](https://github.com/guaifish).
This project is [MIT](https://github.com/guaifish/ccpp/blob/master/LICENSE) license.