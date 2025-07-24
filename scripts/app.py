import streamlit as st
import pandas as pd
import plotly.express as px
from crash_cost_analysis import run_crash_analysis
from initial_pert import run_pert_analysis 
from completion_probability import show_completion_probability_ui
from plot_aoa_diagram import plot_aoa_network
# # from plot_aoa import plot_aoa_network

# import sys
# import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "scripts")))
# # import sys
# # import os
# sys.path.append(os.path.dirname(__file__))




st.title("📊 PERT Scheduler + Crash Cost Analyzer")

uploaded_file = st.file_uploader("📥 Upload Cleaned Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Rename for consistency
    df = df.rename(columns={
        "Most Likely": "MostLikely",
        "Optimistic Time": "Optimistic",
        "Pessimistic Time": "Pessimistic",
        "Predecessors": "Dependencies",
        "Activity": "Activity_id",
        "Activity Name": "Activity N",

    })

    st.subheader("🧾 Raw Data")
    st.dataframe(df)

    if st.button("🚀 Run PERT Analysis"):
        result_df, critical_path, G = run_pert_analysis(df)      # debug 1
        st.success("PERT Analysis Complete ✅")
        st.write("🔴 Critical Path:", " → ".join(critical_path))   # maybe
        st.dataframe(result_df)


         
        # st.subheader("📊 AOA Network Diagram")
        # fig = plot_aoa_network(G, critical_path)  # Pass both G and critical_path
        # st.plotly_chart(fig, use_container_width=True)
      




        # Completion Probability UI
        show_completion_probability_ui(result_df, critical_path)   #debug 3










        # # Optional Gantt Chart
        # fig = px.timeline(result_df, x_start="ES", x_end="EF", y="Activity", color="Slack")
        # fig.update_yaxes(autorange="reversed")
        # st.plotly_chart(fig)

        # # Crash Cost Section
        # if {'NormalDuration', 'CrashDuration', 'NormalCost', 'CrashCost'}.issubset(df.columns):
        #     st.subheader("💰 Crash Cost Analysis")
        #     crash_df = run_crash_analysis(result_df)
        #     st.dataframe(crash_df)
        # else:
        #     st.warning("❗ Please include Crash columns: NormalDuration, CrashDuration, NormalCost, CrashCost")

    