# PyTime Converter

[![codecov](https://codecov.io/gh/massicer/PyTime-Converter/branch/master/graph/badge.svg)](https://codecov.io/gh/massicer/PyTime-Converter)
[![Build Status](https://travis-ci.org/massicer/PyTime-Converter.svg?branch=master)](https://travis-ci.org/massicer/PyTime-Converter)


Easily manage different `time interval values` and convert them to `milliseconds`.

## How To use

### Available time formats
| Unit Measure       | Allowed Sigles | default |
| ------------- |:-----:| :-----:|
| `milliseconds`  | `ms` , `milliseconds`, `sec`| `X`
| `seconds`  | `seconds` , `s`, `sec`|
| `minutes`  | `min` , `minute`, `minutes`|
| `hours`  | `h` , `hours`, `hrs`, `hour`|
| `days`  | `d` , `days`, `day`|
| `years`  | `y` , `years`, `yrs`, `year`|



- Simply using the `get_milliseconds_value_for_input` with the string value to convert. The below example use the number value `90` and the sigle `s`. 

```python
from pytime_converter.service.convert_service import get_milliseconds_value_for_input

job_time =  '90 seconds' 

assert 90000 == get_milliseconds_value_for_input(job_time)
```

- When the time measure unit is missing the default value is `milliseconds`

```python
from pytime_converter.service.convert_service import get_milliseconds_value_for_input

assert 90 == get_milliseconds_value_for_input('90')

# Using seconds
assert 9000 == get_milliseconds_value_for_input('9 seconds')
assert 9000 == get_milliseconds_value_for_input('9 s')
assert 9000 == get_milliseconds_value_for_input('9 sec')
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- [Poetry >=0.12](https://python-poetry.org)
- Python ^3.5
- Virtualenvwrapper or other virtualenv environment
- make utility


### Installing

- Install it with pypi
    ```
    pip install pytime-converter
    ```

- Or Clone/download the repository

    ```
    git clone https://github.com/massicer/Env-Time-Converter.git
    ```

    Install project package
    ```
    make install
    ```

    or without the make utility
    ```
    poetry install
    ```
## Running the tests

Clone the rempo and simply type 
```
make test
```


## Authors

* **[Massimiliano Ceriani](massimilianoceriani08@gmail.com)** - *Initial work* - [PYTime Converter](https://github.com/massicer/PyTime-Converter)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

