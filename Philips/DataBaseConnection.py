'''
Created on April 14, 2021

@author: Syed, Sowmya
'''
import pyodbc 
from tabulate import tabulate
from _datetime import date
from Philips import XMLReader
import time

#Store the new records Job ids from the database
NewJobIds = []

'''
Establish a Connection with the default database Name : master.
'''
print('XMLReader.Servername:',XMLReader.Servername)
print('XMLReader.Database_name:',XMLReader.Database_name)
cnxn = pyodbc.connect('Driver='+XMLReader.Drivername+';'
                      'Server='+XMLReader.Servername+';'
                      'Database='+XMLReader.Database_name+';'
                      'Trusted_Connection=yes;')

'''
Following are the table name, which will store the data for Philips websites, 
the old job records which no longer exists(to be deleted/updated in the database)
and new job records(to be INSERTED into the database)
'''
tableName = ''


'''
Returns the connection to the database.
'''
def getConnection():
    return cnxn.cursor()

'''
Execute the given SQL Query and print the table content in a particular format on the console.
'''
def executeQuery(sql):
    print(sql)
    cursoe = getConnection().execute(sql)
    print(cursoe)
    print(tabulate(cursoe.fetchall(), headers=['JOBID', 'JOBTYPE','JOBCATEGORY','JOBTITLE','JOBPOSTEDDATE' , 'JOBLOCATION' , 'DATEOFUPDATE','URL'], tablefmt='psql'))
    return cursoe
    


def createTable():
    global tableName
    print('Table name = ', tableName)
    sql = "IF OBJECT_ID('"+ tableName+"','U') is null CREATE TABLE ["+ tableName+''']
    ([JOB ID] char(15) NOT NULL UNIQUE,
    [JOB TYPE]nvarchar(max) NOT NULL,
    [JOB CATEGORY] nvarchar(30),
    [JOB TITLE]varchar(max) NOT NULL,
    [JOB POSTED DATE] nvarchar(50) NOT NULL,
    [JOB LOCATION] nvarchar(max) NOT NULL,
    [DATE OF UPDATE] char(10) NOT NULL,
    [URL] nvarchar(max),PRIMARY KEY ([JOB ID]));'''
    print('SQL = ',sql)
    try:
        getConnection().execute(sql)
        getConnection().commit()
        getConnection().close()
    except:
        getConnection().rollback()
        getConnection().commit()
        getConnection().close()
        
#Write the extracted data into the database, with the conditions either to INSERT new records or to update existing records.
def dataBaseWriting(ReScrapping):
    JobIds = [] 
    ### Fetch job ids from database table.
    cursor = getConnection().execute("SELECT [JOB ID] from "+ tableName)
    jobidsRecords = cursor.fetchall()
    for i in range(len(jobidsRecords)):
        temp = str(jobidsRecords[i])
        JobIds.append(temp)
    print("From Database Length of JobIds : ",len(JobIds)," : ",JobIds)
    
    ### remove additional characters from the job id 
    for i in range(len(JobIds)):
        id = JobIds[i].replace("', )",'').replace("('",'').strip()
        #print('id : ' ,id)
        JobIds[i] = id
    print("After splitting and replace, Length of JobIds : ",len(JobIds)," : ",JobIds)
    ###Iterate over job ids currently scrapped
    for i in range(len(ReScrapping.job_id_store)):
        #print("################JobIds.count(ReScrapping.job_id_store[i]) : ",JobIds.count(ReScrapping.job_id_store[i]))
        if JobIds.count(ReScrapping.job_id_store[i]) == 0 :
            print("Unique Data is : ",ReScrapping.job_id_store[i],'Date ', str(date.today()))
            Sql_Entry(ReScrapping.job_id_store[i], ReScrapping.job_type_store[i], ReScrapping.job_category_store[i], ReScrapping.job_title_store[i], ReScrapping.job_date_of_post_store[i], ReScrapping.job_location_store[i],str(date.today()),ReScrapping.job_url_store[i])
            NewJobIds.append(ReScrapping.job_id_store[i])
        else : 
            print("Updated Data for : ",ReScrapping.job_id_store[i],'Date ', str(date.today())) 
            Sql_Unique_Update(ReScrapping.job_type_store[i], ReScrapping.job_category_store[i], ReScrapping.job_title_store[i], ReScrapping.job_date_of_post_store[i], ReScrapping.job_location_store[i],str(date.today()),ReScrapping.job_url_store[i],ReScrapping.job_id_store[i]) 
    print(cursor.rowcount, "record(s) affected")  


