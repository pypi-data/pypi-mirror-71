# Eurostat

Package is a simple interface for parsing data from Eurostat:

* deaths counts
* population sizes

Download the package with

```bash
pip3 install eurostat_deaths
```

To import and fetch data, simply write

```python
import eurostat_deaths as eurostat
```

Function `deaths()` fetches the deaths, function `populations()` fetches the populations.
Their description is in following sections below.

Package is regularly updated. Upgrade your local version typing

```bash
pip3 install eurostat_deaths --upgrade
```

## Deaths

```python
from datetime import datetime
import eurostat_deaths as eurostat

data = eurostat.deaths(start = datetime(2019,1,1))
```

Parameter `start` sets the start of the data. The end is always `now()`.

You receive per-week data of deaths. Since the total size of the data frame is about 218 MB, call taes more than 15 minutes. The usage of memory is significant.

In the future, module will be reimplemented to use Big Data framework, such as PySpark.

The data are forwarded directly to file by default:
* raw output
* cleaned (.csv)
* pickle file

```python
from datetime import datetime
import eurostat_deaths as eurostat

# does not return, create a file with result
eurostat.deaths(output = True, start = datetime(2019,1,1))
```

Parameter `output = True` causes that the output is collected into a single dataframe and returned.

One additional setting is `chunksize` to set the size of chunk, that is processed at a time. The unit used is thousands of rows.

### Caching

A simple local caching is already embedded in the deaths reading by default.

Cache is operated (disabled) with parameters `cache` (reading from) and `output` (write to)

```python
eurostat.deaths(output = False) # reading enabled, but keeps the old versions
```

The newest result to be written into file is done with

```python
eurostat.deaths(cache = False) # fetch newest result
```

## Population

Populations in years for NUTS-2 and NUTS-3 regions can be fetched such as

```python
import eurostat_deaths as eurostat

data = eurostat.populations()
```

Similarly as in `deaths()` call, `populations()` can be parametrized with `chunksize` (in thousands of lines) and `output`, forwarding the output to file rather than returning and hence saving time allocating a big data frame in main memory.

```python
import eurostat_deaths as eurostat

# does not return, create a file with result
eurostat.populations(output = True)
```

Here the data volume is incomparably lower and hence the regular usage to return the data frame is possible.


## Credits

Author: [Martin Benes](https://www.github.com/martinbenes1996).