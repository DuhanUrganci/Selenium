from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from username import username,password
from bs4 import BeautifulSoup
import json
class Trendyol:
    edge = "C:\drivers\msedgedriver.exe"
    def __init__(self):
        self.baseUrl = "https://www.trendyol.com/giris"
        self.browser = webdriver.Edge(executable_path=Trendyol.edge)
        self.username = username
        self.password = password
        self.productList = []
    #LOGİN
    def sıgn_In(self):
        self.browser.get(self.baseUrl)
        time.sleep(1)
        emailBox = self.browser.find_element(By.NAME,"login email")
        emailBox.send_keys(self.username)
        time.sleep(1)
        passwordBox = self.browser.find_element(By.NAME,"login-password")
        passwordBox.send_keys(self.password)
        time.sleep(1)
        passwordBox.send_keys(Keys.ENTER)
        time.sleep(1)
    #SEARCHİNG
    def searching(self):
        self.sıgn_In()
        time.sleep(3)
        self.browser.refresh()
        time.sleep(1)
        searchBox = self.browser.find_element(By.CLASS_NAME,"search-box")
        searchBox.send_keys("Android Telefon")
        time.sleep(1) 
        searchBox.send_keys(Keys.ENTER)
        time.sleep(2)
    # Bring The Documents
    def load_documents(self):
        docx =  self.browser.page_source
        soup = BeautifulSoup(docx,"html.parser")
        elements = soup.find("div",class_="prdct-cntnr-wrppr").find_all("div",class_="p-card-wrppr with-campaign-view")
        for el in elements:
            markable = el.find("span",class_="prdct-desc-cntnr-ttl").text
            name = el.find("span",class_="prdct-desc-cntnr-name hasRatings").text
            price = float(el.find_all("div",class_="prc-box-dscntd")[0].text.strip("TL ")[:5])
            base = {
                "marka":markable,
                "isim":name,
                "fiyat":price
            } 
            self.productList.append(base)
        print(len(self.productList))
    # Print to File
    def print_to_file(self):
        with open("trend-products.json","w",encoding="utf-8") as file:
            json.dump(self.productList,file,ensure_ascii=False,indent=1)
    # Bring The Documents
    def get_documents(self):
        try:
            self.searching()
            time.sleep(10)
            self.browser.refresh()
            time.sleep(3)
            priceBtn = self.browser.find_element(By.CSS_SELECTOR,"#sticky > div > div:nth-child(5) > div.fltr-cntnr-ttl-area > div.i-dropdown-arrow")
            priceBtn.click()
            time.sleep(5)
            minPrice = self.browser.find_element(By.CSS_SELECTOR,"#sticky > div > div:nth-child(5) > div:nth-child(2) > div > input.fltr-srch-prc-rng-input.min")
            minPrice.send_keys("1000")
            time.sleep(6)
            priceSearch = self.browser.find_element(By.CSS_SELECTOR,"#sticky > div > div:nth-child(5) > div:nth-child(2) > div > button")
            priceSearch.click()
            time.sleep(6)
            i = 0
            #I kept it limited because the Product Scale is very Large
            while i <= 4:
                i+=1
                self.browser.execute_script('window.scrollBy(0,3000);')
                time.sleep(5)
            self.load_documents()
            self.print_to_file()
            time.sleep(2)
            self.browser.close()
        except Exception as e:
            print(e)
        finally:
            print("Done.")

p1 = Trendyol()
# p1.sıgn_In()
# p1.searching()
# p1.load_documents()
p1.get_documents()
