#read the train data (Quarter 2, 2003)
install.packages("forecast")
install.packages("data.table")
library(foreach)
library(data.table)
train <- fread("D:/ADS/ads_team_7-ads_midterm_team7-276bcb1fad71/ads_midterm_team7/files/cleaned_historical_data1_Q22005.csv",select=c('CREDIT SCORE', 'FIRST PAYMENT YEAR', 'FIRST PAYMENT MONTH',
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
                     'METROPOLITANSTATISTICALAREA.MSA.ORMETROPOLITANDIVISION',
                     'MORTGAGEINSURANCEPERCENTAGE.MI..','NUMBEROFUNITS',
                     'ORIGINALCOMBINEDLOAN.TO.VALUE.CLTV.','ORIGINALDEBT.TO.INCOME.DTI.RATIO',
                     'ORIGINALUPB','ORIGINALLOAN.TO.VALUE.LTV','ORIGINALINTERESTRATE',
                     'POSTALCODE','ORIGINALLOANTERM','NUMBEROFBORROWERS','FIRSTTIMEHOMEBUYERFLAGYES',
                     'FIRSTTIMEHOMEBUYERFLAGNO','FIRSTTIMEHOMEBUYERFLAGNA','METROPOLITAN_AREA_FLAG','MORTGAGE_INSURANCE_FLAG','OWNEROCCUPIEDFLAG','INVESTMENTPROPERTYFLAG',
                     'SECONDHOMESPACEFLAG','RETAILCHANNELFLAG','BROKERCHANNELFLAG','CORRESPONDENTCHANNELFLAG',
                     'TP0NOTSPECIFIEDCHANNELFLAG','PREPAYMENTPENALTYMORTGAGE.PPM.FLAGYES',
                     'PREPAYMENTPENALTYMORTGAGE.PPM.FLAGNO','FIXEDRATEMORTGAGEPRODUCTTYPEFLAGYES',
                     'FIXEDRATEMORTGAGEPRODUCTTYPEFLAGNO','CONDOPROPERTYTYPEFLAG','LEASEHOLDPROPERTYTYPEFLAG',
                     'PUDPROPERTYTYPEFLAG','MANUFACTUREHOUSINGPROPERTYTYPEFLAG','FREESIMPLEHOUSINGPROPERTYTYPEFLAG',
                     'COOPHOUSINGPROPERTYTYPEFLAG','ORIGINATIONYEAR','ORIGINATIONQUARTER','LOANPURPOSEISPURCHASEFLAG',
                     'LOANPURPOSEISCASHOUTREFINANCEFLAG','LOANPURPOSEISNOCASHOUTREFINANCEFLAG',
                     'SUPERCONFORMINGFLAGYES','SUPERCONFORMINGFLAGNO')



library(forecast)
lm.fit = lm(ORIGINALINTERESTRATE ~ .,data = train)
summary(lm.fit)


test <- fread("D:/ADS/ads_team_7-ads_midterm_team7-276bcb1fad71/ads_midterm_team7/files/cleaned_historical_data1_Q32005.csv",select=c('CREDIT SCORE', 'FIRST PAYMENT YEAR', 'FIRST PAYMENT MONTH',
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
                     'METROPOLITANSTATISTICALAREA.MSA.ORMETROPOLITANDIVISION',
                     'MORTGAGEINSURANCEPERCENTAGE.MI..','NUMBEROFUNITS',
                     'ORIGINALCOMBINEDLOAN.TO.VALUE.CLTV.','ORIGINALDEBT.TO.INCOME.DTI.RATIO',
                     'ORIGINALUPB','ORIGINALLOAN.TO.VALUE.LTV','ORIGINALINTERESTRATE',
                     'POSTALCODE','ORIGINALLOANTERM','NUMBEROFBORROWERS','FIRSTTIMEHOMEBUYERFLAGYES',
                     'FIRSTTIMEHOMEBUYERFLAGNO','FIRSTTIMEHOMEBUYERFLAGNA','METROPOLITAN_AREA_FLAG','MORTGAGE_INSURANCE_FLAG','OWNEROCCUPIEDFLAG','INVESTMENTPROPERTYFLAG',
                     'SECONDHOMESPACEFLAG','RETAILCHANNELFLAG','BROKERCHANNELFLAG','CORRESPONDENTCHANNELFLAG',
                     'TP0NOTSPECIFIEDCHANNELFLAG','PREPAYMENTPENALTYMORTGAGE.PPM.FLAGYES',
                     'PREPAYMENTPENALTYMORTGAGE.PPM.FLAGNO','FIXEDRATEMORTGAGEPRODUCTTYPEFLAGYES',
                     'FIXEDRATEMORTGAGEPRODUCTTYPEFLAGNO','CONDOPROPERTYTYPEFLAG','LEASEHOLDPROPERTYTYPEFLAG',
                     'PUDPROPERTYTYPEFLAG','MANUFACTUREHOUSINGPROPERTYTYPEFLAG','FREESIMPLEHOUSINGPROPERTYTYPEFLAG',
                     'COOPHOUSINGPROPERTYTYPEFLAG','ORIGINATIONYEAR','ORIGINATIONQUARTER','LOANPURPOSEISPURCHASEFLAG',
                     'LOANPURPOSEISCASHOUTREFINANCEFLAG','LOANPURPOSEISNOCASHOUTREFINANCEFLAG',
                     'SUPERCONFORMINGFLAGYES','SUPERCONFORMINGFLAGNO')

library(forecast)
pred = predict(lm.fit, test)
accuracy(pred, train$ORIGINALINTERESTRATE)

#Selecting only the significat Columns:

#train2 <- subset(df1, select = c(1, 2, 5))

train2 <- subset(train, select =  c('CREDITSCORE','FIRSTPAYMENTYEAR','FIRSTPAYMENTMONTH',
                                    'MATURITYYEAR','MATURITYMONTH',
                                    'METROPOLITANSTATISTICALAREA.MSA.ORMETROPOLITANDIVISION',
                                    'MORTGAGEINSURANCEPERCENTAGE.MI..','NUMBEROFUNITS',
                                    'ORIGINALCOMBINEDLOAN.TO.VALUE.CLTV.','ORIGINALDEBT.TO.INCOME.DTI.RATIO',
                                    'ORIGINALUPB','ORIGINALLOAN.TO.VALUE.LTV','ORIGINALINTERESTRATE',
                                    'POSTALCODE','NUMBEROFBORROWERS','FIRSTTIMEHOMEBUYERFLAGYES',
                                    'FIRSTTIMEHOMEBUYERFLAGNO','METROPOLITAN_AREA_FLAG','MORTGAGE_INSURANCE_FLAG','OWNEROCCUPIEDFLAG','INVESTMENTPROPERTYFLAG',
                                   'RETAILCHANNELFLAG','BROKERCHANNELFLAG','CORRESPONDENTCHANNELFLAG',
                                    'TP0NOTSPECIFIEDCHANNELFLAG','PREPAYMENTPENALTYMORTGAGE.PPM.FLAGYES',
                                   'CONDOPROPERTYTYPEFLAG','LEASEHOLDPROPERTYTYPEFLAG',
                                    'PUDPROPERTYTYPEFLAG','MANUFACTUREHOUSINGPROPERTYTYPEFLAG','FREESIMPLEHOUSINGPROPERTYTYPEFLAG',
                                    'LOANPURPOSEISPURCHASEFLAG',
                                    'LOANPURPOSEISCASHOUTREFINANCEFLAG'))

#Removing the insignificant columns (Singularity)
pred = predict(lm.fit, test)
accuracy(pred, train$ORIGINALINTERESTRATE)

#Forward Selection
install.packages("MASS")
library(MASS)
fit <- lm(ORIGINALINTERESTRATE ~ .,data = train2)
step <- stepAIC(fit, direction="forward")
step$anova # display results
#************************************************************************************************************
#EXHAUSTIVE SEARCH
#install.packages('ISLR',repos = "http://cran.us.r-project.org")
#install.packages("leaps", repos = "http://cran.us.r-project.org")
library(leaps)
library(ISLR)
regfit.full = regsubsets(ORIGINALINTERESTRATE ~ .,data = train2,method = "exhaustive",nvmax = 10)
reg.summary = summary(regfit.full)
names(reg.summary)
reg.summary$rss
#PLOTTING
par(mfrow=c(2,2)) 
plot(reg.summary$rss ,xlab="Number of Variables ",ylab="RSS", type="l") 
plot(reg.summary$adjr2 ,xlab="Number of Variables ", ylab="Adjusted RSq",type="l")
coef(regfit.full ,10)
#Choosing exhaustive search columns
train_exhaustive = subset(train2, select =  c('CREDITSCORE','FIRSTPAYMENTMONTH',
                                   'MATURITYYEAR','ORIGINALUPB',
                                   'MORTGAGE_INSURANCE_FLAG',
                                   'INVESTMENTPROPERTYFLAG','CORRESPONDENTCHANNELFLAG','ORIGINALINTERESTRATE',
                                   'PREPAYMENTPENALTYMORTGAGE.PPM.FLAGYES','FREESIMPLEHOUSINGPROPERTYTYPEFLAG','LOANPURPOSEISCASHOUTREFINANCEFLAG'))
lm.fit_exhaustive = lm(ORIGINALINTERESTRATE ~ .,data = train_exhaustive)
summary(lm.fit_exhaustive)
#Test Exhaustive subset
test_exhaustive = subset(test, select =  c('CREDITSCORE','FIRSTPAYMENTMONTH',
                                              'MATURITYYEAR','ORIGINALUPB',
                                              'MORTGAGE_INSURANCE_FLAG',
                                              'INVESTMENTPROPERTYFLAG','CORRESPONDENTCHANNELFLAG','ORIGINALINTERESTRATE',
                                              'PREPAYMENTPENALTYMORTGAGE.PPM.FLAGYES','FREESIMPLEHOUSINGPROPERTYTYPEFLAG','LOANPURPOSEISCASHOUTREFINANCEFLAG'))

#Predict Exhaustive 
pred_exhaustive = predict(lm.fit_exhaustive, test_exhaustive)
#Accuracy Exhaustive
accuracy(pred_exhaustive, train_exhaustive$ORIGINALINTERESTRATE)
#************************************************************************************************************
#FORWARD SELECTION

library(leaps)
library(ISLR)
regfit.forward = regsubsets(ORIGINALINTERESTRATE ~ .,data = train2,method = "forward",nvmax = 30)
reg.fwd.summary = summary(regfit.forward)
names(reg.fwd.summary)
#Plotting
par(mfrow=c(2,2)) 
plot(reg.fwd.summary$rss ,xlab="Number of Variables ",ylab="RSS", type="l") 
plot(reg.fwd.summary$adjr2 ,xlab="Number of Variables ", ylab="Adjusted RSq",type="l")
coef(regfit.forward ,10)

#************************************************************************************************************
#BACKWARD SELECTION

library(leaps)
library(ISLR)
regfit.backward = regsubsets(ORIGINALINTERESTRATE ~ .,data = train2,method = "backward",nvmax = 30)
reg.bcwd.summary = summary(regfit.backward)
names(reg.bcwd.summary)
#Plotting
par(mfrow=c(2,2)) 
plot(reg.bcwd.summary$rss ,xlab="Number of Variables ",ylab="RSS", type="l") 
plot(reg.bcwd.summary$adjr2 ,xlab="Number of Variables ", ylab="Adjusted RSq",type="l")
coef(regfit.backward ,10)

#Choosing backward search columns
train_backward  = subset(train, select =  c('CREDITSCORE','FIRSTPAYMENTMONTH',
                                              'MATURITYYEAR','ORIGINALUPB',
                                              'MORTGAGE_INSURANCE_FLAG',
                                              'INVESTMENTPROPERTYFLAG','RETAILCHANNELFLAG','CORRESPONDENTCHANNELFLAG',
                                              'FREESIMPLEHOUSINGPROPERTYTYPEFLAG','ORIGINALINTERESTRATE','LOANPURPOSEISCASHOUTREFINANCEFLAG'))
lm.fit_backward = lm(ORIGINALINTERESTRATE ~ .,data = train_backward)
summary(lm.fit_backward)
#Test Exhaustive subset
test_backward = subset(train, select =  c('CREDITSCORE','FIRSTPAYMENTMONTH',
                                         'MATURITYYEAR','ORIGINALUPB',
                                         'MORTGAGE_INSURANCE_FLAG',
                                         'INVESTMENTPROPERTYFLAG','RETAILCHANNELFLAG','CORRESPONDENTCHANNELFLAG',
                                         'FREESIMPLEHOUSINGPROPERTYTYPEFLAG','LOANPURPOSEISCASHOUTREFINANCEFLAG'))
#Predict Exhaustive 
pred_backward = predict(lm.fit_backward, test_backward)
#Accuracy Exhaustive
accuracy(pred_backward, train_backward$ORIGINALINTERESTRATE)
#************************************************************************************************************
#RANDOM FOREST
#************************************************************************************************************
#install.packages("randomForest")
#install.packages("MASS")
library(randomForest)
library(MASS)
rf <- randomForest(ORIGINALINTERESTRATE~CREDITSCORE,data = train_backward, n_tree=1)

#************************************************************************************************************
#NEURALNETS
#************************************************************************************************************
install.packages("grid")
install.packages("neuralnet")
#library (MASS)
library (grid)
library (neuralnet)
trainingdata <- train_backward[ ,-c('ORIGINALINTERESTRATE')]
trainingoutput <- train_backward$ORIGINALINTERESTRATE
gc()
n <- names(train_backward)
f <- as.formula(paste("ORIGINALINTERESTRATE~", paste(n[!n %in% "ORIGINALINTERESTRATE"],collapse="+")))
net.interest <- neuralnet(f, data = train_backward, hidden=c(5,3),linear.output=T)
plot(net.interest)
#PREDICTING USING THE NEURAL NETWORK
predicted.nn.values <- compute(net.interest,test_backward)
#Caculating MSE
nrow(test_nn_values)
test_nn_values <- as.data.frame(test$ORIGINALINTERESTRATE)
pred_df <- as.data.frame(predicted.nn.values$net.result)
x <- (test_nn_values - pred_df)
sum((x^2))/nrow(test_nn_values)




