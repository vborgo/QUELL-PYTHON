import pandas as pd
from uk_covid19 import Cov19API
import matplotlib.pyplot as plt
import os
import seaborn as sns

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

    #Start the classification in columns
    dfUK = pd.DataFrame(df['date'])
    #dfUK[columnName + 'UK'] = 0
    for nation in df['areaName'].unique():

        df1 = df[df['areaName'].str.contains(nation)][['date', columnName]]
        nation = nation.replace(' ', '')
        df1 = df1.rename(columns={columnName: columnName + nation})

        #Merge the nation dataframe into the main one
        dfUK = dfUK.merge(df1, on=['date'], how='outer')

    dfUK = dfUK.drop_duplicates(subset = 'date').reset_index(drop=True) #This duplicates rows when merge still need to be understood, drop_duplicates used to correct it
    dfUK[columnName + 'UK'] = dfUK.iloc[:, -4:].sum(axis=1)

    return dfUK.iloc[::-1].reset_index(drop=True)

if __name__ == "__main__":

    # Get the COVID dataframe from UK
    dfUKNewCases = getUKDataFrameBy('newCases')
    dfUKNewDeaths = getUKDataFrameBy('newDeaths')

    # Make the relation deaths over covid cases (to check how agressive it is)
    dfDeathsOverCases = dfUKNewDeaths[['date', 'newDeathsUK']].merge(dfUKNewCases[['date', 'newCasesUK']], on=['date'], how='outer')
    dfDeathsOverCases['newDeathsOvernewCases'] = dfDeathsOverCases[['newDeathsUK']].div(dfDeathsOverCases['newCasesUK'], axis=0)

    # Apply moving average to visualize the tendency
    movingAverageDays = 3
    dfUKNewCases['newCasesUKMovAvrg' + str(movingAverageDays)] = dfUKNewCases['newCasesUK'].rolling(movingAverageDays).mean()
    dfUKNewDeaths['newDeathsUKMovAvrg' + str(movingAverageDays)] = dfUKNewDeaths['newDeathsUK'].rolling(movingAverageDays).mean()
    dfDeathsOverCases['newDeathsOvernewCasesMovAvrg'+ str(movingAverageDays)] = dfDeathsOverCases['newDeathsOvernewCases'].rolling(movingAverageDays).mean()

    # Export data in csv file
    if(os.path.isdir('csv') == False):
        os.mkdir("csv")
    dfUKNewCases.to_csv('csv/UKCovidNewCases.csv', index=False) #The best would be to add a timestamp to no overwrite older files
    dfUKNewDeaths.to_csv('csv/UKCovidNewDeaths.csv.csv', index=False)
    dfDeathsOverCases.to_csv('csv/UKCovidNewDeathsOverNewCases.csv', index=False)

    # Plot
    sns.lineplot(data=dfUKNewCases['newCasesUKMovAvrg' + str(movingAverageDays)])
    #sns.lineplot(data=dfDeathsOverCases['newDeathsOvernewCases'])
    if (os.path.isdir('plot') == False):
        os.mkdir("plot")
    plt.savefig('plot/Graph.png')

    print('Script Finished')
