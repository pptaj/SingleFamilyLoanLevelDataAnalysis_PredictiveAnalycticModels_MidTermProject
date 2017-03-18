import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
from Classes.Part1.clean_orig import Clean_origination_data
# from Classes.Download_sf_loan import Download_loan_data
# from Classes.Summary_raw_data import Summary_raw_data
import re, os, zipfile, io
import numpy as np


def clean_loan_seq_num(performance):
    performance['LOAN SEQUENCE NUMBER'].fillna("F155Q9999999" ,inplace=True) # DISCARD RECORD? 
    performance['ORIGINATION YEAR'] = re.search(r'F1(\d{2})Q\d{1}\d{6}', str(performance['LOAN SEQUENCE NUMBER'])).group(1)
    performance['ORIGINATION QUARTER']    = (performance['LOAN SEQUENCE NUMBER'].str.rpartition('Q')[2].astype(np.int64)/1000000).astype(np.int64)
    return performance


def clean_monthly_reporting_period(performance):
    performance['MONTHLY REPORTING PERIOD'].fillna('999999', inplace=True)
        # performance['MONTHLY REPORTING YEAR']= performance['MONTHLY REPORTING PERIOD'] // 100
    performance['MONTHLY REPORTING YEAR']= re.search(r'(\d{4})(\d{2})', str(performance['MONTHLY REPORTING PERIOD'])).group(1)
    performance['MONTHLY REPORTING MONTH'] = re.search(r'(\d{4})(\d{2})', str(performance['MONTHLY REPORTING PERIOD'])).group(2)
    return performance

def clean_loan_del_status(performance):
    performance['CURRENT LOAN DELINQUENCY STATUS'].fillna('XX', inplace=True)
    performance['CURRENT LOAN DELINQUENCY STATUS'] = performance['CURRENT LOAN DELINQUENCY STATUS'].replace('   ', 'XX')
    return performance

def clean_repurchase_flag(performance):
    performance['REPURCHASE FLAG'].fillna('NA', inplace=True)
    performance['REPURCHASE FLAG'] = performance['REPURCHASE FLAG'].replace(' ', 'NA')
    return performance

def clean_modification_flag(performance):
    performance['MODIFICATION FLAG'].fillna('NO', inplace=True)
    performance['MODIFICATION FLAG'] = performance['MODIFICATION FLAG'].replace(' ', 'NO')
    return performance
def clean_zero_balance_code(performance):
    performance['ZERO BALANCE CODE'].fillna('NA', inplace=True)
    performance['ZERO BALANCE CODE'] = performance['ZERO BALANCE CODE'].replace('  ', 'NA')
    return performance
def clean_zero_balance_effective_date(performance):
    performance['ZERO BALANCE EFFECTIVE DATE'].fillna('999999', inplace=True)
    performance['ZERO BALANCE EFFECTIVE YEAR']= re.search(r'(\d{4})(\d{2})', str(performance['ZERO BALANCE EFFECTIVE DATE'])).group(1)
    performance['ZERO BALANCE EFFECTIVE MONTH'] = re.search(r'(\d{4})(\d{2})', str(performance['ZERO BALANCE EFFECTIVE DATE'])).group(2)
    return performance



def clean_ddlpi(performance):
    performance['DUE DATE OF LAST PAID INSTALLMENT'].fillna('999999', inplace=True)
    performance['DUE DATE OF LAST PAID INSTALLMENT YEAR']= re.search(r'(\d{4})(\d{2})', str(performance['DUE DATE OF LAST PAID INSTALLMENT'])).group(1)
    performance['DUE DATE OF LAST PAID INSTALLMENT MONTH'] = re.search(r'(\d{4})(\d{2})', str(performance['DUE DATE OF LAST PAID INSTALLMENT'])).group(2)
    return performance

def replace_all_other_NaNs_With_zero(performance):
    performance.fillna(0)
    return performance

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
                        "LEGAL COSTS",
                        "MAINTENANCE AND PRESERVATION COSTS",
                        "TAXES AND INSURANCE",
                        "MISCELLANEOUS EXPENSES",
                        "ACTUAL LOSS CALCULATION",
                        "MODIFICATION COST"
                       ])

        # CLEAN THE PERFORMANCE FILE

        # NEEDS A CONDITIONAL FUNCTION FOR YEAR 2000
        clean_monthly_reporting_period(performance)
        clean_loan_del_status(performance)
        clean_repurchase_flag(performance)
        clean_modification_flag(performance)
        clean_zero_balance_code(performance)
        clean_zero_balance_effective_date(performance)
        clean_ddlpi(performance)
        replace_all_other_NaNs_With_zero(performance)
        

        # SAVE DATAFRAME TO CLEANED DIRECTORY
        performance.to_csv(cleaned_filePath, sep=',', index = False)


    print ("cleaned performance files")











# __________________________________________________________________________________________________________________________________________