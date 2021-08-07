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
setwd('/Users/ananyagangadhar/Desktop/M.Eng\ Project/Shortages_network/UCRB_networks/network_scripts')

# # Line plot showing mean annual streamflow
# strmflw <- read.table('ucrb_annual_flows', header = TRUE)
# head(strmflw)
# ggplot(data=strmflw, aes(x=year_nu, y=mean_va, group=1)) +
#   geom_line(color="skyblue") +
#   geom_point(color="darkblue") +
#   theme_classic() +
#   ggtitle("Mean annual basin streamflow 1952-2020") +
#   labs(y="Streamflow (cfs)", x = "Year") +
#   scale_x_continuous(breaks = seq(1900, 2020, by = 5), limits = c(1900,2020)) +
#   geom_vline(xintercept = 2011, color='darkblue', linetype='dotted') +
#   geom_vline(xintercept = 2007, color='darkblue', linetype='dotted') +
#   geom_vline(xintercept = 2002, color='darkblue', linetype='dotted') +
#   geom_vline(xintercept = 1987, color='red', linetype='solid') +
#   theme(axis.text.x = element_text(size=8, angle=50, vjust=1,hjust=1))

###########################################################################################


# CREATE ANNUAL NETWORK

# set directory

# only include top n users by seniority
n <- 200
users <- read.csv('../data/Attributes.csv', colClasses=c("adminNumber"="character"))
users <- head(users[order(users$adminNumber),], n)

top_users <- users$adminNumber


years <- c(1987:1987)

# comps <- c()
# sr_users <- c()

# iterate through each year
for (yr in years){
  
  yr
  
  # read subset of network .csv file
  data <- read.csv(paste('network_csv/', yr, '.csv', sep = ""))
  
  ##########################################################################################
  
  # create nodes
  nodes <- data.frame()
  
  from <- unique(data[c('priorityAdminNo','priorityNetAbs', 'priorityStreamMile')]) %>% 
    rename(key = priorityAdminNo) %>% rename(netAbs = priorityNetAbs) %>% 
    rename(streamMile = priorityStreamMile) 
  
  to <- unique(data[c('analysisAdminNo', 'analysisNetAbs','analysisStreamMile')]) %>% 
    rename(key = analysisAdminNo) %>% rename(netAbs = analysisNetAbs) %>%
    rename(streamMile = analysisStreamMile) 
  
  nodes <- unique(rbind(from, to))
  nodes
  
  # create edges
  edges <- data[c('priorityAdminNo', 'analysisAdminNo', 'wt')]
  
  # create network using igraph package
  network <- graph_from_data_frame(d = edges, vertices = nodes, directed = TRUE)
  
  # create subnetwork with only top 200 users by seniority
  sub_nodes <- intersect(nodes$key, top_users)
 
  subnet <- induced.subgraph(network, sub_nodes)
  ##########################################################################################

# plot network in circular layout

  # calculate out degree of each node
  deg <- degree(subnet, mode="out")
  for (i in 1:length(deg)){
    deg[i] <- deg[i] + 0.1
  }

  colfunc <- colorRampPalette(c("#00008B", "#63B8FF"))
  cols <- colfunc(vcount(subnet))

  # save plot as svg file
  p <- ggraph(subnet, layout = "circle") +
    geom_edge_link(alpha = 0.8) +
    ggtitle(paste(yr, sep="")) +
    theme_graph()
  ggsave(p, filename = paste('circular_', yr, '.svg', sep=""), width = 10, height = 8)

  ##########################################################################################
  # 
  # # Calculate number of components in each full network
  # comps <- cbind(comps, count_components(network))
  # 
  # # calculate number of senior users in each network
  # sr_users <- rbind(sr_users, length(V(subnet)))
  
  ##########################################################################################
  
  
}

##########################################################################################
##########################################################################################
##########################################################################################
# # draw bar plot of number of components
# df1 <- data.frame(year=years, users=comps)
# p <- ggplot(data=df1, aes(x=year, y=comps)) +
#   geom_bar(stat="identity", fill = 'skyblue') +
#   geom_text(aes(label=comps), vjust=-0.3, size=3.5) +
#   theme_classic() +
#   ggtitle("Number of network components each year") +
#   labs(y="Number of components", x = "Year") +
#   scale_x_continuous(breaks = seq(1987, 2020, by = 5)) +
#   theme(axis.text.x = element_text(size=8, angle=50, vjust=1,hjust=1))
# p
# 
# 
# # draw bar plot of number of top n senior-most users each year
# df2 <- data.frame(year=years, users=sr_users)
# q <- ggplot(data=df2, aes(x=year, y=users)) +
#   geom_bar(stat="identity", fill = 'cornflowerblue') +
#   geom_text(aes(label=users), vjust=-0.3, size=3.5) +
#   theme_classic() +
#   ggtitle(paste('Number of top', n, 'seniormost users per year', sep=" ")) +
#   labs(y="Number of users", x = "Year") +
#   scale_x_continuous(breaks = seq(1987,2020, by = 5)) +
#   theme(axis.text.x = element_text(size=8, angle=50, vjust=1,hjust=1))
# q
