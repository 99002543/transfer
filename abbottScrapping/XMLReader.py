'''
Created on Oct 12, 2020

@author: mahes
'''
from bs4 import BeautifulSoup

CC = []
TO = []
FROM = ''
Drivername = ''
Servername = ''
Database_name=''
Database_TableName = ''
ExcelReportFilePath = ''
print('MAHESH ','你好')
  
def extractEmailIds(Bs_data):
    global CC,TO,FROM
    cc_data = Bs_data.find('CC').find_all('value')
    for cc in cc_data:
        print('CC : ',cc.text)
        CC.append(cc.text)
        #CC.append(';')
        
    to_data = Bs_data.find('TO').find_all('value')
    for to in to_data:
        print('TO : ',to.text)
        TO.append(to.text)
        #TO.append(';')
    from_data = Bs_data.find('FROM').find('value')
    print('FROM : ',from_data.text)
    FROM = from_data.text
    
def extractDatabaseConnectionDetails(Bs_data):
    global Drivername,Servername,Database_name
    driver_data = Bs_data.find('DriverName').find_all('value')
    for data in driver_data:
        print('driver_data :',data.text)
        Drivername = data.text
    server_data = Bs_data.find('ServerName').find_all('value')
    for data in server_data:
        print('server_data :',data.text)
        Servername = data.text
    database_data = Bs_data.find('DatabaseName').find_all('value')
    for data in database_data:
        print('database_data :',data.text)
        Database_name = data.text
        
def extractDatabaseTableName(Bs_data):
    global Database_TableName
    databaseTable_data = Bs_data.find('TableName').find_all('value') 
    for data in databaseTable_data:
        print('databaseTable_data :',data.text)
        Database_TableName = data.text   
        
def extractExcelReportpath(Bs_data):
    global ExcelReportFilePath
    ExcelReportFilePath_data = Bs_data.find('ExcelReportFileName').find_all('value') 
    for data in ExcelReportFilePath_data:
        print('ExcelReportFilePath_data :',data.text)
        ExcelReportFilePath = data.text         
    
with open('UserInput.xml', 'r') as f: 
    data = f.read() 

raw_data = BeautifulSoup(data, "xml")    
extractEmailIds(raw_data)    
extractDatabaseConnectionDetails(raw_data)
extractDatabaseTableName(raw_data)
extractExcelReportpath(raw_data)
print('###############',Servername,'$$$',Drivername,'%%%',Database_name,'%%',Database_TableName,'%^&',ExcelReportFilePath)


     
