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

The data can be forwarded directly to file. Give the function a filename by parameter `output`.

```python
from datetime import datetime
import eurostat_deaths as eurostat

data = eurostat.deaths(output = "file.csv", start = datetime(2019,1,1))
```

Parameter `output = None` causes that the output is collected into a single dataframe and returned.

One additional setting is `chunksize` to set the size of chunk, that is processed at a time. The unit used is thousands of rows.

## Population

**TODO**

## Credits

Author: [Martin Benes](https://www.github.com/martinbenes1996).