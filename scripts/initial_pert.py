# import networkx as nx
# import pandas as pd

# def run_pert_analysis(df):
    

#     # Calculate Expected Time using PERT formula
#     df["ExpectedTime"] = (df["Optimistic"] + 4 * df["MostLikely"] + df["Pessimistic"]) / 6
#     df["Variance"] = ((df["Pessimistic"] - df["Optimistic"]) / 6) ** 2

#     # Initialize graph
#     G = nx.DiGraph()

#     # Add nodes with duration
#     for _, row in df.iterrows():
#         act_id = row["Activity_id"]
#         label = f"{act_id} - {row['Activity N']}"
#         G.add_node(label, duration=row["ExpectedTime"])

#     # Add edges based on dependencies
#     for _, row in df.iterrows():
#         current = f"{row['Activity_id']} - {row['Activity N']}"
#         if pd.notna(row["Dependencies"]):
#             deps = [d.strip() for d in str(row["Dependencies"]).split(',')]
#             for dep in deps:
#                 dep_name = df[df["Activity_id"] == dep]["Activity N"].values
#                 if len(dep_name) == 0:
#                     continue
#                 dep_full = f"{dep} - {dep_name[0]}"
#                 G.add_edge(dep_full, current)

#     # Forward pass (Early Start and Finish)
#     ES, EF = {}, {}
#     for node in nx.topological_sort(G):
#         preds = list(G.predecessors(node))
#         ES[node] = max([EF[p] for p in preds], default=0)
#         EF[node] = ES[node] + G.nodes[node]['duration']
#         G.nodes[node]['ES'] = ES[node]
#         G.nodes[node]['EF'] = EF[node]

#     # Backward pass (Late Start and Finish)
#     LS, LF = {}, {}
#     max_EF = max(EF.values())
#     for node in reversed(list(nx.topological_sort(G))):
#         succs = list(G.successors(node))
#         LF[node] = min([LS[s] for s in succs], default=max_EF)
#         LS[node] = LF[node] - G.nodes[node]['duration']
#         G.nodes[node]['LS'] = LS[node]
#         G.nodes[node]['LF'] = LF[node]
#         G.nodes[node]['Slack'] = LS[node] - ES[node]

#     # Critical Path
#     critical_path = [node for node in G.nodes if G.nodes[node]['Slack'] == 0]

#     # Convert to result dataframe
#     result_data = []
#     for node in G.nodes:
#         result_data.append({
#             "Activity N": node,
#             "Duration": G.nodes[node]['duration'],
#             "ES": G.nodes[node]['ES'],
#             "EF": G.nodes[node]['EF'],
#             "LS": G.nodes[node]['LS'],
#             "LF": G.nodes[node]['LF'],
#             "Slack": G.nodes[node]['Slack'],
#             "IsCritical": node in critical_path
#         })
#     result_df = pd.DataFrame(result_data)

#     return result_df, critical_path, G



import pandas as pd
import networkx as nx
from typing import Tuple, List

