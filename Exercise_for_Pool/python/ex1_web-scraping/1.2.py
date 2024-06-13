from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd

Shop_Name_List_Sum = []
Shop_Call_List_Sum = []
Shop_Mail_List_Sum = []
prefecture_list_Sum = []
municipalities_list_Sum = []
number_list_Sum = []
building_list_Sum = []
Shop_URL_List_Sum = []
Shop_SSL_List_Sum = []

url = 'https://r.gnavi.co.jp/area/jp/rs/'
chrome_options = Options()
chrome_options.add_argument("--user-agent=YUKi pythonCrawler/1.0.0 (yuki71246402@gmail.com)")
driver = webdriver.Chrome(options = chrome_options)
get_info = driver.get(url)

def Link_Access(): #店舗一覧から店舗の詳細ページのリンクを得る
    Shop_Link_List = []
    for i in range(21):
        if not i == 3:
            Shop_Link = driver.find_element(By.CSS_SELECTOR,'#__next > div > div.layout_body__LvaRc > main > div.style_resultRestaurant__WhVwP > div:nth-of-type(2) > div:nth-of-type({}) > article > div.style_title___HrjW > a'.format(i+1))
            Shop_Link_List.append(Shop_Link.get_attribute('href'))
        else:
            Shop_Link_List.append(None)
    return Shop_Link_List

def GetShopInfo(): #詳細ページから店舗の情報を抽出する
    Shop_Name_List = []
    Shop_Call_List = []
    Shop_Mail_List = []
    Shop_Adress_List = []
    prefecture_list = []
    municipalities_list = []
    number_list = []
    building_list = []
    Shop_URL_List = []
    Shop_SSL_List = []
    for i in range(21):
        if not i == 3:
            time.sleep(3)
            driver.get(Shop_Link_Access[i])
            #店舗の名前を取得してリストに格納する
            Shop_Info_Table = driver.find_element(By.CLASS_NAME,"basic-table")
            Shop_Name = Shop_Info_Table.find_element(By.ID,"info-name").text
            Shop_Name_List.append(Shop_Name)

            #店舗の電話番号を取得してリストに格納する
            Shop_Info_Table = driver.find_element(By.CLASS_NAME,"basic-table")
            Shop_Call = Shop_Info_Table.find_element(By.ID, "info-phone").find_element(By.CLASS_NAME, "number").text
            Shop_Call_List.append(Shop_Call)

            #店舗のメールアドレスを取得してリストに格納する
            try:
                email_get = driver.find_element(By.XPATH, '//a[contains(@href, "mailto:")]')
                email = email_get.get_attribute("href").split(":")[1]
                Shop_Mail_List.append(email)
            except:
                email = None
                Shop_Mail_List.append(email)

            #店舗の住所を取得してリストに格納する
            Shop_Adress = driver.find_element(By.CSS_SELECTOR, "p.adr.slink")
            Shop_Adress_List.append(Shop_Adress.find_element(By.CLASS_NAME, "region").text)
            if __name__ == '__main__':
                address = Shop_Adress_List[i]
                matches = re.match(r'(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村|宮古|富良野|別府|佐伯|黒部|小諸|塩尻|玉野|周南)市|(?:余市|高市|[^市]{2,3}?)郡(?:玉村|大町|.{1,5}?)[町村]|(?:.{1,4}市)?[^町]{1,4}?区|.{1,7}?[市町村])(.+)' , address)
                prefecture_list.append(matches[1])
                municipalities_list.append(matches[2])
                number_list.append(matches[3])
            try:
                building_name = Shop_Adress.find(class_ = 'locality').get_text()
                building_list.append(building_name)
            except:
                    building_name = None
                    building_list.append(building_name)
            else:
                Shop_Adress_List.append(None)

            #店舗のURLとSSLの有無を取得してリストに格納する
            try:
                Shop_URL_Info = driver.find_element(By.CSS_SELECTOR, '#sv-site > li > a')
                Shop_URL = Shop_URL_Info.get_attribute('href')
            except:
                None

            if Shop_URL.startswith("http://"):
                Shop_SSL = False
            else:
                Shop_SSL = True

            Shop_URL_List.append(Shop_URL)
            Shop_SSL_List.append(Shop_SSL)
        else:
            Shop_Adress_List.append(None)

    return Shop_Name_List, Shop_Call_List, Shop_Mail_List, prefecture_list, municipalities_list, number_list, building_list, Shop_URL_List, Shop_SSL_List

for j in range(3):
    get_info = driver.get(url)
    Shop_Link_Access = Link_Access()
    Shop_Name_List, Shop_Call_List, Shop_Mail_List, prefecture_list, municipalities_list, number_list, building_list, Shop_URL_List, Shop_SSL_List = GetShopInfo()

    Shop_Name_List_Sum += Shop_Name_List
    Shop_Call_List_Sum += Shop_Call_List
    Shop_Mail_List_Sum += Shop_Mail_List
    prefecture_list_Sum += prefecture_list
    municipalities_list_Sum += municipalities_list
    number_list_Sum += number_list
    building_list_Sum += building_list
    Shop_URL_List_Sum += Shop_URL_List
    Shop_SSL_List_Sum += Shop_SSL_List
    driver.get(url)
    Next_Page_Link = driver.find_element(By.CSS_SELECTOR,"#__next > div > div.layout_body__LvaRc > main > div.style_pageNation__AZy1A > nav > ul > li:nth-child(10) > a")
    next_page_url = Next_Page_Link.get_attribute('href')
    url = next_page_url
    Next_Page_Link.click()
    WebDriverWait(driver, 10).until(EC.url_to_be(url))

data = {'店舗名': Shop_Name_List_Sum[:50], '電話番号': Shop_Call_List_Sum[:50], 'メールアドレス':Shop_Mail_List_Sum[:50], '都道府県':prefecture_list_Sum[:50], '市区町村':municipalities_list_Sum[:50], '番地':number_list_Sum[:50], '建物名':building_list_Sum[:50], 'URL':Shop_URL_List_Sum[:50], 'SSL':Shop_SSL_List_Sum[:50]}
dateframe = pd.DataFrame(data)
dateframe.to_csv('Exercise_for_Pool/python/ex1_web-scraping/1-2.csv', index=False, encoding="utf-8-sig")
