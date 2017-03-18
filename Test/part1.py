import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
from Classes.Part1.clean_orig import Clean_origination_data
from Classes.Part1.clean_perf import Clean_performance_data
# from Classes.Download_sf_loan import Download_loan_data
# from Classes.Summary_raw_data import Summary_raw_data
import re, os, zipfile, io
import numpy as np

        

class Summarize_data(luigi.Task):
  def requires(self):
    return[Clean_performance_data()]

  def output(self):
    return{ 'output1' : luigi.LocalTarget("summary/summary_sample_orig.csv") ,
    'output2' : luigi.LocalTarget("summary/summary_sample_orig_quarter.csv")  }

  def run(self):
    create_directory("summary")
    summary_filePath = "summary/summary_sample_orig.csv"
    summary_filePath2 = "summary/summary_sample_orig_quarter.csv"
    cleaned_dir = "cleaned/"
    
    
      
    for year in range (1999,2017):
        summary = pd.read_csv("cleaned/cleaned_sample_orig_" + str(year) + ".csv",
                              usecols = ['LOAN SEQUENCE NUMBER',
                                'LOAN PURPOSE',
                                'ORIGINAL LOAN TERM'])            

        summary = pd.read_csv("cleaned/cleaned_sample_orig_" + str(year) + ".csv",
                              usecols = ["ORIGINAL UPB",
                                         "ORIGINATION YEAR",
                                         "ORIGINATION QUARTER"])    

        #Sum of Original UPB
        s = summary.sum(axis=0)
        #print(s)

        #Sum of Original UPB per year
        s1=summary.groupby(["ORIGINATION YEAR"])["ORIGINAL UPB"].sum().reset_index(name="Sum of UPB per year")
    #     print(s1)


        #Sum of Original UPB per year per Quarter
        s3=summary.groupby(["ORIGINATION YEAR","ORIGINATION QUARTER"])["ORIGINAL UPB"].sum().reset_index(name="Sum of UPB per year per quarter")

        s4=summary.groupby(["ORIGINATION YEAR"])["ORIGINAL UPB"].mean().reset_index(name="Average of UPB per year")
    #     print(s4)

        #Average of Original UPB per year per Quarter
        s6=summary.groupby(["ORIGINATION YEAR","ORIGINATION QUARTER"])["ORIGINAL UPB"].mean().reset_index(name="Average of UPB per year per quarter")
    #     print(s6)


        summary = pd.read_csv("cleaned/cleaned_sample_orig_" + str(year) + ".csv",
                              usecols = ["CREDIT SCORE",
                                         "ORIGINATION YEAR",
                                         "ORIGINATION QUARTER"]) 

        #Average of Credit Score per year per Year
        s7=summary.groupby(["ORIGINATION YEAR"])["CREDIT SCORE"].mean().reset_index(name="Average of Credit Score per year")
    #     print(s7)


        #Average of Credit Score per year per Quarter
        s9=summary.groupby(["ORIGINATION YEAR","ORIGINATION QUARTER"])["CREDIT SCORE"].mean().reset_index(name="Average of Credit Score per year per quarter")

        
        
        all_year_summary = pd.merge((pd.merge(s1, s4, on = ["ORIGINATION YEAR"])), s7, on = ["ORIGINATION YEAR"])
        
        all_year_quarter_summary = pd.merge((pd.merge(s3, s6, on = ["ORIGINATION YEAR", "ORIGINATION QUARTER"])), s9, on = ["ORIGINATION YEAR", "ORIGINATION QUARTER" ])
        

        
        summary = pd.read_csv("cleaned/cleaned_sample_orig_" + str(year) + ".csv",
                              usecols = ["ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)",
                                         "ORIGINATION YEAR",
                                         "ORIGINATION QUARTER"]) 

        #Average of CLTV per year per Year
        s10=summary.groupby(["ORIGINATION YEAR"])["ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)"].mean().reset_index(name="Average of CLTV per year")


        #Average of CLTV per year per Quarter
        s12=summary.groupby(["ORIGINATION YEAR","ORIGINATION QUARTER"])["ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)"].mean().reset_index(name="Average of CLTV Score per year per quarter")


        all_year_summary = pd.merge(all_year_summary,s10, on = ["ORIGINATION YEAR"])
        
        all_year_quarter_summary = pd.merge(all_year_quarter_summary, s12, on = ["ORIGINATION YEAR", "ORIGINATION QUARTER"])
        
        
        summary = pd.read_csv("cleaned/cleaned_sample_orig_" + str(year) + ".csv",
                              usecols = ["ORIGINAL LOAN-TO-VALUE (LTV)",
                                         "ORIGINATION YEAR",
                                         "ORIGINATION QUARTER"]) 

        #Average of LTV per Year
        s13=summary.groupby(["ORIGINATION YEAR"])["ORIGINAL LOAN-TO-VALUE (LTV)"].mean().reset_index(name="Average of LTV per Year")

        #Average of LTV per year per Quarter
        s15=summary.groupby(["ORIGINATION YEAR","ORIGINATION QUARTER"])["ORIGINAL LOAN-TO-VALUE (LTV)"].mean().reset_index(name="Average of LTV Score per year per quarter")

        
        all_year_summary = all_year_summary = pd.merge(all_year_summary,s13, on = ["ORIGINATION YEAR"])
        all_year_quarter_summary = pd.merge(all_year_quarter_summary, s15, on = ["ORIGINATION YEAR", "ORIGINATION QUARTER"])
        
        
        summary = pd.read_csv("cleaned/cleaned_sample_orig_" + str(year) + ".csv",
                              usecols = ["ORIGINAL INTEREST RATE",
                                         "ORIGINATION YEAR",
                                         "ORIGINATION QUARTER"]) 

        #Average of Interest Rate per Year
        s16=summary.groupby(["ORIGINATION YEAR"])["ORIGINAL INTEREST RATE"].mean().reset_index(name="Average of Interest Rate per Year")


        #Average of Interest Rate per year per Quarter
        s18=summary.groupby(["ORIGINATION YEAR","ORIGINATION QUARTER"])["ORIGINAL INTEREST RATE"].mean().reset_index(name="Average of Interest rate per year per quarter")

        all_year_summary = all_year_summary = pd.merge(all_year_summary,s16, on = ["ORIGINATION YEAR"])
        all_year_quarter_summary = pd.merge(all_year_quarter_summary, s18, on = ["ORIGINATION YEAR", "ORIGINATION QUARTER"])
        

        summary = pd.read_csv("cleaned/cleaned_sample_orig_" + str(year) + ".csv",
                              usecols = ["LOAN SEQUENCE NUMBER","FIRST TIME HOMEBUYER FLAG","OCCUPANCY STATUS","LOAN PURPOSE"]) 

        #Count of Loans with First Time Home Buyer equal to "Y", Occupancy equal to "I" or "S" and Loan Purpose equal to "C" and "N"
        result = summary[((summary["FIRST TIME HOMEBUYER FLAG"] =='Y')) & ((summary["OCCUPANCY STATUS"]=='I') | (summary["OCCUPANCY STATUS"]=='S')) & ((summary["LOAN PURPOSE"]=='C') | (summary["LOAN PURPOSE"]=='N'))]
        
        s = int(result["LOAN SEQUENCE NUMBER"].count())
    #     print("COUNT OF FALSE Y FLAG FOR FIRSTTIME HOMEBUYER =  " )
    #     print(str(s))
        
        

        anomaly = pd.DataFrame({"ORIGINATION YEAR": [year], "COUNT OF FALSE Y FLAG FOR FIRSTTIME HOMEBUYER" : [s]})

        all_year_summary.loc[all_year_summary["ORIGINATION YEAR"] >=0 , 'ORIGINATION YEAR'] = year
        
        
        all_year_summary = pd.merge(all_year_summary,anomaly, on = ["ORIGINATION YEAR"])


        

        try:
            alls = pd.concat([alls, all_year_summary])
            alls_quarter = pd.concat([alls_quarter, all_year_quarter_summary])
        except:
            alls = all_year_summary
            alls_quarter = all_year_quarter_summary
    alls.to_csv(summary_filePath, sep=',', index = False)
    alls_quarter.to_csv(summary_filePath2, sep=',', index = False)
    print ("files summarized")
    

if __name__ == '__main__':
    luigi.run()