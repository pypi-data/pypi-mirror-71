# Eurostat

The program `eurostat.py` is a simple interface to parse Eurostat data.

## Executing the modul

Parsing data from Eurostat to a file is as easy as

```bash
python3 eurostat.py --output data.csv --start 2019-01-01 --verbose
```

It downloads the file from Eurostat and parses it according to the input to an output format.

```
sex,age,geo\time,2020W23,2020W22,2020W21, ... ,2019W03,2019W02,2019W01
F,OTAL,AT,,,,                             ... ,852,877,914
F,OTAL,AT1,,,                             ... ,364,361,387
...
```

All parameters of the command can be shown with

```bash
python3 eurostat.py --help
```

```
usage: eurostat.py [-h] [-o OUTPUT] [-n CHUNKSIZE] [-s START] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Directs the output to a name of your choice.
  -n CHUNKSIZE, --chunksize CHUNKSIZE
                        Number of lines in chunk (in thousands).
  -s START, --start START
                        Start date.
  -v, --verbose         Sets verbose log (logging level INFO).
```

## Importing

It can be imported as well. Following code is using the inner function `read_eurostat()` to load the data. The total size of the data frame is about 218 MB, so the call takes more than 15 minutes and the usage of memory is enormous.

The module should not be used like this. Recommended is implementation using Big Data framework, e.g. PySpark.

```python
from datetime import datetime
import eurostat

data = eurostat.read_eurostat(output = None, start = datetime(2019,1,1))
```

Parameter `output = None` causes that the output is collected into a single dataframe and returned.

## Credits

Author: [Martin Benes](https://www.github.com/martinbenes1996).