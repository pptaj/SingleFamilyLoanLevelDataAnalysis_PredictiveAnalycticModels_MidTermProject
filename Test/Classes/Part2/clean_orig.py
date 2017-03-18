import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
from Classes.Part2.Download_sf_loan import Download_loan_data
# from Classes.Part2.Summary_raw_data import Summary_raw_data
import re, os, zipfile, io
import numpy as np
import glob


def clean_credit_score(orig_file,i,t):
    orig_file['CREDIT SCORE'] = orig_file['CREDIT SCORE'].astype(str)
    orig_file =  orig_file[orig_file['CREDIT SCORE'].notnull()]
    orig_file =  orig_file[orig_file['CREDIT SCORE'] != '   ']
    x = len(orig_file.index)
    t = t-x
    print("Removed %d rows that had no values for credit score for quarter %d"% (t, i) )
    return orig_file

def clean_first_payment_date(orig_file):
    orig_file['FIRST PAYMENT DATE'].fillna('999999', inplace=True)
    orig_file['FIRST PAYMENT YEAR']= orig_file['FIRST PAYMENT DATE'] // 100
    orig_file['FIRST PAYMENT MONTH'] = orig_file['FIRST PAYMENT DATE'].astype(str).str[-2:].astype(np.int64)
    return orig_file


def clean_first_time_homebuyer_flag(orig_file):
    orig_file['FIRST TIME HOMEBUYER FLAG'].fillna('NA', inplace=True) # MODE?
    orig_file['FIRST TIME HOMEBUYER FLAG'] = orig_file['FIRST TIME HOMEBUYER FLAG'].replace({' ':'NA'})
    # if((orig_file['FIRST TIME HOMEBUYER FLAG'] == 'NA')\
    #                             &((orig_file['OCCUPANCY STATUS'] == 'I') \
    #                             | (orig_file['OCCUPANCY STATUS'] == 'S') \
    #                             | (orig_file['LOAN PURPOSE'] == 'N') \
    #                             | (orig_file['LOAN PURPOSE'] == 'C') \
    #                             )):
    #     condition = True
    # else:
    #     condition = False
    # orig_file['FIRST TIME HOMEBUYER FLAG'] = orig_file['FIRST TIME HOMEBUYER FLAG'].apply(lambda x: 'NA' if (condition) else 'NO')
    orig_file['FIRST TIME HOMEBUYER FLAG YES'] = 0
    orig_file['FIRST TIME HOMEBUYER FLAG NO'] = 0
    orig_file['FIRST TIME HOMEBUYER FLAG NA'] = 0
    orig_file.loc[(orig_file['FIRST TIME HOMEBUYER FLAG'] == 'Y'), ['FIRST TIME HOMEBUYER FLAG YES']] = 1
    orig_file.loc[(orig_file['FIRST TIME HOMEBUYER FLAG'] == 'N'), ['FIRST TIME HOMEBUYER FLAG NO']] = 1
    orig_file.loc[(orig_file['FIRST TIME HOMEBUYER FLAG'] == 'NA'), ['FIRST TIME HOMEBUYER FLAG NA']] = 1
    return orig_file
            

def clean_maturity_date(orig_file):
    orig_file['MATURITY DATE'].fillna('999999', inplace=True)
    orig_file['MATURITY YEAR']= orig_file['MATURITY DATE'] // 100
    orig_file['MATURITY MONTH'] = orig_file['MATURITY DATE'].astype(str).str[-2:].astype(np.int64)
    return orig_file

def clean_msa_md(orig_file):
    orig_file['METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION'].fillna('0', inplace=True)
    orig_file['METROPOLITAN_AREA_FLAG'] = orig_file['METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION'].apply(lambda x: 1 if int(x) != 0 else 0)
    return orig_file
            
def clean_mi_percentage(orig_file):
    orig_file['MORTGAGE INSURANCE PERCENTAGE (MI %)'].fillna('999', inplace=True) #MEAN, MEDIAN?
    orig_file['MORTGAGE INSURANCE PERCENTAGE (MI %)'] = orig_file['MORTGAGE INSURANCE PERCENTAGE (MI %)'].astype(str)
    orig_file['MORTGAGE INSURANCE PERCENTAGE (MI %)'] = orig_file['MORTGAGE INSURANCE PERCENTAGE (MI %)'].replace({'   ' : 999})
    orig_file['MORTGAGE_INSURANCE_FLAG'] = orig_file['MORTGAGE INSURANCE PERCENTAGE (MI %)'].apply(lambda x: 1 if int(x) != 0 else 0)
    return orig_file
            
            
