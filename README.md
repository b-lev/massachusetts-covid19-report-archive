# massachusetts-covid19-report-archive

A csv file and archive of daily reports from the Massachusetts state government. The reports are released on this web page: https://www.mass.gov/info-details/covid-19-cases-quarantine-and-monitoring

See also: https://b-lev.github.io/covid19-vis/

They keep adding columns, and so the csv does too. My apologies if it breaks your code.

In R, using tidyverse and lubridate packages, you can read in the data directly:

```
ma.gov<- read_csv('https://raw.githubusercontent.com/b-lev/massachusetts-covid19-report-archive/master/MA-stats.csv') %>% 
  mutate(date=mdy(date))
```
You can select the columns that are relevant by listing them with select(), or using a prefix like so:

```
select(ma.gov,date,contains("Test_")) 
```


I hereby disclaim any and all representations and warranties with respect to this data, including accuracy, fitness for use, and merchantability. Reliance for medical guidance or use in commerce is strictly prohibited.
