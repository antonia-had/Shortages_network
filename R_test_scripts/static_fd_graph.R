# Libraries
library(tidyverse)
library(viridis)
library(patchwork)
library(hrbrthemes)
library(ggraph)
library(igraph)
library(networkD3)

# Load researcher data
setwd('/Users/ananyagangadhar/Desktop/M.Eng\ Project/Shortages_network/R_scripts')
# Load researcher data
dataUU <- read.csv("2002_adj_matrix.csv", header=TRUE)
head(dataUU[1:3])

# Transform the adjacency matrix in a long format
connect <- dataUU %>% gather(destination, value, 2:ncol(dataUU))
connect <- connect[!connect$value == 0, ]

# Number of connection per person
c( as.character(connect$X), as.character(connect$destination)) %>% as_tibble() %>%
  group_by(value) %>% summarize(n=n()) -> coauth
colnames(coauth) <- c("name", "n")

coauth

# Create a graph object with igraph
mygraph <- graph_from_data_frame( connect, vertices = coauth )

# Make the graph
ggraph(mygraph, layout="fr") + 
  #geom_edge_density(edge_fill="#69b3a2") +
  geom_edge_link(edge_colour="black", edge_alpha=0.5, edge_width=0.1) +
  geom_node_point(aes(size=n/2, alpha=n)) +
  #geom_node_text(aes(label=name, alpha=n), size=2, vjust=2, hjust=1) + 
  theme_void() +
  theme(legend.position="none", plot.margin=unit(rep(1,4), "cm")
  ) 

