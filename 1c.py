import osmnx as ox
import networkx as nx
import folium

# Load graph from OSM XML file
filepath = r"C:\Users\ASUS\Documents\Assignment2\source codes\map.osm"
G = ox.graph_from_xml(filepath)

# Compute travel time for each edge
for u, v, k, data in G.edges(data=True, keys=True):
    travel_time = data.get("length", 0) / 15.0
    highway = data.get("highway", "")
    if isinstance(highway, list):
        highway = highway[0]
    if highway in ['primary', 'secondary', 'trunk']:
        travel_time *= 1.5
    data["travel_time"] = travel_time

# Compute PageRank for the graph
pagerank_dict = nx.pagerank(G)

# Sort nodes by PageRank in descending order and select the top 3 nodes
top_3_pagerank = sorted(pagerank_dict.items(), key=lambda x: x[1], reverse=True)[:4]
print("Top 3 PageRank nodes:")
for node, pr in top_3_pagerank:
    print(f"Node: {node}, PageRank: {pr}")

# Select the first of the top 3 as the center for map initialization
center_node = top_3_pagerank[0][0]
center_lat = G.nodes[center_node]['y']
center_lon = G.nodes[center_node]['x']

# Initialize a folium map
m = folium.Map(location=[center_lat, center_lon], zoom_start=16)

# Add all edges to the map
for u, v, data in G.edges(data=True):
    try:
        points = [(G.nodes[u]['y'], G.nodes[u]['x']), (G.nodes[v]['y'], G.nodes[v]['x'])]
        folium.PolyLine(points, color="gray", weight=2).add_to(m)
    except KeyError:
        continue

# Define distinct colors for the top nodes (adjust as needed)
colors = ['red', 'blue', 'green', 'yellow'] 

# Mark the top 3 PageRank nodes on the map
for (node, pr), color in zip(top_3_pagerank, colors):
    node_lat = G.nodes[node]['y']
    node_lon = G.nodes[node]['x']
    folium.CircleMarker(
        location=[node_lat, node_lon],
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"Node: {node}\nPageRank: {pr:.4f}"
    ).add_to(m)

# Save the interactive map
m.save("interactive_road_network.html")
print("Map saved as interactive_road_network.html. Open this file in a browser to interact.")
