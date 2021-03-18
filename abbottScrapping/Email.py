'''
Created on Aug 18, 2020

@author: mahesh
'''
import pandas as pd
from _datetime import date
import win32com.client as com

from abbottScrapping import DataBaseConnection, XMLReader
'''
Print to save the python script in utf8 encoding. This will avoid encoding exception.
Use encoding option as utf-8 in eclipse workspace.
'''
print('MAHESH ','你好')

'''
Global variables to store various data in this script for manipulation.
'''
oldEmailTemplate = []
newEmailTemplate = []
todaysJobEmailTemplate = []
oldJobCount = 0
newJobCount = 0
todaysJobCount = 0

'''
Draft the content for the body of the email, which will be sent to the respective sales team.
'''
def emailFormat(oldJobPost, newJobPost):
    jobGone = oldJobPost
    global oldEmailTemplate, newEmailTemplate, todaysJobEmailTemplate, oldJobCount, newJobCount, todaysJobCount
    for i in range(len(jobGone)):
        oldCursor = DataBaseConnection.getConnection().execute("SELECT * from "+ DataBaseConnection.tableName+" WHERE [JOB ID]=?",jobGone[i])
        for row in oldCursor.fetchall():
            template = """
                    <tr>
                    <td>"""+row[0]+"""</td>
                    <td>"""+row[1]+"""</td>
                    <td>"""+row[2]+"""</td>
                    <td>"""+row[3]+"""</td>
                    <td>"""+row[4]+"""</td>
                    <td>"""+row[5]+"""</td>
                    <td>"""+row[6]+"""</td>
                    <td>"""+row[7]+"""</td>
                    </tr>
                    """
            oldEmailTemplate.append(template)
            oldJobCount = oldJobCount+1       
            #print("Id = ", row[0], )
            #print("Category = ", row[1])
            #print("Title = ", row[2])
            #print("Posteddate  = ", row[3])
            #print("Location  = ", row[4])
            #print("DateOfUpdate  = ", row[5], "\n")
            #print("URL  = ", row[6], "\n")
            #print("Category  = ", row[7], "\n")
            
    jobPosting = newJobPost
    for i in range(len(jobPosting)):
        newCursor = DataBaseConnection.getConnection().execute("SELECT * from "+ DataBaseConnection.tableName+ " WHERE [JOB ID]=?",jobPosting[i])
        for row in newCursor.fetchall():
            template =  """
                    <tr>
                    <td>"""+row[0]+"""</td>
                    <td>"""+row[1]+"""</td>
                    <td>"""+row[2]+"""</td>
                    <td>"""+row[3]+"""</td>
                    <td>"""+row[4]+"""</td>
                    <td>"""+row[5]+"""</td>
                    <td>"""+row[6]+"""</td>
                    <td>"""+row[7]+"""</td>
                    </tr>
                    """
            newEmailTemplate.append(template)
            newJobCount = newJobCount+1         
            #print("Id = ", row[0], )
            #print("Category = ", row[1])
            #print("Title = ", row[2])
            #print("Posteddate  = ", row[3])
            #print("Location  = ", row[4])
            #print("DateOfUpdate  = ", row[5], "\n")
            #print("URL  = ", row[6], "\n")
            #print("Category  = ", row[7], "\n")  
            
#Convert a lsit into string.
def stringFromList(emailIds):
    email_list = ''
    for i in range(len(emailIds)):
        email_list = email_list+ emailIds[i]+';'
    print('email list = ', email_list)   
    print('email list = ', email_list[:-1])  
    email_list = email_list[:-1]
    return email_list   
    
'''
Form the final email format and send to the respective team.
Here the body is appended with the output of emailFormat method, both new and old job records.
'''       
def mailReport(receiver, sender, cc, nameOfFile):
    global oldEmailTemplate, newEmailTemplate, todaysJobEmailTemplate, oldJobCount, newJobCount, todaysJobCount
    print('oldEmailTemplate and oldJobCount : ',len(str(oldEmailTemplate)),"and ",len(str(oldJobCount)))
    print('newEmailTemplate and newJobCount : ',len(str(newEmailTemplate)),"and ",len(str(newJobCount)))
    print('todaysJobEmailTemplate and todaysJobCount : ',len(str(todaysJobEmailTemplate)),"and ",len(str(todaysJobCount)))
    
    #This if is required to report todays job post if the program is run more than once ion a day.
    tempComment = ' new'
    if (newJobCount == 0 and todaysJobCount >0):
        newEmailTemplate = todaysJobEmailTemplate
        newJobCount = todaysJobCount
        tempComment = ' todays'
    try:
        outlook = com.GetActiveObject('Outlook.Application')
    except:
        outlook = com.Dispatch('Outlook.Application')
    #outlook = com.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    receiver = stringFromList(receiver)
    print('receiver = ', receiver)
    mail.To =  receiver
    print('sender = ', sender)
    cc = stringFromList(cc)
    print('cc = ',cc)
    print('+ ', cc +';' +sender)
    mail.Cc = cc+';'+sender
    ###Email Subject
    mail.Subject = ("ABBOTT Today's Openings ||" + str(date.today()))
    mail.HTMLBody = """
   <html>
      <head></head>
      <style>
      table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        th, td {
          padding: 5px;
        }
      </style>
      <body>
        <p>Hi All,<br><br>
        Please find the attached list of job openings available as of today.
        
        </p>
        <p><b>
        Following are the """+str(newJobCount)+ tempComment+ """ Job Openings : 
        </b></p>
        <table>
          <tr>
            <th>"""+DataBaseConnection.getTableHeaders()[0]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[1]+"""</th> 
            <th>"""+DataBaseConnection.getTableHeaders()[2]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[3]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[4]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[5]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[6]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[7]+"""</th>
          </tr>"""+ ''.join(newEmailTemplate) +"""</table>
        <p>
        
        <p><b><mark>
         Following are the """+str(oldJobCount)+""" jobs which do not exists : 
        </mark></b></p>
        <table>
          <tr>
            <th>"""+DataBaseConnection.getTableHeaders()[0]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[1]+"""</th> 
            <th>"""+DataBaseConnection.getTableHeaders()[2]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[3]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[4]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[5]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[6]+"""</th>
            <th>"""+DataBaseConnection.getTableHeaders()[7]+"""</th>
          </tr>"""+ ''.join(oldEmailTemplate) +"""</table>
        <p>
        Regards,<br>
        Mahesh  Pati
        </p>
      </body>
    </html>
    """
    mail.BodyFormat = 2
    filename = nameOfFile
    mail.Attachments.Add(filename)
    #mail.Display(True)  
    mail.Send()
    print('Mail Sent')
    
'''
Form the Excel report, which will then be attached to the email.
'''
def detailReport(ReScrapping):
    dataframe = pd.DataFrame({'Job Id': ReScrapping.job_id_store,'Job Type' : ReScrapping.job_type_store, 'Job Category' : ReScrapping.job_category_store,'Job Title': ReScrapping.job_title_store,'Job Location' : ReScrapping.job_location_store, 'Date Of Post': ReScrapping.job_date_of_post_store , 'URL':ReScrapping.job_url_store})
    NameofFile = XMLReader.ExcelReportFilePath + (str(date.today())) +'.xlsx'
    print('\n')
    writer_object = pd.ExcelWriter(NameofFile,engine ='xlsxwriter')
    dataframe.to_excel(writer_object, sheet_name ='Openings',index = False)

    writer_object.save()
    print('Detail Report Created path - ',NameofFile)
    return NameofFile
