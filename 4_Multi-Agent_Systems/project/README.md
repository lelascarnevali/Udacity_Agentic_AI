# Beaver's Choice Paper Company Multi-Agent Project

This folder contains the completed module 4 project. The final implementation stays in
`project_starter.py`, while this README now acts as the single source of truth for
setup, architecture, helper usage, workflow, and evaluation results.

## Files In This Folder

- `project_starter.py` — single-file implementation of the multi-agent system
- `architecture.mmd` — Mermaid source for the workflow diagram
- `architecture.svg` — exported version of the workflow diagram
- `test_results.csv` — generated evaluation log for the sample request set
- `evidence/run_test_scenarios_output.txt` — captured console output from the batch run

## Environment Setup

1. From the repository root, create or reuse the local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. If you want to use the API-backed model path, add a root-level `.env` file:

```env
UDACITY_OPENAI_API_KEY=your_key_here
```

The implementation also supports deterministic local execution, so the project still
runs without a remote key.

## How To Run

Run the project from this folder so the CSV paths resolve correctly:

```bash
cd 4_Multi-Agent_Systems/project
../../.venv/bin/python project_starter.py
```

This command:

1. Initializes the SQLite database
2. Replays all requests from `quote_requests_sample.csv`
3. Routes each request through the orchestrator and worker agents
4. Prints the updated cash and inventory state after every request
5. Writes `test_results.csv`

## Expected Outputs

After a successful run you should have:

- Console output for each request
- A final financial report
- `test_results.csv` with the columns:
  - `request_id`
  - `request_date`
  - `cash_balance`
  - `inventory_value`
  - `response`
- `evidence/run_test_scenarios_output.txt` if you capture the session output

## Implemented Agent System

The final system uses four agents in the module 4 `smolagents` style.

| Agent | Responsibility | Main Tools |
| --- | --- | --- |
| `PaperCompanyOrchestrator` | Parses the request, routes work, and returns the customer-facing response | coordination tools that call `self.<agent>.run(...)` |
| `InventoryAgent` | Checks stock, calculates shortfalls, validates supplier timing, and decides if each item is feasible | `get_all_inventory`, `get_stock_level`, `get_supplier_delivery_date`, `generate_financial_report` |
| `QuoteAgent` | Prices accepted items, applies bulk discount tiers, and uses quote history to add contextual pricing | `search_quote_history` |
| `FulfillmentAgent` | Records `stock_orders` and `sales` and summarizes the final outcome | `create_transaction`, `get_cash_balance`, `generate_financial_report` |

## Starter Helpers And How They Are Used

| Helper | How the implementation uses it |
| --- | --- |
| `generate_sample_inventory()` | Used indirectly through the starter database initialization |
| `init_database()` | Reused as the bootstrap entrypoint for every test run |
| `create_transaction()` | Wrapped by the fulfillment tools for replenishment and sales |
| `get_all_inventory()` | Exposed through the inventory snapshot tool |
| `get_stock_level()` | Used for per-item feasibility checks |
| `get_supplier_delivery_date()` | Used to decide whether replenishment can satisfy the deadline |
| `get_cash_balance()` | Used before replenishment and for reporting |
| `generate_financial_report()` | Used for operational reporting and the starter harness snapshots |
| `search_quote_history()` | Used by the quote agent to add a contextual discount signal |

## Request Handling Workflow

1. The harness appends the request date to each customer request.
2. `PaperCompanyOrchestrator` parses the text into request date, deadline, request kind,
   and normalized item list.
3. `InventoryAgent` evaluates every requested item against:
   - current stock
   - shortfall
   - supplier arrival date
   - feasibility against deadline and cash
4. `QuoteAgent` prices only the accepted items using:
   - live catalog subtotal
   - bulk discount tier (`5%`, `8%`, `12%`)
   - contextual quote-history bonus (`0%`, `1%`, `2%`)
   - capped total discount of `15%`
5. `FulfillmentAgent` records:
   - replenishment transaction if shortfall exists
   - sales transaction for each accepted item
6. The orchestrator returns a customer-safe response with:
   - confirmed items
   - expected delivery date
   - discount rationale
   - unsupported or rejected items with reasons

## Evaluation Results

The project was evaluated with the full `quote_requests_sample.csv` dataset.

Observed results from `test_results.csv`:

- `20` total processed requests
- `17` confirmed outcomes
- `3` rejected outcomes
- `8` partial outcomes with excluded items
- `16` cash balance changes across the log
- No negative inventory valuation

These results satisfy the rubric expectation that:

- several requests change cash balance
- several requests are fulfilled
- not all requests are fulfilled
- failures are explained by unknown items or delivery timing limits

## Strengths

- The implementation preserves the starter structure and keeps the new logic in the
  editable regions.
- Alias normalization makes the catalog usable against noisy natural-language requests.
- Customer responses remain readable and explain both acceptance and rejection logic.
- The fulfillment flow uses the SQLite transaction history instead of inventing a
  second state store.

## Limitations

- Some accepted items use the closest stocked equivalent when the exact size variant is
  not in the catalog.
- The quote-history lookup is keyword-based because the starter does not provide
  embeddings or semantic retrieval.
- Delivery timing is simplified to the rules already encoded in the starter helpers.

## Future Improvements

1. Add stronger unit normalization for packs, boxes, and custom packaging quantities.
2. Replace keyword quote history search with an embedding-based retrieval step.
3. Add dedicated automated tests for normalization, pricing, and transaction dates.
4. Split the deterministic parser from the agent classes if this project evolves
   beyond the single-file submission constraint.

## Operational Notes

- The orchestrator expects the request date to be present in the text passed through
  the harness.
- Item aliases are normalized into exact catalog names before any transaction is
  written.
- Unknown items and deadline misses are surfaced explicitly in the customer response.
- Historical quotes with invalid totals are ignored when the quote agent calculates
  the contextual discount.
