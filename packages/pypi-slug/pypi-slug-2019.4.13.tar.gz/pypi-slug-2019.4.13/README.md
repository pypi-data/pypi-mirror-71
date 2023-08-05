<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/v/pypi-slug.svg?maxAge=3600)](https://pypi.org/project/pypi-slug/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/pypi-slug.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/pypi-slug.py/)

#### Installation
```bash
$ [sudo] pip install pypi-slug
```

#### Examples
```python
>>> import pypi_slug
>>> pypi_slug.getslug('0-._.-._.-._.-._.-._.-._.-0')
'0-0'
>>> pypi_slug.getslug('00SMALINUX')
'00smalinux'
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>