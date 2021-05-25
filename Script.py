from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from get_gecko_driver import GetGeckoDriver

import time
import os
import pandas as pd 
import requests
import subprocess



class WhatsappAutomation:


    def __init__(self,filePath="Files/user_names.csv",messageFile="Files/message.txt",initialSleep=6,BaseDir = ""):
        #validators

        if self.checkInternetConnection()==False:
            print("Please Check your internet connection...")
            time.sleep(3)
            exit()
        
        self.fileExist(filePath)
        self.fileExist(messageFile)

        #------------------------------------------
        self.attachmentBaseDir= BaseDir+"\\attachment\\"
        # self.attachmentBaseDir = os.curdir+"/"
        self.filePath = filePath
        self.Controller = None
        self.initialSleep = initialSleep
        self.messageFile = messageFile
        self.attachmentFileName = self.getAttachmentFileName()

    def getAttachmentFileName(self):
        try:
            files = os.listdir(self.attachmentBaseDir)
            return files[0]
        except :
            return ""
    def checkInternetConnection(self):
        # check internet connection if yes return True else False
        
        try:
            if requests.get('https://www.google.com/').status_code ==200:
                return True
            else:
                return False
        except:
            return False
    
    def fileExist(self,filePath):
        #filepath is valid or not.
        try:
            with open(filePath,'r') as file:
                file.tell()
                return 
        except Exception:
            
            print("*",filePath," file not found in Files")
            time.sleep(3)
            exit()
    
    def sendFile(self,attachmentPath):
        # arg1: attachment path

        try:
            open(attachmentPath,'rb')
            # print("file Exist")
            self.Controller.find_element_by_xpath("//span[@data-icon='clip']").click()

            self.Controller.find_element_by_xpath("//span[@data-icon='attach-document']").click()

            # print("clip")
            
            os.system("upload.exe "+attachmentPath)
            # WebDriverWait(self.Controller, 2).until(EC.presence_of_element_located((By.XPATH,"//span[@data-icon='send']" ))
            WebDriverWait(self.Controller , 20).until(EC.presence_of_element_located((By.XPATH,"//span[@data-icon='send']")))
            time.sleep(1)
            # class="SncVf _3doiV"
            self.Controller.find_element_by_xpath("//div[@class='SncVf _3doiV']").click()
            time.sleep(2)
            # WebDriverWait(self.Controller , 20).until(EC.presence_of_element_located((By.XPATH,"//span[@data-icon='audio-download']")))
            # print("done")
                    
        except:
            print("Attachment is not selected...")
 
    def runBrowser(self):
        try:
            #firefox connectivity
            # get_driver = GetGeckoDriver()
            # get_driver.install()
            # self.Controller = webdriver.Firefox(executable_path=r'drivers/geckodriver')

            #chrome connectivity.
            self.Controller = webdriver.Chrome("drivers/chromedriver")

            self.Controller.maximize_window()
        except Exception as e:
            print("Check your Chrome browser...")
            time.sleep(3)
            print(str(e))
            exit()
     
    def readMessage(self):
        with open(self.messageFile,'r',encoding="utf-8") as file:
            message =  file.read()
            message.replace("\n"," ")
            tt=""
            for i in message:   
                if(i!="\n"):
                    tt+=i
            message = tt

            newMessage = []
            for val in message.split(" "):
                newMessage.append(val)
            return " ".join(newMessage)

    def readUsers(self):
        userFile = pd.read_csv(self.filePath)
        # print(userFile)
        userList = userFile['name'].tolist()
        return userList

    def checkWebSite(self, url):
        try:
            if not requests.get(url).status_code==200:
                print("Check URL passing in driver method.")
                time.sleep(3)
                exit()
        except :
            print("Check URL passing in driver method.")
            time.sleep(3)
            exit()
        return True


    # Main Runner
    def open(self, website=""):
        

        #check website 
        self.checkWebSite(website)

        self.runBrowser()


        #running driver and open Chrome
        self.Controller.get(website)

        #get all user to whom we have to send data
        userList = self.readUsers()
        
        # read message which is send to the users
        message = self.readMessage()
        # time.sleep(10)
        # firstTimeLap = 1
        # print("enter to send Messages to users.")
        delay = 600 # seconds
        WebDriverWait(self.Controller, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='{}']".format("_2_1wd copyable-text selectable-text"))))
        
        searchBar = self.Controller.find_element_by_xpath("//div[@class='{}']".format("_2_1wd copyable-text selectable-text"))
        
        for name in userList:
            # find user name and proceed with validation
            if name is None or not isinstance(name,str) or len(name)==0:
                continue
            
            try:
                # search user is necessory due to whatsapp dynamic loading of content.
                searchBar.send_keys(name)
                # time.sleep(2)

                #wait until user loaded
                WebDriverWait(self.Controller, 2).until(EC.presence_of_element_located((By.XPATH, "//span[@title='{}']".format(name))))
                user = self.Controller.find_element_by_xpath("//span[@title='{}']".format(name))
                user.click()
                time.sleep(2)
                
                # find message BOx
                # WebDriverWait(self.Controller, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"_2A8P4")))
                messageBox = self.Controller.find_element_by_class_name("_2A8P4")


                # write message in box
                # print(message)
                messageBox.send_keys(message)
                # print("message Typed")
                # press send btn
                # time.sleep(1)
                sendBtn = self.Controller.find_element_by_class_name("_1E0Oz")
                sendBtn.click()
                # time.sleep(1)
                print("Message sent to :",name)
                
                #attachment functionality is unimplemented

                if len(self.attachmentFileName)>0:
                    print("Send attachment.")
                    self.sendFile(self.attachmentBaseDir+ self.attachmentFileName)

            except Exception as e:
                # searchBar.send_keys("")
                #find back arrow
                self.Controller.find_element_by_xpath("//button[@class='_1Ek-U']").click()
                print("User not found "+name)
                # time.sleep(1)
                print(str(e))

        print("Task Completed.")
        self.Controller.close()
        

# driver code

if __name__ =='__main__':
    obj = WhatsappAutomation(BaseDir="D:\\WORK\\Python\\Whatsapp_Automation")
    # print(obj.readMessage())

    obj.open("https://web.whatsapp.com/")
    # obj.open()
    
        


