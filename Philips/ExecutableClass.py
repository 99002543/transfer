'''
Created on April 05, 2021

@author: Syed Mohammed Thameem
'''

import timeit
#Start Timer
start = timeit.default_timer()
from Philips import Email, DataBaseConnection,PhilipsScrapping, XMLReader

'''
The required methods were called in the sequential order.
'''
filePath = Email.detailReport(PhilipsScrapping)

##Do not proceed further if extracted data are not equal or zero.
if len(PhilipsScrapping.job_id_store)==0 or (len(PhilipsScrapping.job_date_of_post_store) != len(PhilipsScrapping.job_id_store)):
    SystemExit("Scrapped data are not in proper format")
else:  
    DataBaseConnection.setDataBaseTableName(XMLReader.Database_TableName)
    DataBaseConnection.createTable()
    DataBaseConnection.dataBaseWriting(PhilipsScrapping)
    DataBaseConnection.deleteOldRecords()
    ###Format the data into a tabular format for email body.
    Email.emailFormat(DataBaseConnection.jobsGone(), DataBaseConnection.NewJobIds)   
    Email.mailReport(XMLReader.TO,XMLReader.FROM, XMLReader.CC, filePath)
    #Stop timer.
    stop = timeit.default_timer()
    execution_time = stop - start
    print("Program Executed in "+str(execution_time)) # It returns time in seconds