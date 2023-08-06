<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/v/requests-api-pagination.svg?maxAge=3600)](https://pypi.org/project/requests-api-pagination/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/requests-api-pagination.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/requests-api-pagination.py/)

#### Installation
```bash
$ [sudo] pip install requests-api-pagination
```

#### Examples
```python
import requests_api_pagination

url='https://api.github.com/gists?per_page=100'
headers = {"Authorization": "Bearer %s" % GITHUB_TOKEN}

requests_api_pagination.get(url,headers=headers)
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>