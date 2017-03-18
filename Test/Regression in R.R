#read the train data (Quarter 2, 2003)
install.packages("forecast")
install.packages("data.table")
library(foreach)
library(data.table)
train <- fread("D:/ADS/ads_team_7-ads_midterm_team7-276bcb1fad71/files/cleaned_historical_data1_Q22005.csv",select=c('CREDIT SCORE', 'FIRST PAYMENT YEAR', 'FIRST PAYMENT MONTH',
                                                                                                                     'MATURITY YEAR', 'MATURITY MONTH',
                                                                                                                     'METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION', 
                                                                                                                     'MORTGAGE INSURANCE PERCENTAGE (MI %)', 'NUMBER OF UNITS',
                                                                                                                     'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT-TO-INCOME (DTI) RATIO', 
                                                                                                                     'ORIGINAL UPB', 'ORIGINAL LOAN-TO-VALUE (LTV)', 'ORIGINAL INTEREST RATE',
                                                                                                                     'POSTAL CODE','ORIGINAL LOAN TERM','NUMBER OF BORROWERS', 'FIRST TIME HOMEBUYER FLAG YES',
                                                                                                                     'FIRST TIME HOMEBUYER FLAG NO', 'FIRST TIME HOMEBUYER FLAG NA','METROPOLITAN_AREA_FLAG', 'MORTGAGE_INSURANCE_FLAG', 'OWNER OCCUPIED FLAG', 'INVESTMENT PROPERTY FLAG', 
                                                                                                                     'SECOND HOME SPACE FLAG', 'RETAIL CHANNEL FLAG', 'BROKER CHANNEL FLAG', 'CORRESPONDENT CHANNEL FLAG',
                                                                                                                     'TP0 NOT SPECIFIED CHANNEL FLAG', 'PREPAYMENT PENALTY MORTGAGE (PPM) FLAG YES', 
                                                                                                                     'PREPAYMENT PENALTY MORTGAGE (PPM) FLAG NO', 'FIXED RATE MORTGAGE PRODUCT TYPE FLAG YES', 
                                                                                                                     'FIXED RATE MORTGAGE PRODUCT TYPE FLAG NO', 'CONDO PROPERTY TYPE FLAG', 'LEASE HOLD PROPERTY TYPE FLAG',
                                                                                                                     'PUD PROPERTY TYPE FLAG', 'MANUFACTURE HOUSING PROPERTY TYPE FLAG', 'FREE SIMPLE HOUSING PROPERTY TYPE FLAG', 
                                                                                                                     'CO OP HOUSING PROPERTY TYPE FLAG', 'ORIGINATION YEAR', 'ORIGINATION QUARTER', 'LOAN PURPOSE IS PURCHASE FLAG',
                                                                                                                     'LOAN PURPOSE IS CASH OUT REFINANCE FLAG', 'LOAN PURPOSE IS NO CASH OUT REFINANCE FLAG',
                                                                                                                     'SUPER CONFORMING FLAG YES', 'SUPER CONFORMING FLAG NO'))

