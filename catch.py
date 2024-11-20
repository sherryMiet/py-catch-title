from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from zhconv import convert
import requests
options = Options()
prefs = {
    'profile.default_content_setting_values' :
        {
        'notifications' : 2
        }
}
options.add_experimental_option('prefs',prefs)
options.add_argument("--incognito")           #開啟無痕模式
# options.add_argument("--headless")      #不開啟實體瀏覽器背景執行
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
driver.get('https://udndata.com/ndapp/Index?cp=udn')
html = driver.page_source


try:

        #開始爬蟲的頁數
        start= 1
        #結束的頁數    
        page=5000
        #檔名
        file_name="udn_"
        #起始日期
        after = date(2020,1,6)
        #結束日期
        before = date(2020,1,10)
        #間隔區間
        delta = timedelta(days=7)
        keyword = '影視．消費'
        while after <= before:
            print(after.strftime("%Y-%m-%d"))
            temp_date= after+delta-timedelta(days=1)
            # print(temp_date.strftime("%Y-%m-%d"))
            search = driver.find_element(By.NAME, 'oldSearchString')
            search.send_keys(keyword+"+日期>="+temp_date.strftime("%Y-%m-%d")+"+日期<="+after.strftime("%Y-%m-%d"))
            search.send_keys(Keys.ENTER)
           
            with open(file_name+"_"+after.strftime("%Y-%m-%d")+"_"+temp_date.strftime("%Y-%m-%d")+".txt", "a") as f:
                while start <= page:
                    items = driver.find_elements(By.CLASS_NAME, "control-pic")
                   
                    for item in items:
                        title = item.text
                        print(f'{title}')
                        f.write(convert(title, 'zh-hant')+"\n")
                            
                    else:
                        print('已經沒有下一頁了')
                        after += delta
                        break
                    start=start+1
except NoSuchElementException:
    print('無法定位')
   


driver.quit()