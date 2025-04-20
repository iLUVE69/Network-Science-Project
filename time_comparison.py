import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# Load and simplify the OSM street network
filepath = r"C:\Users\ASUS\Documents\Assignment2\source codes\map.osm"
G = ox.graph_from_xml(filepath)
G_undirected = G.to_undirected()
G_simple = nx.Graph(G_undirected)

# Get node degrees
degrees = np.array([deg for _, deg in G_simple.degree()])
degrees = degrees[degrees > 0]  # Remove zero degrees to avoid log(0)

# Logarithmic binning
num_bins = 15
min_deg, max_deg = degrees.min(), degrees.max()
bins = np.geomspace(min_deg, max_deg, num_bins)

# Histogram
hist, bin_edges = np.histogram(degrees, bins=bins)
bin_widths = np.diff(bin_edges)
bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])

# Normalize to get density
density = hist / (bin_widths * degrees.size)

# Plot as bar chart with log-log scale
plt.figure(figsize=(10, 6))
plt.bar(bin_centers, density, width=bin_widths, align='center',
        color='skyblue', edgecolor='navy', log=True)

plt.xscale('log')
plt.xlabel('Degree (log scale)')
plt.ylabel('Normalized Node Density (log scale)')
plt.title('Node Degree Distribution (Log-Binned Histogram)')
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
