# F1 API Wrapper

An API wrapper for Formula 1 racing data based on [Ergast Developer API](https://ergast.com/mrd/)

# Install

`pip install f1-api-wrapper`

# Usage

```python
from f1.schedule import get_current_schedule

schedule = get_current_schedule()

races = schedule.races
```

# Features

* Retrieve current season schedule
