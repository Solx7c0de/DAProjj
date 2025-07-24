import networkx as nx
import pandas as pd


# def build_activity_graph(df):
#     """
#     Constructs a directed graph from activity data with duration and predecessors.
#     """
#     G = nx.DiGraph()

#     # Add nodes with duration as attribute
#     for _, row in df.iterrows():
#         G.add_node(row['Activity'], duration=row['Duration'])

#     # Add edges for dependencies
#     for _, row in df.iterrows():
#         if pd.isna(row['Predecessors']) or row['Predecessors'] in ['', [], None]:
#             continue
#         preds = row['Predecessors']
#         if isinstance(preds, str):
#             preds = [preds]  # in case it's a single string
#         for pred in preds:
#             G.add_edge(pred.strip(), row['Activity'])

#     return G

def build_activity_graph(df):
    """
    Constructs an AOA graph where:
    - Nodes are events (1, 2, 3, ...)
    - Edges are activities with 'activity', 'duration', and 'TE'
    """
    G = nx.DiGraph()
    event_counter = 1
    activity_to_events = {}  # To remember which activity maps to which (u, v)

    for _, row in df.iterrows():
        activity = row['Activity']
        duration = row['Duration']
        preds = row['Predecessors']

        # Clean preds
        if pd.isna(preds) or preds in ['', [], None]:
            preds = []
        elif isinstance(preds, str):
            preds = [p.strip() for p in preds.split(',')]

        if not preds:
            # Start node to activity
            u = event_counter
            event_counter += 1
            v = event_counter
            event_counter += 1
            G.add_edge(u, v, activity=activity, duration=duration)
            activity_to_events[activity] = (u, v)
        else:
            for pred in preds:
                pred = pred.strip()
                if pred not in activity_to_events:
                    continue
                u = activity_to_events[pred][1]  # End of predecessor
                v = event_counter
                event_counter += 1
                G.add_edge(u, v, activity=activity, duration=duration)
                activity_to_events[activity] = (u, v)

    # Assign TE (Earliest Finish) as cumulative durations for simplicity
    for path in nx.topological_sort(G):
        for succ in G.successors(path):
            edge = G[path][succ]
            prev_te = G.nodes[path].get('TE', 0)
            edge['TE'] = prev_te + edge['duration']
            G.nodes[succ]['TE'] = max(G.nodes.get(succ, {}).get('TE', 0), edge['TE'])

    return G
