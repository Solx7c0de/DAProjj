import networkx as nx
import pandas as pd


def build_activity_graph(df):
    """
    Constructs a directed graph from activity data with duration and predecessors.
    """
    G = nx.DiGraph()

    # Add nodes with duration as attribute
    for _, row in df.iterrows():
        G.add_node(row['Activity'], duration=row['Duration'])

    # Add edges for dependencies
    for _, row in df.iterrows():
        if pd.isna(row['Predecessors']) or row['Predecessors'] in ['', [], None]:
            continue
        preds = row['Predecessors']
        if isinstance(preds, str):
            preds = [preds]  # in case it's a single string
        for pred in preds:
            G.add_edge(pred.strip(), row['Activity'])

    return G
