import osmnx as ox
import networkx as nx

# Step 1: Load and simplify the graph
filepath = r"C:\Users\ASUS\Documents\Assignment2\source codes\Kudasan.osm"
G = ox.graph_from_xml(filepath, simplify=True)  # Simplify to clean up the network

# Step 2: Convert to undirected graph
G_undir = G.to_undirected()

# Step 3: Extract the largest connected component
largest_cc = max(nx.connected_components(G_undir), key=len)
G_sub = G_undir.subgraph(largest_cc).copy()

# Step 4: Convert to simple graph for clustering computations
G_simple = nx.Graph(G_sub)  # Removes parallel edges and self-loops

# Step 5: Calculate degree for all nodes
degrees = dict(G_simple.degree())

# Step 6: Get top 10 nodes by degree
top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]

# Step 7: Calculate local clustering coefficients
local_clustering = nx.clustering(G_simple)

# Step 8: Combine degree and clustering for top nodes
top_nodes_clustering = [(node, degrees[node], local_clustering[node]) for node, _ in top_nodes]

# Step 9: Print top node metrics
print("Top 10 Nodes by Degree - Local Clustering Coefficients")
print("{:<10} {:<10} {:<25}".format("Node ID", "Degree", "Clustering Coefficient"))
print("-" * 45)
for node, degree, cc in top_nodes_clustering:
    print("{:<10} {:<10} {:<25.4f}".format(node, degree, cc))

# Step 10: Calculate average degree
num_nodes = G_simple.number_of_nodes()
num_edges = G_simple.number_of_edges()
average_degree = (2 * num_edges) / num_nodes
print(f"\nAverage Degree: {average_degree:.4f}")

# Step 11: Global Clustering Metrics
transitivity = nx.transitivity(G_simple)
avg_clustering = nx.average_clustering(G_simple)

print(f"Global Clustering Coefficient (Transitivity): {transitivity:.4f}")
print(f"Average Local Clustering (Global Metric): {avg_clustering:.4f}")
