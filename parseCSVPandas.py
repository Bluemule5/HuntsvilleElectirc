import pandas as pd
import numpy as np
import os 
from time import strptime
import string

#Take date string from  csv and convert to mm/dd/yyyy format
def weathercsv_date_convert(date_string) : 
    month_number = str(strptime(date_string.split(" ")[1], '%b').tm_mon).zfill(2)
    day_number = date_string.split(" ")[2]
    year = date_string.split(" ")[3]
    full_date_converted = month_number + "/" + day_number + "/" + year
    #full_date_converted = year + "-" + month_number + "-" + day_number
    return full_date_converted

#Set dataframe for Huntsville Utilities .csv export
huntsville_bills_df = pd.read_csv("test.csv")

#Convert Start Date and End Date to python date object, then sort by start date
huntsville_bills_df['Start Date'] = pd.to_datetime(huntsville_bills_df['Start Date'], format='%m/%d/%Y')
huntsville_bills_df['End Date'] = pd.to_datetime(huntsville_bills_df['End Date'], format='%m/%d/%Y')
huntsville_bills_df.sort_values('Start Date', inplace=True, ascending=True)

#Add columns to the dataframe to populate later
huntsville_bills_df['Avg. apparentTemperatureMax'] = np.nan
huntsville_bills_df['Avg. apparentTemperatureMin'] = np.nan
huntsville_bills_df['Max of apparentTemperatureMax'] = np.nan
huntsville_bills_df['Min of apparentTemperatureMin'] = np.nan
huntsville_bills_df['Avg. cloudCover'] = np.nan
huntsville_bills_df['Avg. precipIntensityMax'] = np.nan
huntsville_bills_df['Avg. dewPoint'] = np.nan
huntsville_bills_df['Avg. humidity'] = np.nan
huntsville_bills_df['Avg. pressure'] = np.nan
huntsville_bills_df['Avg. windSpeed'] = np.nan

# Set full path for weather csvs 
directory = "C:\\Users\\bluem\\Documents\\PythonProjects\\HuntsvilleElectric\\HuntsvilleElectric\\weathercsvs\\"

#Loop through weather csvs and create one large weather dataframe in pandas 
weather_df = pd.DataFrame()
list_ = []
for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
        filename_full_path = directory + filename
        df = pd.read_csv(filename_full_path,index_col=None, header=0)
        list_.append(df)
weather_df = pd.concat(list_)

#Convert 'time' column format from Day of week, Month Name, Day Number, year number to mm/dd/yyyy then to dateobject
weather_df['time'] = weather_df['time'].apply(weathercsv_date_convert)
weather_df['time'] = pd.to_datetime(weather_df['time'], format='%m/%d/%Y')

#Reset index to use the new date format as the index
weather_df = weather_df.set_index('time')

#Loop through the rows of the huntsville_bills dataframe and add weather values data
for index, row in huntsville_bills_df.iterrows() :
        start_date = row['Start Date']
        end_date = row['End Date']
        #Create a new dataframe from larger allweather dataframe, but only have records from the bill start and end date
        new_df =  weather_df.loc[start_date:end_date]
        huntsville_bills_df.at[index,'Avg. apparentTemperatureMax'] = round(new_df['apparentTemperatureMax'].mean(),2)
        huntsville_bills_df.at[index,'Avg. apparentTemperatureMin'] = round(new_df['apparentTemperatureMin'].mean(),2)
        huntsville_bills_df.at[index,'Max of apparentTemperatureMax'] = round(new_df['apparentTemperatureMax'].max(),2)
        huntsville_bills_df.at[index,'Min of apparentTemperatureMin'] = round(new_df['apparentTemperatureMin'].min(),2)
        huntsville_bills_df.at[index,'Avg. cloudCover'] = round(new_df['cloudCover'].mean(),2)
        huntsville_bills_df.at[index,'Avg. precipIntensityMax'] = round(new_df['precipIntensityMax'].mean(),2)
        huntsville_bills_df.at[index,'Avg. dewPoint'] = round(new_df['dewPoint'].mean(),2)
        huntsville_bills_df.at[index,'Avg. humidity'] = round(new_df['humidity'].mean(),2)
        huntsville_bills_df.at[index,'Avg. pressure'] = round(new_df['pressure'].mean(),2)
        huntsville_bills_df.at[index,'Avg. windSpeed'] = round(new_df['windSpeed'].mean(),2)

huntsville_bills_df.to_csv("complete_weather_utiliy_information.csv", encoding='utf-8')
#weather_df.to_csv("allweather.csv", encoding='utf-8')