colnames(train) <- c('CREDITSCORE','FIRSTPAYMENTYEAR','FIRSTPAYMENTMONTH',
                     'MATURITYYEAR','MATURITYMONTH',
                     'METROPOLITANSTATISTICALAREA(MSA)ORMETROPOLITANDIVISION',
                     'MORTGAGEINSURANCEPERCENTAGE(MI%)','NUMBEROFUNITS',
                     'ORIGINALCOMBINEDLOAN-TO-VALUE(CLTV)','ORIGINALDEBT-TO-INCOME(DTI)RATIO',
                     'ORIGINALUPB','ORIGINALLOAN-TO-VALUE(LTV)','ORIGINALINTERESTRATE',
                     'POSTALCODE','ORIGINALLOANTERM','NUMBEROFBORROWERS','FIRSTTIMEHOMEBUYERFLAGYES',
                     'FIRSTTIMEHOMEBUYERFLAGNO','FIRSTTIMEHOMEBUYERFLAGNA','METROPOLITAN_AREA_FLAG','MORTGAGE_INSURANCE_FLAG','OWNEROCCUPIEDFLAG','INVESTMENTPROPERTYFLAG',
                     'SECONDHOMESPACEFLAG','RETAILCHANNELFLAG','BROKERCHANNELFLAG','CORRESPONDENTCHANNELFLAG',
                     'TP0NOTSPECIFIEDCHANNELFLAG','PREPAYMENTPENALTYMORTGAGE(PPM)FLAGYES',
                     'PREPAYMENTPENALTYMORTGAGE(PPM)FLAGNO','FIXEDRATEMORTGAGEPRODUCTTYPEFLAGYES',
                     'FIXEDRATEMORTGAGEPRODUCTTYPEFLAGNO','CONDOPROPERTYTYPEFLAG','LEASEHOLDPROPERTYTYPEFLAG',
                     'PUDPROPERTYTYPEFLAG','MANUFACTUREHOUSINGPROPERTYTYPEFLAG','FREESIMPLEHOUSINGPROPERTYTYPEFLAG',
                     'COOPHOUSINGPROPERTYTYPEFLAG','ORIGINATIONYEAR','ORIGINATIONQUARTER','LOANPURPOSEISPURCHASEFLAG',
                     'LOANPURPOSEISCASHOUTREFINANCEFLAG','LOANPURPOSEISNOCASHOUTREFINANCEFLAG',
                     'SUPERCONFORMINGFLAGYES','SUPERCONFORMINGFLAGNO')

library(forecast)
lm.fit = lm(ORIGINALINTERESTRATE ~ .,data = train)
summary(lm.fit)

train <- fread("D:/ADS/ads_team_7-ads_midterm_team7-276bcb1fad71/files/cleaned_historical_data1_Q22005.csv",select=c('CREDIT SCORE', 'FIRST PAYMENT YEAR', 'FIRST PAYMENT MONTH',
                                                                                                                     'MATURITY YEAR', 'MATURITY MONTH',
                                                                                                                     'METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION', 
                                                                                                                     'MORTGAGE INSURANCE PERCENTAGE (MI %)', 'NUMBER OF UNITS',
                                                                                                                     'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT-TO-INCOME (DTI) RATIO', 
                                                                                                                     'ORIGINAL UPB', 'ORIGINAL LOAN-TO-VALUE (LTV)', 'ORIGINAL INTEREST RATE',
                                                                                                                     'POSTAL CODE','ORIGINAL LOAN TERM','NUMBER OF BORROWERS', 'FIRST TIME HOMEBUYER FLAG YES',
                                                                                                                     'FIRST TIME HOMEBUYER FLAG NO', 'FIRST TIME HOMEBUYER FLAG NA','METROPOLITAN_AREA_FLAG', 'MORTGAGE_INSURANCE_FLAG', 'OWNER OCCUPIED FLAG', 'INVESTMENT PROPERTY FLAG', 
                                                                                                                     'SECOND HOME SPACE FLAG', 'RETAIL CHANNEL FLAG', 'BROKER CHANNEL FLAG', 'CORRESPONDENT CHANNEL FLAG',
                                                                                                                     'TP0 NOT SPECIFIED CHANNEL FLAG', 'PREPAYMENT PENALTY MORTGAGE (PPM) FLAG YES', 
                                                                                                                     'PREPAYMENT PENALTY MORTGAGE (PPM) FLAG NO', 'FIXED RATE MORTGAGE PRODUCT TYPE FLAG YES', 
                                                                                                                     'FIXED RATE MORTGAGE PRODUCT TYPE FLAG NO', 'CONDO PROPERTY TYPE FLAG', 'LEASE HOLD PROPERTY TYPE FLAG',
                                                                                                                     'PUD PROPERTY TYPE FLAG', 'MANUFACTURE HOUSING PROPERTY TYPE FLAG', 'FREE SIMPLE HOUSING PROPERTY TYPE FLAG', 
                                                                                                                     'CO OP HOUSING PROPERTY TYPE FLAG', 'ORIGINATION YEAR', 'ORIGINATION QUARTER', 'LOAN PURPOSE IS PURCHASE FLAG',
                                                                                                                     'LOAN PURPOSE IS CASH OUT REFINANCE FLAG', 'LOAN PURPOSE IS NO CASH OUT REFINANCE FLAG',
                                                                                                                     'SUPER CONFORMING FLAG YES', 'SUPER CONFORMING FLAG NO'))