def clean_number_of_units(orig_file):
    orig_file['NUMBER OF UNITS'].fillna(orig_file['NUMBER OF UNITS'].mode()[0], inplace=True) 
    mode_of = orig_file['NUMBER OF UNITS'].mode()[0]
    orig_file['NUMBER OF UNITS'] = orig_file['NUMBER OF UNITS'].astype(str)
    orig_file['NUMBER OF UNITS'] = orig_file['NUMBER OF UNITS'].replace({' ':mode_of})
    return orig_file
           
def clean_occupancy_status(orig_file):
    orig_file['OCCUPANCY STATUS'].fillna(orig_file['OCCUPANCY STATUS'].mode()[0], inplace=True) 
    mode_of = orig_file['OCCUPANCY STATUS'].mode()[0]
    orig_file['OCCUPANCY STATUS'] = orig_file['OCCUPANCY STATUS'].astype(str)
    orig_file['OCCUPANCY STATUS'] = orig_file['OCCUPANCY STATUS'].replace({' ':mode_of})
    orig_file['OWNER OCCUPIED FLAG'] = 0
    orig_file['INVESTMENT PROPERTY FLAG'] = 0
    orig_file['SECOND HOME SPACE FLAG'] = 0
    orig_file.loc[(orig_file['OCCUPANCY STATUS'] == 'O'), ['OWNER OCCUPIED FLAG']] = 1
    orig_file.loc[(orig_file['OCCUPANCY STATUS'] == 'I'), ['INVESTMENT PROPERTY FLAG']] = 1
    orig_file.loc[(orig_file['OCCUPANCY STATUS']=='S'), ['SECOND HOME SPACE FLAG']] = 1
    
    return orig_file

def clean_cltv(orig_file):
    orig_file["ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)"].fillna('999', inplace=True)
    return orig_file

def clean_dti_ratio(orig_file):
    orig_file['ORIGINAL DEBT-TO-INCOME (DTI) RATIO'].fillna('99', inplace=True)
    orig_file['ORIGINAL DEBT-TO-INCOME (DTI) RATIO'] = orig_file['ORIGINAL DEBT-TO-INCOME (DTI) RATIO'].astype(str)
    orig_file['ORIGINAL DEBT-TO-INCOME (DTI) RATIO'] = orig_file['ORIGINAL DEBT-TO-INCOME (DTI) RATIO'].replace({'   ': '70'})

    return orig_file

            
            
            
def clean_original_upb(orig_file,i,t):
    # orig_file['ORIGINAL UPB'].fillna("0" ,inplace=True) #MEAN, MEDIAN?
    orig_file['ORIGINAL UPB'] = orig_file['ORIGINAL UPB'].astype(str)
    orig_file =  orig_file[orig_file['ORIGINAL UPB'].notnull()]
    x = len(orig_file.index)
    t = t-x
    print("Removed %d rows that had no values for original upb for quarter %d"% (t, i) )
    return orig_file

def clean_original_ltv(orig_file, i, t):
    orig_file['ORIGINAL LOAN-TO-VALUE (LTV)'].fillna(orig_file['ORIGINAL LOAN-TO-VALUE (LTV)'].mean(), inplace=True) 
    orig_file['ORIGINAL LOAN-TO-VALUE (LTV)'] = orig_file['ORIGINAL LOAN-TO-VALUE (LTV)'].astype(str)
    orig_file =  orig_file[orig_file['ORIGINAL LOAN-TO-VALUE (LTV)'].notnull()]
    orig_file =  orig_file[orig_file['ORIGINAL LOAN-TO-VALUE (LTV)'] != '   ']
    x = len(orig_file.index)
    t = t-x
    print("Removed %d rows that had no values for original Loan-To-Value for quarter %d"% (t, i) )
    return orig_file

def clean_original_interest(orig_file):
    orig_file['ORIGINAL INTEREST RATE'].fillna(orig_file['ORIGINAL INTEREST RATE'].mode()[0], inplace=True) 
    return orig_file

            
            
            
