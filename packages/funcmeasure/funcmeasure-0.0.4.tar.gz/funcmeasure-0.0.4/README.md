# funcmeasure
![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/funcmeasure?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/funcmeasure)

## Todo
- Clean up code because it's a bit messy

## Description
Measure and compare function execution times

## Install
~~~~bash
pip install funcmeasure
# or
pip3 install funcmeasure
~~~~

## Usage
~~~~python
from funcmeasure import measure, partial, Measurement

def f1():
    5**2

def f2():
    5**2**10

def f3():
    5**2**2**2

measurements = measure([f1, (f2, 'second'), f3], times=1000)

measurements = measure(
    {
        f1: None,
        f2: 'second',
        f3: None
    },
    times=1000
)
~~~~
These will print:
~~~~
Ran 1000 times

-------------------------------------------
| rank |  name  |   duration  | benchmark |
-------------------------------------------
|    1 |     f1 | 0.00000023s |           |
|    2 |     f3 | 0.00000026s |     1.12x |
|    3 | second | 0.00000263s |    11.22x |
-------------------------------------------

Ran 1000 times

-------------------------------------------
| rank |  name  |   duration  | benchmark |
-------------------------------------------
|    1 |     f3 | 0.00000024s |           |
|    2 |     f1 | 0.00000026s |     1.07x |
|    3 | second | 0.00000260s |    10.91x |
-------------------------------------------
~~~~

## Notes
The lib also provides a helper function for partials, so you don't have to import functools