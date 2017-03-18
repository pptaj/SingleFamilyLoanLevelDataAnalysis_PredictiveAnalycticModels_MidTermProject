#install.packages("data.table")
library(data.table)
setwd("E:/Dropbox/1- Spring 2017 Courses/ADS/Midterm/ads_midterm_team7/")
performance_train <- fread("cleaned/cleaned_historical_data1_time_Q12005.csv",
                           select=c('LOAN SEQUENCE NUMBER', 'MONTHLY REPORTING PERIOD', 'CURRENT ACTUAL UPB', 
                                    'CURRENT LOAN DELINQUENCY STATUS', 'LOAN AGE', 'REMAINING MONTHS TO LEGAL MATURITY', 
                                    'REPURCHASE FLAG', 'MODIFICATION FLAG', 'ZERO BALANCE CODE', 'ZERO BALANCE EFFECTIVE DATE', 
                                    'CURRENT INTEREST RATE', 'CURRENT DEFERRED UPB', 'DUE DATE OF LAST PAID INSTALLMENT', 
                                    'MI RECOVERIES', 'NET SALES PROCEEDS', 'NON MI RECOVERIES', 'EXPENSES', 'LEGAL COSTS', 
                                    'MAINTENANCE AND PRESERVATION COSTS', 'TAXES AND INSURANCE', 'MISCELLANEOUS EXPENSES', 
                                    'ACTUAL LOSS CALCULATION', 'MODIFICATION COST', 'MONTHLY REPORTING YEAR', 
                                    'MONTHLY REPORTING MONTH', 'DELINQUENT', 'REPURCHASE FLAG YES', 'MODIFICATION FLAG YES', 
                                    'ZERO BALANCE EFFECTIVE YEAR', 'ZERO BALANCE EFFECTIVE MONTH', 
                                    'DUE DATE OF LAST PAID INSTALLMENT YEAR', 'DUE DATE OF LAST PAID INSTALLMENT MONTH'))


colnames(performance_train) <- c('LOAN.SEQUENCE.NUMBER', 'MONTHLY.REPORTING.PERIOD', 'CURRENT.ACTUAL.UPB', 
                                 'CURRENT.LOAN.DELINQUENCY.STATUS', 'LOAN.AGE', 
                                 'REMAINING.MONTHS.TO.LEGAL.MATURITY', 'REPURCHASE.FLAG', 'MODIFICATION.FLAG', 
                                 'ZERO.BALANCE.CODE', 'ZERO.BALANCE.EFFECTIVE.DATE', 'CURRENT.INTEREST.RATE',
                                 'CURRENT.DEFERRED.UPB', 'DUE.DATE.OF.LAST.PAID.INSTALLMENT', 'MI.RECOVERIES', 
                                 'NET.SALES.PROCEEDS', 'NON.MI.RECOVERIES', 'EXPENSES', 
                                 'LEGAL.COSTS', 'MAINTENANCE.AND.PRESERVATION.COSTS', 'TAXES.AND.INSURANCE', 
                                 'MISCELLANEOUS.EXPENSES', 'ACTUAL.LOSS.CALCULATION', 
                                 'MODIFICATION.COST', 'MONTHLY.REPORTING.YEAR', 'MONTHLY.REPORTING.MONTH', 'DELINQUENT', 
                                 'REPURCHASE.FLAG.YES', 'MODIFICATION.FLAG.YES', 
                                 'ZERO.BALANCE.EFFECTIVE.YEAR', 'ZERO.BALANCE.EFFECTIVE.MONTH', 
                                 'DUE.DATE.OF.LAST.PAID.INSTALLMENT.YEAR', 'DUE.DATE.OF.LAST.PAID.INSTALLMENT.MONTH')

performance_test <- fread("cleaned/cleaned_historical_data1_time_Q22005.csv",
                          select=c('LOAN SEQUENCE NUMBER', 'MONTHLY REPORTING PERIOD', 'CURRENT ACTUAL UPB', 
                                   'CURRENT LOAN DELINQUENCY STATUS', 'LOAN AGE', 'REMAINING MONTHS TO LEGAL MATURITY', 
                                   'REPURCHASE FLAG', 'MODIFICATION FLAG', 'ZERO BALANCE CODE', 'ZERO BALANCE EFFECTIVE DATE', 
                                   'CURRENT INTEREST RATE', 'CURRENT DEFERRED UPB', 'DUE DATE OF LAST PAID INSTALLMENT', 
                                   'MI RECOVERIES', 'NET SALES PROCEEDS', 'NON MI RECOVERIES', 'EXPENSES', 'LEGAL COSTS', 
                                   'MAINTENANCE AND PRESERVATION COSTS', 'TAXES AND INSURANCE', 'MISCELLANEOUS EXPENSES', 
                                   'ACTUAL LOSS CALCULATION', 'MODIFICATION COST', 'MONTHLY REPORTING YEAR', 
                                   'MONTHLY REPORTING MONTH', 'DELINQUENT', 'REPURCHASE FLAG YES', 'MODIFICATION FLAG YES', 
                                   'ZERO BALANCE EFFECTIVE YEAR', 'ZERO BALANCE EFFECTIVE MONTH', 
                                   'DUE DATE OF LAST PAID INSTALLMENT YEAR', 'DUE DATE OF LAST PAID INSTALLMENT MONTH'))

colnames(performance_test) <- c('LOAN.SEQUENCE.NUMBER', 'MONTHLY.REPORTING.PERIOD', 'CURRENT.ACTUAL.UPB', 
                                'CURRENT.LOAN.DELINQUENCY.STATUS', 'LOAN.AGE', 
                                'REMAINING.MONTHS.TO.LEGAL.MATURITY', 'REPURCHASE.FLAG', 'MODIFICATION.FLAG', 
                                'ZERO.BALANCE.CODE', 'ZERO.BALANCE.EFFECTIVE.DATE', 'CURRENT.INTEREST.RATE',
                                'CURRENT.DEFERRED.UPB', 'DUE.DATE.OF.LAST.PAID.INSTALLMENT', 'MI.RECOVERIES', 
                                'NET.SALES.PROCEEDS', 'NON.MI.RECOVERIES', 'EXPENSES', 
                                'LEGAL.COSTS', 'MAINTENANCE.AND.PRESERVATION.COSTS', 'TAXES.AND.INSURANCE', 
                                'MISCELLANEOUS.EXPENSES', 'ACTUAL.LOSS.CALCULATION', 
                                'MODIFICATION.COST', 'MONTHLY.REPORTING.YEAR', 'MONTHLY.REPORTING.MONTH', 'DELINQUENT', 
                                'REPURCHASE.FLAG.YES', 'MODIFICATION.FLAG.YES', 
                                'ZERO.BALANCE.EFFECTIVE.YEAR', 'ZERO.BALANCE.EFFECTIVE.MONTH', 
                                'DUE.DATE.OF.LAST.PAID.INSTALLMENT.YEAR', 'DUE.DATE.OF.LAST.PAID.INSTALLMENT.MONTH')

gc()

#fitting the logistic regression model, based on the important parameters
#credit_limit, sex, education, marriage, age, bill amount, amount paid and status are important parameters amongst all others
modelLogit <-  randomForest(DELINQUENT ~ ., family=binomial(link='logit'), data=train)

#summary of the logistic regression
summary(modelLogit)

#analyzing the table of deviance
anova(modelLogit, test="Chisq")

gc()
#r2 in logit, we see McFadden which is similar to R2. Closer to zero implies model is good
#install.packages("pscl")
library(pscl)
pR2(modelLogit)




######## END OF LOGISTIC REGRESSION #######
###########################################



