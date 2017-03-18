import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
from Classes.clean_orig import Clean_origination_data
from Classes.Download_sf_loan import Download_loan_data
import re, os, zipfile, io

# _______________________________________________________________________________________________________________________
class Clean_performance_data(luigi.Task):
  def requires(self):
    return[Clean_origination_data()]

  def output(self):
    return{ 'output1' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2016.csv") ,\
                'output2' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2015.csv") ,\
                'output3' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2014.csv") ,\
                'output4' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2013.csv") ,\
                'output5' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2012.csv") ,\
                'output6' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2011.csv") ,\
                'output7' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2010.csv") ,\
                'output8' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2009.csv") ,\
                'output9' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2008.csv") ,\
                'output10' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2007.csv") ,\
                'output11' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2006.csv") ,\
                'output12' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2005.csv") ,\
                'output13' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2004.csv") ,\
                'output14' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2003.csv") ,\
                'output15' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2002.csv") ,\
                'output16' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2001.csv") ,\
                'output17' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_2000.csv") ,\
                'output18' : luigi.LocalTarget("cleaned/cleaned_sample_svcg_1999.csv") }

  def run(self):
    create_directory("cleaned")
    cleaned_dir = "cleaned/"
    downloads_dir = "downloads/"
    
    
      
    # Itereate through all the years. Check if the cleaned file exists! If not Read the downloads csv and Clean it. And Place it in the cleaned directory
    for i in range(1999,2017):
      downloads_filePath = downloads_dir + "sample_svcg_" + str(i) + ".txt"
      cleaned_filePath = cleaned_dir + "cleaned_sample_svcg_" + str(i) + ".csv"
      
      if not (os.path.isfile(cleaned_filePath)):

        # LOAD AND ADD HEADERS TO THE PERFORMANCE DATA
        performance = pd.read_csv(downloads_filePath,sep="|", header=None, 
               names = ["LOAN SEQUENCE NUMBER", 
                        "MONTHLY REPORTING PERIOD", 
                        "CURRENT ACTUAL UPB", 
                        "CURRENT LOAN DELINQUENCY STATUS",
                        "LOAN AGE",
                        "REMAINING MONTHS TO LEGAL MATURITY",
                        "REPURCHASE FLAG",
                        "MODIFICATION FLAG",
                        "ZERO BALANCE CODE",
                        "ZERO BALANCE EFFECTIVE DATE",
                        "CURRENT INTEREST RATE",
                        "CURRENT DEFERRED UPB",
                        "DUE DATE OF LAST PAID INSTALLMENT",
                        "MI RECOVERIES",
                        "NET SALES PROCEEDS",
                        "NON MI RECOVERIES",
                        "EXPENSES",
                        "Legal Costs",
                        "Maintenance and Preservation Costs",
                        "Taxes and Insurance",
                        "Miscellaneous Expenses",
                        "Actual Loss Calculation",
                        "Modification Cost"
                       ])

        # CLEAN THE PERFORMANCE FILE


        # SAVE DATAFRAME TO CLEANED DIRECTORY
        performance.to_csv(cleaned_filePath, sep=',', index = False)
      

    print ("cleaned performance files")











# __________________________________________________________________________________________________________________________________________




if __name__ == '__main__':
    luigi.run()