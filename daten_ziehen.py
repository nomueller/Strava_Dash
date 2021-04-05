#%%

#https://selenium-python.readthedocs.io/locating-elements.html
from selenium import webdriver
import pandas as pd
import os
from selenium.webdriver.common.keys import Keys
def get_data():
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")
    #op.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options = op)

    driver.get('https://www.strava.com/login')
    import time
    #### Login
    time.sleep(2)
    user = 'nomueller@uni-osnabrueck.de'
    pw= 'Kroos92m.'
    search = driver.find_element_by_id("email")
    search.clear()
    search.send_keys(user)
    search2= driver.find_element_by_id("password")
    search2.clear()
    search2.send_keys(pw)
    time.sleep(2)
    login= driver.find_element_by_id("login-button")
    ####/ login

    ### Aktivitäten
    driver.get('https://www.strava.com/athlete/training')

    driver.set_window_size(800, 600)
    #  login.click()
    #  time.sleep(1)
    #  aktivitäten = driver.find_element_by_partial_link_text("Aktivitäten")
    # aktivitäten.click()
    time.sleep(2)


    ### Aktivität einzeln
    table = driver.find_element_by_css_selector("#search-results")
    time.sleep(2)
    spalten = ['td.view-col.col-type','td.view-col.col-dist','td.view-col.col-date','td.view-col.col-time']
    dist=[]
    date=[]
    time2=[]
    typex=[]

    for durchlauf in  range(6):
        for i in spalten:
            tags = table.find_elements_by_css_selector(str(i))
            for tag in tags:
                if str(i) == 'td.view-col.col-dist':
                     x= tag.text
                     print(x)
                     dist.append(x)
                elif str(i) == 'td.view-col.col-date':
                     x= tag.text
                     print(x)
                     date.append(x)
                elif str(i) == 'td.view-col.col-time':
                     x= tag.text
                     print(x)
                     time2.append(x)
                elif str(i) == 'td.view-col.col-type':
                     x= tag.text
                     print(x)
                     typex.append(x)
        next_page = driver.find_element_by_css_selector("button.btn.btn-default.btn-sm.next_page")
        next_page.click()
        time.sleep(2)
    data ={'Type':typex ,'Distance' :dist, 'Date' : date, 'Time' : time}
    data = pd.DataFrame(data)
    time.sleep(2)


    # vitimeew-col col-dist /time/date/title

    data["Date"] =pd.to_datetime(data["Date"].str.slice(4, 15))
    data["Distance"] = data["Distance"].str.split(' ',1).str[0]
    data["Distance"] =data["Distance"].str.replace(',','.').astype('float')
    driver.close()
    return data