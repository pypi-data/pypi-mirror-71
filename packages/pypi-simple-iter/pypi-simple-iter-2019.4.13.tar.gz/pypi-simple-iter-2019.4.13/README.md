<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/v/pypi-simple-iter.svg?maxAge=3600)](https://pypi.org/project/pypi-simple-iter/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/pypi-simple-iter.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/pypi-simple-iter.py/)

#### Installation
```bash
$ [sudo] pip install pypi-simple-iter
```

#### Examples
```python
import pypi_simple_iter

for slug, name in pypi_simple_iter.iter_projects():
    print(slug,name)
```

iterate from file:
```python
import pypi_simple_iter
import requests

r = requests.get('https://pypi.org/simple/')
open('/tmp/simple.txt','w').write(r.text)
for slug, name in pypi_simple_iter.iter_projects_from_file('/tmp/simple.txt'):
    print(slug,name)
```

```
0 0
0-0 0-._.-._.-._.-._.-._.-._.-0
00000a 00000a
0-0-1 0.0.1
007 007
00print-lol 00print_lol
00smalinux 00SMALINUX
...
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>