#Selecting only the significat Columns:

train2 <- subset(df1, select = c(1, 2, 5))

test <- fread("D:/ADS/ads_team_7-ads_midterm_team7-276bcb1fad71/files/cleaned_historical_data1_Q32005.csv",select=c('CREDIT SCORE', 'FIRST PAYMENT YEAR', 'FIRST PAYMENT MONTH',
                                                                                                                    'MATURITY YEAR', 'MATURITY MONTH',
                                                                                                                    'METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION', 
                                                                                                                    'MORTGAGE INSURANCE PERCENTAGE (MI %)', 'NUMBER OF UNITS',
                                                                                                                    'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT-TO-INCOME (DTI) RATIO', 
                                                                                                                    'ORIGINAL UPB', 'ORIGINAL LOAN-TO-VALUE (LTV)', 'ORIGINAL INTEREST RATE',
                                                                                                                    'POSTAL CODE','ORIGINAL LOAN TERM','NUMBER OF BORROWERS', 'FIRST TIME HOMEBUYER FLAG YES',
                                                                                                                    'FIRST TIME HOMEBUYER FLAG NO', 'FIRST TIME HOMEBUYER FLAG NA','METROPOLITAN_AREA_FLAG', 'MORTGAGE_INSURANCE_FLAG', 'OWNER OCCUPIED FLAG', 'INVESTMENT PROPERTY FLAG', 
                                                                                                                    'SECOND HOME SPACE FLAG', 'RETAIL CHANNEL FLAG', 'BROKER CHANNEL FLAG', 'CORRESPONDENT CHANNEL FLAG',
                                                                                                                    'TP0 NOT SPECIFIED CHANNEL FLAG', 'PREPAYMENT PENALTY MORTGAGE (PPM) FLAG YES', 
                                                                                                                    'PREPAYMENT PENALTY MORTGAGE (PPM) FLAG NO', 'FIXED RATE MORTGAGE PRODUCT TYPE FLAG YES', 
                                                                                                                    'FIXED RATE MORTGAGE PRODUCT TYPE FLAG NO', 'CONDO PROPERTY TYPE FLAG', 'LEASE HOLD PROPERTY TYPE FLAG',
                                                                                                                    'PUD PROPERTY TYPE FLAG', 'MANUFACTURE HOUSING PROPERTY TYPE FLAG', 'FREE SIMPLE HOUSING PROPERTY TYPE FLAG', 
                                                                                                                    'CO OP HOUSING PROPERTY TYPE FLAG', 'ORIGINATION YEAR', 'ORIGINATION QUARTER', 'LOAN PURPOSE IS PURCHASE FLAG',
                                                                                                                    'LOAN PURPOSE IS CASH OUT REFINANCE FLAG', 'LOAN PURPOSE IS NO CASH OUT REFINANCE FLAG',
                                                                                                                    'SUPER CONFORMING FLAG YES', 'SUPER CONFORMING FLAG NO'))


