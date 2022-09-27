
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from username import username,password
import time
from bs4 import BeautifulSoup
import requests
class Amazon:
    driver_chrome = "C:\drivers\chromedriver.exe"
    def __init__(self):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(executable_path=Amazon.driver_chrome)
        self.baseUrl = "https://www.amazon.com.tr/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com.tr%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=trflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
        self.productList = []
    # LOGIN
    def sıgn_ın(self):
        self.browser.get(self.baseUrl)
        emailBox = self.browser.find_element(By.NAME,"email")
        emailBox.send_keys(self.username)
        emailBox.send_keys(Keys.ENTER)
        time.sleep(3)
        passwordBox = self.browser.find_element(By.NAME,"password")
        passwordBox.send_keys(self.password)
        time.sleep(2)
        entrySide = self.browser.find_element(By.ID,"signInSubmit")
        entrySide.click()
    #SEARCHİNG
    def searching(self):
        self.sıgn_ın()
        time.sleep(2)
        searchBox = self.browser.find_element(By.ID,"twotabsearchtextbox")
        searchBox.send_keys("The Word You Wanted to Search")
        time.sleep(2)
        searchİcon = self.browser.find_element(By.ID,"nav-search-submit-button")
        searchİcon.click()
    #Printing to a File
    def print_to_file(self):
        import json
        with open("Amazon-Automation.json","w",encoding="utf-8",newline="") as file:
            json.dump(self.productList,file,ensure_ascii=False,indent=1)
    #Getting the Contents
    def load_documents(self):
        while True:
            codeStat = requests.get(self.browser.current_url)
            codeNumber = codeStat.status_code
            if codeNumber == 503:
                self.browser.refresh()
                print(codeNumber)
            elif codeNumber == 200:
                print(codeNumber)
                if codeNumber == 200:
                    pageDoc = self.browser.page_source
                    docx = BeautifulSoup(pageDoc,"html.parser")
                    baseElement = docx.find_all("div",class_="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20")
                    for base in baseElement:
                        priceSide = base.find("div",class_="a-section a-spacing-none a-spacing-top-small s-price-instructions-style")
                        if priceSide != None: 
                            name = base.h2.text
                            price = docx.find(class_="a-price-whole").text.replace(",","TL")
                            base = {
                                "Name":name,
                                "Price":price
                            }
                            self.productList.append(base)
                        else:
                            name = base.h2.text
                            base = {
                                "Name":name,
                                "Price":"The Product Has No Price Information"
                            }
                            self.productList.append(base)
                    break
                elif codeNumber == 503:
                    continue
                else:
                    break
            else:
                continue
    #Fetching the Contents
    def get_documents(self):
        try:
            self.searching()
            time.sleep(1)
            while True:
                time.sleep(1)
                pageBox = self.browser.find_elements(By.CSS_SELECTOR,"div.a-section.a-text-center.s-pagination-container")
                for page in pageBox:
                    nextPage = page.find_element(By.CSS_SELECTOR,"a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")
                    nextPage.click()
                    self.load_documents()
                    self.print_to_file()
        except Exception as e:
            print(e)
        finally:
            print("Done.")
p1 = Amazon()
p1.get_documents()
