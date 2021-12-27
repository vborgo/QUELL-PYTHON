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
    # England
    dfEngland = df[df['areaName'].str.contains('England')][['date','newCases']]
    dfEngland = dfEngland.rename(columns={"newCases": "newCasesEngland"})
    # Northern Ireland
    dfNorthernIreland = df[df['areaName'].str.contains('Northern Ireland')][['date','newCases']]
    dfNorthernIreland = dfNorthernIreland.rename(columns={"newCases": "newCasesNorthernIreland"})
    # Wales
    dfWales = df[df['areaName'].str.contains('Wales')][['date','newCases']]
    dfWales = dfWales.rename(columns={"newCases": "DeathsWales"})
    # Scotland
    dfScotland = df[df['areaName'].str.contains('Scotland')][['date','newCases']]
    dfScotland = dfScotland.rename(columns={"newCases": "newCasesScotland"})

    # Create dataframe for merging data and for summing latter
    dfUK = pd.merge(dfEngland, dfNorthernIreland, how='outer', on='date')
    dfUK = pd.merge(dfUK, dfWales, how='outer', on='date')
    dfUK = pd.merge(dfUK, dfScotland, how='outer', on='date')

    print('Script Finished')