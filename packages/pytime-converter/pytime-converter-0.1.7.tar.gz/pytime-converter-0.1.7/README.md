![codecov](https://codecov.io/gh/massicer/Env-Time-Converter/branch/master/graph/badge.svg)
[![Build Status](https://travis-ci.org/massicer/PyTime-Converter.svg?branch=master)](https://travis-ci.org/massicer/PyTime-Converter)

# PyTime Converter

Easily manage different `time interval values` and convert them to `milliseconds`.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- [Poetry >=0.12](https://python-poetry.org)
- Python ^3.5
- Virtualenvwrapper or other virtualenv environment
- make utility

### Installing

Clone or download the repository

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

Simply type
```
make test
```
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
 
    ```
    from pytime_converter.service.convert_service import get_milliseconds_value_for_input
    
    # Assume this ENV is set by your .yaml or other configuration file.
    job_time =  '90 seconds' 

    assert 9000 == get_milliseconds_value_for_input(job_time)
    ```

- When the time measure unit is missing the default value is `milliseconds`

    ```
    from pytime_converter.service.convert_service import get_milliseconds_value_for_input
    
    assert 90 == get_milliseconds_value_for_input('90')
    ```


## Authors

* **[Massimiliano Ceriani](massimilianoceriani08@gmail.com)** - *Initial work* - [ENV Time Converter](https://github.com/massicer/Env-Time-Converter)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

