import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory

import re, os, zipfile, io



class Download_loan_data(luigi.Task):
    

  def requires(self):
    return []
 
  def output(self):
    # return luigi.LocalTarget("downloads/sample_orig_2016.txt", "downloads/sample_svcg_2016.txt")
    return { 'output1' : luigi.LocalTarget("downloads/sample_orig_2016.txt") ,'output2' : luigi.LocalTarget("downloads/sample_svcg_2016.txt"),\
                'output3' : luigi.LocalTarget("downloads/sample_orig_2015.txt") ,'output4' : luigi.LocalTarget("downloads/sample_svcg_2015.txt"),\
                'output5' : luigi.LocalTarget("downloads/sample_orig_2014.txt") ,'output6' : luigi.LocalTarget("downloads/sample_svcg_2014.txt"),\
                'output7' : luigi.LocalTarget("downloads/sample_orig_2013.txt") ,'output8' : luigi.LocalTarget("downloads/sample_svcg_2013.txt"),\
                'output9' : luigi.LocalTarget("downloads/sample_orig_2012.txt") ,'output10' : luigi.LocalTarget("downloads/sample_svcg_2012.txt"),\
                'output11' : luigi.LocalTarget("downloads/sample_orig_2011.txt") ,'output12' : luigi.LocalTarget("downloads/sample_svcg_2011.txt"),\
                'output13' : luigi.LocalTarget("downloads/sample_orig_2010.txt") ,'output14' : luigi.LocalTarget("downloads/sample_svcg_2010.txt"),\
                'output15' : luigi.LocalTarget("downloads/sample_orig_2009.txt") ,'output16' : luigi.LocalTarget("downloads/sample_svcg_2009.txt"),\
                'output17' : luigi.LocalTarget("downloads/sample_orig_2008.txt") ,'output18' : luigi.LocalTarget("downloads/sample_svcg_2008.txt"),\
                'output19' : luigi.LocalTarget("downloads/sample_orig_2007.txt") ,'output20' : luigi.LocalTarget("downloads/sample_svcg_2007.txt"),\
                'output21' : luigi.LocalTarget("downloads/sample_orig_2006.txt") ,'output22' : luigi.LocalTarget("downloads/sample_svcg_2006.txt"),\
                'output23' : luigi.LocalTarget("downloads/sample_orig_2005.txt") ,'output24' : luigi.LocalTarget("downloads/sample_svcg_2005.txt"),\
                'output25' : luigi.LocalTarget("downloads/sample_orig_2004.txt") ,'output26' : luigi.LocalTarget("downloads/sample_svcg_2004.txt"),\
                'output27' : luigi.LocalTarget("downloads/sample_orig_2003.txt") ,'output28' : luigi.LocalTarget("downloads/sample_svcg_2003.txt"),\
                'output29' : luigi.LocalTarget("downloads/sample_orig_2002.txt") ,'output30' : luigi.LocalTarget("downloads/sample_svcg_2002.txt"),\
                'output31' : luigi.LocalTarget("downloads/sample_orig_2001.txt") ,'output32' : luigi.LocalTarget("downloads/sample_svcg_2001.txt"),\
                'output33' : luigi.LocalTarget("downloads/sample_orig_2000.txt") ,'output34' : luigi.LocalTarget("downloads/sample_svcg_2000.txt"),\
                'output35' : luigi.LocalTarget("downloads/sample_orig_1999.txt") ,'output36' : luigi.LocalTarget("downloads/sample_svcg_1999.txt")}
 
  def run(self):
    url = "https://freddiemac.embs.com/FLoan/secure/login.php"

    myusername = 'palecanda.t@husky.neu.edu'
    mypassword = '9C||3T{w'

    # Create Browser
    browser = mechanicalsoup.Browser()

    login_page = browser.get(url)
    login_form = login_page.soup.find('form', {"name":"loginform"})
    login_form.find("input", {"name" : "username"})["value"] = myusername
    login_form.find("input", {"name" : "password"})["value"] = mypassword

    # Logging in 
    response = browser.submit(login_form, login_page.url)
    termsPage = response.soup.find("html")

    # confirming login
    h2 = termsPage.find("h2")

    if not (h2.text == "Loan-Level Dataset"):
      print("Please check your credentials to login")
    else:
      termsForm = termsPage.find('form')
      termsForm.find("input", {"name" : "accept"})["checked"] = True

          # Submitting form on terms and conditions page
      response = browser.submit(termsForm, response.url)

      dataPage = response.soup.find("html")

      table = dataPage.find("table", {"class" : "table1"})
      # print(tables)

      files = []
      for row in table.findAll('tr'):
                 
        try:
          data = row.findAll('td')
          file = [data[0].string, data[0].a['href'], data[2].string]
          files.append(file)
        except:
          pass

      files = pd.DataFrame(data=files, columns = ["fileName","downloadURL","fileSize"])
      # print(files)

      pattern = r'download.php'
      downloadURL = re.sub(pattern, "", response.url)

      create_directory("downloads")
      dir = "downloads/"
      for index, row in files.iterrows():
        # Check if its a sample file
        if("sample_" in row['fileName']):
        # Get url for sample file
          fileURL = downloadURL + row['downloadURL']
          year = re.search(r'sample_(.+?).zip', row['fileName']).group(1)
          filePath1 = dir + "sample_orig_" + year + ".txt" 
          filePath2 = dir + "sample_svcg_" + year + ".txt"
          print(filePath1 + filePath2)
          # print(fileURL)
          # Check if sample file exists in the directory, and download if doesnt
          if not (os.path.isfile(filePath1) & os.path.isfile(filePath2)):
            zf = browser.get(fileURL)
            # open("filePath", "w").write(response.read()).close()
            z = zipfile.ZipFile(io.BytesIO(zf.content))
            z.extractall(path=dir)
    print("Data downloaded")        