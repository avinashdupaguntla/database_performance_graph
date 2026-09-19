# Database Performance Investigation Assistant -- Architecture

## How It Works

```
User enters a database performance issue
        |
        v
  [understand_issue] -- acknowledges issue, classifies severity
        |
        +--> [analyze_query_structure] \
        |                               |
        +--> [analyze_index_strategy]   +--> run in PARALLEL
        |                               |
        +--> [analyze_database_load]   /
        |
        v
  [classify_performance_issue] -- reads all 3 analyses, decides quick vs deep
        |
        +-- SIMPLE --> [quick_optimization_plan] --------> quick optimization recommendations
        |
        +-- COMPLEX -> [deep_performance_investigation] -> detailed investigation plan
        |
        v
  Final output printed to user
```

## Interactive Mode

```
$ python database_performance_graph.py

  =======================================================
    DATABASE PERFORMANCE INVESTIGATION ASSISTANT
  =======================================================

    Describe a database performance issue.
    Type 'quit' to exit.

    Describe the issue > Query takes 15 seconds to return 200 rows
    ...graph runs...
    PERFORMANCE RECOMMENDATION
    ...

    Describe the issue > quit
    Goodbye!
```

## Graph Structure (Detailed)

```
                    +-------+
                    | START |
                    +---+---+
                        |
                        v
            +-----------+-----------+
            |    understand_issue   |
            |                       |
            | Acknowledges issue    |
            | Severity: LOW /       |
            |   MEDIUM / HIGH       |
            +-----------+-----------+
                        |
           PARALLEL FAN-OUT (3 edges from one node)
          /             |              \
         v              v               v
+--------+------+ +-----+--------+ +----+---------+
| analyze_      | | analyze_     | | analyze_     |
| query_        | | index_       | | database_    |
| structure     | | strategy     | | load         |
|               | |              | |              |
| Reviews joins | | Reviews      | | Reviews      |
| filters,      | | indexes,     | | locks, CPU,  |
| aggregations, | | missing and  | | memory, I/O, |
| subqueries    | | redundant    | | concurrency  |
+--------+------+ +-----+--------+ +----+---------+
         \              |               /
          FAN-IN (all 3 must finish)
                        |
                        v
      +-----------------+-----------------+
      | classify_performance_issue        |
      |                                   |
      | Reads all 3 analyses              |
      | Returns JSON:                     |
      | {needs_deep_investigation,        |
      |  reason}                          |
      +-----------------+-----------------+
                        |
                CONDITIONAL EDGE
               route_after_decision()
                    /         \
      false        /           \       true
     (SIMPLE)     /             \    (COMPLEX)
                 v               v
     +-----------+------+ +------+-------------------+
     | quick_           | | deep_                    |
     | optimization_    | | performance_            |
     | plan             | | investigation           |
     |                  | |                          |
     | Top fixes        | | 3 phases:               |
     | Priority order   | | 1. Query Investigation  |
     | Expected impact  | | 2. Index Review         |
     |                  | | 3. Infrastructure       |
     +-----------+------+ +------+-------------------+
                 \                /
                  \              /
                   v            v
                   +-----+------+
                   |    END     |
                   +------------+
```

## State Fields

```
PerformanceState
|
|-- user_issue                  <-- set by user input
|-- query_structure_analysis    <-- written by analyze_query_structure
|-- index_strategy_analysis     <-- written by analyze_index_strategy
|-- database_load_analysis      <-- written by analyze_database_load
|-- needs_deep_investigation    <-- written by classify_performance_issue
|-- investigation_reason        <-- written by classify_performance_issue
|-- final_recommendation        <-- written by quick_optimization_plan OR
|                                  deep_performance_investigation
|-- messages                    <-- appended by ALL nodes (operator.add)
```

## LangGraph Concepts Used

| Concept | Where in Code | What It Does |
|---------|--------------|--------------|
| State (Pydantic) | `PerformanceState` class | Typed data that flows through every node |
| Nodes | `understand_issue`, `analyze_*`, etc. | Functions that read state, do one job, return updates |
| Parallel Execution | 3 edges from `understand_issue` | LangGraph runs all 3 analysis nodes simultaneously |
| Fan-In | 3 edges into `classify_performance_issue` | Waits for all parallel nodes to finish |
| Conditional Edge | `route_after_decision()` | Routes to quick optimization or deep investigation |
| Graph Compilation | `graph.compile()` | Turns graph definition into runnable `app` |
| Invocation | `app.invoke({...})` | Runs the graph with initial state |
| Message Accumulation | `Annotated[list, operator.add]` | Parallel nodes append without overwriting |

## Tech Stack

| Component | Purpose |
|-----------|---------|
| LangGraph | Graph orchestration -- nodes, edges, parallel, conditional |
| LangChain | OpenAI LLM wrapper (`ChatOpenAI`) |
| OpenAI | `gpt-4.1-mini` for analysis and recommendation generation |
| Pydantic | State validation and type safety |
| python-dotenv | Load `OPENAI_API_KEY` from `.env` |

## File Structure

```
LangGraph_AgentFramework/
|-- database_performance_graph.py   Main code (graph + interactive loop)
|-- architecture.md                 This file
|-- architecture.drawio             Visual diagram (open with draw.io extension)
|-- requirements.txt                Dependencies
|-- .env                            OPENAI_API_KEY (not committed)
|-- .env.example                    Template for .env
|-- .gitignore                      Ignores .env, venv, __pycache__
```