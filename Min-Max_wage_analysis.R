# Set Working Directory
# setwd("C:/.../SDCTA/San-Diego-County-Quid-Pro-Quo-Wage-Analysis")

# Load respective data sets
police = read.csv("police_salaries_cleaned.csv")
k12 = read.csv("k12_sd_salaries_cleaned.csv")
fire = read.csv("fire_salaries_cleaned.csv")
eng = read.csv("eng_salaries_cleaned.csv")

# Calculate min and max total pay for each job.title in a given data set
min.max.sum.job.title = function(dat){
  # Get list of every job title from data set 
  jobs = unique(dat$Job.title)
  
  # Loop through every job title and calculate min and max 
  jobs.min.max.sum = rbind()# Create empty vector
  for (job in jobs) {
    job.dat = dat[dat$Job.title == job,] # Filter data set to job title
    job.dat.2023 = job.dat[job.dat$Year == max(job.dat$Year),] # Filter data set to latest year
    job.min = min(job.dat.2023[job.dat.2023$Regular.pay > 0,]$Regular.pay) # Calc min
    job.max = max(job.dat.2023[job.dat.2023$Regular.pay > 0,]$Regular.pay) # Calc max
    job.num = length(job.dat.2023$Regular.pay) # Calc number of employees
    job.sum = sum(job.dat.2023$Regular.pay) # Calc REAL total salaries
    
    job.min.max.sum = cbind(job, job.min, job.max, job.num, job.sum)
    jobs.min.max.sum = rbind(jobs.min.max.sum, job.min.max.sum)
  }
  return(jobs.min.max.sum)
}

# Apply function
police.min.max = min.max.sum.job.title(police)
k12.min.max = min.max.sum.job.title(k12)
fire.min.max = min.max.sum.job.title(fire)
eng.min.max = min.max.sum.job.title(eng)

# Combine into one data frame
sd_employees.min.max = rbind(police.min.max, k12.min.max, fire.min.max, eng.min.max)
sd_employees = data.frame(sd_employees.min.max)

sd_employees$job.min <- as.numeric(sd_employees$job.min)
sd_employees$job.max <- as.numeric(sd_employees$job.max)
sd_employees$job.num <- as.numeric(sd_employees$job.num)

sd_employees$Regular.pay.min = sd_employees$job.min * sd_employees$job.num
sd_employees$Regular.pay.max = sd_employees$job.max * sd_employees$job.num

sd_employees = sd_employees[sd_employees$job.min != Inf,]

sd_employees$min.sum = sd_employees$job.num * sd_employees$job.min
sd_employees$max.sum = sd_employees$job.num * sd_employees$job.max

min.diff = sum(as.numeric(sd_employees$job.sum)) - sum(sd_employees$min.sum)
max.diff = sum(as.numeric(sd_employees$job.sum)) - sum(sd_employees$max.sum)

print(paste("Money Saved",min.diff))
print(paste("Money Lost",max.diff))

