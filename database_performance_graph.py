# =============================================================================
# Database Performance Investigation Assistant -- A LangGraph Learning Project
# =============================================================================
#
# This project teaches you how LangGraph works by building a database
# performance investigation assistant.
#
# WHAT THIS DOES:
# A user enters a slow-query description, SQL statement, execution details,
# or performance problem. The system runs 3 specialist analyzers in PARALLEL
# (query structure, indexing strategy, database load), then a decision node
# determines whether the issue needs a QUICK optimization plan or a DEEP
# investigation.
#
# LANGGRAPH CONCEPTS COVERED:
# 1. State Management (Pydantic)
# 2. Nodes
# 3. Parallel Execution
# 4. Fan-in
# 5. Conditional Edges
# 6. Graph Compilation
#
# GRAPH STRUCTURE:
#
#   START
#     |
#   understand_issue
#     |
#     +--> analyze_query_structure -----+
#     |                                 |
#     +--> analyze_index_strategy ------+--> classify_performance_issue
#     |                                 |             |
#     +--> analyze_database_load -------+      (conditional)
#                                                  /        \
#                                             quick?       deep?
#                                                |            |
#                                 quick_optimization_plan
#                                                |
#                                               END
#
#                                   OR
#
#                                deep_performance_investigation
#                                                |
#                                               END
#
# HOW TO RUN:
#   python database_performance_graph.py
#
# DEPENDENCIES:
#   langgraph
#   langchain-openai
#   python-dotenv
#   pydantic
#
# =============================================================================

import sys
import operator
import json
from typing import Annotated

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()


class PerformanceState(BaseModel):
    user_issue: str = ""

    query_structure_analysis: str = ""
    index_strategy_analysis: str = ""
    database_load_analysis: str = ""
    needs_deep_investigation: bool = False
    investigation_reason: str = ""
    final_recommendation: str = ""
    messages: Annotated[list, operator.add] = []


llm = ChatOpenAI(model="gpt-4.1-mini",temperature=1.2)


def understand_issue(state: PerformanceState) -> dict:
    response = llm.invoke(
        f"You are a database performance analyst. "
        f"A user reports the following issue:\n\n"
        f"'{state.user_issue}'.\n\n"
        f"Acknowledge the problem in 1-2 sentences. "
        f"Then classify the severity as LOW, MEDIUM, or HIGH on a new line like:\n"
        f"Severity: LOW"
    )

    return {
        "messages": [f"[understand_issue] {response.content}"]
    }


def analyze_query_structure(state: PerformanceState) -> dict:
    response = llm.invoke(
        f"You are a SQL query optimization specialist. "
        f"The user reports:\n\n"
        f"'{state.user_issue}'.\n\n"
        f"Analyze query structure. Review:\n"
        f"- joins\n"
        f"- filters\n"
        f"- aggregations\n"
        f"- subqueries\n"
        f"- sorting\n"
        f"- result volume\n\n"
        f"Provide findings and recommendations. "
        f"Keep it under 5 sentences."
    )

    return {
        "query_structure_analysis": response.content,
        "messages": ["[analyze_query_structure] Done"]
    }


def analyze_index_strategy(state: PerformanceState) -> dict:
    response = llm.invoke(
        f"You are a database indexing specialist. "
        f"The user reports:\n\n"
        f"'{state.user_issue}'.\n\n"
        f"Review the indexing strategy. "
        f"Identify:\n"
        f"- useful indexes\n"
        f"- missing indexes\n"
        f"- redundant indexes\n"
        f"- inefficient indexes\n\n"
        f"Suggest improvements."
    )

    return {
        "index_strategy_analysis": response.content,
        "messages": ["[analyze_index_strategy] Done"]
    }


def analyze_database_load(state: PerformanceState) -> dict:
    response = llm.invoke(
        f"You are a database operations specialist. "
        f"The user reports:\n\n"
        f"'{state.user_issue}'.\n\n"
        f"Review:\n"
        f"- locking\n"
        f"- blocking\n"
        f"- concurrency\n"
        f"- memory usage\n"
        f"- CPU utilization\n"
        f"- disk I/O\n"
        f"- workload conditions\n\n"
        f"Explain possible bottlenecks."
    )

    return {
        "database_load_analysis": response.content,
        "messages": ["[analyze_database_load] Done"]
    }


def classify_performance_issue(state: PerformanceState) -> dict:
    response = llm.invoke(
        f"You are a database performance decision system.\n\n"

        f"QUERY STRUCTURE ANALYSIS:\n"
        f"{state.query_structure_analysis}\n\n"

        f"INDEX STRATEGY ANALYSIS:\n"
        f"{state.index_strategy_analysis}\n\n"

        f"DATABASE LOAD ANALYSIS:\n"
        f"{state.database_load_analysis}\n\n"

        f"Determine whether this issue needs:\n"
        f"1. QUICK optimization (simple fixes)\n"
        f"2. DEEP investigation (complex troubleshooting)\n\n"

        f"Reply STRICTLY in this JSON format:\n"
        f'{{"needs_deep_investigation": true, '
        f'"reason": "one sentence explanation"}}'
    )

    try:
        result = json.loads(response.content)

        needs_deep = result["needs_deep_investigation"]
        reason = result["reason"]

    except (json.JSONDecodeError, KeyError):

        needs_deep = False
        reason = "Could not parse decision. Defaulting to quick optimization."

    return {
        "needs_deep_investigation": needs_deep,
        "investigation_reason": reason,
        "messages": [
            f"[classify_performance_issue] deep_investigation={needs_deep}"
        ]
    }


