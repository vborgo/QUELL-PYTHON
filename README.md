# QUELL-PYTHON
Python: Using an API of your choice get the last 6 months of daily Covid infection numbers in the UK. Import data and add to an appropriate format, save it to your choice of file, and plot this data and a rolling average of 3 points. What can you predict about the trends for the next month?

2021-01-03:
From december to january, it is hard to predict watching the big picture of 6 months, considering the spread rate of the new Omicron variation and the 3-5 incubation days. But considering the few last days of the year, I would predict that the covid cases might spike for a few days in the beginning of the year, then start to decrease after the second half of the month and reaching a stability of daily cases, that I would assume It will be become the average number looking back again for the incubation days.

The number of cases, to be fair, are not so important at all, if the severity is mild. One good corelation to understand it, would be inbetween number of new deaths and new positive cases. For Omicron variation, while the number of new cases might scare, the number of new deaths brings a relief, with the smallest amount in proportion to cases in the history of this new disease. Of course, to bring to the game the number of people in hospital beds, ICUs and mechanical ventilation would improve the accuracy of the judgement, but with this one relation it is a good start to undersatand about how much to worry about it.

---------------------------------------

- Execute **_BUILD_WITH_DEPENDANCIES.bat** to create **_QUELL.exe** 

---------------------------------------

The execution will create two folders:
1. csv: Where the Dataframes are exported in csv format;
2. plot: Where the graphs ploted are exported;

--------------------------------------

**EXECUTION**

A plot with 3 days of moving average on the last 6 months of daily COVID-19 in UK will be saved on /plot folder.
Extra, there is a plot showing the moving average (3 days) of the number of daily deaths over number of daily  cases, to verify how intense the disease is.
