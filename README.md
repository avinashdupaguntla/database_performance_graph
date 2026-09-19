# Database Performance Investigation Assistant - Learn LangGraph Step by Step
2
 
3
A beginner-friendly LangGraph project that investigates database performance
4
issues and generates optimization recommendations.
5
 
6
The project demonstrates a clear LangGraph pattern:
7
 
8
```text
9
[Database Performance Issue]
10
|
11
v
12
understand_issue
13
|
14
+--> analyze_query_structure -----+
15
+--> analyze_index_strategy ------+--> classify_performance_issue
16
+--> analyze_database_load -------+ |
17
conditional
18
/ \
19
quick_optimization_plan deep_performance_investigation
20
| |
21
END END
22
```
23
 
24
---
25
 
26
## What This Project Does
27
 
28
A user enters a database performance issue such as:
29
 
30
- `A query takes 12 seconds to return 500 rows`
31
- `Users are experiencing locking and blocking issues`
32
- `Database CPU remains above 90% during peak hours`
33
- `A reporting query joins multiple large tables and runs for 30 minutes`
34
 
35
The graph then:
36
 
37
1. Understands the reported performance issue.
38
2. Runs three specialist analysis nodes in parallel:
39
- query structure specialist
40
- indexing strategy specialist
41
- database load specialist
42
3. Uses a decision node to determine whether the issue needs:
43
- a quick optimization plan, or
44
- a deeper performance investigation
45
4. Routes to the correct final node.
46
5. Prints the performance recommendation and message log.
47
 
48
---
49
 
50
## LangGraph Concepts Covered
51
 
52
| Concept | Where It Appears |
53
|---|---|
54
| State | `PerformanceState` Pydantic model |
55
| Nodes | `understand_issue`, `analyze_query_structure`, `analyze_index_strategy`, `analyze_database_load`, `classify_performance_issue`, `quick_optimization_plan`, `deep_performance_investigation` |
56
| Parallel execution | Three analysis nodes run after `understand_issue` |
57
| Fan-in | All three specialist analyses flow into `classify_performance_issue` |
58
| Conditional edges | `route_after_decision` sends the graph to quick or deep investigation |
59
| Final output | `quick_optimization_plan` or `deep_performance_investigation` |
60
| Message accumulation | `messages: Annotated[list, operator.add]` |
61
 
62
---
63
 
64
## Project Files
65
 
66
```text
67
database_performance_graph.py Main LangGraph project
68
architecture.md Architecture explanation
69
architecture.drawio Diagram source file
70
requirements.txt Python dependencies
71
.env.example Example environment file
72
.gitignore Ignored local files
73
```
74
 
75
---
76
 
77
## Setup
78
 
79
### 1. Create and activate a virtual environment
80
 
81
```powershell
82
python -m venv venv
83
venv\Scripts\activate
84
```
85
 
86
On macOS/Linux:
87
 
88
```bash
89
python -m venv venv
90
source venv/bin/activate
91
```
92
 
93
### 2. Install dependencies
94
 
95
```powershell
96
pip install -r requirements.txt
97
```
98
 
99
### 3. Configure your OpenAI API key
100
 
101
```powershell
102
copy .env.example .env
103
```
104
 
105
Edit `.env` and add your API key:
106
 
107
```text
108
OPENAI_API_KEY=sk-...
109
```
110
 
111
Never commit your real `.env` file.
112
 
113
### 4. Run the project
114
 
115
```powershell
116
python database_performance_graph.py
117
```
118
 
119
---
120
 
121
## Expected Flow
122
 
123
Example input:
124
 
125
```text
126
A reporting query takes over 25 minutes to complete.
127
 
128
SELECT customer_id,
129
SUM(order_total)
130
FROM orders
131
GROUP BY customer_id;
132
 
133
The orders table contains more than 100 million rows.
134
CPU usage remains above 90%.
135
```
136
 
137
The graph will:
138
 
139
1. Acknowledge and summarize the issue.
140
2. Analyze the query structure.
141
3. Analyze the indexing strategy.
142
4. Analyze database workload conditions.
143
5. Decide whether the issue needs a quick optimization plan or a deeper investigation.
144
6. Print the final recommendation.
145
7. Print the message log showing which nodes executed.
146
 
147
---
148
 
149
## Code Walkthrough
150
 
151
| Step | What Happens | File |
152
|---|---|---|
153
| 1 | Define `PerformanceState` | `database_performance_graph.py` |
154
| 2 | Initialize `ChatOpenAI` | `database_performance_graph.py` |
155
| 3 | Define graph node functions | `database_performance_graph.py` |
156
| 4 | Define `route_after_decision` | `database_performance_graph.py` |
157
| 5 | Add nodes and edges to `StateGraph` | `database_performance_graph.py` |
158
| 6 | Compile graph as `app` | `database_performance_graph.py` |
159
| 7 | Run with `run_performance_check()` | `database_performance_graph.py` |
160
 
161
---
162
 
163
## Important Note
164
 
165
This is a learning project, not a production database tuning tool. The output is
166
intended to demonstrate LangGraph concepts and provide educational
167
performance recommendations. Any optimization suggestions should be validated
168
using execution plans, database monitoring tools, and testing before being
169
applied to production systems.
170
 
171
---
172
 
173
## Key Takeaways
174
 
175
1. State holds the data that travels through the graph.
176
2. Nodes are normal Python functions that read state and return updates.
177
3. Parallel execution happens when one node connects to multiple next nodes.
178
4. Fan-in happens when multiple nodes connect into one later node.
179
5. Conditional edges let the graph choose the next path at runtime.
180
6. LangGraph can model real-world database troubleshooting workflows.