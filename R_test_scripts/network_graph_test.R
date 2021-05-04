# Libraries
library(tidyverse)
library(viridis)
library(patchwork)
library(hrbrthemes)
library(ggraph)
library(igraph)
library(networkD3)
library(tidyr)
library(dplyr)


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

# NetworkD3 format
graph=simpleNetwork(connect)
# use forceNetwork to make more customizable graphs

# Plot
simpleNetwork(connect,     
              Source = 1,                 # column number of source
              Target = 2,                 # column number of target
              height = 880,               # height of frame area in pixels
              width = 1980,
              linkDistance = 100,         # distance between node. Increase this value to have more space between nodes
              charge = -4,              # numeric value indicating either the strength of the node repulsion (negative value) or attraction (positive value)
              fontSize = 5,              # size of the node names
              fontFamily = "serif",       # font og node names
              linkColour = "#666",        # colour of edges, MUST be a common colour for the whole graph
              nodeColour = "#69b3a2",     # colour of nodes, MUST be a common colour for the whole graph
              opacity = 0.9,              # opacity of nodes. 0=transparent. 1=no transparency
              zoom = TRUE                    # Can you zoom on the figure?
)