def run_pert_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], nx.DiGraph]:
    """
    Complete PERT analysis with:
    - Accurate forward/backward passes
    - Head/Tail slacks and all float types
    - Critical path detection
    - Variance calculation
    - Strict 3-decimal precision
    """
    # ===== 1. Input Validation =====
    required_cols = {"Activity_id", "Optimistic", "MostLikely", "Pessimistic", "Dependencies"}
    if missing := required_cols - set(df.columns):
        raise KeyError(f"Missing columns: {missing}")

    # ===== 2. Time Estimates =====
    df = df.copy()
    df['TE'] = round((df['Optimistic'] + 4*df['MostLikely'] + df['Pessimistic']) / 6, 3)
    df['Variance'] = round(((df['Pessimistic'] - df['Optimistic']) / 6).pow(2), 3)

    # ===== 3. Build AOA Network =====
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_node(row['Activity_id'], 
                  duration=row['TE'],
                  variance=row['Variance'])
        
        if pd.notna(row['Dependencies']):
            for dep in str(row['Dependencies']).replace(" ", "").split(','):
                if dep: G.add_edge(dep, row['Activity_id'])

    if not nx.is_directed_acyclic_graph(G):
        raise ValueError("Cyclic dependencies detected!")

    # ===== 4. Forward Pass (ES/EF) =====
    ES, EF = {}, {}
    for node in nx.topological_sort(G):
        ES[node] = max([EF.get(p, 0) for p in G.predecessors(node)], default=0)
        EF[node] = round((ES[node] + G.nodes[node]['duration']), 3)
        G.nodes[node].update({'ES': ES[node], 'EF': EF[node]})

    project_duration = max(EF.values()) if EF else 0

    # ===== 5. Backward Pass (LS/LF) =====
    LF, LS = {}, {}
    for node in reversed(list(nx.topological_sort(G))):
        LF[node] = min([LS.get(s, project_duration) for s in G.successors(node)], default=project_duration)
        LS[node] = round((LF[node] - G.nodes[node]['duration']), 3)
        G.nodes[node].update({'LF': LF[node], 'LS': LS[node]})

    # ===== 6. Slack & Float Calculations =====
    for node in G.nodes:
        # Head Slack (HS) = LS - ES
        HS = round(G.nodes[node]['LS'] - G.nodes[node]['ES'], 3)
        
        # Tail Slack (TS) = LF - EF
        TS = round(G.nodes[node]['LF'] - G.nodes[node]['EF'], 3)
        
        # Total Float (TF) = LS - ES
        TF = HS
        
        # Free Float (FF) = min(ES successors) - EF
        successors = list(G.successors(node))
        FF = round(min([G.nodes[s]['ES'] for s in successors]) - G.nodes[node]['EF'], 3) if successors else 0
        
        # Independent Float (IF) = max(0, FF - max(0, ES - max(EF predecessors)))
        pred_EFs = [G.nodes[p]['EF'] for p in G.predecessors(node)]
        IF =round(max(0, FF - max(0, G.nodes[node]['ES'] - max(pred_EFs, default=0))), 3)
        
        # Interfering Float (ItF) = TF - FF
        ItF = round((TF - FF), 3)
        
        G.nodes[node].update({
            'HeadSlack': HS,
            'TailSlack': TS,
            'TotalFloat': TF,
            'FreeFloat': FF,
            'IndependentFloat': IF,
            'InterferingFloat': ItF,
            'IsCritical': (HS == 0) and (TS == 0)
        })

    # ===== 7. Critical Path Detection =====
    critical_path = []
    current_nodes = [n for n in G.nodes if G.in_degree(n) == 0]
    
    while current_nodes:
        node = current_nodes.pop(0)
        if G.nodes[node]['IsCritical']:
            critical_path.append(node)
            current_nodes = [n for n in G.successors(node) if G.nodes[n]['IsCritical']]

    # ===== 8. Prepare Results =====
    result_data = []
    for node in G.nodes:
        result_data.append({
            'Activity_id': node,
            'TE': G.nodes[node]['duration'],
            'Variance': G.nodes[node]['variance'],
            'ES': G.nodes[node]['ES'],
            'EF': G.nodes[node]['EF'],
            'LS': G.nodes[node]['LS'],
            'LF': G.nodes[node]['LF'],
            'HeadSlack': G.nodes[node]['HeadSlack'],
            'TailSlack': G.nodes[node]['TailSlack'],
            'TotalFloat': G.nodes[node]['TotalFloat'],
            'FreeFloat': G.nodes[node]['FreeFloat'],
            'IndependentFloat': G.nodes[node]['IndependentFloat'],
            'InterferingFloat': G.nodes[node]['InterferingFloat'],
            'IsCritical': G.nodes[node]['IsCritical']
        })

    result_df = pd.DataFrame(result_data)[[
        'Activity_id', 'TE', 'Variance', 'ES', 'EF', 'LS', 'LF',
        'HeadSlack', 'TailSlack', 'TotalFloat', 'FreeFloat',
        'IndependentFloat', 'InterferingFloat', 'IsCritical'
    ]]

    return result_df, critical_path, G