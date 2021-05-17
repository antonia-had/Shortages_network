library(tidyverse)
library(igraph)
library(ggraph)
library(visNetwork)
library(networkD3)

setwd('/Users/ananyagangadhar/Desktop/M.Eng\ Project/Shortages_network/R_networks_scripts')

# Using igraph library to make networks

# read subset of network .csv file
my_data <- read.csv('network_csv_files/priorityWdid/v2_network_2002.csv')

# create node list
sources <- my_data %>% distinct(priorityStructure) %>% rename(label = priorityStructure)
destinations <- my_data %>% distinct(analysisStructure) %>% rename(label = analysisStructure)

# add unique IDs
nodes <- full_join(sources, destinations, by = "label")
nodes <- nodes %>% rowid_to_column("id")
nodes

# create edge list
interactions <- my_data %>% group_by(priorityStructure, analysisStructure) %>% summarise(weight = sumWtdCount) %>% ungroup()
interactions <- distinct(interactions)
interactions

edges <- interactions %>% left_join(nodes, by = c("priorityStructure" = "label")) %>% rename(from = id)
edges <- edges %>% left_join(nodes, by = c("analysisStructure" = "label")) %>% rename(to = id)
edges

# remove superfluous rows
edges <- select(edges, from, to, weight)
edges

# create network using igraph package
network_2002 <- graph_from_data_frame(d = edges, vertices = nodes, directed = TRUE)

# plot(network_2002, layout = layout_with_graphopt, edge.arrow.size = 0.2)
# 
# # plot network using ggraph
# ggraph(network_2002, layout = "graphopt") + 
#   geom_node_point() +
#   geom_edge_link(aes(width = weight), alpha = 0.8) + 
#   scale_edge_width(range = c(0.2, 2)) +
#   geom_node_text(aes(label = label), repel = TRUE) +
#   labs(edge_width = "Days") +
#   theme_graph()
# 
# # plot linear map
# ggraph(network_2002, layout = "linear") + 
#   geom_edge_arc(aes(width = weight), alpha = 0.8) + 
#   scale_edge_width(range = c(0.2, 2)) +
#   geom_node_text(aes(label = label)) +
#   labs(edge_width = "Days") +
#   theme_graph()
# 
# # interactive plot using visNetwork
# visNetwork(nodes, edges)
# 
# # add attributes
# edges <- mutate(edges, width = weight/50 + 1)
# visNetwork(nodes, edges) %>% 
#   visIgraphLayout(layout = "layout_with_fr") %>% 
#   visEdges(arrows = "middle")

# Make arc diagram
ggraph(network_2002, layout="linear") + 
  geom_edge_arc(edge_colour="black", edge_alpha=0.1, edge_width=0.1, fold=TRUE) +
  #geom_node_point(aes(size=n, color=as.factor(grp), fill=grp), alpha=0.5) +
  scale_size_continuous(range=c(0.5,8)) +
  #scale_color_manual(values=mycolor) +
  geom_node_text(aes(label=name), angle=65, hjust=1, nudge_y = -1.1, size=2.3) +
  theme_void() +
  theme(
    legend.position="none",
    plot.margin=unit(c(0,0,0.4,0), "null"),
    panel.spacing=unit(c(0,0,3.4,0), "null")
  ) +
  expand_limits(x = c(-10, 10), y = c(-5.6, 1.2)) 


