# Scrape job listings from EmCare's website
This code (currently fully functional) is intended to scrape job titles, facilities, and locations a physician-outsourcing firm, EmCare, operates in. It is used as part of our identification strategy in the following paper: [Surprise! Out-of-Network Billing for Emergency Care in the United States](https://www.journals.uchicago.edu/doi/abs/10.1086/708819)

Link to site we scrape: [Envision Job Listings](https://www.envisionphysicianservices.com/find-a-career/clinical-job-search?positiontype=225180003#JobList)

Output data from the script are formatted as follows (examples are as of 6/01/2020):

| Job Title  | Hospital | City | State |
| :---: | :---: | :---: | :---: |
| EM Physician  | Memorial Hospital Jacksonville  | Jacksonville  | FL  |
| Trauma Surgeon  | North Suburban Medical Center  | Thornton  | CO  |

There are 51 pages with job listings on each, the code will iterate through all pages.

### Setting up Selenium
[Selenium](https://selenium-python.readthedocs.io/) is an open-sourced web-based automation tool. It is a powerful tool that can automate most user-oriented behavior.

Selenium is necessary due to Envision's URL structure. Clicking "*next*" on a page does not update the URL to URL/page/2 as is commonly structured. Selenium can be used to get past this limitation. In addition, Envision's site automates to *map view* when navigating to the second page of job listings. Conditions using Selenium's tools are built into the script to deal with this issue.

Below are the following packages necessary in the code:

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='file_path_to_driver')
```

### XPATHs to identify and scrape elements
XPATHs are used to identify the elements of interest on each page. XPATHs iterate nicely for each item of interest. For example, the job titles on each page can be identified with the following code:

```python
xml_post='//*[@id="DivResults"]/div[2]/div['+pager+']/div/div[1]/div[1]/div'
            post=driver.find_elements_by_xpath(xml_post)
            post_title=post[0].text
```
Where "pager" is in a loop that iterates 1-11 (there are 11 job listings per page). 

Envion's site uses a form of lazy loading that loads up each element on a page through a top-down process. As a result, there are instances when the script calls for an element that has yet to load (and will result in error). To deal with this issue, the following technique is used:

```python
WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,xml)))
```
Where xml is defined as the XPATH element of interest. This tells Python to wait until the element is visible (and will give an error if this takes more than 20 seconds).

### Putting it all together
The rest of the script should be self-explanatory (and commented out). Pandas is used to create a dataframe that each element is appended into. There is code at the end to deal with "long-dashes", a character present in some hospital names that Pandas does not recognize as a string. 
