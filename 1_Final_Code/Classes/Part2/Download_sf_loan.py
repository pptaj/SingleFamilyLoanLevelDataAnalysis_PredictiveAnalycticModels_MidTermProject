import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
# import getpass

import re, os, zipfile, io



class Download_loan_data(luigi.Task):
    

  def requires(self):
    return []
 
  def output(self):
    # return luigi.LocalTarget("downloads/sample_orig_2016.txt", "downloads/sample_svcg_2016.txt")
    return { 'output1' : luigi.LocalTarget("downloads/downloaded.txt")\
                


                }
 
  def run(self):
    url = "https://freddiemac.embs.com/FLoan/secure/login.php"

    # myusername = 'palecanda.t@husky.neu.edu'
    # mypassword = '9C||3T{w'

    myusername = input("Enter your username: ")
    mypassword = input("Enter your password: ")
    year = 0
    quarter = 0

    # mypassword = getpass("Enter your password: ")
    
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
      print("Please check your credentials to login and try again")
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

      # TAKE YEAR AND QUARTER FROM USER
      while(year not in range(1999,2017) or quarter not in range(2, 5)):
      	year = input("Please enter the year for which you want to run the model: ")
      	quarter = input("Please enter the quarter for which you want to predict (2nd,3rd or 4th): ")

      	try:
      		year = int(year)
      		quarter = int(quarter)
      	except:
      		print("Please enter a valid year and quarter")
      		year = 0
      		quarter = 0
      		pass

      files = pd.DataFrame(data=files, columns = ["fileName","downloadURL","fileSize"])
      # print(files)

      pattern = r'download.php'
      downloadURL = re.sub(pattern, "", response.url)

      create_directory("downloads")
      dir = "downloads/"
      filePath1 = "historical_data1_Q" + str(quarter-1) + str(year) 
      filePath2 = "historical_data1_time_Q" + str(quarter-1) + str(year)
      filePath3 = "historical_data1_Q" + str(quarter) + str(year)
      filePath4 = "historical_data1_time_Q" + str(quarter) + str(year)
      fs = [filePath1, filePath2, filePath3, filePath4]

      for index, row in files.iterrows():
      	for f in fs:
      		if(f in row['fileName']):
      			fileURL = downloadURL + row['downloadURL']
      			if not (os.path.isfile(dir + f + '.txt')):
      				zf = browser.get(fileURL)
      				z = zipfile.ZipFile(io.BytesIO(zf.content))
      				z.extractall(path=dir)

      if (os.path.isfile(dir + filePath1 + '.txt') & os.path.isfile(dir +filePath2 + '.txt') & os.path.isfile(dir + filePath3 + '.txt') & os.path.isfile(dir + filePath4 + '.txt') ):
          	file = open(dir + 'downloaded.txt', 'w+')
          	file.close()
          	file = open(dir+ str(quarter)+str(year), 'w+')
          	file.close()
          	print("Data downloaded")        