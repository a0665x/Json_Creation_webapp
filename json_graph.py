import networkx as nx
from pyvis.network import Network
import streamlit as st
import json


def show_Json_graph(json_input):
    # Parse JSON input
    json_data = json.loads(json_input) if isinstance(json_input, str) else json_input

    G = nx.DiGraph()  # Create a directed graph

    def build_graph(json_data, parent=None):
        if isinstance(json_data, dict):
            for k, v in json_data.items():
                if parent is not None:
                    G.add_edge(parent, k)
                build_graph(v, parent=k)
        elif isinstance(json_data, list):
            for i, item in enumerate(json_data):
                new_node = f"{parent}_{i}"
                G.add_edge(parent, new_node)
                build_graph(item, parent=new_node)

    build_graph(json_data)

    # Build the network
    nt = Network(notebook=True)
    nt.from_nx(G)

    # Show the network
    nt.show("nx.html")
    st.components.v1.html(open("nx.html").read(), height=600, scrolling=True)
