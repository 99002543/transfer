import pandas as pd
import openpyxl as pxl

file ="Philips_final2021-06-07_filtered.xlsx"
dataframe = pd.read_excel(file)


NameofFile = 'test.xlsx'
writer_object = pd.ExcelWriter(NameofFile,engine ='xlsxwriter')

# Filter based on job category
df_category= dataframe.loc[(dataframe['Job Category']=='Engineering') | 
            (dataframe['Job Category']=='Software development') |
            (dataframe['Job Category']=='R & D')|
            (dataframe['Job Category']=='IT') |
            (dataframe['Job Category']=='Quality & Regulatory') |
            (dataframe['Job Category']=='Manufacturing') |
            (dataframe['Job Category']=='Experience Design')]
            
# Final Filtered Openings - both job category and job location******************************************************************************

df_final = df_category[df_category['Job Location'].str.startswith('United States of America:') | df_category['Job Location'].str.startswith('India:') |
                       df_category['Job Location'].str.startswith('Singapore:') | df_category['Job Location'].str.startswith('Japan:') | 
                       df_category['Job Location'].str.startswith('China:') | df_category['Job Location'].str.startswith('Netherlands:') |
                       df_category['Job Location'].str.startswith('Israel:') |  df_category['Job Location'].str.startswith('Germany:') | 
                       df_category['Job Location'].str.startswith('Italy:') | df_category['Job Location'].str.startswith('United Kingdom:') | 
                       df_category['Job Location'].str.startswith('Poland:')]

openings = pd.DataFrame(df_final)

openings.to_excel(writer_object, sheet_name ='Openings',index = False)
print("Written openings sheet to excel..................")

#USA Jobs**************************************************************************************************************************************

usa = df_category[df_category['Job Location'].str.startswith('United States of America:')]
RemoveUSA=usa['Job Location']
RemoveUSA=list(RemoveUSA)
AddUSA=[]
for i in range(len(RemoveUSA)):
    AddUSA.append(RemoveUSA[i].replace("United States of America:","USA:"))

#insertingUSA=pd.DataFrame(AddUSA)
usa['Job Location']=usa['Job Location'].replace(RemoveUSA,AddUSA)
    


sheet1 = pd.DataFrame(usa)

sheet1.to_excel(writer_object, sheet_name ='USA',index = False)
print("Written USA sheet to excel..................")

# India Jobs**************************************************************************************************************************************

India = df_category[df_category['Job Location'].str.startswith('India:')]


sheet2 = pd.DataFrame(India)

sheet2.to_excel(writer_object, sheet_name ='India',index = False)
print("Written India sheet to excel..................")

# ASIA Jobs - Singapoer, Japan, China******************************************************************************************************************

Asia = df_category[df_category['Job Location'].str.startswith('Singapore:') | df_category['Job Location'].str.startswith('Japan:') | df_category['Job Location'].str.startswith('China:')]


sheet3 = pd.DataFrame(Asia)

sheet3.to_excel(writer_object, sheet_name ='Asia',index = False)
print("Written Asia sheet to excel..................")


# Europe Jobs - UK, Netherlands, Germany, Israel, Italy, Poland

Europe = df_category[df_category['Job Location'].str.startswith('Netherlands:') | df_category['Job Location'].str.startswith('Israel:') | 
         df_category['Job Location'].str.startswith('Germany:') | df_category['Job Location'].str.startswith('Italy:') |
         df_category['Job Location'].str.startswith('United Kingdom:') | df_category['Job Location'].str.startswith('Poland:')]

sheet4 = pd.DataFrame(Europe)

sheet4.to_excel(writer_object, sheet_name ='Europe',index = False)
print("Written Europe sheet to excel..................")

print("Closing the excel..................")

writer_object.save()














