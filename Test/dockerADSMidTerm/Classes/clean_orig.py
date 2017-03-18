import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
from Classes.Download_sf_loan import Download_loan_data
import re, os, zipfile, io

class Clean_origination_data(luigi.Task):
  def requires(self):
    return[Download_loan_data()]

  def output(self):
    return{ 'output1' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2016.csv") ,\
                'output2' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2015.csv") ,\
                'output3' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2014.csv") ,\
                'output4' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2013.csv") ,\
                'output5' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2012.csv") ,\
                'output6' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2011.csv") ,\
                'output7' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2010.csv") ,\
                'output8' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2009.csv") ,\
                'output9' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2008.csv") ,\
                'output10' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2007.csv") ,\
                'output11' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2006.csv") ,\
                'output12' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2005.csv") ,\
                'output13' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2004.csv") ,\
                'output14' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2003.csv") ,\
                'output15' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2002.csv") ,\
                'output16' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2001.csv") ,\
                'output17' : luigi.LocalTarget("cleaned/cleaned_sample_orig_2000.csv") ,\
                'output18' : luigi.LocalTarget("cleaned/cleaned_sample_orig_1999.csv") }

  def run(self):
    create_directory("cleaned")
    cleaned_dir = "cleaned/"
    downloads_dir = "downloads/"
    
    
      
    # Itereate through all the years. Check if the cleaned file exists! If not Read the downloads csv and Clean it. And Place it in the cleaned directory
    for i in range(1999,2017):
      downloads_filePath = downloads_dir + "sample_orig_" + str(i) + ".txt"
      cleaned_filePath = cleaned_dir + "cleaned_sample_orig_" + str(i) + ".csv"
      
      if not (os.path.isfile(cleaned_filePath)):
        # LOAD AND ADD HEADERS TO THE ORIG DATA
        orig_file = pd.read_csv(downloads_filePath ,sep="|", header=None, \
               names = ["CREDIT SCORE",\
                        "FIRST PAYMENT DATE",\
                        "FIRST TIME HOMEBUYER FLAG",\
                        "MATURITY DATE",\
                        "METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION",\
                        "MORTGAGE INSURANCE PERCENTAGE (MI %)",\
                        "NUMBER OF UNITS",\
                        "OCCUPANCY STATUS",\
                        "ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)",\
                        "ORIGINAL DEBT-TO-INCOME (DTI) RATIO",\
                        "ORIGINAL UPB",\
                        "ORIGINAL LOAN-TO-VALUE (LTV)",\
                        "ORIGINAL INTEREST RATE",\
                        "CHANNEL",\
                        "PREPAYMENT PENALTY MORTGAGE (PPM) FLAG",\
                        "PRODUCT TYPE",\
                        "PROPERTY STATE",\
                        "PROPERTY TYPE",\
                        "POSTAL CODE",\
                        "LOAN SEQUENCE NUMBER",\
                        "LOAN PURPOSE",\
                        "ORIGINAL LOAN TERM",\
                        "NUMBER OF BORROWERS",\
                        "SELLER NAME",\
                        "SERVICER NAME",\
                        "Super Conforming Flag"\
                       ])

        # CLEAN THE ORIG FILE





        # SAVE DATAFRAME TO CLEANED DIRECTORY
        orig_file.to_csv(cleaned_filePath, sep=',', index = False)



    print ("cleaned origination files")