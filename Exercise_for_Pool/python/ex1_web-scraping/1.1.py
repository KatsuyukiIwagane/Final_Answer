import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import time

Shop_Name_List_Sum = []
Shop_Call_List_Sum = []
Shop_Mail_List_Sum = []
prefecture_list_Sum = []
municipalities_list_Sum = []
number_list_Sum = []
building_list_Sum = []
headers = {'User-Agent':'YUKi pythonCrawler/1.0.0 (yuki71246402@gmail.com)'}

url = 'https://r.gnavi.co.jp/area/jp/rs/?p=1'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content)

def Link_Access(): #店舗一覧から店舗の詳細ページのリンクを得る
    Shop_Link_List = []
    for i in range(21):
        if not i == 3:
            Shop_Link = soup.select('#__next > div > div.layout_body__LvaRc > main > div.style_resultRestaurant__WhVwP > div:nth-of-type(2) > div:nth-of-type({}) > article > div.style_title___HrjW > a'.format(i+1))
            Shop_Link_List.append(Shop_Link[0].attrs['href'])
        else:
            Shop_Link_List.append(None)
    return Shop_Link_List
Shop_Link_Access = Link_Access()


def GetShopInfo(): #詳細ページから店舗の情報を抽出する
    Shop_Name_List = []
    Shop_Call_List = []
    Shop_Mail_List = []
    Shop_Adress_List = []
    prefecture_list = []
    municipalities_list = []
    number_list = []
    building_list = []
    for i in range(21):
        if not i == 3:
            time.sleep(3)
            sourse = requests.get(Shop_Link_Access[i])
            soup_sourse = BeautifulSoup(sourse.content)
            #店舗の名前を取得してリストに格納する
            Shop_Name = soup_sourse.select('#info-table > table > tbody > tr:nth-child(1)')
            Shop_Name_List.append(Shop_Name[0].find('p').text)

            #店舗の電話番号を取得してリストに格納する
            Shop_Call = soup_sourse.select('#info-phone > td > ul > li:nth-child(1) > span.number')
            Shop_Call_List.append(Shop_Call[0].contents[0])

            #店舗のメールアドレスを取得してリストに格納する
            email_search = re.compile(r'^mailto:(.+)$')
            email_get = soup_sourse.find('a', href = email_search)
            if email_get:
                email = email_search.match(email_get['href']).group(1)
                Shop_Mail_List.append(email)
            else:
                email = None
                Shop_Mail_List.append(email)

            #店舗の住所を取得してリストに格納する
            Shop_Adress = soup_sourse.select('#info-table > table > tbody > tr:nth-child(3) > td > p > span.region')
            Shop_Adress_List.append(Shop_Adress[0].contents[0])
            if __name__ == '__main__':
                address = Shop_Adress_List[i]
                matches = re.match(r'(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村|宮古|富良野|別府|佐伯|黒部|小諸|塩尻|玉野|周南)市|(?:余市|高市|[^市]{2,3}?)郡(?:玉村|大町|.{1,5}?)[町村]|(?:.{1,4}市)?[^町]{1,4}?区|.{1,7}?[市町村])(.+)' , address)
                prefecture_list.append(matches[1])
                municipalities_list.append(matches[2])
                number_list.append(matches[3])
            try:
                building_name = soup_sourse.find(class_ = 'locality').get_text()
                building_list.append(building_name)
            except:
                    building_name = None
                    building_list.append(building_name)
        else:
            Shop_Adress_List.append(None)
    return Shop_Name_List, Shop_Call_List, Shop_Mail_List, prefecture_list, municipalities_list, number_list, building_list

Shop_Name_List, Shop_Call_List, Shop_Mail_List, prefecture_list, municipalities_list, number_list, building_list = GetShopInfo()

for j in range(3):
    url = 'https://r.gnavi.co.jp/area/jp/rs/?p={}'.format(j+1)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content)
    Shop_Link_Access = Link_Access()
    GetShopInfo()
    Shop_Name_List_Sum += Shop_Name_List
    Shop_Call_List_Sum += Shop_Call_List
    Shop_Mail_List_Sum += Shop_Mail_List
    prefecture_list_Sum += prefecture_list
    municipalities_list_Sum += municipalities_list
    number_list_Sum += number_list
    building_list_Sum += building_list

#URLとSSLの取得は不可であるためNoneを返す
URL_List = [None for i in range(50)]
SSL_List = [None for i in range(50)]

data = {'店舗名': Shop_Name_List_Sum[:50], '電話番号': Shop_Call_List_Sum[:50], 'メールアドレス':Shop_Mail_List_Sum[:50], '都道府県':prefecture_list_Sum[:50], '市区町村':municipalities_list_Sum[:50], '番地':number_list_Sum[:50], '建物名':building_list_Sum[:50], 'URL':URL_List, 'SSL':SSL_List}
dateframe = pd.DataFrame(data)
dateframe.to_csv('Exercise_for_Pool/python/ex1_web-scraping/1.1.csv', index=False, encoding="utf-8-sig")
