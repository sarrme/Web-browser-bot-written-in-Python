from splinter import Browser
import os 
from selenium.webdriver.common.keys import Keys
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path+"\\photos\\"
import random
import os
import xlrd 
import schedule
import time
import _thread
loc = ("base.xlsx") 
wb = xlrd.open_workbook(loc)


def post(thread,i):
    browser=Browser("chrome")
    try:
        j = 0
        an = 0
        sheet = wb.sheet_by_index(i)
        email = sheet.cell_value(2, 0)
        title = sheet.cell_value(j+5, 2)
        password = sheet.cell_value(2, 1)
        while(title.strip()!=""):
            text = sheet.cell_value(j+5, 3)
            price = sheet.cell_value(j+5, 4)
            doc = sheet.cell_value(j+5, 5)
            city = sheet.cell_value(j+5, 6)
            email_annonce = sheet.cell_value(j+5, 7)
            tel = sheet.cell_value(j+5, 8)
            tel = "0"+str(tel)
            dir_path_annonce = dir_path + "\\"+doc+"\\"
            files = os.listdir(dir_path_annonce)
            chosen = random.sample(files,3)
            if(j==0):
                url = "https://www.leboncoin.fr/"
                browser.visit(url)
                time.sleep(1)
                if browser.is_element_present_by_css('button[class*="_2sNbI _1xIyN _2xk2l"]'):
                    browser.find_by_css('button[class*="_2sNbI _1xIyN _2xk2l"]').first.click()
                time.sleep(1)
                browser.visit("https://www.leboncoin.fr/compte/part/mes-annonces/")
                browser.find_by_id('email').fill(email)
                browser.find_by_id('password').fill(password)
                active_web_element = browser.driver.switch_to.active_element
                active_web_element.send_keys(Keys.ENTER)
                time.sleep(1)    
            url = "https://www.leboncoin.fr/ai/form/"+str(an)
            browser.visit(url)
            browser.find_by_id('subject').fill(title)
            element = browser.find_by_id('category').first
            element.select('34')
            browser.find_by_id('location_p').fill(city[0])
            browser.find_by_id('location_p').fill(city)
            time.sleep(2)
            active_web_element = browser.driver.switch_to.active_element
            active_web_element.send_keys(Keys.ENTER)
            browser.find_by_id("body").fill(text)
            browser.find_by_id("price").fill("{}".format(price))
            browser.find_by_id("email").fill(email_annonce)
            browser.find_by_id("phone").fill(tel)
            time.sleep(2)
            for k in range(3):
                browser.attach_file('image{}'.format(k) , dir_path_annonce + chosen[k])
                time.sleep(2)
            t=0
            browser.find_by_id("newadSubmit").click()
            while(browser.is_element_not_present_by_id("accept_rule")):
                if(t==2):
                    break
                browser.find_by_id("address").fill("")
                browser.find_by_id("newadSubmit").click()
                t+=1
            print(thread,j,t+1)
            if(t==2):
                an+=1
                continue
            time.sleep(1)
            browser.find_by_id("accept_rule").click()
            browser.find_by_id("lbc_submit").click()
            time.sleep(1)
            j+=1
            an+=1
            try:
                title = sheet.cell_value(j+5, 2)
            except:
                browser.quit()
                title=""
        browser.quit()
    except:
        browser.quit()
        
        
def process(x):
    num =0
    for e in x:
        t = ("Thread-{}".format(num), int(e), )
        num+=1
        print(t)
        _thread.start_new_thread( post, t )

p=0
enter = True
dic = {}
while enter:
    
    try:
        sheet = wb.sheet_by_index(p)
        publication  = sheet.cell_value(0,1)
        if publication == "OUI":
            hours = sheet.cell_value(3, 1)
            hours = hours.split(",")
            for hour in hours:
                if hour not in dic:
                    dic[hour]=[]
                dic[hour].append(p)
    except:
        enter = False
    p+=1
exc = list(sorted(dic.keys()))
for x in exc:
    schedule.every().day.at(x).do(process,dic[x])
    print(x+" "+str(dic[x]))

    
while True:
    schedule.run_pending()
    time.sleep(1)
        
