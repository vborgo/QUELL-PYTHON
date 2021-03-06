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

    dfUK = dfUK.drop_duplicates(subset='date').reset_index(drop=True) #This duplicates rows when merge still need to be understood, drop_duplicates used to correct it
    dfUK[columnName + 'UK'] = dfUK.iloc[:, -4:].sum(axis=1)

    # Make it a time series
    dfUK.index = pd.DatetimeIndex(dfUK['date'])

    return dfUK.sort_index()

def savePlot(df, columnName, show = True):
    plt.clf()
    sns.lineplot(y=columnName, x=df.index, data=df)
    plt.gcf().autofmt_xdate()
    if (os.path.isdir('plot') == False):
        os.mkdir("plot")
    plt.savefig('plot/' + columnName + '.png', dpi=1200)
    if show == True:
        plt.show()

if __name__ == "__main__":

    # Get the COVID dataframe from UK
    print('Getting UK data...')
    dfUKNewCases = getUKDataFrameBy('newCases').last("6M")
    dfUKNewDeaths = getUKDataFrameBy('newDeaths').last("6M")

    # Make the relation deaths over covid cases (to check how agressive it is)
    dfDeathsOverCases = dfUKNewDeaths[['newDeathsUK']].merge(dfUKNewCases[['newCasesUK']], on=['date'], how='outer')
    dfDeathsOverCases['newDeathsOvernewCases'] = dfDeathsOverCases[['newDeathsUK']].div(dfDeathsOverCases['newCasesUK'], axis=0)

    # Apply moving average to visualize the tendency
    movingAverageDays = 3
    dfUKNewCases['newCasesUKMovAvrg' + str(movingAverageDays)] = dfUKNewCases['newCasesUK'].rolling(movingAverageDays).mean()
    dfUKNewDeaths['newDeathsUKMovAvrg' + str(movingAverageDays)] = dfUKNewDeaths['newDeathsUK'].rolling(movingAverageDays).mean()
    dfDeathsOverCases['newDeathsOvernewCasesMovAvrg'+ str(movingAverageDays)] = dfDeathsOverCases['newDeathsOvernewCases'].rolling(movingAverageDays).mean()

    # Export data in csv file
    print('Exporting csvs into /csv folder...')
    if(os.path.isdir('csv') == False):
        os.mkdir("csv")
    dfUKNewCases.to_csv('csv/UKCovidNewCases.csv') #The best would be to add a timestamp to no overwrite older files
    dfUKNewDeaths.to_csv('csv/UKCovidNewDeaths.csv.csv')
    dfDeathsOverCases.to_csv('csv/UKCovidNewDeathsOverNewCases.csv')

    # Plot
    print('Ploting graphs and saving into /plot folder...')
    #Plot the number of cases and save
    savePlot(dfUKNewCases, 'newCasesUKMovAvrg' + str(movingAverageDays))
    # Plot the number of deaths over cases and save in png
    savePlot(dfDeathsOverCases, 'newDeathsOvernewCasesMovAvrg' + str(movingAverageDays))

    print('Script Finished')
