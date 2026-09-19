# Database Performance Investigation Assistant -- Learn LangGraph Step by Step

A beginner-friendly LangGraph project that investigates database performance issues and generates optimization recommendations.

The project demonstrates a clear LangGraph pattern:

```text
[Database Performance Issue]
             |
             v
     understand_issue
             |
             +--> analyze_query_structure -----+
             +--> analyze_index_strategy ------+--> classify_performance_issue
             +--> analyze_database_load -------+          |
                                             conditional
                                          /              \
                        quick_optimization_plan   deep_performance_investigation
                                          |              |
                                         END            END
```

---

## What This Project Does

A user enters a database performance issue such as:

- A query takes 12 seconds to return 500 rows
- Users are experiencing locking and blocking issues
- Database CPU remains above 90% during peak hours
- A reporting query joins multiple large tables and runs for 30 minutes

The graph then:

1. Understands the reported performance issue.
2. Runs three specialist analysis nodes in parallel.
3. Uses a decision node to determine whether the issue needs a quick optimization plan or a deeper performance investigation.
4. Routes to the correct final node.
5. Prints the performance recommendation and message log.

---

## Project Files

```text
database_performance_graph.py
architecture.md
architecture.drawio
requirements.txt
.env.example
.gitignore
```

---

## Setup

### Create and activate virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Configure API Key

```powershell
copy .env.example .env
```

Add:

```text
OPENAI_API_KEY=sk-...
```

### Run Project

```powershell
python database_performance_graph.py
```

---

## Key Takeaways

1. State travels through the graph.
2. Nodes perform specialized tasks.
3. Parallel execution improves workflow design.
4. Fan-in combines parallel results.
5. Conditional routing chooses the next path dynamically.
6. LangGraph can model real-world database troubleshooting workflows.