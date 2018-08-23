from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import string
import csv
import os
from datetime import datetime

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

"""
To get the data we are interested in, the functions below require the pdf to passed to it 
as a string converted by pdf miner. Since the output of pdf miner includes carriage returns
such as \n, its easier to get a list of words by using the split function. From there we treat
the words as elements in a list. The value we want is adjacent to the description in the list,
for example the value of kilowatts used in a month is directly after the words Monthly Usage, 
so to obtain the value we look for the words Monthly Usage and grab the next value. All the data
collection functions below follow this method.
"""

def get_monthly_kilowatt_usage(pdf_string):
    list_of_words = pdf_string.split()
    for i,w in enumerate(list_of_words) : 
        if w == "Monthly" and list_of_words[i+1] == "Usage" : 
            monthly_kilowatt_usage = (list_of_words[i+2])
            return monthly_kilowatt_usage

def get_bill_start_date(pdf_string):
    list_of_words = pdf_string.split()
    for i,w in enumerate(list_of_words) : 
        if w == "Previous" and list_of_words[i+1] == "Read" and list_of_words[i+2] == "Date" : 
            bill_start_date = (list_of_words[i+3])
            return bill_start_date

def get_bill_end_date(pdf_string):
    list_of_words = pdf_string.split()
    for i,w in enumerate(list_of_words) : 
        if w == "Present" and list_of_words[i+1] == "Read" and list_of_words[i+2] == "Date" : 
            bill_end_date = (list_of_words[i+3])
            return bill_end_date

def get_number_of_days(pdf_string):
    list_of_words = pdf_string.split()
    for i,w in enumerate(list_of_words) : 
        if w == "No." and list_of_words[i+1] == "of" and list_of_words[i+2] == "Days" : 
            number_of_days = (list_of_words[i+3])
            return number_of_days

#Some of the dates grabbed from Huntsville Electricity bills were in the format of mm/dd/yyyy and others mm/dd/yy, this converts them all to mm/dd/yyyy
def cleanse_dates(date_string):
    year_string = date_string.split("/")[2]
    if len(year_string) == 2 :  
        year_string = "20" + year_string
        date_string = date_string[0:6] + year_string
    return date_string

directory = "C:\\Users\\bluem\\Documents\\PythonProjects\\HuntsvilleElectric\\HuntsvilleElectric\\huntsvilleelectricbills\\"

with open ('test.csv', 'w', newline='') as csvfile: 
    rowwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    column_headers = ["Start Date","End Date","KW Used","Number of Days","Daily KW Used"]
    rowwriter.writerow(column_headers)

    #Pass in directory and iterate over files looking just for .pdfs
    for filename in os.listdir(directory): 
        if filename.endswith(".pdf") : 
            filename_full_path = directory + filename

            #Convert pdf to text using pdfminer library
            pdf_text = convert_pdf_to_txt(filename_full_path)
            
            #Pass the text pdf to various functions to obtain data we are looking for
            monthly_kilowatts_used = get_monthly_kilowatt_usage(pdf_text)
            bill_started = cleanse_dates(get_bill_start_date(pdf_text))
            bill_ended = cleanse_dates(get_bill_end_date(pdf_text))
            number_of_days = get_number_of_days(pdf_text)

            #Since the number of days in a billing cycle varies, divide monthly usage by number of days to get kw per day measurement
            kw_used_a_day = float(monthly_kilowatts_used)/float(number_of_days)

            #Export data
            print (bill_started,bill_ended,monthly_kilowatts_used,number_of_days,round(kw_used_a_day,2))
            data_list = [bill_started,bill_ended,monthly_kilowatts_used,number_of_days,round(kw_used_a_day,2)]
            rowwriter.writerow(data_list)