'''
The new records are inserted into the database.
'''       
def Sql_Entry(jobid, jobtype, jobcategory, jobtitle,dateofposting,worklocation,todaysdate,url):
    global tableName
    try:
        getConnection().execute("INSERT INTO "+tableName+" ([JOB ID], [JOB TYPE], [JOB CATEGORY], [JOB TITLE],[JOB POSTED DATE],[JOB LOCATION], [DATE OF UPDATE], [URL]) VALUES (?,?,?,?,?,?,?,?) ",(jobid,jobtype,jobcategory,jobtitle,dateofposting,worklocation,todaysdate,url))
        print('Entry To table '+tableName+' is successful')
        getConnection().commit()
        getConnection().close()
    except:
        getConnection().rollback()
        getConnection().commit()
        getConnection().close()

'''
The old records are updated in the database, with jobid as reference.
'''
def Sql_Unique_Update(jobtype, jobcategory, jobtitle,dateofposting,worklocation,todaysdate,url,jobid):
    global tableName
    try:
        getConnection().execute("UPDATE "+tableName+" SET [JOB TYPE]=?, [JOB CATEGORY]=?, [JOB TITLE]=? ,[JOB POSTED DATE]=?, [JOB LOCATION]=?, [DATE OF UPDATE]=? , [URL]=? WHERE [JOB ID] = ?", (jobtype,jobcategory,jobtitle,dateofposting,worklocation,todaysdate,url,jobid))
        print('Update To table '+tableName+' is successful')
        getConnection().commit()
        getConnection().close()
    except:
        getConnection().rollback()
        getConnection().commit()
        getConnection().close()
        
'''
Identify the records which no longer exists in the Website.
'''
def jobsGone():
    global tableName
    IdsOfJobsGone = []
    try:
        cursor = getConnection().execute("SELECT [JOB ID] from "+ tableName + " WHERE [DATE OF UPDATE] != ?",(str(date.today())))
    except:
        print("Unable to connect to databse")
                
    oldJobsRecords = cursor.fetchall()
    for i in range(len(oldJobsRecords)):
        temp = str(oldJobsRecords[i])
        IdsOfJobsGone.append(temp)
    
    for i in range(len(IdsOfJobsGone)):
        JobGone= IdsOfJobsGone[i].replace("', )",'').replace("('",'').strip()
        IdsOfJobsGone[i] = JobGone
    return IdsOfJobsGone

'''
For development purpose only
Print the entire table.
'''
def PrintTable():
    global tableName
    sql = "SELECT * from "+tableName;
    executeQuery(sql)

'''
For development purpose only
Get the desired record as required by passing value to serach and the reference of the search
'''    
def getDesiredRecord(valueToFound,jobId):
    global tableName
    executeQuery("SELECT "+valueToFound+" from "+ tableName+" WHERE JOBID=?",jobId)

'''
Get the Database table headers name for each column.
'''
def getTableHeaders():
    global tableName
    cursor = getConnection().execute("Select * from "+tableName)
    return [i[0] for i in cursor.description]

'''
Sets a name, to the databaseTable, which will be used throughout the program execution.
'''
def setDataBaseTableName(name):
    global tableName
    tableName = name
'''
Delete job records which are no loger availaible on job portal and stays more than 9 days in the database.
'''    
def deleteOldRecords():
    global tableName
    try:
        getConnection().execute("DELETE FROM "+tableName+" WHERE [DATE OF UPDATE] < GETDATE() - 9")
        getConnection().commit()
        print('Delete from table '+tableName+' is successful')
        getConnection().close()
    except:
        getConnection().rollback()
        getConnection().commit()
        getConnection().close()
        