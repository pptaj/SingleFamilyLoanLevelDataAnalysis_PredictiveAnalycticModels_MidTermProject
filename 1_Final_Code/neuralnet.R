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

traindatannet = merge(x = performance_train, y = origination_train, by = "LOAN_SEQUENCE_NUMBER")
testdatannet = merge(x = performance_test, y = origination_test, by = "LOAN_SEQUENCE_NUMBER")
traindatannet$LOAN_SEQUENCE_NUMBER = NULL
testdatannet$LOAN_SEQUENCE_NUMBER = NULL

rm(origination_train)
rm(origination_test)
rm(performance_train)
rm(performance_test)



traindatannet <- traindatannet[1:40000,]
testdatannet <- testdatannet[1:40000,]
#### 3. Neural Network  ##########
######## START OF NEURAL NETWORK #######
#C. Neural Network for classification
#assigning the card dataset to datannet, since we need to normalize in
#neural network we are assiging to different dataset
# datannet <- train
# 
# #normalizing the data in the datannet, so that we can implement nnet
# normalize <- function(x) {
#   return ((x - min(x)) / (max(x) - min(x))) }
# 
# #normalizing the datannet
# datannet_n <- as.data.frame(lapply(datannet, normalize))
# #View(summary(datannet_n))
# 
# #import the function from Github
# #install.packages("clusterGeneration")
# #install.packages("neuralnet")
# #install.packages("devtools")
# library(devtools)
# #source_url('https://gist.githubusercontent.com/Peque/41a9e20d6687f2f3108d/raw/85e14f3a292e126f1454864427e3a189c2fe33f3/nnet_plot_update.r')
# #source_url('https://gist.githubusercontent.com/fawda123/7471137/raw/466c1474d0a505ff044412703516c34f1a4684a5/nnet_plot_update.r')
# library(clusterGeneration)
# library(nnet)
# require(nnet)
# 
# #Sampling of the dataset
# #75% of the sample size
# class_new1 <- floor(0.75 * nrow(datannet_n))
# 
# #set the seed to make your partition reproductible
# set.seed(13)
# train_datannet <- sample(seq_len(nrow(datannet_n)), size = class_new1)

# #split the data into training and testing
# traindatannet <- datannet_n[train_datannet, ]
# testdatannet  <- datannet_n[-train_datannet,]
# #testdatannet <- datannet_n[-train_datannet,c('default_payment','status') ]

View(traindatannet$DELINQUENT)

gc()
library(clusterGeneration)
library(nnet)
require(nnet)
library(devtools)
#applying the neural net algorithm
#install.packages("NeuralNetTools")
library(NeuralNetTools)
#training the neural network with size = 10 and 1 hidden layers
fitnn <- nnet(DELINQUENT ~ ., traindatannet, size=20, 
              maxit = 90, entropy = TRUE, softmax = FALSE,censored = FALSE, skip = FALSE, 
              rang = 0.7, Hess = FALSE, trace = TRUE, MaxNWts = 1000, abstol = 1.0e-4, 
              decay = 15e-4, reltol = 1.0e-8, hidden = 2,threshold = 0.01,act.fct="tanh")
fitnn
#summary of the neural net
summary(fitnn)

#plotting the neural net, to visualize the nodes
library(scales)
library(reshape)
#plot.nnet(fitnn, pos.col='darkgreen',neg.col='darkblue', alpha.val=0.7, rel.rsc=10, circle.cex=5, cex=1.4,circle.col='brown')

#predicting the delinquent using nnet model
predict.neural.Delinquent <- predict(fitnn, newdata=testdatannet)
View(predict.neural.Delinquent)
#converting the prediction to vector
predict.neural.Delinquent <- as.vector(predict.neural.Delinquent)

#changing matrix to numeric
#Create predicted target value as 1 or 0 based on threshold of 0.2
pred.resp.level.nnet1  <- ifelse(predict.neural.Delinquent > 0.005, 1, 0)
#View(predict.neural.Delinquent)

#Validation of Predicted Values, Confusion Matrix
#Create predicted target value as 1 or 0
library(e1071)
library(caret)
#confusion Matrix for decision tree
#sensitivity = 0.65
#specificity = 0.74
#accuracy = 0.73
pred.resp.nnet.factor <- factor(pred.resp.level.nnet1)
confusionMatrix(data=pred.resp.nnet.factor,reference=factor(testdatannet$DELINQUENT), positive='1')

#computing the overall error - 0.32
delinquent.neural.error <- 1- sum(pred.resp.nnet.factor==testdatannet$DELINQUENT)/length(testdatannet$DELINQUENT)
delinquent.neural.error

#plot the ROC curve
#install.packages("ROCR")
library(ROCR)

pred.resp.nnet.num <- as.numeric(pred.resp.level.nnet1)
testdatannet <- as.data.frame(testdatannet)
roc_pred.nnnet <- prediction(pred.resp.nnet.num, testdatannet["DELINQUENT"])
#roc_pred.nnnet
View(summary(testdatannet))
perf.nnet.model <- performance(roc_pred.nnnet, measure="tpr", x.measure="fpr")
plot(perf.nnet.model, colorize=TRUE)


#plot the lift curve
testdatannet$pred <- predict.neural.Delinquent
testdatannet$pred <- sort(testdatannet$pred, decreasing = T)
lift <- lift( factor(DELINQUENT) ~ pred, data = testdatannet)
lift
xyplot(lift, plot = "gain")

#Sensitivity/specificity curve and precision/recall curve:
plot(performance(roc_pred.nnnet, measure="sens", x.measure="spec"), colorize=TRUE)
plot(performance(roc_pred.nnnet, measure="prec", x.measure="rec"), colorize=TRUE)

##################### END OF NEURAL NETWORK ####################
################################################################