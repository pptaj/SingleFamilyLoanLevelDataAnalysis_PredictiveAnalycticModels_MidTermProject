import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
from Classes.Part1.Download_sf_loan import Download_loan_data
import re, os, zipfile, io
import numpy as np

class Summary_raw_data(luigi.Task):
    def requires(self):
        return[Download_loan_data()]
    
    def output(self):
        return{ 'output1'  : luigi.LocalTarget("summary/summary_raw_sample_orig_CREDIT SCORE.csv") ,\
                'output2'  : luigi.LocalTarget("summary/summary_raw_sample_orig_FIRST PAYMENT DATE.csv") ,\
                'output3'  : luigi.LocalTarget("summary/summary_raw_sample_orig_FIRST TIME HOMEBUYER FLAG.csv") ,\
                'output4'  : luigi.LocalTarget("summary/summary_raw_sample_orig_MATURITY DATE.csv") ,\
                'output5'  : luigi.LocalTarget("summary/summary_raw_sample_orig_METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION.csv") ,\
                'output6'  : luigi.LocalTarget("summary/summary_raw_sample_orig_MORTGAGE INSURANCE PERCENTAGE (MI %).csv") ,\
                'output7'  : luigi.LocalTarget("summary/summary_raw_sample_orig_NUMBER OF UNITS.csv") ,\
                'output8'  : luigi.LocalTarget("summary/summary_raw_sample_orig_OCCUPANCY STATUS.csv") ,\
                'output9'  : luigi.LocalTarget("summary/summary_raw_sample_orig_ORIGINAL COMBINED LOAN-TO-VALUE (CLTV).csv") ,\
                'output10' : luigi.LocalTarget("summary/summary_raw_sample_orig_ORIGINAL DEBT-TO-INCOME (DTI) RATIO.csv") ,\
                'output11' : luigi.LocalTarget("summary/summary_raw_sample_orig_ORIGINAL UPB.csv") ,\
                'output12' : luigi.LocalTarget("summary/summary_raw_sample_orig_ORIGINAL LOAN-TO-VALUE (LTV).csv") ,\
                'output13' : luigi.LocalTarget("summary/summary_raw_sample_orig_ORIGINAL INTEREST RATE.csv") ,\
                'output14' : luigi.LocalTarget("summary/summary_raw_sample_orig_CHANNEL.csv") ,\
                'output15' : luigi.LocalTarget("summary/summary_raw_sample_orig_PREPAYMENT PENALTY MORTGAGE (PPM) FLAG.csv") ,\
                'output16' : luigi.LocalTarget("summary/summary_raw_sample_orig_PRODUCT TYPE.csv") ,\
                'output17' : luigi.LocalTarget("summary/summary_raw_sample_orig_PROPERTY STATE.csv") ,\
                'output18' : luigi.LocalTarget("summary/summary_raw_sample_orig_PROPERTY TYPE.csv") ,\
                'output19' : luigi.LocalTarget("summary/summary_raw_sample_orig_POSTAL CODE.csv") ,\
                'output20' : luigi.LocalTarget("summary/summary_raw_sample_orig_LOAN PURPOSE.csv") ,\
                'output21' : luigi.LocalTarget("summary/summary_raw_sample_orig_ORIGINAL LOAN TERM.csv") ,\
                'output22' : luigi.LocalTarget("summary/summary_raw_sample_orig_NUMBER OF BORROWERS.csv") ,\
                'output23' : luigi.LocalTarget("summary/summary_raw_sample_orig_SELLER NAME.csv") ,\
                'output24' : luigi.LocalTarget("summary/summary_raw_sample_orig_SERVICER NAME.csv") ,\
                'output25' : luigi.LocalTarget("summary/summary_raw_sample_orig_SUPER CONFORMING FLAG.csv") ,\
                'output26' : luigi.LocalTarget("summary/summary_raw_sample_svcg_LOAN SEQUENCE NUMBER.csv") ,\
				'output27' : luigi.LocalTarget("summary/summary_raw_sample_svcg_MONTHLY REPORTING PERIOD.csv") ,\
				'output28' : luigi.LocalTarget("summary/summary_raw_sample_svcg_CURRENT ACTUAL UPB.csv") ,\
				'output29' : luigi.LocalTarget("summary/summary_raw_sample_svcg_CURRENT LOAN DELINQUENCY STATUS.csv") ,\
				'output30' : luigi.LocalTarget("summary/summary_raw_sample_svcg_LOAN AGE.csv") ,\
				'output31' : luigi.LocalTarget("summary/summary_raw_sample_svcg_REMAINING MONTHS TO LEGAL MATURITY.csv") ,\
				'output32' : luigi.LocalTarget("summary/summary_raw_sample_svcg_REPURCHASE FLAG.csv") ,\
				'output33' : luigi.LocalTarget("summary/summary_raw_sample_svcg_MODIFICATION FLAG.csv") ,\
				'output34' : luigi.LocalTarget("summary/summary_raw_sample_svcg_ZERO BALANCE CODE.csv") ,\
				'output35' : luigi.LocalTarget("summary/summary_raw_sample_svcg_ZERO BALANCE EFFECTIVE DATE.csv") ,\
				'output36' : luigi.LocalTarget("summary/summary_raw_sample_svcg_CURRENT INTEREST RATE.csv") ,\
				'output37' : luigi.LocalTarget("summary/summary_raw_sample_svcg_CURRENT DEFERRED UPB.csv") ,\
				'output38' : luigi.LocalTarget("summary/summary_raw_sample_svcg_DUE DATE OF LAST PAID INSTALLMENT.csv") ,\
				'output39' : luigi.LocalTarget("summary/summary_raw_sample_svcg_MI RECOVERIES.csv") ,\
				'output40' : luigi.LocalTarget("summary/summary_raw_sample_svcg_NET SALES PROCEEDS.csv") ,\
				'output41' : luigi.LocalTarget("summary/summary_raw_sample_svcg_NON MI RECOVERIES.csv") ,\
				'output42' : luigi.LocalTarget("summary/summary_raw_sample_svcg_EXPENSES.csv") ,\
				'output43' : luigi.LocalTarget("summary/summary_raw_sample_svcg_LEGAL COSTS.csv") ,\
				'output44' : luigi.LocalTarget("summary/summary_raw_sample_svcg_MAINTENANCE AND PRESERVATION COSTS.csv") ,\
				'output45' : luigi.LocalTarget("summary/summary_raw_sample_svcg_TAXES AND INSURANCE.csv") ,\
				'output46' : luigi.LocalTarget("summary/summary_raw_sample_svcg_MISCELLANEOUS EXPENSES.csv") ,\
				'output47' : luigi.LocalTarget("summary/summary_raw_sample_svcg_ACTUAL LOSS CALCULATION.csv") ,\
				'output48' : luigi.LocalTarget("summary/summary_raw_sample_svcg_MODIFICATION COST.csv")\

            }

    def run(self):
        create_directory("summary")
        summary_dir = "summary/"
        downloads_dir = "downloads/"

        # FOR ORIGINATION DATA
        headers_orig = ["CREDIT SCORE",\
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
                                   ]

        # CREATE EMPTY FILES AND INSERT headers_orig TO THE FILES
        for head in headers_orig:
        	 if not (head == "LOAN SEQUENCE NUMBER"):
        	 	summary_filePath = summary_dir + "summary_raw_sample_orig_"  +    head   + ".csv"
        	 	with open(summary_filePath, 'a') as f:
        	 		f.write(head)
        	 		f.write(',COUNT,YEAR\n')
        	 		f.close()
        # ADD SUMMARY TO THE FILES CREATED!!
        for i in range(1999,2017):
            downloads_filePath = downloads_dir + "sample_orig_" + str(i) + ".txt"
                
                # downloads_filePath = downloads_dir + "historical_data1_Q" + str(i) + "2007.txt"
                # cleaned_filePath = cleaned_dir + "cleaned_historical_data1_Q" + str(i) + "2007.csv"
            

            orig_file = pd.read_csv(downloads_filePath ,sep="|", header=None, names = headers_orig)

                        # SUMMARIZE THE RAW SAMPLE FILE

            for head in headers_orig:
                    # d = orig_file[['col1', 'col2', 'col3', 'col4']].groupby(['col1', 'col2']).agg(['mean', 'count'])
                if not (head == "LOAN SEQUENCE NUMBER"):

                    d = orig_file.groupby(head) \
                          			.agg({"LOAN SEQUENCE NUMBER" : len}) \
                            			.rename(columns={'LOAN SEQUENCE NUMBER':'COUNT'})
                    d['Year']= str(i)
                    summary_filePath = summary_dir + "summary_raw_sample_orig_"  +    head   + ".csv"

                    with open(summary_filePath, 'a') as f:
                        d.to_csv(f,sep=',', header=False)
                        f.close()
        print("SUMMARIZED RAW ORIGINATION FILES")

        # ______________________________________________-

        # FOR PERFORMANCE DATA
        headers_svcg = ["LOAN SEQUENCE NUMBER",\
                        "MONTHLY REPORTING PERIOD",\
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
                                   ]

        # CREATE EMPTY FILES AND INSERT headers_svcg TO THE FILES
        for head in headers_svcg:
        	summary_filePath = summary_dir + "summary_raw_sample_svcg_"  +    head   + ".csv"
        	with open(summary_filePath, 'a') as f:
        	 	f.write(head)
        	 	f.write(',COUNT,YEAR\n')
        	 	f.close()
        # ADD SUMMARY TO THE FILES CREATED!!
        for i in range(1999,2017):
            downloads_filePath = downloads_dir + "sample_svcg_" + str(i) + ".txt"
                
                # downloads_filePath = downloads_dir + "historical_data1_Q" + str(i) + "2007.txt"
                # cleaned_filePath = cleaned_dir + "cleaned_historical_data1_Q" + str(i) + "2007.csv"
            

            svcg_file = pd.read_csv(downloads_filePath ,sep="|", header=None, names = headers_svcg)
            svcg_file = svcg_file.reset_index()
            # svcg_file = svcg_file.set_index(['LOAN SEQUENCE NUMBER', 'MONTHLY REPORTING PERIOD'], inplace=False)
                # SUMMARIZE THE RAW SAMPLE FILE
            print(svcg_file[2:3])
            for head in headers_svcg:
                    # d = orig_file[['col1', 'col2', 'col3', 'col4']].groupby(['col1', 'col2']).agg(['mean', 'count'])
                
                
	            d = svcg_file.groupby(head).count()
	            d = svcg_file.groupby(head) \
	                          			.agg({'index'  : len }) \
	                            			.rename(columns={'index' : 'COUNT'}) 
	            d['Year']= str(i)
	            summary_filePath = summary_dir + "summary_raw_sample_svcg_"  +    head   + ".csv"

	            with open(summary_filePath, 'a') as f:
	                d.to_csv(f,sep=',', header=False)
	                f.close()
        print("SUMMARIZED RAW PERFORMANCE FILES")
