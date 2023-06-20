import networkx as nx
from pyvis.network import Network
import matplotlib.cm as cm
import matplotlib.colors as colors
import streamlit as st
import json


def show_Json_graph(json_input):
    # Parse JSON input
    json_data = json.loads(json_input) if isinstance(json_input, str) else json_input

    G = nx.DiGraph()  # Create a directed graph

    # Generate colormap for different levels of nodes
    cmap = cm.get_cmap('gnuplot')

    def build_graph(json_data, parent=None, depth=0):
        if isinstance(json_data, dict):
            for k, v in json_data.items():
                G.add_node(k, level=depth)
                if parent is not None:
                    G.add_edge(parent, k)
                build_graph(v, parent=k, depth=depth + 0.2)
        elif isinstance(json_data, list):
            for i, item in enumerate(json_data):
                new_node = f"{parent}_{i}"
                G.add_node(new_node, level=depth)
                G.add_edge(parent, new_node)
                build_graph(item, parent=new_node, depth=depth + 0.2)
        else:
            G.add_node(str(json_data), level=depth)
            if parent is not None:
                G.add_edge(parent, str(json_data))

    build_graph(json_data)

    # Build the network
    nt = Network(notebook=True)
    nt.from_nx(G)

    # Color the nodes and set their size
    max_depth = max(nx.get_node_attributes(G, 'level').values())
    for i, node in enumerate(nt.nodes):
        level = G.nodes[node['id']]['level']
        color = colors.to_hex(cmap(level / max_depth))
        node['color'] = color
        node['size'] = (max_depth - level + 1) * 10  # Size is inverse proportional to level

    # Show the network
    nt.show("nx.html")
    st.components.v1.html(open("nx.html").read(), height=610, scrolling=True)
