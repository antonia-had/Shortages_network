library(tidyverse)
library(igraph)
library(ggraph)
library(visNetwork)
library(networkD3)
library(dplyr)
library(ggplot2)
library(svglite)
library(lubridate)

# set directory
setwd('/Users/ananyagangadhar/Desktop/M.Eng\ Project/Shortages_network/R_networks_scripts')

# Line plot showing mean annual streamflow
strmflw <- read.csv('../data/UCRB_mean_annual_flows.csv')
ggplot(data=strmflw, aes(x=year_nu, y=mean_va, group=1)) +
  geom_line(color="skyblue") +
  geom_point(color="darkblue") +
  theme_classic() +
  ggtitle("Mean annual basin streamflow") +
  labs(y="Streamflow (cfs)", x = "Year") +
  scale_x_continuous(breaks = seq(2000, 2019, by = 1)) +
  #geom_vline(xintercept = 2011, color='darkblue') +
  geom_vline(xintercept = 2007, color='darkblue') +
  #geom_vline(xintercept = 2002, color='darkblue') +
  theme(axis.text.x = element_text(size=10, angle=90))

# histogram showing streamflow gage lifespans
gages <- read.csv('../data/div5_gauges.csv')

numYears <- na.omit(as.numeric(gages$numYears))
numYears <- data.frame(numYears)
colnames(numYears) <- c("yrs")
head(numYears)

ggplot(numYears, aes(x=yrs)) +  
  geom_histogram(binwidth = 5, fill='skyblue') + 
  theme_classic() +
  ggtitle("Lifespans of streamflow gages in UCRB ") +
  labs(x = "Number of years active")

# monthly streamflow 2000-2003
strmflw <- read.csv('../data/ucrb_monthly_flow_2000-2003.csv')
ggplot(data=strmflw, aes(x=month, y=mean_va, group=1)) +
  geom_line(color="skyblue") +
  geom_point(color="darkblue") +
  theme_classic() +
  ggtitle("Mean monthly basin streamflow") +
  labs(y="Streamflow (cfs)", x = "Month") +
  #scale_x_continuous(breaks = seq(2000, 2019, by = 1)) +
  #geom_vline(xintercept = 2011, color='darkblue') +
  #geom_vline(xintercept = 2007, color='darkblue') +
  #geom_vline(xintercept = 2002, color='darkblue') +
  theme(axis.text.x = element_text(size=10, angle=90))