def clean_channel(orig_file):
    mode_of = orig_file['CHANNEL'].mode()[0]
    orig_file['CHANNEL'].fillna(mode_of, inplace=True)
    orig_file['CHANNEL'] = orig_file['CHANNEL'].replace({' ':mode_of})
   
    orig_file['RETAIL CHANNEL FLAG'] = 0
    orig_file['BROKER CHANNEL FLAG'] = 0
    orig_file['CORRESPONDENT CHANNEL FLAG'] = 0
    orig_file['TP0 NOT SPECIFIED CHANNEL FLAG'] = 0
    orig_file.loc[(orig_file['CHANNEL'] == 'R'), ['RETAIL CHANNEL FLAG']] = 1
    orig_file.loc[(orig_file['CHANNEL'] == 'B'), ['BROKER CHANNEL FLAG']] = 1
    orig_file.loc[(orig_file['CHANNEL']=='C'), ['CORRESPONDENT CHANNEL FLAG']] = 1
    orig_file.loc[(orig_file['CHANNEL']=='T'), ['TP0 NOT SPECIFIED CHANNEL FLAG']] = 1
    
    return orig_file

def clean_ppm_flag(orig_file):
    mode_of = orig_file['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG'].mode()[0]
    orig_file['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG'].fillna(mode_of ,inplace=True)
    orig_file['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG'] = orig_file['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG'].replace({' ' : mode_of})
    
    orig_file['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG YES'] = 0
    orig_file['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG NO'] = 0
    orig_file.loc[(orig_file['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG'] == 'N'), ['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG NO']] = 1
    orig_file.loc[(orig_file['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG'] == 'Y'), ['PREPAYMENT PENALTY MORTGAGE (PPM) FLAG YES']] = 1
    
    return orig_file

def clean_product_type(orig_file):
    orig_file['PRODUCT TYPE'].fillna("FRM" ,inplace=True) #FRM?
    orig_file['PRODUCT TYPE'] = orig_file['PRODUCT TYPE'].replace({'  ' : 'FRM'})
    orig_file['FIXED RATE MORTGAGE PRODUCT TYPE FLAG YES'] = 0
    orig_file['FIXED RATE MORTGAGE PRODUCT TYPE FLAG NO'] = 0
    orig_file.loc[(orig_file['PRODUCT TYPE'] == 'FRM'), ['FIXED RATE MORTGAGE PRODUCT TYPE FLAG YES']] = 1
    orig_file.loc[(orig_file['PRODUCT TYPE'] != 'FRM'), ['FIXED RATE MORTGAGE PRODUCT TYPE FLAG NO']] = 1
    return orig_file

def clean_property_state(orig_file):
    orig_file['PROPERTY STATE'].fillna("Unknown" ,inplace=True) 
    return orig_file

def clean_property_type(orig_file):
    mode_of = orig_file['PROPERTY TYPE'].mode()[0]
    orig_file['PROPERTY TYPE'].fillna(mode_of, inplace=True)
    orig_file['PROPERTY TYPE']= orig_file['PROPERTY TYPE'].replace({'  ' : mode_of})
    orig_file['CONDO PROPERTY TYPE FLAG'] = 0
    orig_file['LEASE HOLD PROPERTY TYPE FLAG'] = 0
    orig_file['PUD PROPERTY TYPE FLAG'] = 0
    orig_file['MANUFACTURE HOUSING PROPERTY TYPE FLAG'] = 0
    orig_file['FREE SIMPLE HOUSING PROPERTY TYPE FLAG'] = 0
    orig_file['CO OP HOUSING PROPERTY TYPE FLAG'] = 0
    orig_file.loc[(orig_file['PROPERTY TYPE'] == 'CO'), ['CONDO PROPERTY TYPE FLAG']] = 1
    orig_file.loc[(orig_file['PROPERTY TYPE'] == 'LH'), ['LEASE HOLD PROPERTY TYPE FLAG']] = 1
    orig_file.loc[(orig_file['PROPERTY TYPE'] == 'PU'), ['PUD PROPERTY TYPE FLAG']] = 1
    orig_file.loc[(orig_file['PROPERTY TYPE'] == 'MH'), ['MANUFACTURE HOUSING PROPERTY TYPE FLAG']] = 1
    orig_file.loc[(orig_file['PROPERTY TYPE'] == 'SF'), ['FREE SIMPLE HOUSING PROPERTY TYPE FLAG']] = 1
    orig_file.loc[(orig_file['PROPERTY TYPE'] == 'CP'), ['CO OP HOUSING PROPERTY TYPE FLAG']] = 1
    return orig_file

