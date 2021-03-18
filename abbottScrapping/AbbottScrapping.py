'''
Created on Oct 25, 2020

@author: mahesh
'''
import scrapy
import json
from scrapy.crawler import CrawlerProcess
import time
from bs4 import BeautifulSoup
from googletrans import Translator
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
### Make google chrome invisible.
options.add_argument("headless")
### Auto download google chrome driver for running browser which will load javascript in the url. This is selenium process.
chromeDriver  = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)

##Final lists after scrapping complete. This is the data which will be used by the complete application.
job_title_store = []
job_location_store = []
job_date_of_post_store = []
job_type_store = []
job_category_store = []
job_id_store = []
job_url_store = []


##Store the scrapped category urls.
jobCategoryUrls = []
print('MAHESH ','你好')
#Base url
base_url = 'https://www.jobs.abbott/us/en'
#List to store job titles in each category url.
jobTitlesInCategoryList = []
#List to store job link in each category url
jobLinksInCategoryList = []

#string to form url.
JobUrlLink = ''
#Object for google translator.
translator = Translator()

##class to scrape data vis spider.
class AbbottApider(scrapy.Spider):
    
    name = 'AbbottSpider'
    ## url to start scrapping from
    start_urls = ['https://www.jobs.abbott/us/en']
    
    ##Write the data extracted to csv file. Keep commented after code finalization.
    #custom_settings = {
    #       'FEED_FORMAT': 'csv',
    #       'FEED_URI': 'ABBOTT_OUTPUT.csv'
    #  }
    
    ##headers to pass while making scrapy request. This is not mandatory. It depends on the website.
    headers = {
        ":authority": "www.jobs.abbott",
        ":method": "GET",
        ":path": "/us/en/c/sales-jobs",
        ":scheme" : "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
    
    ##Fetch all the job links present in the source
    def getLinks(self, source):
        websiteLinks = []
        for link in source.find_all('a',{'ph-tevent' : 'job_click'}):
            url = link.get('href')
            if url:
                if '/search?' not in url:
                    websiteLinks.append(url)
        return websiteLinks
    
    
    ##Fetch/scrape all the required fields from each job url. 
    ##This is the final method which will scrap all the fields of a job. 
    def parseEachJobDetail(self, response):
        pageSource = response.css('script::text').get()
        #print('1 :', pageSource)
        print('**************************************************************')
        jsonResponse = json.loads(pageSource)
        print('type ',type(jsonResponse))
        ### Store job url. 
        job_url_store.append(response.url)
        
        JobId = jsonResponse["identifier"]["value"]
        print('JobId : ',JobId)
        ### Store job id.
        job_id_store.append(JobId)
        
        temp = ""
        if "addressRegion" in jsonResponse["jobLocation"]["address"]:
            temp = ":"+ jsonResponse["jobLocation"]["address"]["addressRegion"]
            
        JobAddress = jsonResponse["jobLocation"]["address"]["addressCountry"]+temp
        print('JobAddress : ',JobAddress)
        ### Store job address.
        job_location_store.append(JobAddress)
        
        title = jsonResponse["title"]
        print('title : ',title)
        ## detect language and translate the title into English.
        try:
            if translator.detect(title) !="en":
                title = translator.translate(title).text
        except:
            SystemExit
        ### Store job title. 
        job_title_store.append(title)
        
        employmentType = jsonResponse["employmentType"]
        print('employmentType : ',employmentType)
        ### Store job emplyment type.
        job_type_store.append(employmentType)
        
        datePosted = jsonResponse["datePosted"]
        print('datePosted : ',datePosted)
        ### Store job posted date.
        job_date_of_post_store.append(datePosted)
        
        occupationalCategory = jsonResponse["occupationalCategory"]
        print('occupationalCategory : ',occupationalCategory)
        ###Store job category.
        job_category_store.append(occupationalCategory)
        
        ### Add these job details to excel sheet. Keep this commented during final code delivery.
        ### To be uncommented only for development purpose. This is in relation to 'FEED_FORMAT': 'csv',
        ### 'FEED_URI': 'ABBOTT_OUTPUT.csv'.
        '''
        yield {
                'Job ID':JobId,
                'Job Title': title,
                'employmentType':employmentType,
                'datePosted':datePosted,
                'occupationalCategory':occupationalCategory,
                'JobAddress':JobAddress,
                'Job Url': response.url,
              }      
        '''
    ##Fetch/scrape the job categories in Abbott and then browse each 
    ##job category and fetch job links and title from each job category.        
    def parse(self, response):
        global jobCategoryUrls
        raw_text = response.text
        #print('Mahesh',raw_text)
        ##Fetch categaory urls.
        raw_text = raw_text.split('categoryUrlMap')
        #print('Mahesh1',len(raw_text), raw_text[1])
        raw_text = raw_text[1]
        raw_text = raw_text.split('":{"')[1]
        #print('Mahesh2', len(raw_text), raw_text)
        raw_text = raw_text.split('"},"')[0]
        #print('Mahesh2', len(raw_text), raw_text)
        raw_text = raw_text.split('","')
        for i in range(len(raw_text)):
            raw_text[i] = raw_text[i].split('":"')[1].strip()
            jobCategoryUrls.append(raw_text[i])
            
        #print(len(jobCategoryUrls), ': ',jobCategoryUrls)
        
        ##Remove duplicates from the category urls.
        jobCategoryUrls = list(dict.fromkeys(jobCategoryUrls))
        print(len(jobCategoryUrls), ': ',jobCategoryUrls)
       
        global jobTitlesInCategoryList, jobLinksInCategoryList
        for i in range(len(jobCategoryUrls)):
            category_url = base_url + '/'+ jobCategoryUrls[i]
            pageNumber = 0
            chromeDriver.get(category_url)
            print("Category url : ", category_url) 
            time.sleep(5)
            soup=BeautifulSoup(chromeDriver.page_source, 'html.parser')
            ##Get the pagination url at once for each job category and store for pagination.
            pageLinks = soup.find_all('a',{'data-ph-at-id' : 'pagination-page-number-link'})
            pageLinksList = []
            for link in pageLinks:
                print(link.get('href'))
                pageLinksList.append(link.get('href'))
                
            ##Get all the job links present in a job category    
            while pageNumber < len(pageLinksList):
                    chromeDriver.get(pageLinksList[pageNumber])
                    time.sleep(5)
                    print("Job url : ", pageNumber, ': ',pageLinksList[pageNumber])    
                    soup=BeautifulSoup(chromeDriver.page_source, 'html.parser')
            
                    jobTitles = soup.find_all('h4',{'data-ph-at-id' : 'searchresults-job-title'})
                    joblinks = self.getLinks(soup)
                    #print('links : ', len(links), links)
                    for i in range(len(jobTitles)):
                        title = jobTitles[i].text
                        print('Jobs Title ',i,' : ',title)
                        print('Jobs url ',i,": ",joblinks[i])
                        jobTitlesInCategoryList.append(title)
                        jobLinksInCategoryList.append(joblinks[i])
                    ##Go to next page of specific job category.      
                    pageNumber +=1
                    print("Length of Job Titles : ",len(jobTitlesInCategoryList))
                    print("Length of Job Links : ",len(jobLinksInCategoryList))
        
        ##Request to go through all job links.
        chromeDriver.quit()           
        for jobLink in jobLinksInCategoryList:
            yield scrapy.Request(jobLink, callback=self.parseEachJobDetail)
        
            
process = CrawlerProcess()
process.crawl(AbbottApider)
process.start() 
print('length of url', len(job_url_store))  
print('length of title', len(job_title_store))
print('length of locations ', len(job_location_store))
print('length of posted date ', len(job_date_of_post_store))
print('length of job type ', len(job_type_store))
print('Length of job category ', len(job_category_store))
print('length of job ids ', len(job_id_store))

    