def quick_optimization_plan(state: PerformanceState) -> dict:
    response = llm.invoke(
        f"You are a database performance consultant.\n\n"

        f"Based on these specialist analyses, create a SHORT optimization plan:\n\n"

        f"QUERY STRUCTURE:\n"
        f"{state.query_structure_analysis}\n\n"

        f"INDEX STRATEGY:\n"
        f"{state.index_strategy_analysis}\n\n"

        f"DATABASE LOAD:\n"
        f"{state.database_load_analysis}\n\n"

        f"Provide:\n"
        f"1. Top 5 fixes\n"
        f"2. Expected impact\n"
        f"3. Recommended implementation order\n\n"

        f"Keep it concise and practical."
    )

    return {
        "final_recommendation":
            f"QUICK OPTIMIZATION PLAN\n{'=' * 45}\n{response.content}",
        "messages": ["[quick_optimization_plan] Generated"]
    }


def deep_performance_investigation(state: PerformanceState) -> dict:
    response = llm.invoke(
        f"You are a senior database performance consultant.\n\n"

        f"Based on these specialist analyses, create a DEEP investigation plan:\n\n"

        f"QUERY STRUCTURE:\n"
        f"{state.query_structure_analysis}\n\n"

        f"INDEX STRATEGY:\n"
        f"{state.index_strategy_analysis}\n\n"

        f"DATABASE LOAD:\n"
        f"{state.database_load_analysis}\n\n"

        f"Structure the investigation into 3 phases:\n\n"

        f"Phase 1: Query Investigation\n"
        f"Phase 2: Index and Statistics Review\n"
        f"Phase 3: Infrastructure and Workload Analysis\n\n"

        f"Provide detailed step-by-step recommendations."
    )

    return {
        "final_recommendation":
            f"DEEP PERFORMANCE INVESTIGATION\n{'=' * 45}\n{response.content}",
        "messages": ["[deep_performance_investigation] Generated"]
    }


def route_after_decision(state: PerformanceState) -> str:
    if state.needs_deep_investigation:
        return "deep"
    else:
        return "quick"


graph = StateGraph(PerformanceState)

graph.add_node("understand_issue", understand_issue)

graph.add_node(
    "analyze_query_structure",
    analyze_query_structure
)

graph.add_node(
    "analyze_index_strategy",
    analyze_index_strategy
)

graph.add_node(
    "analyze_database_load",
    analyze_database_load
)

graph.add_node(
    "classify_performance_issue",
    classify_performance_issue
)

graph.add_node(
    "quick_optimization_plan",
    quick_optimization_plan
)

graph.add_node(
    "deep_performance_investigation",
    deep_performance_investigation
)

graph.add_edge(START, "understand_issue")

graph.add_edge(
    "understand_issue",
    "analyze_query_structure"
)

graph.add_edge(
    "understand_issue",
    "analyze_index_strategy"
)

graph.add_edge(
    "understand_issue",
    "analyze_database_load"
)

graph.add_edge(
    "analyze_query_structure",
    "classify_performance_issue"
)

graph.add_edge(
    "analyze_index_strategy",
    "classify_performance_issue"
)

graph.add_edge(
    "analyze_database_load",
    "classify_performance_issue"
)

graph.add_conditional_edges(
    "classify_performance_issue",
    route_after_decision,
    {
        "quick": "quick_optimization_plan",
        "deep": "deep_performance_investigation",
    }
)

graph.add_edge(
    "quick_optimization_plan",
    END
)

graph.add_edge(
    "deep_performance_investigation",
    END
)

app = graph.compile()


def run_performance_check(issue: str):
    print("=" * 55)
    print("  DATABASE PERFORMANCE INVESTIGATION ASSISTANT")
    print(f'  Issue: "{issue}"')
    print("=" * 55)

    result = app.invoke(
        {
            "user_issue": issue,
            "messages": [],
        }
    )

    print("\n" + "=" * 55)
    print("  PERFORMANCE RECOMMENDATION")
    print("=" * 55)

    print(f"\n{result['final_recommendation']}")

    print("\n" + "-" * 55)
    print("  MESSAGE LOG")
    print("-" * 55)

    for msg in result["messages"]:
        print(f"  {msg}")

    return result


if __name__ == "__main__":

    print("\n" + "=" * 55)
    print("  DATABASE PERFORMANCE INVESTIGATION ASSISTANT")
    print("=" * 55)

    print("\n  Describe a database performance issue.")
    print("  Examples:")
    print("  - Slow SQL query")
    print("  - Missing indexes")
    print("  - High CPU usage")
    print("  - Locking issues")
    print("  Type 'quit' to exit.\n")

    while True:

        issue = input("  Describe the issue > ").strip()

        if issue.lower() in ("quit", "exit", "q"):
            print("\n  Goodbye!\n")
            break

        if not issue:
            continue

        run_performance_check(issue)
        print("\n")