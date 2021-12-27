import pandas as pd
from uk_covid19 import Cov19API

all_nations = [
    "areaType=nation"
]

cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCases": "newCasesByPublishDate",
    "cumCases": "cumCasesByPublishDate",
    "newDeaths": "newDeaths28DaysByDeathDate",
    "cumDeaths": "cumDeaths28DaysByDeathDate"
}

api = Cov19API(
    filters=all_nations,
    structure=cases_and_deaths
)


if __name__ == "__main__":

    # Get the COVID dataframe from UK
    df = api.get_dataframe()

    # Extract data for every nation
    # print(df['areaName'].unique())
    dfEngland = df[df['areaName'].str.contains('England')]
    dfNorthernIreland = df[df['areaName'].str.contains('NorthernIreland')]
    dfWales = df[df['areaName'].str.contains('Wales')]
    dfScotland = df[df['areaName'].str.contains('Scotland')]

