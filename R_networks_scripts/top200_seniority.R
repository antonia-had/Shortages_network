library(tidyverse)
library(igraph)
library(ggraph)
library(visNetwork)
library(networkD3)
library(dplyr)
library(ggplot2)
library(svglite)


# set directory
setwd('/Users/ananyagangadhar/Desktop/M.Eng\ Project/Shortages_network/R_networks_scripts')

# only include top 200 users by seniority
users <- read.csv('../data/CDSS_WaterRights.csv')
users <- head(users[order(users$Priority.Admin.No),], 200)
users <- head(users[order(users$Stream.Mile),], 200)

top_users <- users$WDID
for (i in 1:length(top_users)){
  top_users[i] <- toString(top_users[i])
}


years <- c(2000:2019)

comps <- c()

# iterate through each year
for (yr in years){
  
  yr
  
  # read subset of network .csv file
  data <- read.csv(paste('network_csv_files/priorityWdid/v2_network_', yr, '.csv', sep = ""))
  
  ##########################################################################################
  
  # create nodes
  from <- unique(data[c('priorityWdid','priorityStructure', 'priorityNetAbs', 
                        'priorityStreamMile')]) %>% rename(wdid = priorityWdid) %>%
    rename(structure = priorityStructure) %>% rename(netAbs = priorityNetAbs) %>%
    rename(streamMile = priorityStreamMile)
  to <- unique(data[c('analysisWdid','analysisStructure', 'analysisNetAbs',
                      'analysisStreamMile')]) %>% rename(wdid = analysisWdid) %>% 
    rename(structure = analysisStructure) %>% rename(netAbs = analysisNetAbs) %>%
    rename(streamMile = analysisStreamMile)
  nodes <- unique(rbind(from, to))
  nodes
  
  # create edges
  edges <- data[c('priorityWdid', 'analysisWdid', 'sumWtdCount')] %>% rename(from = priorityWdid) %>% rename(to = analysisWdid)
  
  # create network using igraph package
  network <- graph_from_data_frame(d = edges, vertices = nodes, directed = TRUE)
  
  # create subnetwork with only top 200 users by seniority
  sub_nodes <- intersect(nodes$wdid, top_users)
  sub_nodes
  subnet <- induced.subgraph(network, sub_nodes)
  ##########################################################################################
  
  # plot network in circular layout
  
  # calculate out degree of each node
  deg <- degree(subnet, mode="out")
  for (i in 1:length(deg)){
    deg[i] <- deg[i] + 0.1
  }
  
  # set edge width as days * netAbs
  # days <- vertex_attr(subnet, 'sumWtdCount')
  # netAbs <- vertex_attr(subnet, 'netAbs')
  # w <- c(1:length(days))
  # for (i in 1:length(days)){
  #   w[i] <- days[i] * netAbs[i]
  
  colfunc <- colorRampPalette(c("#00008B", "#63B8FF"))
  cols <- colfunc(vcount(subnet))
  
  # save plot as svg file
  p <- ggraph(subnet, layout = "circle") +
    ggtitle(paste(yr, sep="")) +
    geom_edge_link(aes(width = sumWtdCount), alpha = 0.8, color = 'skyblue', arrow = arrow(length = unit(2, 'mm')), 
                   end_cap = circle(2, 'mm')) +
    labs(edge_width = "Water allocation lost (cfs/year)") +
    scale_edge_colour_gradient(low = "skyblue", high = "darkblue") + 
    geom_node_point(aes(size = deg, colour=streamMile)) +
    labs(colour = "Stream mile") +
    labs(size = "Out-degree") +
    scale_color_gradient(low = "skyblue", high = "darkblue") +
    scale_edge_width(range = c(0.2, 2)) +
    geom_node_text(aes(label = structure), repel = TRUE, size=2) +
    theme_graph()
  
  ggsave(p, filename = paste('circular_', yr, '.svg', sep=""))
  
  ##########################################################################################
  
  # Calculate number of components in each network
  comps <- cbind(comps, count_components(network))
  
}

  






