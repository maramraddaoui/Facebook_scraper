from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import re
import mysql.connector
 


class FBPageScraper:

    def __init__(self, page_id, nb_page=1):
        self.page_id = page_id
        self.page_url = "https://m.facebook.com/" + self.page_id
        self.nb_page=nb_page
    #login function
    def login(self): 
        EMAIL = "scraping.count@gmail.com"
        PASSWORD = "facebook.0"
        desired_capabilities = {
            'browserName': 'firefox',
            'javascriptEnabled': True,
            'version': "3.9",
        }
        browser = webdriver.Remote('http://selenium:4444/wd/hub', desired_capabilities=desired_capabilities)
        browser.get("http://m.facebook.com")
        browser.maximize_window()
        wait = WebDriverWait(browser, 30)
        email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
        email_field.send_keys(EMAIL)
        pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
        pass_field.send_keys(PASSWORD)
        pass_field.send_keys(Keys.RETURN)

        time.sleep(5)
        return browser
    #scraping function
    def parse(self): 
        driver=self.login()
        driver.get(self.page_url)
        #wait 5 seconds to allow your new page to load
        time.sleep(5)

        for j in range(0,self.nb_page): # scrolling the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
        # extracting posts
        posts=driver.find_elements(By.XPATH, ".//div[@class='_5rgt _5nk5 _5msi']/div/span/p")
        all_data=[]
        for post in posts:
            more_element=post.find_elements(By.XPATH,".//span[@class='text_exposed_show']")
            if(more_element!=[]):
                for element in more_element:
                    all_data.append({'post':self.delete_more(post.text)+self.cleanhtml(element.get_attribute('innerHTML'))})
            else:
                all_data.append({'post':post.text})
            time.sleep(5)
        return all_data
    #remove special caracters from html code
    def cleanhtml(self, text): 
        CLEANR = re.compile('<.*?>') 
        cleantext = re.sub(CLEANR, '', text)
        return cleantext
    #delete "... Plus" from some posts
    def delete_more(self, text): 
        return re.sub('… Plus', '', text)
    #connexion to the database
    def db_connexion(self): 
        con= mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="facebook_scraper",
        auth_plugin='mysql_native_password'
        )
        return con
    #Saving in the database
    def save_db(self, data): 
        con=self.db_connexion()
        cur=con.cursor()
        for i in range(len(data)):
            sql = "INSERT INTO data (post) VALUES (%s)"
            val = (data[i]['post'],)
            cur.execute(sql, val)
            con.commit()

