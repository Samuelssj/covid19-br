import datetime
from functools import lru_cache

from rows.utils.date import date_range

one_day = datetime.timedelta(days=1)


@lru_cache(4096)
def brazilian_epidemiological_week(date):
    """Calculate Brazilian epidemiological weeks
    Information from:
    <https://portalsinan.saude.gov.br/calendario-epidemiologico-2020/43-institucional>

    >>> brazilian_epidemiological_week(datetime.date(2019, 1, 1))
    (2019, 1)
    >>> brazilian_epidemiological_week(datetime.date(2019, 1, 6))
    (2019, 2)
    >>> brazilian_epidemiological_week(datetime.date(2019, 12, 28))
    (2019, 52)
    >>> brazilian_epidemiological_week(datetime.date(2020, 1, 1))
    (2020, 1)
    >>> brazilian_epidemiological_week(datetime.date(2020, 1, 5))
    (2020, 2)
    >>> brazilian_epidemiological_week(datetime.date(2020, 12, 27))
    (2020, 53)
    >>> brazilian_epidemiological_week(datetime.date(2021, 1, 2))
    (2020, 53)
    >>> brazilian_epidemiological_week(datetime.date(2021, 1, 3))
    (2021, 1)
    >>> brazilian_epidemiological_week(datetime.date(2021, 1, 10))
    (2021, 2)
    """
    dates = {
        2012: {"start_date": datetime.date(2012, 1, 1), "end_date": datetime.date(2012, 12, 29),},
        2013: {"start_date": datetime.date(2012, 12, 30), "end_date": datetime.date(2013, 12, 28),},
        2014: {"start_date": datetime.date(2013, 12, 29), "end_date": datetime.date(2015, 1, 3),},
        2015: {"start_date": datetime.date(2015, 1, 4), "end_date": datetime.date(2016, 1, 2),},
        2016: {"start_date": datetime.date(2016, 1, 3), "end_date": datetime.date(2016, 12, 31),},
        2017: {"start_date": datetime.date(2017, 1, 1), "end_date": datetime.date(2017, 12, 30),},
        2018: {"start_date": datetime.date(2017, 12, 31), "end_date": datetime.date(2018, 12, 29),},
        2019: {"start_date": datetime.date(2018, 12, 30), "end_date": datetime.date(2019, 12, 28),},
        2020: {"start_date": datetime.date(2019, 12, 29), "end_date": datetime.date(2021, 1, 2),},
        2021: {"start_date": datetime.date(2021, 1, 3), "end_date": datetime.date(2022, 1, 1),},
        2022: {"start_date": datetime.date(2022, 1, 2), "end_date": datetime.date(2023, 1, 1),},
    }
    year = None
    for possible_year, year_data in dates.items():
        if year_data["start_date"] <= date <= year_data["end_date"]:
            year = possible_year
            break
    if year is None:
        raise ValueError(f"Cannot calculate year for date {date}")

    start_date = dates[year]["start_date"]
    end_date = dates[year]["end_date"]
    week_range = date_range(start_date, end_date + one_day, step="weekly")
    for count, start in enumerate(week_range, start=1):
        end = start + 6 * one_day
        if start <= date <= end:
            return year, count
