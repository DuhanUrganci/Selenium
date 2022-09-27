
from email.policy import default
from pickle import TRUE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from username import username,password

class Github:
    edge = "C:\drivers\chromedriver.exe"
    def __init__(self):
        self.baseUrl = "https://github.com/"
        self.browser = webdriver.Chrome(executable_path=Github.edge)
        self.username = username
        self.password = password
        self.followersList = []
    # LOGİN
    def signIn(self):
        self.browser.get(self.baseUrl)
        self.browser.maximize_window()
        time.sleep(1)
        sıgnIn = self.browser.find_element(By.LINK_TEXT,"Sign in")
        sıgnIn.click()
        time.sleep(1)
        email = self.browser.find_element(By.NAME,"login")
        email.send_keys(self.username)
        password = self.browser.find_element(By.NAME,"password")
        password.send_keys(self.password)
        time.sleep(1)
        entryBtn = self.browser.find_element(By.NAME,"commit")
        entryBtn.click()
        time.sleep(1)
        self.browser.close()
    # FİNDİNG A REPOS
    def find_repos(self,keyWord):
        self.browser.get(self.baseUrl)
        self.browser.maximize_window()
        searchBox = self.browser.find_element(By.NAME,"q")
        searchBox.send_keys(keyWord)
        time.sleep(1)
        searchBox.send_keys(Keys.ENTER)
        docx = self.browser.page_source
        soup = BeautifulSoup(docx,"html.parser")
        subjectTitle = soup.find(class_="mb-1").text
        topics = soup.find("ul",class_="repo-list").find_all("li","repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source")
        for top in topics:
            author = top.find("a",class_="v-align-middle").text
            link = top.find("a",class_="v-align-middle").get("href")
            desc = top.find("p",class_="mb-1").text.strip("\n")
            repos = {
                "Subject Header":subjectTitle,
                "Author":author,
                "Description":desc,
                "link":self.baseUrl+link
            }
            print(repos)
        time.sleep(1)
        self.browser.close()
    #BRİNGİNG USERS INFORMATION
    def load_followers(self):
        source = self.browser.page_source
        soup = BeautifulSoup(source,"html.parser")
        baseSoup = soup.select(".d-table.table-fixed")
        for base in baseSoup:
            name = base.find_all("span")[1].text
            users = {"name":name}
            self.followersList.append(users)
    #BRİNGİNG IN USERS
    def get_followers(self):
        try:
            self.browser.get(f"{self.baseUrl}sadikturan?tab=followers")
            while True:
                links = self.browser.find_element(By.CLASS_NAME,"pagination").find_elements(By.TAG_NAME,"a")
                if len(links) == 1:
                    if links[0].text == "Next":
                        links[0].click()
                        self.load_followers()
                        time.sleep(2)
                    else:
                        break
                else:
                    for link in links:
                        if link.text == "Next":
                            link.click()
                            self.load_followers()
                            time.sleep(2)
                        else:
                            continue
            print(self.followersList)
            print(len(self.followersList))
        except Exception as e:
            print(e)
        finally:
            print("Done.")
p1 = Github()
# p1.signIn()
# p1.find_repos("Python")
p1.get_followers()