# Task 1: Data Import & Inspection
weather <- read.csv("C:/Users/DELL/Downloads/Ram/Weather data report.CSV")

head(weather)
colnames(weather)
sum(is.na(weather))
# Task 2: Data Cleaning & Manipulation
cities <- c("Hyd", " Vizag", "chennai")
weather <- subset(weather, CITIES %in% cities)

# Convert Temperature to Fahrenheit
weather$TEMP_F <- weather$TEMPERATURE * 9/5 + 32

# Convert Date to Date format
weather$DATE<- as.Date(weather$DATE)

# Load dplyr for manipulation
library(dplyr)
weekly_avg <- weather %>%
  mutate(Week = format(DATE, "%Y-%U")) %>%
  group_by(CITIES, Week) %>%
  summarise(
    Avg_Temp = mean(TEMPERATURE),
    Avg_HUMIDITY = mean(HUMIDITY),
    Avg_RAINFALL = mean(RAIN..FALL)
  )
head(weekly_avg)
# Task 3: Data Analysis

# Hottest and coldest city
avg_CITIES_temp <- weather %>%
  group_by(CITIES) %>%
  summarise(Mean_Temp = mean(TEMPERATURE))

hottest <- avg_CITIES_temp[which.max(avg_CITIES_temp$Mean_Temp),]
coldest <- avg_CITIES_temp[which.min(avg_CITIES_temp$Mean_Temp),]

hottest
coldest

# Day with highest rainfall in each city
max_rain <- weather %>%
  group_by(CITIES) %>%
  filter(RAIN..FALL == max(RAIN..FALL))

max_rain

# Compare average humidity
avg_HUMIDITY <- weather %>%
  group_by(CITIES) %>%
  summarise(Mean_HUMIDITY = mean(HUMIDITY))

avg_HUMIDITY
# ----------------------
# Task 4: Visualization
# ----------------------
#install.packages("ggplot2")
library(ggplot2)
# 1. Line graph of temperature trends
ggplot(weather, aes(x=CITIES, y=TEMPERATURE, color=DATE)) +
  geom_line(size=10) +
  labs(title="Daily Temperature Trends", y="TEMPERATURE (°C)")
# 2. Bar plot of weekly average rainfall
ggplot(weekly_avg, aes(x=AVG_TEMP, y=AVG_RAINFALL, fill=CITIES)) +
  geom_bar(stat="identity", position="dodge") +
  labs(title="Weekly Average Rainfall", y="RAIN..FALL (mm)")
# 3. Boxplot for humidity distribution
ggplot(weather, aes(x=CITIES, y=HUMIDITY, fill=CITIES)) +
  geom_boxplot() +
  labs(title="Humidity Distribution Across Cities", y="HUMMIDITY (%)")