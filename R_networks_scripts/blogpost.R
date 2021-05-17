library(tidyverse)
library(igraph)
library(ggraph)
library(dplyr)
library(ggplot2)
library(svglite)


# set directory
setwd('/Users/ananyagangadhar/Desktop/M.Eng\ Project/Shortages_network/R_networks_scripts')

# read network .csv file
data <- read.csv('network_csv_files/priorityWdid/v2_network_2011.csv')

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

# create edges
edges <- data[c('priorityWdid', 'analysisWdid', 'sumWtdCount')] %>% rename(from = priorityWdid) %>% rename(to = analysisWdid)

# create network using igraph package
network <- graph_from_data_frame(d = edges, vertices = nodes, directed = TRUE)

# only include top 200 users by seniority
users <- read.csv('../data/CDSS_WaterRights.csv')
users <- head(users[order(users$Priority.Admin.No),], 200)

top_users <- users$WDID
for (i in 1:length(top_users)){
  top_users[i] <- toString(top_users[i])
}

# create subnetwork with only top 200 users by seniority
sub_nodes <- intersect(nodes$wdid, top_users)
subnet <- induced.subgraph(network, sub_nodes)
################################################

# basic network graph
ggraph(subnet, layout = 'stress') +
  ggtitle('2002') + 
  geom_edge_link() +
  geom_node_point() +
  theme_graph()
################################################

# calculate out degree of each node
deg <- degree(subnet, mode="out")
for (i in 1:length(deg)){
  deg[i] <- deg[i] + 0.1
  
# create a color gradient  
colfunc <- colorRampPalette(c("#00008B", "#63B8FF"))
cols <- colfunc(vcount(subnet))


# plot graph in circular layout
ggraph(subnet, layout = "circle") +
  ggtitle('2002: "circle" Layout') +
  geom_edge_link(aes(width = sumWtdCount), alpha = 0.8, color = 'skyblue', 
                 arrow = arrow(length = unit(2, 'mm')), end_cap = circle(2, 'mm')) +
  labs(edge_width = "Number of days") + 
  geom_node_point(aes(size = deg, colour=streamMile)) +
  labs(colour = "Stream mile") +
  labs(size = "Out-degree") +
  scale_color_gradient(low = "skyblue", high = "darkblue") +
  scale_edge_width(range = c(0.2, 2)) +
  geom_node_text(aes(label = structure), repel = TRUE, size=2) +
  theme_graph()

set.seed(1998)
ggraph(subnet, layout = "graphopt") +
  ggtitle('2011: "graphopt" Layout') +
  geom_edge_link(aes(width = sumWtdCount), alpha = 0.8, color = 'skyblue', 
                 arrow = arrow(length = unit(2, 'mm')), end_cap = circle(2, 'mm')) +
  labs(edge_width = "Number of days") + 
  geom_node_point(aes(size = deg, colour=streamMile)) +
  labs(colour = "Stream mile") +
  labs(size = "Out-degree") +
  scale_color_gradient(low = "skyblue", high = "darkblue") +
  scale_edge_width(range = c(0.2, 2)) +
  geom_node_text(aes(label = structure, alpha=deg), repel = TRUE, size=2, show.legend = F) +
  theme_graph()



