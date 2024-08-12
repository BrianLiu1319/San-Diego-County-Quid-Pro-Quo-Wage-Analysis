#Load California Employee Compensation Data from 2009-2023
city <- read.csv("C:\\Users\\ashvi\\OneDrive\\Desktop\\San Diego Taxpayer\\Employee Compensation Data\\CAEmployee_data\\CAEmployee_data.csv")

#Load Packages
library(dplyr)
library(stringr)

#Filter for keywords in DepartmentOrSubdivision and Position for teacher and school district
filtered_data <- city %>%
  filter(str_detect(DepartmentOrSubdivision, regex("\\bteacher\\b", ignore_case = TRUE)) | 
           str_detect(DepartmentOrSubdivision, regex("\\bschool district\\b", ignore_case = TRUE)) |
           str_detect(Position, regex("\\bteacher\\b", ignore_case = TRUE)) | 
           str_detect(Position, regex("\\bschool district\\b", ignore_case = TRUE)))

#cities of interest
cities <- c("San Diego", "Chula Vista", "Carlsbad", "Coronado", "Del Mar", "National City")

#Filter for cities
final_filtered_data <- dplyr::filter(filtered_data,
                                     str_detect(EmployerName, regex(paste(cities, collapse = "|"), ignore_case = TRUE))
)
#The teacher compensation is not found in the dataset

#Lets check for county
county <- read.csv("C:/Users/ashvi/OneDrive/Desktop/San Diego Taxpayer/Employee Compensation Data/San Diego County Data/SDCountyEmployee_Data.csv")

#Filter for keywords in DepartmentOrSubdivision and Position for teacher and school district
filtered_data_county <- county %>%
  filter(str_detect(DepartmentOrSubdivision, regex("\\bteacher\\b", ignore_case = TRUE)) | 
           str_detect(DepartmentOrSubdivision, regex("\\bschool district\\b", ignore_case = TRUE)) |
           str_detect(Position, regex("\\bteacher\\b", ignore_case = TRUE)) | 
           str_detect(Position, regex("\\bschool district\\b", ignore_case = TRUE)))


#Not in county data, K-12 only avalaible 2013-2023

#Set working directory
setwd("C:/Users/ashvi/OneDrive/Desktop/San Diego Taxpayer/Employee Compensation Data/K-12 Education Compensation Data")

#List .csv files
files <- list.files(pattern = "^\\d{4}_K12Education\\.csv$")

#Load library
library(purrr)

#List CSV files
files <- list.files(pattern = "^201[3-9]|202[0-2]_K12Education\\.csv$")

#Load CSV files into a list of dataframes
data <- map(files, read.csv)

#Combine all dataframes into one dataset
combined_data <- bind_rows(data)
K12 <- map(files, read.csv)

#Save
write.csv(combined_data, file = "K12_Compensation_Data_2013-2022.csv", row.names = FALSE)

k12 <-read.csv("C:/Users/ashvi/OneDrive/Desktop/San Diego Taxpayer/Employee Compensation Data/K-12 Education Compensation Data/K12_Compensation_Data_2013-2022.csv")

#Store unique values of employers
unique_employers <- k12 %>%
  select(EmployerName) %>%
  distinct()

#Using https://www.sdcoe.net/schools/finder, isolate for schools in san diego county
school_districts <- data.frame(
  employername = c("Alpine Union School District",
                   "Borrego Springs Unified",
                   "Bonsall Unified",
                   "Cajon Valley Union",
                   "Cardiff Elementary",
                   "Carlsbad Unified",
                   "Chula Vista Elementary",
                   "Coronado Unified",
                   "Del Mar Union Elementary",
                   "Encinitas Union Elementary",
                   "Escondido Union",
                   "Escondido Union High",
                   "Escondido Charter High",
                   "Fallbrook Union Elementary",
                   "Fallbrook Union High",
                   "Grossmont Union High",
                   "Jamul-Dulzura Union Elementary",
                   "Julian Union Elementary",
                   "Julian Charter",
                   "Julian Union High",
                   "Lakeside Union Elementary (San Diego)",
                   "La Mesa-Spring Valley",
                   "Lemon Grove",
                   "Mountain Empire Unified",
                   "Poway Unified",
                   "National Elementary",
                   "Rancho Santa Fe Elementary",
                   "Ramona City Unified",
                   "San Diego Virtual",
                   "San Diego Unified Port District",
                   "San Dieguito Union High",
                   "San Marcos Unified",
                   "San Pasqual Union Elementary",
                   "San Pasqual Valley Unified",
                   "San Diego Unified",
                   "Santee",
                   "San Ysidro Elementary",
                   "Solana Beach Elementary",
                   "South Bay Union",
                   "South Bay Union Elementary",
                   "Sweetwater Union High",
                   "Vallecito Union",
                   "Valley Center-Pauma Unified",
                   "Vista Unified")
)
#Ensure the column names match exactly
colnames(school_districts) <- c("employername")
colnames(k12) <- tolower(colnames(k12))

#Check if the column 'EmployerName' exists in both data frames
if (!"employername" %in% colnames(k12)) {
  stop("Column 'employername' not found in k12")
}

#Filter the K12 dataset for exact matches
SDk12 <- k12 %>%
  semi_join(school_districts, by = "employername")

#Save Data
write.csv(REAL_SD_Employee, file = "C:/Users/ashvi/OneDrive/Desktop/San Diego Taxpayer/Employee Compensation Data/K-12 Education Compensation Data/REAL_EmployeeCompensation.csv", row.names = FALSE)

