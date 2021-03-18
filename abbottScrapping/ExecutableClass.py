'''
Created on Aug 27, 2020

@author: mahesh
'''

import timeit
#Start Timer
start = timeit.default_timer()
from abbottScrapping import Email, DataBaseConnection,AbbottScrapping, XMLReader

#url = 'https://alcon.wd5.myworkdayjobs.com/en-US/careers_alcon'

###Use encoding option as utf-8 in eclipse workspace.
print('MAHESH ','你好')
'''
The required methods were called in the sequential order.
'''
filePath = Email.detailReport(AbbottScrapping)
##Do not proceed further if extracted data are not equal or zero.
if len(AbbottScrapping.job_id_store)==0 or (len(AbbottScrapping.job_date_of_post_store) != len(AbbottScrapping.job_id_store)):
    SystemExit("Scrapped data are not in proper format")
else:  
    DataBaseConnection.setDataBaseTableName(XMLReader.Database_TableName)
    DataBaseConnection.createTable()
    DataBaseConnection.dataBaseWriting(AbbottScrapping)
    DataBaseConnection.deleteOldRecords()
    ###Format the data into a tabular format for email body.
    Email.emailFormat(DataBaseConnection.jobsGone(), DataBaseConnection.NewJobIds)   
    Email.mailReport(XMLReader.TO,XMLReader.FROM, XMLReader.CC, filePath)
    #Stop timer.
    stop = timeit.default_timer()
    execution_time = stop - start
    print("Program Executed in "+str(execution_time)) # It returns time in seconds