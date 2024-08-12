#Working Directory
setwd("C:/Users/ashvi/OneDrive/Desktop/San Diego Taxpayer/Employee Compensation Data/San Diego County Data")

#Load packages
library(readxl)
library(dplyr)

#Load Data
SD_Employee <-read.csv("SD_City_Sheriff_Teacher.csv")

Inflation_Data <- read_xlsx("SeriesReport-20240712171831_4c56aa.xlsx")
#Reformate Inflation_Data as format is in excel and unworkable
#First 10 rows useless
Inflation_Data <- Inflation_Data %>%
  slice(-(1:10))
#Assign the first row as column names
colnames(Inflation_Data) <- as.character(Inflation_Data[1, ])

#Create a new data frame without the first row
Inflation_Data <- Inflation_Data[-1, ]

#Remove .0 in data frame(because formatting)
Inflation_Data <- Inflation_Data %>%
  mutate(Year = as.integer(Year))
#Turn Annual Numeric for future function
Inflation_Data$Annual <- as.numeric(Inflation_Data$Annual)

#Keep only Annual column
Inflation_Data <- Inflation_Data %>%
  select(contains("Annual"), ("Year"))

#Prepare for merge
colnames(Inflation_Data) <- tolower(colnames(Inflation_Data))

#Merge data set
REAL_SD_Employee <- merge(SD_Employee, Inflation_Data, by = "year", all.x = TRUE)

#Get the CPI value for the base year (e.g., 2023)
base_year_cpi <- as.numeric(Inflation_Data$annual[Inflation_Data$year == 2023])

#Calculate real values
REAL_SD_Employee <- REAL_SD_Employee %>%
  mutate(
    #Calculate the relative CPI for each year
    relative_CPI = annual / base_year_cpi,
    
    #Adjust the salaries to real values based on the relative CPI
    real_minpositionsalary = minpositionsalary / relative_CPI,
    real_maxpositionsalary = maxpositionsalary / relative_CPI,
    real_reportedbasewage = reportedbasewage / relative_CPI,
    real_totalwages = totalwages / relative_CPI
  )
#Save
write.csv(REAL_SD_Employee, file = "C:/Users/ashvi/OneDrive/Desktop/San Diego Taxpayer/Employee Compensation Data/SanDiegoCity+Sheriff/REAL_SD_Employee.csv", row.names = FALSE)