from datetime import date
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CovidNineteen:
    def get_latest_daily_report(self):
        """
        Get latest daily report(world) from:
        https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
        """
        data_date = date.today()
        data_date_delta = timedelta(days=1)
        daily_report_url_no_date = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv"
        while True:
            data_date_str = date.strftime(data_date, '%m-%d-%Y')
            daily_report_url = daily_report_url_no_date.format(data_date_str)
            try:
                print("Trying to get {} daily report.".format(data_date_str))    
                daily_report = pd.read_csv(daily_report_url)
                print("The file exists，got {} daily report.".format(data_date_str))
                break
            except:
                print("{} hasn't uploaded yet.".format(data_date_str))
                data_date -= data_date_delta # data_date = data_date - data_date_delta
        return daily_report

    def get_time_series(self):
        """
        Get time series data from:
        https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
        """
        time_series = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
        return time_series
        
covid_19 = CovidNineteen()
daily_report = covid_19.get_latest_daily_report()
time_series = covid_19.get_time_series()

time_series.head()

idVars  =['Province/State', 'Country/Region', 'Lat', 'Long']
time_series_long = pd.melt(time_series, id_vars=idVars, var_name='Date', value_name='Confirmed')
time_series_long['Date'] = pd.to_datetime(time_series_long['Date'])
country_confirmed_groupby = time_series_long.groupby(['Date', 'Country/Region'])['Confirmed'].sum()
df_country_confirmed = pd.DataFrame(country_confirmed_groupby).reset_index()
country_confirmed = df_country_confirmed.sort_values('Confirmed', ascending=True)


#============================= Make a matplotlib picture =========================================
#us = country_confirmed[country_confirmed['Country/Region'].str.contains('US')]
#If we use USA plot on this pic, we won't see the other Country's progress.

cn = country_confirmed[country_confirmed['Country/Region'].str.contains('China')]
jpn = country_confirmed[country_confirmed['Country/Region'].str.contains('Japan')]
kr = country_confirmed[country_confirmed['Country/Region'].str.contains('Korea, South')]
tw = country_confirmed[country_confirmed['Country/Region'].str.contains('Taiwan')]

plt.figure(figsize=(20, 5))
plt.title('Covid 19 Confirmed Results', fontsize=20)
plt.xlabel('Date', fontsize=20)
plt.ylabel('Population', fontsize=20)

#plt.plot(us['Date'], us['Confirmed'], label='USA')
plt.plot(cn['Date'], cn['Confirmed'], label='China')
plt.plot(jpn['Date'], jpn['Confirmed'], label='Japan')
plt.plot(kr['Date'], kr['Confirmed'], label='Korea South')
plt.plot(tw['Date'], tw['Confirmed'], label='Taiwan')
plt.legend(loc=2)

plt.show()
