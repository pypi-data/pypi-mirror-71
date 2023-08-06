# Porfolio Finder

[![PyPI version fury.io](https://badge.fury.io/py/portfoliofinder.svg)](https://pypi.python.org/pypi/portfoliofinder/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/portfoliofinder.svg)](https://pypi.python.org/pypi/portfoliofinder/)
[![Build Status](https://travis-ci.org/asteffey/portfolio-finder.svg?branch=master)](https://travis-ci.org/asteffey/portfolio-finder)
[![Documentation Status](https://readthedocs.org/projects/portfolio-finder/badge/?version=latest)](https://portfolio-finder.readthedocs.io/en/latest/?badge=latest)

A Python library, based primarily around [pandas](https://pandas.pydata.org/docs/index.html), 
to identify an optimal portfolio allocation through back-testing.

[API Documentation](https://portfolio-finder.readthedocs.io/en/latest/) is available on Read the Docs.

## Example Usage

Each of these examples make use of [data.csv](https://github.com/asteffey/portfolio-finder/blob/master/data.csv) which provides returns for a 
handful of funds over 1970-2019.

### Find best portfolio allocation to minimize the required timeframe to achieve a target value
```python
from portfoliofinder import Allocations

Allocations(0.05, ['USA_TSM', 'WLDx_TSM', 'USA_INT', 'EM'])\
    .filter('USA_TSM>=0.6 & WLDx_TSM<=0.2 & USA_INT>=0.3')\
    .with_returns("data.csv")\
    .with_regular_contributions(100000, 10000)\
    .get_backtested_timeframes(target_value=1000000)\
    .get_statistics(['min', 'max', 'mean', 'std'])\
    .filter_by_min_of('max')\
    .filter_by_max_of('min')\
    .get_allocation_which_min_statistic('std')
```

**Output**
```text
Statistic
min     14.000000
max     22.000000
mean    16.965517
std      2.809204
Name: Allocation(USA_TSM=0.65, WLDx_TSM=0.0, USA_INT=0.3, EM=0.05), dtype: float64
```

### Find best portfolio allocation to maximize value with minimal risk over a fixed timeframe
```python
from portfoliofinder import Allocations

Allocations(0.05, ['USA_TSM', 'WLDx_TSM', 'USA_INT', 'EM'])\
    .filter('USA_TSM>=0.6 & WLDx_TSM<=0.2 & USA_INT>=0.3')\
    .with_returns("data.csv")\
    .with_regular_contributions(100000, 10000)\
    .get_backtested_values(timeframe=10)\
    .get_statistics(['mean', 'std'])\
    .filter_by_gte_percentile_of(90, 'mean')\
    .get_allocation_which_min_statistic('std')
```

**Output**
```text
Statistic
mean    446560.590088
std     117448.007302
Name: Allocation(USA_TSM=0.6, WLDx_TSM=0.0, USA_INT=0.3, EM=0.1), dtype: float64
```

### Graph statistics from multiple portfolio allocations to visualize their efficient frontier

```python
from portfoliofinder import Allocations

Allocations(0.05, ['USA_TSM', 'WLDx_TSM', 'USA_INT', 'EM'])\
    .filter('USA_TSM>=0.2 & USA_INT>=0.2')\
    .with_returns("data.csv")\
    .with_regular_contributions(100000, 10000)\
    .get_backtested_values(timeframe=10)\
    .get_statistics()\
    .graph('std', 'mean')
```

**Output**

![efficient_frontier](https://user-images.githubusercontent.com/23619800/84746213-a4484e00-af83-11ea-9ee6-da2d6330a4b9.png)