def clean_postal_code(orig_file):
    orig_file['POSTAL CODE'].fillna("99999" ,inplace=True)
    orig_file['POSTAL CODE']= orig_file['POSTAL CODE'].replace({"     " ,"99999"})
    return orig_file

def clean_loan_seq_num(orig_file):
    orig_file['LOAN SEQUENCE NUMBER'].fillna("F155Q9999999" ,inplace=True) # DISCARD RECORD? 
    orig_file['ORIGINATION YEAR'] = re.search(r'F1(\d{2})Q\d{1}\d{6}', str(orig_file['LOAN SEQUENCE NUMBER'])).group(1)
    orig_file['ORIGINATION QUARTER']    = (orig_file['LOAN SEQUENCE NUMBER'].str.rpartition('Q')[2].astype(np.int64)/1000000).astype(np.int64)
    return orig_file


def clean_loan_purpose(orig_file):
    mode_of = orig_file['LOAN PURPOSE'].mode()[0]
    orig_file['LOAN PURPOSE'].fillna(mode_of ,inplace=True)
    orig_file['LOAN PURPOSE'] = orig_file['LOAN PURPOSE'].replace({' ' : mode_of})
    orig_file['LOAN PURPOSE IS PURCHASE FLAG'] = 0
    orig_file['LOAN PURPOSE IS CASH OUT REFINANCE FLAG'] = 0
    orig_file['LOAN PURPOSE IS NO CASH OUT REFINANCE FLAG'] = 0
    orig_file.loc[(orig_file['LOAN PURPOSE'] == 'P'), ['LOAN PURPOSE IS PURCHASE FLAG']] = 1
    orig_file.loc[(orig_file['LOAN PURPOSE'] == 'C'), ['LOAN PURPOSE IS CASH OUT REFINANCE FLAG']] = 1
    orig_file.loc[(orig_file['LOAN PURPOSE'] == 'N'), ['LOAN PURPOSE IS NO CASH OUT REFINANCE FLAG']] = 1
    
    return orig_file

            
            
            
def clean_orig_loan_term(orig_file):
    orig_file['ORIGINAL LOAN TERM'].fillna(orig_file['ORIGINAL LOAN TERM'].mode()[0] ,inplace=True)
    return orig_file

           
def clean_num_of_borrowers(orig_file):
    orig_file['NUMBER OF BORROWERS'].fillna(orig_file['NUMBER OF BORROWERS'].mode()[0] ,inplace=True) #MODE? 
    return orig_file
            # orig_file['NUMBER OF BORROWERS'] = orig_file['NUMBER OF BORROWERS'].replace({'  ' : '8'})

def clean_seller_and_servicer_name(orig_file):
    orig_file['SELLER NAME'].fillna("Unknown" ,inplace=True) 
    orig_file['SERVICER NAME'].fillna("Unknown" ,inplace=True)
    return orig_file

def clean_super_conf_flag(orig_file):
    orig_file['SUPER CONFORMING FLAG'].fillna("N" ,inplace=True)
    orig_file['SUPER CONFORMING FLAG'] = orig_file['SUPER CONFORMING FLAG'].replace({' ', 'N'})
    orig_file['SUPER CONFORMING FLAG YES'] = 0
    orig_file['SUPER CONFORMING FLAG NO'] = 0
    orig_file.loc[(orig_file['SUPER CONFORMING FLAG'] == 'Y'), ['SUPER CONFORMING FLAG YES']] = 1
    orig_file.loc[(orig_file['SUPER CONFORMING FLAG'] == 'N'), ['SUPER CONFORMING FLAG NO']] = 1
    
    return orig_file


