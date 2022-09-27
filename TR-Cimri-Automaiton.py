
from username import username,password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import json

class Cimri:
    edge = "C:\drivers\msedgedriver.exe"
    def __init__(self):
        self.browser = webdriver.Edge(executable_path=Cimri.edge)
        self.baseUrl = "https://www.cimri.com/uyelik/giris-yap"
        self.userName = username
        self.password = password
        self.productList = []
    #LOGİN
    def sıgn_In(self):
        self.browser.get(self.baseUrl)
        time.sleep(1)
        emailBox = self.browser.find_element(By.NAME,"email")
        emailBox.send_keys(self.userName)
        time.sleep(1)
        passwordBox = self.browser.find_element(By.NAME,"password")
        passwordBox.send_keys(self.password)
        passwordBox.send_keys(Keys.ENTER)
        time.sleep(2)
    #SEARCHİNG
    def searching(self):
        self.browser.get("https://www.cimri.com/")
        time.sleep(1)
        self.browser.refresh()
        time.sleep(2)
        searchBox = self.browser.find_element(By.TAG_NAME,"input")
        searchBox.send_keys("Biker Bot")
        time.sleep(2)
        searchBox = self.browser.find_elements(By.TAG_NAME,"button")[3]
        searchBox.click()
    # PRİNTİNG TO A FİLE
    def print_to_file(self):
        with open("cimri-products.json","w",encoding="utf-8") as file:
            json.dump(self.productList,file,ensure_ascii=False,indent=1)
    #UPLOADING DATA
    def load_documents(self):
        self.browser.refresh()
        time.sleep(3)
        docx = self.browser.page_source
        soup = BeautifulSoup(docx,"html.parser")
        elements = soup.find_all("div",id="cimri-product")
        for elem in elements:
            proName = elem.find("a",class_="link-detail").get("title")
            priceList = elem.find_all("a",class_="s14oa9nh-0 lihtyI")
            base = elem.find("div",class_="top-offers").text
            if base == "En Ucuz Fiyatlarla Yakında Cimri.com'da":
                print("The Product Has Not Yet Gone On Sale")
            else:
                if len(priceList) == 1:
                    dealer = elem.find("div",class_="tag").text
                    price = priceList[0].get_text().strip(dealer)
                    base = {
                            "Product" : proName,
                            "Salesman 11" : dealer,
                            "Price" : price
                            }
                    self.productList.append(base)
                    print(base)
                else:
                    dealer1 = elem.find_all("div",class_="tag")[0].text
                    dealer2 = elem.find_all("div",class_="tag")[1].text
                    price1 = priceList[0].get_text().strip(dealer1)
                    if (dealer1 or dealer2) == "n11.com":
                        price3 = priceList[1].get_text().strip("n11.com").strip(dealer2).strip(dealer1)
                        base = {
                            "Product" : proName,
                            "Salesman 1" : dealer1,
                            "Initial Price" : price1,
                            "Salesman 2" : dealer2,
                            "The Second Price" : price3
                            }
                        self.productList.append(base)
                        print(base)
                    else:
                        price2 = priceList[1].get_text().strip("n11.com").strip(dealer2).strip(dealer1)
                        base = {
                            "Product" : proName,
                            "Salesman 1" : dealer1,
                            "Initial Price" : price1,
                            "Salesman 2" : dealer2,
                            "The Second Price" : price2
                            }
                        self.productList.append(base)
                        print(base)
    #FETCHING DATA
    def get_documents(self):
        try:
            self.searching()
            while True:
                firstPageElements = self.browser.find_elements(By.CSS_SELECTOR,"div.s1pk8cwy-1.kxoiYk")
                for el in firstPageElements:
                    a = el.find_elements(By.TAG_NAME,"path")
                    a[1].click()
                    self.load_documents()
                    self.print_to_file()
        except Exception as e:
            print(e)
        finally:
            print("Done")

p1 = Cimri()
# p1.searching()
# p1.load_documents()
p1.get_documents()