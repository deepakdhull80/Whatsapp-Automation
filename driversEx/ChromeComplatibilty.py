from selenium import webdriver
from urllib3 import request

import requests 
import sys
from selenium.common.exceptions import SessionNotCreatedException
if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile


from jproperties import Properties

class ChromeComplatibility:
    def __init__(self):
        self.driver=None
        self.chromeVersion=None
        self.config = Properties()

        self.dir = "driversEx"
        self.fileName="chromedriver_win32.zip"
        
        # path= {chromeVersion}
        self.driverDownloadUrl = None
        
        try:
            self.driver = webdriver.Chrome(self.dir+"/chromedriver")
            self.chromeVersion=self.driver.capabilities['browserVersion']
            self.driver.close()
        except SessionNotCreatedException as e:
            print("___________________________________________________")
            self.chromeVersion = e.args[0].split("Current browser version is ")[1].split(" ")[0]
            print("Compatible error")

        self.driverDownloadUrl = "https://chromedriver.storage.googleapis.com/"+self.chromeVersion+"/"+self.fileName
        
        f=open(self.dir+"/application.properties",'r+b')

        self.config.load(f)
        f.close()
        

        self.checkVersion()

        
    def checkVersion(self):
        
        version = self.config.get("version").data

        print("browser version: "+self.chromeVersion)
        print("old version : "+version)

        if(version!=self.chromeVersion):
            # update version and download new browser version driver
            print("version isn't compatible.")

            self.downloadWebDriver()

            self.extractFile()

            self.changeDriverVersion()

        else:
            print("Version is complatible.")



    

    def downloadWebDriver(self):
        print("wait for some minutes")
        
        flie = downloadFile(self.driverDownloadUrl)
        
        print("driver downloaded.")

    def extractFile(self):
        with zipfile.ZipFile(self.dir+"/"+self.fileName, 'r') as zip_ref:
            zip_ref.extractall(self.dir)
    

    def changeDriverVersion(self):

        data = "version="+self.chromeVersion
        
        with open(self.dir+"/application.properties",'w') as f:
            f.write(data)


def downloadFile(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open("driversEx/"+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

def check():
    obj = ChromeComplatibility()

