
# Data Analytics Project ( P.M. Tool)

A streamlit deployable, programme consisting of modular scripts, which could do analysis based on statistical methods of CPM, PERT, still in progress for future ammends and additions.

##  Project Structure

P.M. Tool/
├── data/ # Excel/CSV files for scheduling inputs
├── notebooks/ # Jupyter notebooks (logic development, exploration)
├── scripts/ # Modular Python scripts (CPM logic, DB connectors, etc.)
├── outputs/ # Generated charts, Gantt diagrams, and reports
├── sql/ # SQLite DB schemas and sample queries
├── docs/ # Internal documentation, designs, and references
├── requirements.txt
├── README.md
└── .gitignore



---

## ✅ Features Implemented

- ✅ CPM (Critical Path Method) scheduling
- ✅ PERT-based analysis using optimistic, pessimistic, and most-likely durations
- ✅ Critical path identification
- ✅ Total float & slack calculation
- ✅ Early Start (ES), Early Finish (EF), Late Start (LS), Late Finish (LF)
- ✅ Project duration & critical variance computation
- ✅ Probability of target completion (Z-score & deviation)
- ✅ Matplotlib Gantt chart visualization
- ✅ Streamlit-based UI for input, config & output
- ✅ SQLite database setup for future integration

---

## 🐞 Known Bugs (to be fixed)

- ❌ Target duration probability button non-functional
- ❌ Formula display UI incorrectly formats values
- ❌ No exception handling for incorrect Excel headers or nulls
- ⏳ Minor formatting issues on Gantt chart for longer activity names

---

## 🚀 Planned Future Updates

- 🔜 AOA (Activity-on-Arrow) network diagram (using `networkx` or `graphviz`)
- 🔜 Crash cost analysis module with trade-off curves
- 🔜 Delay prediction module using historical project datasets
- 🔜 Resource leveling & smoothing with priority heuristics
- 🔜 Export final schedule as PDF / Excel with legends and charts
- 🔜 Fully fleged app deployment with all mentioned features for easy access.
---

## 📦 Getting Started

```bash
# Clone the repository
git clone https://github.com/Solx7c0de/DAProjj
cd DAProjj

# Install dependencies
pip install -r requirements.txt

# navigate to the project root first
streamlit run scripts/app.py

#add the tasks cleaned V1 file from the data -> cleaned folder.. Welcome!





