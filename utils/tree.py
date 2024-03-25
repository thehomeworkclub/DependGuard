from igraph import Graph, plot
import cairo


# Example dependency data structure representing a dependency tree
dependencies = {
    "project": {"certifi": "2024.2.2", "requests": "2.25.1"},
    "requests": {"urllib3": "1.26.3", "idna": "2.10", "chardet": "3.0.4"},
    "urllib3": {"brotli": None},  # Example where a dependency has no further dependencies
    "idna": {},  # No dependencies
    "chardet": {},  # No dependencies
    "brotli": {}  # No dependencies
}



def build_graph(dep_dict):
    """
    Builds an igraph Graph object from a dependency dictionary.

    Args:
        dep_dict: A dictionary representing the dependency tree.

    Returns:
        A tuple containing the igraph Graph object and a visual style dictionary for plotting.
    """

    g = Graph(directed=True)  # Create a directed graph
    vertices = set()  # Set to store unique vertices
    edges = []  # List to store edges

    # Iterate through the dependency dictionary to add vertices and edges
    for parent, deps in dep_dict.items():
        vertices.add(parent)
        for child, version in deps.items():
            vertices.add(child)
            edges.append((parent, child))  # Add a directed edge from parent to child

    g.add_vertices(list(vertices))  # Add vertices to the graph
    g.add_edges(edges)  # Add edges to the graph

    # Set labels and styles for the graph
    g.vs["label"] = g.vs["name"]  # Use vertex names as labels
    layout = g.layout("tree")  # Use a tree layout for visualization

    visual_style = {
        "vertex_size": 20,  # Vertex size
        "vertex_color": "lightblue",  # Vertex color
        "vertex_label": g.vs["label"],  # Vertex labels
        "edge_arrow_size": 1,  # Edge arrow size
        "layout": layout,  # Graph layout
        "bbox": (300, 300),  # Size of the plot
        "margin": 20  # Margin around the plot
    }

    return g, visual_style


# Build the graph from the dependency dictionary
g, visual_style = build_graph(dependencies)

# Plot the graph and save it as "dependency_tree.png"
plot(g, "dependency_tree.png", **visual_style)