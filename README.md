# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end analytics and agent workflow for monitoring Meesho reseller category revenue, identifying significant month-on-month movements, generating stakeholder-friendly narratives, and preparing controlled alerts for human approval.

## Objective

This project builds a reliable revenue-monitoring workflow using SQL, Python validation and growth calculations, deterministic narrative generation, privacy-safe reporting, and a guarded monitoring agent.

The workflow follows this sequence:

**Part 1 → Part 2 → Part 3 → Part 4**

Part 1 calculates verified business metrics from the seeded dataset. Part 2 validates the revenue feed and identifies significant month-on-month movements. Part 3 converts verified results into stakeholder-friendly narratives. Part 4 combines the previous components into a guarded agent workflow that drafts alerts for human approval.

## Key Features

- Category-level revenue analysis using SQL
- Monthly and regional revenue analysis
- Top-reseller analysis
- Zero-order reseller analysis
- June Delivered Average Order Value (AOV)
- Month-on-month revenue growth calculation
- 8% revenue movement threshold
- Exact 8% boundary escalation
- Input-feed validation
- Corrupted-data detection
- Deterministic stakeholder narrative generation
- Privacy-safe reseller name masking
- Top-3 alert drafting limit
- Suppression of additional flagged categories
- Human approval checkpoint before messages are considered ready to send
- Structured JSON output from the monitoring agent

## End-to-End Workflow

### Part 1 → SQL Business Query Engine

Part 1 generates the seeded reseller and order dataset and uses SQL to calculate the required business metrics.

The SQL analysis produces:

- Monthly revenue by category
- Region-wise revenue and order count
- Top 5 resellers by total spend
- Resellers with no orders
- `COUNT(*)` versus `COUNT(order_id)` demonstration for the zero-order case
- June Delivered AOV

The main handoff file is:

`part1_sql/output/monthly_category_revenue.csv`

This file provides the monthly category revenue values used by the later growth-detection and agent workflow.

### Part 2 → Python Guardrail & Growth Engine

Part 2 consumes the monthly revenue feed and provides three reusable functions:

- `mom_growth()` — calculates month-on-month percentage movement
- `is_flagged()` — classifies movement using the 8% threshold
- `validate_feed()` — validates the incoming CSV before calculations are performed

The engine also contains tests for normal growth, non-flagged growth, the exact 8% boundary, and corrupted-feed validation.

### Part 3 → Reliable Narrative & Privacy

Part 3 converts verified analytical results into stakeholder-friendly narrative text.

The narrative process separates:

- **Facts** — values supported by the verified data
- **Hypotheses** — possible explanations that are not presented as proven causes
- **Implications** — areas that may require managerial review or action

The prompt pack provides a reusable template structure, while `masking.py` prevents raw reseller names from appearing in external-facing narratives.

### Part 4 → Guarded Agent Workflow

Part 4 combines the previous components into a controlled monitoring workflow.

The agent:

1. Loads the current monthly feed.
2. Validates the feed before performing calculations.
3. Performs a hard stop if validation fails.
4. Calculates month-on-month movement for each category.
5. Applies the 8% threshold.
6. Sorts flagged categories by absolute movement.
7. Drafts messages for at most the top 3 flagged categories.
8. Suppresses remaining flagged categories.
9. Separately escalates exact 8% boundary cases.
10. Produces one structured JSON result.

The agent does not send emails or messages automatically. Drafted messages are held for human approval.

## Zero API Keys Required

The entire project runs offline and does not require:

- API keys
- Paid subscriptions
- Hosted AI services
- LLM APIs
- Email or messaging integrations

The narrative generation uses deterministic template filling rather than a live LLM API.

Therefore, the complete workflow can be executed with zero API keys configured.

## Project Structure

```text
meesho-reseller-growth-alert-intelligence/

├── data/
│   ├── generate_dataset.py
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
│
├── part1_sql/
│   ├── queries.sql
│   └── output/
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       ├── top_resellers.csv
│       ├── zero_order_resellers.csv
│       ├── zero_order_count_demo.csv
│       └── june_delivered_aov.csv
│
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
│
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
│
├── part4_agent/
│   ├── agent_spec.md
│   └── mock_agent_runner.py
│
├── .gitignore
└── README.md