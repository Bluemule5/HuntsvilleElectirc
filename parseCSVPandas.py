import pandas as pd 

df = pd.read_csv("test.csv")
dateWeWant = "11/02/2015"
dateWeWantTruc = "11/02/15"
#set2 = set(dateWeWant.split('/'))

for index, row in df.iterrows() : 
    startDate = str(row[0])
    #print(startDate)
    set1 = set(startDate.split('/'))
    if startDate == dateWeWant or startDate == dateWeWantTruc :  
        print(row[4])