colnames(test) <- c('CREDITSCORE','FIRSTPAYMENTYEAR','FIRSTPAYMENTMONTH',
                    'MATURITYYEAR','MATURITYMONTH',
                    'METROPOLITANSTATISTICALAREA(MSA)ORMETROPOLITANDIVISION',
                    'MORTGAGEINSURANCEPERCENTAGE(MI%)','NUMBEROFUNITS',
                    'ORIGINALCOMBINEDLOAN-TO-VALUE(CLTV)','ORIGINALDEBT-TO-INCOME(DTI)RATIO',
                    'ORIGINALUPB','ORIGINALLOAN-TO-VALUE(LTV)','ORIGINALINTERESTRATE',
                    'POSTALCODE','ORIGINALLOANTERM','NUMBEROFBORROWERS','FIRSTTIMEHOMEBUYERFLAGYES',
                    'FIRSTTIMEHOMEBUYERFLAGNO','FIRSTTIMEHOMEBUYERFLAGNA','METROPOLITAN_AREA_FLAG','MORTGAGE_INSURANCE_FLAG','OWNEROCCUPIEDFLAG','INVESTMENTPROPERTYFLAG',
                    'SECONDHOMESPACEFLAG','RETAILCHANNELFLAG','BROKERCHANNELFLAG','CORRESPONDENTCHANNELFLAG',
                    'TP0NOTSPECIFIEDCHANNELFLAG','PREPAYMENTPENALTYMORTGAGE(PPM)FLAGYES',
                    'PREPAYMENTPENALTYMORTGAGE(PPM)FLAGNO','FIXEDRATEMORTGAGEPRODUCTTYPEFLAGYES',
                    'FIXEDRATEMORTGAGEPRODUCTTYPEFLAGNO','CONDOPROPERTYTYPEFLAG','LEASEHOLDPROPERTYTYPEFLAG',
                    'PUDPROPERTYTYPEFLAG','MANUFACTUREHOUSINGPROPERTYTYPEFLAG','FREESIMPLEHOUSINGPROPERTYTYPEFLAG',
                    'COOPHOUSINGPROPERTYTYPEFLAG','ORIGINATIONYEAR','ORIGINATIONQUARTER','LOANPURPOSEISPURCHASEFLAG',
                    'LOANPURPOSEISCASHOUTREFINANCEFLAG','LOANPURPOSEISNOCASHOUTREFINANCEFLAG',
                    'SUPERCONFORMINGFLAGYES','SUPERCONFORMINGFLAGNO')
pred = predict(lm.fit, test)
accuracy(pred, train$ORIGINALINTERESTRATE)


train2 <- subset(train, select =  c('CREDITSCORE','FIRSTPAYMENTYEAR','FIRSTPAYMENTMONTH',
                                    'MATURITYYEAR','MATURITYMONTH',
                                    'METROPOLITANSTATISTICALAREA(MSA)ORMETROPOLITANDIVISION',
                                    'MORTGAGEINSURANCEPERCENTAGE(MI%)','NUMBEROFUNITS',
                                    'ORIGINALCOMBINEDLOAN-TO-VALUE(CLTV)','ORIGINALDEBT-TO-INCOME(DTI)RATIO',
                                    'ORIGINALUPB','ORIGINALLOAN-TO-VALUE(LTV)','ORIGINALINTERESTRATE',
                                    'POSTALCODE','NUMBEROFBORROWERS','FIRSTTIMEHOMEBUYERFLAGYES',
                                    'FIRSTTIMEHOMEBUYERFLAGNO','METROPOLITAN_AREA_FLAG','MORTGAGE_INSURANCE_FLAG','OWNEROCCUPIEDFLAG','INVESTMENTPROPERTYFLAG',
                                    'RETAILCHANNELFLAG','BROKERCHANNELFLAG','CORRESPONDENTCHANNELFLAG',
                                    'PREPAYMENTPENALTYMORTGAGE(PPM)FLAGYES',
                                    'PREPAYMENTPENALTYMORTGAGE(PPM)FLAGNO','FIXEDRATEMORTGAGEPRODUCTTYPEFLAGYES',
                                    'FIXEDRATEMORTGAGEPRODUCTTYPEFLAGNO','CONDOPROPERTYTYPEFLAG','LEASEHOLDPROPERTYTYPEFLAG',
                                    'PUDPROPERTYTYPEFLAG','MANUFACTUREHOUSINGPROPERTYTYPEFLAG','FREESIMPLEHOUSINGPROPERTYTYPEFLAG',
                                    'COOPHOUSINGPROPERTYTYPEFLAG','ORIGINATIONYEAR','ORIGINATIONQUARTER','LOANPURPOSEISPURCHASEFLAG',
                                    'LOANPURPOSEISCASHOUTREFINANCEFLAG','LOANPURPOSEISNOCASHOUTREFINANCEFLAG',
                                    'SUPERCONFORMINGFLAGYES','SUPERCONFORMINGFLAGNO'))

#Removing the insignificant columns (Singularity)
