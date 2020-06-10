# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 22:19:15 2020

@author: ns662
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

#set path to where chrome driver is installed (selenium needs this to work)
driver = webdriver.Chrome(executable_path='C:/Users/ns662/Documents/master_Python/chromedriver_win32/chromedriver.exe')
#set window size for when selenium opens
driver.set_window_size(1080,800)
#website of interest
driver.get('https://www.envisionphysicianservices.com/find-a-career/clinical-job-search?positiontype=225180003#JobList')
           
#initialize dataframe to append into
postlist = pd.DataFrame(columns = ['Title','Hospital','Location1','Location2'])           
           
#loops through pages on website
for p in range(1,52):
    
    #note condition in loop - FIRST TWO PAGES HAVE A TRICKY LOAD SEQUENCE
    if p==1:
        
        #find path of XML element that is the "next" button on page
        xml='//*[@id="cmdNext"]'
        #often, the page opens but loads slowly. selenium will try to induce action (click) before the page is fully loaded
        #this condition makes sure the next button is fully visible before moving to next step
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,xml)))
        
        #each page has 11 boxes, each box has the info from a job listing
        for i in range(1,11):
            
            pager=str(i)
            
            #each XML element iterates nicely, so you can loop through the xml path of each element
            #pull each of the desired fields (selenium pulls elements as a list) and define first list item as string
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[1]/div[1]/div'
            post=driver.find_elements_by_xpath(xml_post)
            post_title=post[0].text
               
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[1]/div'
            post=driver.find_elements_by_xpath(xml_post)
            post_hospital=post[0].text
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[2]/div/span[1]'
            post=driver.find_elements_by_xpath(xml_post)
            post_loc1=post[0].text
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[2]/div/span[2]'
            post=driver.find_elements_by_xpath(xml_post)
            post_loc2=post[0].text
        
            #append each of the desired fields into each column, incrementing row each loop
            postlist.loc[len(postlist)]=[post_title,post_hospital,post_loc1,post_loc2]
         
        #after first page is extracted, go to the next page (2)
        next=driver.find_element_by_xpath(xml)
        next.send_keys(webdriver.common.keys.Keys.RETURN)
           
        #this is where it is tricky - the next page (2) loads as a map, so click to "list view" before extraction
        listview=driver.find_element_by_xpath('//*[@id="href_JobList"]')
        listview.send_keys(webdriver.common.keys.Keys.RETURN)
        
        #again, wait for next button to load
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,xml)))
        
        #now the second page is ready, use the same pull technique for the first page 
        for i in range(1,11):
    
            pager=str(i)
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[1]/div[1]/div'
            post=driver.find_elements_by_xpath(xml_post)
            post_title=post[0].text
               
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[1]/div'
            post=driver.find_elements_by_xpath(xml_post)
            post_hospital=post[0].text
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[2]/div/span[1]'
            post=driver.find_elements_by_xpath(xml_post)
            post_loc1=post[0].text
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[2]/div/span[2]'
            post=driver.find_elements_by_xpath(xml_post)
            post_loc2=post[0].text
            
            postlist.loc[len(postlist)]=[post_title,post_hospital,post_loc1,post_loc2]
        
        #navigates to third page
        next=driver.find_element_by_xpath(xml)
        next.send_keys(webdriver.common.keys.Keys.RETURN)
    
    #all subsequent pages (3 and onwards) load nicely (they do not go into map view), so loop through all remaining pages
    else:
        xml='//*[@id="cmdNext"]'
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,xml)))

        for i in range(1,11):
    
            pager=str(i)
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[1]/div[1]/div'
            post=driver.find_elements_by_xpath(xml_post)
            post_title=post[0].text
               
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[1]/div'
            post=driver.find_elements_by_xpath(xml_post)
            post_hospital=post[0].text
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[2]/div/span[1]'
            post=driver.find_elements_by_xpath(xml_post)
            post_loc1=post[0].text
            
            xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[2]/div[1]/div/div[2]/div/span[2]'
            post=driver.find_elements_by_xpath(xml_post)
            post_loc2=post[0].text
            
            postlist.loc[len(postlist)]=[post_title,post_hospital,post_loc1,post_loc2]
          
        next=driver.find_element_by_xpath(xml)
        next.send_keys(webdriver.common.keys.Keys.RETURN)       

driver.quit()   

#clean out commas in city column
postlist['Location1']=postlist['Location1'].str.replace(',','')

#Some strings have a "long dash character "which pandas does not recognize
#Tell pandas to ignore so it can treat column as string
postlist['Title'] = postlist['Title'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
postlist['Title']=postlist['Title'].astype(str)

    
 
    