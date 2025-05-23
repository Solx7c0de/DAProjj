

```markdown
#  P.M. Tool — Internal Design & Roadmap

##  Objective

To develop a backend scheduling system tailored for civil engineering projects, supporting CPM/PERT scheduling, resource optimization, and predictive analytics.

##  System Components

### 1. Scheduler Core (`scripts/cpm.py`)
- Parses task input from Excel
- Calculates earliest/latest times
- Identifies critical path
- Supports PERT variation

### 2. Database Integration (`sql/`)
- SQLite schema for storing project schedules
- Read/write operations using `sqlite3` or `SQLAlchemy`

### 3. Resource Optimization (`scripts/resource_optim.py`)
- Resource leveling & smoothing
- Uses resource availability matrix

### 4. Visualization Engine
- Gantt chart via `matplotlib` and `plotly`
- (Planned) Interactive timelines using `plotly`

### 5. ML Delay Predictor (Planned)
- Features: task complexity, weather, holidays
- Model: Regression/XGBoost-based

##  Folder Recap

- `data/`: Input files in `.xlsx`/`.csv`
- `notebooks/`: Prototyping logic in Jupyter
- `scripts/`: Finalized, reusable code
- `sql/`: Database schema + test queries
- `outputs/`: Charts and reports
- `docs/`: Design notes, planning roadmap

##  Dev Workflow

1. Prototype logic in Jupyter
2. Migrate tested code to `scripts/`
3. Create reproducible examples in `notebooks/`
4. Push commits to Git regularly
5. Track milestones in `docs/overview.md`
```