from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import mysql.connector
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"E:\Chrome Driver\chromedriver.exe")

url = "https://english.tgju.org/"

driver.get(url)

time.sleep(2)

# USD
USD_Title =driver.find_element(By.CSS_SELECTOR,'.fs-row+ .fs-row .dark-head.market-section-right .pointer:nth-child(1) th')

USD_Rate =driver.find_element(By.CSS_SELECTOR,'.fs-row+ .fs-row .dark-head.market-section-right .pointer:nth-child(1) th+ .nf')

USD_Time =driver.find_element(By.CSS_SELECTOR,'.fs-row+ .fs-row .dark-head.market-section-right .pointer:nth-child(1) td:nth-child(6)')



# EUR
EUR_Title =driver.find_element(By.CSS_SELECTOR,'.fs-row+ .fs-row .dark-head.market-section-right .pointer:nth-child(2) th')

EUR_Rate =driver.find_element(By.CSS_SELECTOR,'.fs-row+ .fs-row .dark-head.market-section-right .pointer:nth-child(2) th+ .nf')

EUR_Time =driver.find_element(By.CSS_SELECTOR,'.fs-row+ .fs-row .dark-head.market-section-right .pointer:nth-child(2) td:nth-child(6)')

# Coin
Coin_Title ='Coin'

Coin_Rate =driver.find_element(By.CSS_SELECTOR,'#coin-table .pointer:nth-child(2) th+ td')

Coin_Time =driver.find_element(By.CSS_SELECTOR,'#coin-table .pointer:nth-child(2) td:nth-child(6)')


# Coin Imami
Coin_Imami_Title ='Coin (Imami)'

Coin_Imami_Rate =driver.find_element(By.CSS_SELECTOR,'#coin-table .pointer:nth-child(1) th+ td')

Coin_Imami_Time =driver.find_element(By.CSS_SELECTOR,'#coin-table .pointer:nth-child(1) td:nth-child(6)')


# Gold 18
Gold18_Title ='Gold 18'

Gold18_Rate =driver.find_element(By.CSS_SELECTOR,'#gold-table .pointer:nth-child(1) th+ .nf')

Gold18_Time =driver.find_element(By.CSS_SELECTOR,'#gold-table .pointer:nth-child(1) td:nth-child(6)')


# Gold 24
Gold24_Title ='Gold 24'

Gold24_Rate =driver.find_element(By.CSS_SELECTOR,'#gold-table .pointer:nth-child(2) th+ .nf')

Gold24_Time =driver.find_element(By.CSS_SELECTOR,'#gold-table .pointer:nth-child(2) td:nth-child(6)')

# Date
Date =driver.find_element(By.CSS_SELECTOR,'.date span')


Titles = [USD_Title.text,EUR_Title.text,Coin_Title,Coin_Imami_Title,Gold18_Title,Gold24_Title]
Rates = [USD_Rate.text,EUR_Rate.text,Coin_Rate.text,Coin_Imami_Rate.text,Gold18_Rate.text,Gold24_Rate.text]
Times = [USD_Time.text,EUR_Time.text,Coin_Time.text,Coin_Imami_Time.text,Gold18_Time.text,Gold24_Time.text]
# transfer to database:

def __init__():
        Create_Connection()
        Create_Table()


def Create_Connection():

        global conn
        global curr
        conn=mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'LmN3LmN3!',
            database = 'currency_rates'
        )

        curr=conn.cursor()
        conn.close()

        

def Create_Table():
        conn._open_connection()
        
        
        curr.execute("""DROP TABLE IF EXISTS crawled_data_tb""")

        curr.execute("""CREATE TABLE crawled_data_tb (
            
            ID int NOT NULL AUTO_INCREMENT,
            Currency text,
            Current_Rate text,
            Time text,
            PRIMARY KEY (ID)
            
            )""")
            
        conn.close()


__init__()
    
def Store_db():
        
        conn._open_connection()

        
        curr.executemany("""INSERT INTO crawled_data_tb (Currency, Current_Rate, Time) VALUES (%s,%s,%s)""",[
            (Titles[0],Rates[0],Times[0]),
            (Titles[1],Rates[1],Times[1]),
            (Titles[2],Rates[2],Times[2]),
            (Titles[3],Rates[3],Times[3]),
            (Titles[4],Rates[4],Times[4]),
            (Titles[5],Rates[5],Times[5]),
            
            ])

        conn.commit()
        curr.execute("""INSERT INTO crawled_data_tb (ID, Time) VALUES ('{}','{}')""".format(100,Date.text))
        
        conn.commit()
        
        conn.close()
Store_db()
