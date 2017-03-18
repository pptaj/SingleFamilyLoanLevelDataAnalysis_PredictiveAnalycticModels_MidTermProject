import luigi
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import mechanicalsoup
import pandas as pd
from Classes.Utils import create_directory
from Classes.Part2.clean_orig import Clean_origination_data
from Classes.Part2.clean_perf import Clean_performance_data
# from Classes.Download_sf_loan import Download_loan_data
# from Classes.Summary_raw_data import Summary_raw_data
import re, os, zipfile, io
import numpy as np

        

class Build_prediction_model(luigi.Task):
  def requires(self):
    return[Clean_performance_data()]

  def output(self):
    return{ 'output1' : luigi.LocalTarget("summary/summary_sample_orig_2016.csv") ,\
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
    create_directory("summary")
    summary_dir = "summary/"
    cleaned_dir = "cleaned/"
    
    
      
    # Itereate through all the years. Check if the cleaned file exists! If not Read the downloads csv and Clean it. And Place it in the cleaned directory
    # for i in range(1999,2017):
      
    #   cleaned_filePath = cleaned_dir + "cleaned_sample_orig_" + str(i) + ".csv"
    #   summary_filePath = summary_dir + "summary_orig_" + str(i) + ".csv"
    #   if not (os.path.isfile(summary_filePath)):

    #     # LOAD THE PERFORMANCE DATA
    #     orig = pd.read_csv(cleaned_filePath,sep="|", header=None)



    #     # SAVE DATAFRAME TO CLEANED DIRECTORY


    print ("Building Prediction Model")








if __name__ == '__main__':
    luigi.run()