import streamlit as st
from scipy.stats import norm

def show_completion_probability_ui(result_df, critical_path):
    st.subheader("📊 PERT Completion Probability Analysis")
    
    # Section 1: Critical Path Summary
    with st.expander("🔍 Critical Path Details"):
        critical_df = result_df[result_df['Activity_id'].isin(critical_path)]
        st.dataframe(critical_df[['Activity_id', 'TE', 'Variance']])
    
    # Section 2: Project Statistics
    project_te = round(critical_df['TE'].sum(), 2)
    project_variance = critical_df['Variance'].sum()
    project_std_dev = round(project_variance ** 0.5, 2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⏳ Expected Duration (TE)", f"{project_te} days")
    with col2:
        st.metric("📉 Std. Deviation (σ)", f"{project_std_dev} days")
    
    # Section 3: Probability Calculator
    st.markdown("---")
    st.subheader("🎯 Completion Probability Calculator")
    
    # Input with custom formatting (3-digit number)
    target_duration = st.number_input(
        "Enter target completion time (days):",
        min_value=0.0,
        max_value=999.0,
        value=float(project_te),
        step=1.0,
        format="%.0f"  # Forces integer display
    )
    
    if target_duration:
        # Calculate Z-score using PERT formula
        z_score = round((target_duration - project_te) / project_std_dev, 2)
        
        # Get probability from normal distribution
        probability = round(norm.cdf(z_score) * 100, 2)
        
        # Display calculation steps
        st.latex(fr"""
        \begin{{aligned}}
        Z &= \frac{{\text{{TD}} - \text{{TE}}}}{{\sigma}} \\
        &= \frac{{{target_duration:.1f} - {project_te:.1f}}}{{{project_std_dev:.2f}}} \\
        &= {z_score:.2f}
        \end{{aligned}}
        """)
        # Visual probability indicator
        st.progress(int(probability))
        
        # Result display
        if probability > 70:
            st.success(f"**{probability:.1f}%** chance of completing by day {target_duration:.0f}")
        elif probability > 30:
            st.warning(f"**{probability:.1f}%** chance of completing by day {target_duration:.0f}")
        else:
            st.error(f"**{probability:.1f}%** chance of completing by day {target_duration:.0f}")
        
        # Normal distribution reference
        with st.expander("📚 Z-score to Probability Reference"):
            st.image("https://www.mathsisfun.com/data/images/normal-distribution-table.gif",
                    caption="Standard Normal Distribution Table")