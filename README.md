A culmination of code written by the San Diego Taxpayers Educational Foundation to conduct an analysis on Police, Firefighter, Teachers, and Engineers and their respective labor union financial backings.
Below is a summary of each file in repo 9/3/2024

**ContributionDataExtraction.py**
- Purpose: Data merging PAC datasets
- Output: ContributionsBinder.csv
- Datasets: 

**K-12.py**
- Purpose: Data merging and data munging K-12 Wage data
- Output: REAL_EmployeeCompensation.csv
- Datasets: CAEmployee_data.csv (Not In Drive), SDCountyEmployee_Data.csv (In Drive), 2013_K12Education.csv, ... , 2022_K12Education.csv


**PolicePACWageXNumEmployees.ipynb**
- Purpose: Data Vizualization of Mean Total Wage Time-Series for Police Officer by City, Minor data munging
- Output: Mean Total Wages vs Year Graph
- Datasets: PoliceDepartmentWagesConsolidated.csv

**PublicEmployeeAnalysis.ipynb**
- Purpose: Clean data and analyze movements of employees
- Output: sdcounty_salaries_names_movements.csv, sdcounty_movement.pdf, sdcounty_salary_num_empls.pdf, sdcounty_avg_salary
- Datasets: cities_sd_salaries.csv, SeriesReport-20240712171831_4c56aa.csv

**ReadWagesCalculation.R**
- Purpose: Data munging
- Output: REAL_SD_Employee.csv
- Datasets: SD_City_Sheriff_Teacher.csv, SeriesReport-20240712171831_4c56aa.xlsx

**SDCountyEmployee_datamunge.ipynb**
- Purpose: Data munging
- Output: SDCountyEmployee_data_MORE_cleaned_07112024.csv
- Datasets: test.csv*

**WageDataScraper.py**
- Purpose: Data gathering through web scraping Transparent California
- Output: police_salaries.csv
- Datasets: Transparent California salaries data from cities in San Diego County from 2011 to 2023

**WageRoC.Rmd**
- Purpose: Plot the change in number of police officers over time(Years) and change in median wage of police officers over time(Years)
- Output: NumEmpls vs Year, MedTotWage vs Year Comparison Graph(NO SD).png, "Log Num of Empl. vs Year.png, Median Total Wage vs Year.png
- Datasets: WageRoC.csv

**WageVsVacancies.ipynb**
- Purpose: Data munging, data visualization of: Employee Movements Between Cities Graph, Adjusted Median Wage Time-Series for Reserve Police Officer by City, Total Reserve Police Officer Workforce Size Over Time, regression analysis
- Output: Employee Movements Between Cities Graph, Adjusted Median Wages vs Year Graph, Total Number of Employees vs Year Graph, OLS Regression Results
- Datasets: police_salaries.csv, SDCountyEmployee_data.csv, police_salaries_corrected_positions.txt

**contributionWageVisualization.py** 
- Purpose: Data Visualization through the creation of a local dashboard
- Output: Local dashboard
- Datasets: SanDiegoPoliceDepartmentWageData.csv, SanDiegoPoliceContributionsBinder.csv


