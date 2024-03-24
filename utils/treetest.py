from igraph import Graph, plot
import cairo

# Example dependency data structure
# Assuming a structure where each key maps to a dictionary of dependencies
dependencies = {
    "project": {"certifi": "2024.2.2", "requests": "2.25.1"},
    "requests": {"urllib3": "1.26.3", "idna": "2.10", "chardet": "3.0.4"},
    "urllib3": {"brotli": None},  # Example where a dependency has no further dependencies
    "idna": {},  # No dependencies
    "chardet": {},  # No dependencies
    "brotli": {}  # No dependencies
}

def build_graph(dep_dict):
    g = Graph(directed=True)
    vertices = set()
    edges = []

    for parent, deps in dep_dict.items():
        vertices.add(parent)
        for child, version in deps.items():
            vertices.add(child)
            edges.append((parent, child))

    g.add_vertices(list(vertices))
    g.add_edges(edges)

    # Set labels and styles
    g.vs["label"] = g.vs["name"]
    layout = g.layout("tree")

    visual_style = {
        "vertex_size": 20,
        "vertex_color": "lightblue",
        "vertex_label": g.vs["label"],
        "edge_arrow_size": 1,
        "layout": layout,
        "bbox": (300, 300),
        "margin": 20
    }
    return g, visual_style

# Build the graph
g, visual_style = build_graph(dependencies)

# Plot the graph
plot(g, "dependency_tree.png", **visual_style)
