import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
from Classes.Part2.clean_orig import Clean_origination_data
# from Classes.Download_sf_loan import Download_loan_data
# from Classes.Summary_raw_data import Summary_raw_data
import re, os, zipfile, io
import numpy as np, glob


def clean_loan_seq_num(performance):
    performance =  performance[performance["LOAN SEQUENCE NUMBER"].notnull()]
    return performance


def clean_monthly_reporting_period(performance):
    performance['MONTHLY REPORTING PERIOD'].fillna('999999', inplace=True)
        # performance['MONTHLY REPORTING YEAR']= performance['MONTHLY REPORTING PERIOD'] // 100
    performance['MONTHLY REPORTING YEAR']= re.search(r'(\d{4})(\d{2})', str(performance['MONTHLY REPORTING PERIOD'])).group(1)
    performance['MONTHLY REPORTING MONTH'] = re.search(r'(\d{4})(\d{2})', str(performance['MONTHLY REPORTING PERIOD'])).group(2)
    return performance

def clean_loan_del_status(performance):
    performance['CURRENT LOAN DELINQUENCY STATUS'].fillna('999', inplace=True)
    # performance['CURRENT LOAN DELINQUENCY STATUS'] = performance['CURRENT LOAN DELINQUENCY STATUS'].replace('   ', 'XX')
    performance['CURRENT LOAN DELINQUENCY STATUS'].replace('   ', '999', inplace = True)
    performance['CURRENT LOAN DELINQUENCY STATUS'].replace('R', '998', inplace = True)
    performance['CURRENT LOAN DELINQUENCY STATUS'].replace('XX', '997', inplace = True)
    performance['DELINQUENT'] = 0
    performance.loc[((performance['CURRENT LOAN DELINQUENCY STATUS'].astype(np.int64)> 0) &( performance['CURRENT LOAN DELINQUENCY STATUS'].astype(np.int64) < 990 ) ), ['DELINQUENT']] = 1 
    return performance

def clean_repurchase_flag(performance):
    performance['REPURCHASE FLAG'].fillna('NA', inplace=True)
    # performance['REPURCHASE FLAG'] = performance['REPURCHASE FLAG'].replace(' ', 'NA')
    performance['REPURCHASE FLAG'].replace(' ', 'NA', inplace=True)
    performance['REPURCHASE FLAG YES'] = 0
    performance.loc[(performance['REPURCHASE FLAG'] == 'Y'), ['REPURCHASE FLAG YES']] = 1
    
    return performance

def clean_modification_flag(performance):
    performance['MODIFICATION FLAG'].fillna('NO', inplace=True)
    # performance['MODIFICATION FLAG'] = performance['MODIFICATION FLAG'].replace(' ', 'NO')
    performance['MODIFICATION FLAG'].replace(' ', 'NO', inplace = True)
    performance['MODIFICATION FLAG YES'] = 0
    performance.loc[(performance['MODIFICATION FLAG'] == 'Y'), ['MODIFICATION FLAG YES']] = 1
    return performance
def clean_zero_balance_code(performance):
    performance['ZERO BALANCE CODE'].fillna('99', inplace=True)
    # performance['ZERO BALANCE CODE'] = performance['ZERO BALANCE CODE'].replace('  ', 'NA')
    performance['ZERO BALANCE CODE'].replace('  ', '99', inplace = True)
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
    return{ 'output1' : luigi.LocalTarget("cleaned/cleaned_perf.txt") 
			}

  def run(self):
    create_directory("cleaned")
    cleaned_dir = "cleaned/"
    downloads_dir = "downloads/"
    
    quarterandyear = glob.glob(cleaned_dir + '[0-9][0-9][0-9][0-9][0-9]')[0]

    quarter = int(re.search(r'(\d)(\d{4})', quarterandyear).group(1))
    year = int(re.search(r'(\d)(\d{4})', quarterandyear).group(2))
    
      
    # Itereate through all the years. Check if the cleaned file exists! If not Read the downloads csv and Clean it. And Place it in the cleaned directory
    for i in range(quarter -1,quarter + 1):
      downloads_filePath = downloads_dir + "historical_data1_time_Q" + str(i) + str(year) + ".txt"
      cleaned_filePath = cleaned_dir + "cleaned_historical_data1_time_Q" + str(i) + str(year) + ".csv"
      
      if not (os.path.isfile(cleaned_filePath)):

        # LOAD AND ADD HEADERS TO THE PERFORMANCE DATA
        chunk = 500000
        perf = None
        for performance in pd.read_csv(downloads_filePath, sep="|", header = None, chunksize = chunk, iterator = True, index_col=False, names = ["LOAN SEQUENCE NUMBER", \
                        "MONTHLY REPORTING PERIOD", \
                        "CURRENT ACTUAL UPB", \
                        "CURRENT LOAN DELINQUENCY STATUS",\
                        "LOAN AGE",\
                        "REMAINING MONTHS TO LEGAL MATURITY",\
                        "REPURCHASE FLAG",\
                        "MODIFICATION FLAG",\
                        "ZERO BALANCE CODE",\
                        "ZERO BALANCE EFFECTIVE DATE",\
                        "CURRENT INTEREST RATE",\
                        "CURRENT DEFERRED UPB",\
                        "DUE DATE OF LAST PAID INSTALLMENT",\
                        "MI RECOVERIES",\
                        "NET SALES PROCEEDS",\
                        "NON MI RECOVERIES",\
                        "EXPENSES",\
                        "LEGAL COSTS",\
                        "MAINTENANCE AND PRESERVATION COSTS",\
                        "TAXES AND INSURANCE",\
                        "MISCELLANEOUS EXPENSES",\
                        "ACTUAL LOSS CALCULATION",\
                        "MODIFICATION COST"\
                       ]):
            

        # CLEAN THE PERFORMANCE FILE

        # NEEDS A CONDITIONAL FUNCTION FOR YEAR 2000
            # performance.index += j
            # i+=1
            clean_loan_seq_num(performance)
            clean_monthly_reporting_period(performance)
            clean_loan_del_status(performance)
            clean_repurchase_flag(performance)
            clean_modification_flag(performance)
            clean_zero_balance_code(performance)
            clean_zero_balance_effective_date(performance)
            clean_ddlpi(performance)
            replace_all_other_NaNs_With_zero(performance)

            # j = performance.index[-1] + 1
        # SAVE DATAFRAME TO CLEANED DIRECTORY
            # performance.columns = ['a', 'b']
            if not (os.path.isfile(cleaned_filePath)):
                performance.to_csv(cleaned_filePath, sep = ',', index = False)
            else:
                with open(cleaned_filePath, 'a') as f:
                    performance.to_csv(f, sep = ',', index = False, header = False)


    if (os.path.isfile(cleaned_dir + 'cleaned_historical_data1_time_Q' + str(quarter) + str(year) + '.csv') & os.path.isfile(cleaned_dir + 'cleaned_historical_data1_time_Q' + str(quarter-1) + str(year) + '.csv')):
        file = open(cleaned_dir + 'cleaned_perf.txt', 'w+')
        file.close()
        file = open(cleaned_dir+ str(quarter) + str(year), 'w+')
        file.close()
        print ("cleaned performance files")


    print("UNCOMMENT THE CODE WHEN SURE OF THIS")








# __________________________________________________________________________________________________________________________________________