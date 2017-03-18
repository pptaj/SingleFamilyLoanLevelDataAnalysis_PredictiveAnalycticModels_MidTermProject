#####MIDTERM PROJECT TEAM 7 #####

#### Please find the final submission in 1_Final_Code####
###Part1: ###
* Open the terminal in the directory "1_Final_Code"
* To run the program enter following command without quotes: 
	"python part1.py Summarize_data --local-scheduler"
	Pre-requisites to run the program: 
	- python3.x
	- pip
	- python libraries: luigi, beautifulsoup, mechanicalsoup, glob, 		pandas, numpy
	The program will ask you for the username and password for freddiemac.embs.com website to download the data.
3. Enter the username and password and it will run the tasks to download the data, clean the data and summarize it

* The downloaded files can be found in the "1_Final_Code/downloads" directory, the cleaned files can be found in the "1_Final_Code/cleaned" directory and the summaries can be found in the "1_Final_Code/summary" directory

* The python notebook for the summary can be found in the "1_Final_Code" directory with the name "New_Summary_Performance". The tableu files can be found in the directory ""1_Final_Code/TableauFiles"



###Part2: 
* Open the terminal in the directory "1_Final_Code"
* To run the program enter following command without quotes: 
	"python part2.py Build_prediction_model --local-scheduler"
	Pre-requisites to run the program: 
	- python3.x
	- pip
	- python libraries: luigi, beautifulsoup, mechanicalsoup, glob, 		pandas, numpy
	The program will ask you for the username and password for freddiemac.embs.com website to download the data.


* Enter the username and password. Enter the year and quarter you want to run the prediction model for. it will run the tasks to download the data, clean the data and summarize it.

* The downloaded files can be found in the "1_Final_Code/downloads" directory and the cleaned files can be found in the "1_Final_Code/cleaned" directory.

* Run the "Classification_Logistic_Regression.R" in RStudio to run the logistic regression for Delinquent, "neuralnet.R" in RStudio to run the neural network for Delinquent.