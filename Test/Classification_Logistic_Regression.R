#install.packages("data.table")
setwd("E:/Dropbox/1- Spring 2017 Courses/ADS/Midterm/ads_midterm_team7/")

library(data.table)

performance_train <- fread("cleaned/cleaned_sample_svcg_2005.csv",
                    select=c("LOAN SEQUENCE NUMBER",
                      "CURRENT ACTUAL UPB",
                             "LOAN AGE", "REMAINING MONTHS TO LEGAL MATURITY",
                             "ZERO BALANCE CODE",
                             "CURRENT INTEREST RATE",
                             "MONTHLY REPORTING YEAR",
                             "MONTHLY REPORTING MONTH", "DELINQUENT", "REPURCHASE FLAG YES", "MODIFICATION FLAG YES",
                             "ZERO BALANCE EFFECTIVE YEAR", "ZERO BALANCE EFFECTIVE MONTH",
                             "DUE DATE OF LAST PAID INSTALLMENT YEAR", "DUE DATE OF LAST PAID INSTALLMENT MONTH"))

# Removing spaces from col names
colnames(performance_train) <- c("LOAN_SEQUENCE_NUMBER", "CURRENTACTUALUPB",
                          "LOANAGE","REMAININGMONTHSTOLEGALMATURITY",
                          "ZEROBALANCECODE",
                          "CURRENTINTERESTRATE",
                          "MONTHLYREPORTINGYEAR",
                          "MONTHLYREPORTINGMONTH","DELINQUENT","REPURCHASEFLAGYES","MODIFICATIONFLAGYES",
                          "ZEROBALANCEEFFECTIVEYEAR","ZEROBALANCEEFFECTIVEMONTH",
                          "DUEDATEOFLASTPAIDINSTALLMENTYEAR","DUEDATEOFLASTPAIDINSTALLMENTMONTH")

origination_train <- fread("cleaned/cleaned_sample_orig_2005.csv",
                                                select=c("LOAN SEQUENCE NUMBER",
                                                      'CREDIT SCORE',
                                                         'NUMBER OF UNITS',
                                                         'ORIGINAL INTEREST RATE'
                                                         ))

# Removing spaces from col names
colnames(origination_train) <- c("LOAN_SEQUENCE_NUMBER",'CREDIT_SCORE',
                                'NUMBER_OF_UNITS',
                                'ORIGINAL_INTEREST_RATE'
                                )


performance_test <- fread("cleaned/cleaned_sample_svcg_2006.csv",
                          select=c("LOAN SEQUENCE NUMBER","CURRENT ACTUAL UPB",
                                   "LOAN AGE", "REMAINING MONTHS TO LEGAL MATURITY",
                                   "ZERO BALANCE CODE",
                                   "CURRENT INTEREST RATE",
                                   "MONTHLY REPORTING YEAR",
                                   "MONTHLY REPORTING MONTH", "DELINQUENT", "REPURCHASE FLAG YES", "MODIFICATION FLAG YES",
                                   "ZERO BALANCE EFFECTIVE YEAR", "ZERO BALANCE EFFECTIVE MONTH",
                                   "DUE DATE OF LAST PAID INSTALLMENT YEAR", "DUE DATE OF LAST PAID INSTALLMENT MONTH"))

# Removing spaces from col names
colnames(performance_test) <- c("LOAN_SEQUENCE_NUMBER","CURRENTACTUALUPB",
                                "LOANAGE","REMAININGMONTHSTOLEGALMATURITY",
                                "ZEROBALANCECODE",
                                "CURRENTINTERESTRATE",
                                "MONTHLYREPORTINGYEAR",
                                "MONTHLYREPORTINGMONTH","DELINQUENT","REPURCHASEFLAGYES","MODIFICATIONFLAGYES",
                                "ZEROBALANCEEFFECTIVEYEAR","ZEROBALANCEEFFECTIVEMONTH",
                                "DUEDATEOFLASTPAIDINSTALLMENTYEAR","DUEDATEOFLASTPAIDINSTALLMENTMONTH")


origination_test <-  fread("cleaned/cleaned_sample_orig_2006.csv",
                                                select=c("LOAN SEQUENCE NUMBER", 'CREDIT SCORE',
                                                         'NUMBER OF UNITS',
                                                         'ORIGINAL INTEREST RATE'
                                                         ))

# Removing spaces from col names
colnames(origination_test) <- c("LOAN_SEQUENCE_NUMBER", 'CREDIT_SCORE',
                                'NUMBER_OF_UNITS',
                                'ORIGINAL_INTEREST_RATE'
                                )



#joining orig and perf data

train = merge(x = performance_train, y = origination_train, by = "LOAN_SEQUENCE_NUMBER")
test = merge(x = performance_test, y = origination_test, by = "LOAN_SEQUENCE_NUMBER")
train$LOAN_SEQUENCE_NUMBER = NULL
test$LOAN_SEQUENCE_NUMBER = NULL

View(summary(train))
View(summary(test))

rm(origination_train)
rm(origination_test)
rm(performance_train)
rm(performance_test)



gc()
##75% of the sample size
#class_smp_size <- floor(0.75 * nrow(train_data))

##Set the seed to make your partition reproductible
#set.seed(1)
#train_logistic <- sample(seq_len(nrow(train_data)), size = class_smp_size)

#Split the data into training and testing
# train <- train_data[train_logistic, ]
# test <- train_data[-train_logistic,]


#### 1. Logistic Regression##################
######## START OF LOGISTIC REGRESSION #######
#A. Logistic Regression steps

#fitting the logistic regression model, based on the parameters
modelLogit <- glm(DELINQUENT ~ ., family=binomial(link='logit'), data=train)

#summary of the logistic regression
summary(modelLogit)

#analyzing the table of deviance
#anova(modelLogit, test="Chisq")

gc()
#r2 in logit, we see McFadden which is similar to R2. Closer to zero implies model is good
# install.packages("pscl")
library(pscl)
pR2(modelLogit)

gc()
# Plot the performance of the model applied to the evaluation set as an ROC curve.
# install.packages("ROCR")
library(ROCR)
#detach("package:neuralnet", unload=TRUE)
#prediction of the test data by the logistic model

#DELINQUENT
predict.Logit.Delinquent <- predict(modelLogit, newdata=test, type="response")

pr <- prediction(predict.Logit.Delinquent, test$DELINQUENT)
prf <- performance(pr, measure = "tpr", x.measure = "fpr")

#plotting ROC Curve
# plot(prf, main="ROC curve", colorize=T)


gc()
#Validation of Predicted Values, Confusion Matrix
# install.packages("e1071" )
# install.packages("caret")
library(e1071)
library(caret)
#Create predicted target value as 1 or 0 based on threshold of 0.3
pred.resp.level  <- ifelse(predict.Logit.Delinquent >0.5,1,0)
#confusion matrix for logistic regression
#sensitivity = 0.47
#specificity = 0.87
#accuracy = 0.79
#print(pred.resp.level)
confusionMatrix(data=factor(pred.resp.level),reference=factor(test$DELINQUENT),positive='1')

#computing the overall error - 0.21
delinquent.logistic.error <- 1- sum(pred.resp.level==test$DELINQUENT)/length(test$DELINQUENT)
delinquent.logistic.error

#plotting the regression
#plot(modelLogit, uniform=TRUE, main="Logistic Regression for delinquent")

######## END OF LOGISTIC REGRESSION #######
###########################################
