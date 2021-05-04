library(tidyverse)
library(igraph)
library(ggraph)
library(visNetwork)
library(networkD3)

setwd('/Users/ananyagangadhar/Desktop/M.Eng\ Project/Shortages_network/R_networks_scripts')

# Using igraph library to make networks

g1 <- graph( edges=c(1,2, 2,3, 3, 1), n=3, directed=F ) 
plot(g1)

# read subset of network .csv file
my_data <- read.csv('network_csv_files/network_2002.csv', nrows=50)

# create node list
sources <- my_data %>% distinct(priorityWdid) %>% rename(label = priorityWdid)
destinations <- my_data %>% distinct(analysisWdid) %>% rename(label = analysisWdid)

# add unique IDs
nodes <- full_join(sources, destinations, by = "label")
nodes <- nodes %>% rowid_to_column("id")
nodes

# create edge list
interactions <- my_data %>% group_by(priorityWdid, analysisWdid) %>% summarise(weight = priority_sum_wtd_count) %>% ungroup()
interactions <- distinct(interactions)
interactions

edges <- interactions %>% left_join(nodes, by = c("priorityWdid" = "label")) %>% rename(from = id)
edges <- edges %>% left_join(nodes, by = c("analysisWdid" = "label")) %>% rename(to = id)

# remove superfluous rows
edges <- select(edges, from, to, weight)
edges

# create network using igraph package
network_2002 <- graph_from_data_frame(d = edges, vertices = nodes, directed = TRUE)

par(mfrow=c(1,1))
plot(network_2002, layout = layout_with_graphopt, edge.arrow.size = 0.2)

# plot network using ggraph
ggraph(network_2002, layout = "graphopt") + 
  geom_node_point() +
  geom_edge_link(aes(width = weight), alpha = 0.8) + 
  scale_edge_width(range = c(0.2, 2)) +
  geom_node_text(aes(label = label), repel = TRUE) +
  labs(edge_width = "Days") +
  theme_graph()

# plot linear map
ggraph(network_2002, layout = "linear") + 
  geom_edge_arc(aes(width = weight), alpha = 0.8) + 
  scale_edge_width(range = c(0.2, 2)) +
  geom_node_text(aes(label = label)) +
  labs(edge_width = "Days") +
  theme_graph()


# interactive plot using visNetwork
visNetwork(nodes, edges)

# add attributes
edges <- mutate(edges, width = weight/50 + 1)
visNetwork(nodes, edges) %>% 
  visIgraphLayout(layout = "layout_with_fr") %>% 
  visEdges(arrows = "middle")
