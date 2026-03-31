# Udacity Project — Beaver's Choice Paper Company Multi-Agent System

## Project: Beaver's Choice Paper Company Inventory, Quoting, and Fulfillment

### Project Introduction

Multi-agent systems become useful when one model or one workflow is no longer enough
to manage the full business process. This module applies the multi-agent patterns from
the lessons to a paper supply company that needs help with inventory checks, quote
generation, and order fulfillment.

In this project, I build a **Beaver's Choice Paper Company Multi-Agent System** using
the module 4 `smolagents` pattern: one orchestrator coordinates three specialist
agents that read the shared SQLite database, normalize customer requests, prepare
quotes, and record transactions.

---

### Project Summary

The delivered solution keeps the starter contract intact while completing the missing
agent system inside `project/project_starter.py`.

#### Runtime Architecture

The system runs with four agents:

| Agent | Responsibility |
|---|---|
| `PaperCompanyOrchestrator` | Parses the request, routes work, and returns the final customer-facing response |
| `InventoryAgent` | Checks stock, estimates supplier timing, and validates deadline feasibility |
| `QuoteAgent` | Prices the accepted items, applies bulk discounts, and uses quote history when useful |
| `FulfillmentAgent` | Persists `stock_orders` and `sales` transactions and builds the fulfillment response |

#### Business Rules Implemented

1. **Deterministic request parsing** normalizes item aliases into exact catalog names.
2. **Partial fulfillment** is allowed when some items are valid and others are unknown
   or miss the deadline.
3. **Bulk discounts** use three tiers (`5%`, `8%`, `12%`) plus a history bonus capped
   at `15%`.
4. **Supplier timing** is checked before any replenishment-based fulfillment is accepted.
5. **Customer responses** explain what was confirmed, what was rejected, and why.

#### Delivered Artifacts

- [project/project_starter.py](./project/project_starter.py) — full implementation
- [project/test_results.csv](./project/test_results.csv) — evaluation output
- [project/evidence/run_test_scenarios_output.txt](./project/evidence/run_test_scenarios_output.txt) — captured console log
- [project/architecture.mmd](./project/architecture.mmd) and [project/architecture.svg](./project/architecture.svg) — workflow diagram

---

### Architecture Overview

```text
Customer Request
      │
      ▼
PaperCompanyOrchestrator
      │
      ├─▶ InventoryAgent
      │     get_all_inventory()
      │     get_stock_level()
      │     get_supplier_delivery_date()
      │
      ├─▶ QuoteAgent
      │     search_quote_history()
      │
      └─▶ FulfillmentAgent
            create_transaction()
            get_cash_balance()
            generate_financial_report()
      │
      ▼
SQLite: munder_difflin.db
```

The orchestrator follows the module 4 pattern: coordination happens through tools
that call the specialist agents, while the database remains the shared source of truth.

---

## Project Evaluation Key Points

### Multi-Agent Implementation

- Uses `smolagents` and `ToolCallingAgent` subclasses for the orchestrator and each worker.
- Keeps the starter helpers intact and wraps them as agent tools.
- Limits the system to four agents, staying within the project constraint of five.
- Uses only text inputs and outputs between the harness, orchestrator, and worker agents.

### Helper Coverage

The implementation defines tool wrappers that use all required starter helpers:

- `create_transaction`
- `get_all_inventory`
- `get_stock_level`
- `get_supplier_delivery_date`
- `get_cash_balance`
- `generate_financial_report`
- `search_quote_history`

### Evaluation Results

Running `run_test_scenarios()` on the full sample set produced:

- `20` processed requests
- `17` confirmed responses
- `3` rejected responses
- `7` partial responses with explicit exclusions
- `11` cash balance changes across the scenario log
- No negative inventory valuation in `test_results.csv`

These results satisfy the rubric expectations that not all requests are fulfilled,
multiple requests change the cash balance, and multiple quote/order requests are
successfully completed.

---

### Directory Structure

```text
4_Multi-Agent_Systems/
├── README.md                           ← This file
├── docs/                               ← Study guides for the module
│   ├── 01-introduction-to-multi-agent-systems.md
│   ├── 02-designing-multi-agent-architecture.md
│   ├── 03-implementing-multi-agent-architecture.md
│   ├── 04-orchestrating-agent-activities.md
│   ├── 05-routing-and-data-flow-in-agentic-systems.md
│   ├── 06-state-management-in-multi-agent-systems.md
│   ├── 07-multi-agent-orchestration-and-state-coordination.md
│   ├── 08-multi-agent-retrieval-augmented-generation.md
│   └── README.md
├── exercises/                          ← Guided exercises and demos
└── project/
    ├── README.md                       ← Operational guide
    ├── project_starter.py              ← Final single-file implementation
    ├── architecture.mmd                ← Source diagram
    ├── architecture.svg                ← Exported diagram
    ├── test_results.csv                ← Evaluation output
    ├── evidence/
    │   └── run_test_scenarios_output.txt
    ├── quote_requests.csv
    ├── quote_requests_sample.csv
    ├── quotes.csv
    └── munder_difflin.db
```

---

## Solution

### Workflow

1. `run_test_scenarios()` initializes the database and replays the sample requests in
   date order.
2. `PaperCompanyOrchestrator` parses each request into a structured representation with
   the request date, deadline, event keyword, and normalized items.
3. `InventoryAgent` checks current stock, evaluates shortfalls, and determines whether
   replenishment can arrive before the customer deadline.
4. `QuoteAgent` prices the accepted items, applies the discount tier, and searches the
   historical quote table for contextual pricing support.
5. `FulfillmentAgent` records any required `stock_orders`, records the `sales`
   transactions, and returns a customer-facing explanation of the outcome.

### Key Design Decisions

#### 1. Deterministic request parsing

The runtime uses deterministic parsing for SKU normalization instead of relying on a
remote LLM call. This keeps the project stable in local execution while preserving the
module 4 `smolagents` architecture.

#### 2. Partial acceptance instead of all-or-nothing rejection

Requests with a mix of valid and unsupported items are still serviced when the valid
portion can be delivered on time. Unsupported or impossible items are called out
explicitly in the customer response.

#### 3. Transaction-backed state

The implementation does not maintain a separate mutable state object. Stock, cash, and
financial reporting always flow through the SQLite transaction history provided by the
starter.

#### 4. Customer-safe explanations

Quotes explain discounts and delivery timing without exposing internal margins,
internal failures, or raw tool output.