class Clean_origination_data(luigi.Task):
  def requires(self):
    return[Download_loan_data()]
    # return[Summary_raw_data()]
  def output(self):
    return{ 'output1' : luigi.LocalTarget("cleaned/cleaned_orig.txt") 
                
                }

  def run(self):
    create_directory("cleaned")
    cleaned_dir = "cleaned/"
    downloads_dir = "downloads/"
    quarterandyear = glob.glob(downloads_dir + '[0-9][0-9][0-9][0-9][0-9]')[0]

    quarter = int(re.search(r'(\d)(\d{4})', quarterandyear).group(1))
    year = int(re.search(r'(\d)(\d{4})', quarterandyear).group(2))
    # Itereate through all the years. Check if the cleaned file exists! If not Read the downloads csv and Clean it. And Place it in the cleaned directory
    for i in range(quarter -1,quarter + 1):
        downloads_filePath = downloads_dir + "historical_data1_Q" + str(i) + str(year) + ".txt"
        cleaned_filePath = cleaned_dir + "cleaned_historical_data1_Q" + str(i) + str(year) + ".csv"
        # downloads_filePath = downloads_dir + "historical_data1_Q" + str(i) + "2007.txt"
        # cleaned_filePath = cleaned_dir + "cleaned_historical_data1_Q" + str(i) + "2007.csv"
        
        if not (os.path.isfile(cleaned_filePath)):
        # LOAD AND ADD HEADERS TO THE ORIG DATA
            orig_f = None
            for orig_file in pd.read_csv(downloads_filePath, sep="|", header = None, chunksize = 100000, iterator = True, names = ["CREDIT SCORE",\
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
                                "SUPER CONFORMING FLAG"\
                               ]):

                t = len(orig_file.index)
                print("number of rows = " + str(t))
                    
                    # CLEAN THE ORIG FILE
                orig_file = clean_credit_score(orig_file, i, t)
                t = len(orig_file.index)
                orig_file = clean_first_payment_date(orig_file)
                t = len(orig_file.index)
                orig_file = clean_first_time_homebuyer_flag(orig_file)
                t = len(orig_file.index)
                orig_file = clean_maturity_date(orig_file)
                t = len(orig_file.index)
                orig_file = clean_msa_md(orig_file)
                t = len(orig_file.index)
                orig_file = clean_mi_percentage(orig_file)
                t = len(orig_file.index)
                orig_file = clean_number_of_units(orig_file)
                t = len(orig_file.index)
                orig_file = clean_occupancy_status(orig_file)
                t = len(orig_file.index)
                orig_file = clean_cltv(orig_file)
                t = len(orig_file.index)
                orig_file = clean_dti_ratio(orig_file)
                t = len(orig_file.index)
                orig_file = clean_original_upb(orig_file, i, t)
                t = len(orig_file.index)
                orig_file = clean_original_ltv(orig_file, i , t)
                t = len(orig_file.index)
                orig_file = clean_original_interest(orig_file)
                t = len(orig_file.index)
                orig_file = clean_channel(orig_file)
                t = len(orig_file.index)
                orig_file = clean_ppm_flag(orig_file)
                t = len(orig_file.index)
                orig_file = clean_product_type(orig_file)
                t = len(orig_file.index)
                orig_file = clean_property_state(orig_file)
                t = len(orig_file.index)
                orig_file = clean_property_type(orig_file)
                t = len(orig_file.index)
                orig_file = clean_postal_code(orig_file)
                t = len(orig_file.index)
                orig_file = clean_loan_seq_num(orig_file)
                t = len(orig_file.index)
                orig_file = clean_loan_purpose(orig_file)
                t = len(orig_file.index)
                orig_file = clean_orig_loan_term(orig_file)
                t = len(orig_file.index)
                orig_file = clean_num_of_borrowers(orig_file)
                t = len(orig_file.index)
                orig_file = clean_seller_and_servicer_name(orig_file)
                t = len(orig_file.index)
                orig_file = clean_super_conf_flag(orig_file)
                print("number of new rows = %d" %len(orig_file.index))
                try:
                    orig_f = pd.concat([orig_f, orig_file])
                except:
                    orig_f = orig_file

            # SAVE DATAFRAME TO CLEANED DIRECTORY
            
            orig_f.to_csv(cleaned_filePath, sep=',', index = False)

    if (os.path.isfile(cleaned_dir + 'cleaned_historical_data1_Q' + str(quarter) + str(year) + '.csv') & os.path.isfile(cleaned_dir + 'cleaned_historical_data1_Q' + str(quarter-1) + str(year) + '.csv')):
        file = open(cleaned_dir + 'cleaned_orig.txt', 'w+')
        file.close()
        file = open(cleaned_dir+ str(quarter) + str(year), 'w+')
        file.close()
        print ("cleaned origination files")




