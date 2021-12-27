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

def getUKDataFrameBy(columnName = 'newCases'):
    # Extract data for every nation
    # print(df['areaName'].unique())

    # Get the COVID dataframe from UK
    df = api.get_dataframe()

    dfUK = df['date']
    for nation in df['areaName'].unique():
        df1 = df[df['areaName'].str.contains(nation)][['date', columnName]]
        df1 = df1.rename(columns={columnName: columnName + nation})
        dfUK = pd.merge(dfUK, df1, how='outer', on='date')

    return dfUK

if __name__ == "__main__":

    # Get the COVID dataframe from UK
    dfUK = getUKDataFrameBy('newCases')

    print('Script Finished')
